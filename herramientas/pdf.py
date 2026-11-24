"""Genera la versión PDF del libro con Typst (incluido en Quarto).

Quarto no admite Typst en proyectos de libro, así que este script une los
capítulos en un solo documento dentro de _pdf/ (un proyecto aparte), lo
compila y deja el resultado en pdf/reutilizacion-datos-abiertos.pdf.

Uso, desde la raíz del libro:   python3 herramientas/pdf.py
Después, `quarto render` copia la carpeta pdf/ al sitio.
"""
import pathlib, re, shutil, subprocess, sys, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BUILD = RAIZ / "_pdf"
SALIDA = RAIZ / "pdf" / "reutilizacion-datos-abiertos.pdf"

cfg = yaml.safe_load((RAIZ / "_quarto.yml").read_text())
libro = cfg["book"]
capitulos = []
for c in libro["chapters"]:
    if isinstance(c, dict):
        capitulos += c["chapters"]
    else:
        capitulos.append(c)
capitulos += libro.get("appendices", [])

def cuerpo(fichero):
    s = (RAIZ / fichero).read_text()
    if s.startswith("---"):
        s = s.split("---", 2)[2]
    return s.strip() + "\n"

aviso = """
::: {.callout-note title="Sobre esta versión en PDF"}
Esta es la versión para leer e imprimir. El código de R aparece sin ejecutar y las preguntas de autoevaluación se muestran sin corrección automática. Para ejecutar el código, hacer los ejercicios con corrección y responder a las preguntas, usa la versión web: <https://pablosancheznunez.com/reutilizacion-datos/>, o descarga el script `.R` de cada capítulo.
:::

"""

partes = []
for i, f in enumerate(capitulos):
    txt = cuerpo(f)
    if f == "index.qmd":
        # tras el encabezado de la presentación, el aviso
        txt = re.sub(r"(# Presentación[^\n]*\n)", lambda m: m.group(1) + aviso, txt, count=1)
        # el botón de descarga del CSV y la celda de prueba no tienen sentido en papel
        txt = re.sub(r"\[Descargar el CSV\][^\n]*\n", "", txt)
        txt = re.sub(r"::: \{\.callout-tip[^\n]*\n## Versión en PDF.*?\n:::\n", "", txt, flags=re.S)
    if f == "92-glosario.qmd" or f == "90-chuleta-r.qmd" or f == "91-guia-docente.qmd":
        pass
    txt = txt.replace("Responde a todas las preguntas y pulsa **Mostrar respuestas**: verás en verde las acertadas, en rojo las falladas y tu recuento. Puedes corregir y volver a comprobar. No cuenta para la nota.",
                      "Responde en el papel y comprueba después con las explicaciones del recuadro. En la versión web estas preguntas se corrigen automáticamente. No cuentan para la nota.")
    # Quarto trata .solution como entorno de demostración: se renombra para el filtro libro-pdf
    txt = re.sub(r"\{\s*\.solution exercise=", "{.solucion-ejercicio exercise=", txt)
    # en Typst los títulos .unnumbered pierden su etiqueta: sin numeración no hace falta la clase
    txt = re.sub(r"\{(#[^ }]+) \.unnumbered\}", r"{\1}", txt)
    partes.append(txt)
doc = "\n\n{{< pagebreak >}}\n\n".join(partes)

autor = libro["author"][0]
cabecera = {
    "title": libro["title"],
    "subtitle": libro.get("subtitle", ""),
    "author": [{"name": autor["name"], "orcid": str(autor["orcid"]), "url": autor.get("url"),
                "affiliation": autor.get("affiliation")}],
    "date": "last-modified",
    "date-format": "D [de] MMMM [de] YYYY",
    "lang": "es",
    "doi": libro.get("doi"),
    "engine": "markdown",
    "filters": ["webex", "libro-pdf"],
    "format": {"typst": {
        "toc": True, "toc-depth": 1, "toc-title": "Índice",
        "papersize": "a4", "fontsize": "10.5pt",
        "margin": {"x": "2.3cm", "y": "2.5cm"},
        "fig-format": "svg", "code-overflow": "wrap",
        "output-file": "reutilizacion-datos-abiertos.pdf",
    }},
}

if BUILD.exists():
    shutil.rmtree(BUILD)
(BUILD / "_extensions").mkdir(parents=True)
for ext in ("webex", "libro-pdf"):
    shutil.copytree(RAIZ / "_extensions" / ext, BUILD / "_extensions" / ext)
shutil.copytree(RAIZ / "figuras", BUILD / "figuras")
(BUILD / "_quarto.yml").write_text("project:\n  type: default\n")
(BUILD / "libro.qmd").write_text("---\n" + yaml.safe_dump(cabecera, allow_unicode=True, sort_keys=False) + "---\n\n" + doc)

r = subprocess.run(["quarto", "render", "libro.qmd", "--to", "typst"], cwd=BUILD, capture_output=True, text=True)
print(r.stdout[-2000:], r.stderr[-4000:])
if r.returncode != 0:
    sys.exit(r.returncode)
SALIDA.parent.mkdir(exist_ok=True)
shutil.copy(BUILD / "reutilizacion-datos-abiertos.pdf", SALIDA)
print("PDF:", SALIDA, SALIDA.stat().st_size // 1024, "KB")
