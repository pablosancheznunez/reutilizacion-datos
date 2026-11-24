"""Comprobación semanal de las fuentes externas del libro.

1. Enlaces: todos los enlaces http(s) de los capítulos responden.
2. Datos de Madrid: el CSV del Ayuntamiento conserva la estructura que usa el
   caso práctico (columnas, codificación, separador y número de filas).
3. API de datos.gob.es: la consulta del Tema 2 devuelve la estructura esperada.

Escribe un informe en Markdown (por defecto, informe_fuentes.md) y termina con
código 1 si hay algún problema que requiera revisar el libro.

Uso, desde la raíz del libro:   python3 herramientas/comprobar_fuentes.py
"""
import csv, io, json, pathlib, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INFORME = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "informe_fuentes.md"
AGENTE = "Mozilla/5.0 (comprobacion-enlaces; libro reutilizacion-datos; +https://pablosancheznunez.com/reutilizacion-datos/)"
URL_MADRID = "https://datos.madrid.es/egob/catalogo/201747-0-bibliobuses-bibliotecas.csv"
COPIA_MADRID = RAIZ / "datos" / "bibliotecas_madrid_2026-11-24.csv"
URL_API = "https://datos.gob.es/apidata/catalog/dataset/title/bibliotecas.json?_pageSize=50"
# Sitios que bloquean a los robots: un 403 o 429 de estos no se considera roto
TOLERANTES = ("boe.es", "eur-lex.europa.eu", "sciencedirect.com", "doi.org", "linkedin.com",
              "tandfonline.com", "researchgate.net", "elsevier.com", "sagepub.com", "jstor.org")


def pedir(url, cabeza=True, limite=25):
    req = urllib.request.Request(url, method="HEAD" if cabeza else "GET", headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=limite) as r:
        return r.status, (b"" if cabeza else r.read())


def enlaces():
    vistos = {}
    for f in sorted(RAIZ.glob("*.qmd")):
        for u in re.findall(r"https?://[^\s)\"'<>\]`]+", f.read_text(encoding="utf-8")):
            u = u.rstrip(".,;:")
            if "localhost" in u or "{" in u or u.endswith("…"):
                continue
            vistos.setdefault(u, f.name)
    return vistos


def comprobar_enlace(u):
    for intento, cabeza in enumerate((True, False, False)):
        try:
            estado, _ = pedir(u, cabeza=cabeza)
            return u, estado, None
        except urllib.error.HTTPError as e:
            if e.code in (403, 405, 429) and cabeza:
                continue
            if e.code in (403, 429) and any(t in u for t in TOLERANTES):
                return u, e.code, "bloquea robots (no se considera roto)"
            if e.code >= 500 and intento < 2:
                time.sleep(3); continue
            return u, e.code, "error"
        except Exception as e:  # tiempo agotado, DNS, TLS…
            if intento < 2:
                time.sleep(3); continue
            return u, None, type(e).__name__
    return u, None, "sin respuesta"


def comprobar_madrid():
    problemas = []
    _, cuerpo = pedir(URL_MADRID, cabeza=False, limite=60)
    try:
        cuerpo.decode("utf-8")
        problemas.append("El CSV ya es UTF-8 válido: revisar `fileEncoding = \"latin1\"` en el caso práctico.")
        texto = cuerpo.decode("utf-8")
    except UnicodeDecodeError:
        texto = cuerpo.decode("latin-1")
    nuevo = list(csv.reader(io.StringIO(texto), delimiter=";"))
    viejo = list(csv.reader(io.StringIO(COPIA_MADRID.read_bytes().decode("latin-1")), delimiter=";"))
    if not nuevo or len(nuevo[0]) < 5:
        problemas.append("El separador ya no es el punto y coma o el fichero está vacío.")
        return problemas, {}
    faltan = [c for c in viejo[0] if c not in nuevo[0]]
    if faltan:
        problemas.append("Faltan columnas que usa el libro: " + ", ".join(faltan))
    filas_nuevo, filas_viejo = len(nuevo) - 1, len(viejo) - 1
    if abs(filas_nuevo - filas_viejo) > 0.2 * filas_viejo:
        problemas.append(f"El número de bibliotecas ha cambiado mucho: {filas_viejo} → {filas_nuevo}.")
    return problemas, {"filas": filas_nuevo, "columnas": len(nuevo[0]), "idéntico a la copia": cuerpo == COPIA_MADRID.read_bytes()}


def comprobar_api():
    problemas = []
    _, cuerpo = pedir(URL_API, cabeza=False, limite=60)
    items = json.loads(cuerpo.decode("utf-8"))["result"]["items"]
    if not items:
        problemas.append("La API no devuelve resultados para «bibliotecas».")
    for campo in ("title", "publisher", "distribution"):
        if not any(campo in it for it in items):
            problemas.append(f"Los resultados ya no incluyen el campo `{campo}`.")
    return problemas, {"resultados": len(items)}


def main():
    lineas = ["# Comprobación semanal de las fuentes del libro", "",
              time.strftime("Fecha: %Y-%m-%d %H:%M UTC", time.gmtime()), ""]
    graves = 0

    mapa = enlaces()
    with ThreadPoolExecutor(8) as ex:
        resultados = list(ex.map(comprobar_enlace, mapa))
    rotos = [(u, e, n) for u, e, n in resultados if n and not n.startswith("bloquea")]
    avisos = [(u, e, n) for u, e, n in resultados if n and n.startswith("bloquea")]
    graves += len(rotos)
    lineas += [f"## Enlaces: {len(mapa)} revisados, {len(rotos)} rotos", ""]
    for u, e, n in rotos:
        lineas.append(f"- [ ] `{mapa[u]}`: <{u}> ({e or n})")
    if avisos:
        lineas += ["", f"{len(avisos)} enlaces responden 403/429 a los robots y no se cuentan como rotos."]
    lineas.append("")

    for titulo, funcion in (("Datos de bibliotecas de Madrid", comprobar_madrid), ("API de datos.gob.es", comprobar_api)):
        try:
            problemas, datos = funcion()
        except Exception as e:
            problemas, datos = [f"No se ha podido comprobar: {type(e).__name__}: {e}"], {}
        graves += len(problemas)
        estado = "correcto" if not problemas else f"{len(problemas)} problema(s)"
        lineas += [f"## {titulo}: {estado}", ""]
        lineas += [f"- [ ] {p}" for p in problemas]
        lineas += [f"- {k}: {v}" for k, v in datos.items()]
        lineas.append("")

    INFORME.write_text("\n".join(lineas), encoding="utf-8")
    print("\n".join(lineas))
    sys.exit(1 if graves else 0)


if __name__ == "__main__":
    main()
