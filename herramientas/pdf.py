"""Genera las versiones PDF (con Typst) y EPUB del libro.

Quarto no admite Typst en proyectos de libro, así que este script une los
capítulos en un solo documento dentro de _pdf/ (un proyecto aparte), lo
compila y deja el resultado en pdf/reutilizacion-datos-abiertos.pdf y .epub.

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

autor0 = yaml.safe_load((RAIZ / "_quarto.yml").read_text())["book"]["author"][0]
doi0 = yaml.safe_load((RAIZ / "_quarto.yml").read_text())["book"]["doi"]
ficha = f"""
::: {{.callout-note title="Ficha del libro"}}
- **Autor:** {autor0["name"]}
- **ORCID:** [https://orcid.org/{autor0["orcid"]}](https://orcid.org/{autor0["orcid"]})
- **Afiliación:** {autor0["affiliation"]}
- **DOI:** [https://doi.org/{doi0}](https://doi.org/{doi0})
- **Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es)
- **Versión web interactiva:** <https://pablosancheznunez.com/reutilizacion-datos/>
- **Cómo citarlo:** Sánchez-Núñez, P. (2026). *Reutilización de datos abiertos y documentos: tutoriales interactivos en R (webR)*. Zenodo. <https://doi.org/{doi0}>
:::
"""

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
        txt = re.sub(r"(# Presentación[^\n]*\n)", lambda m: m.group(1) + ficha + aviso, txt, count=1)
        # el botón de descarga del CSV y la celda de prueba no tienen sentido en papel
        txt = re.sub(r"\[Descargar el CSV\][^\n]*\n", "", txt)
        txt = re.sub(r"::: \{\.callout-tip[^\n]*\n## Descargar el libro.*?\n:::\n", "", txt, flags=re.S)
        txt = re.sub(r"## Tu progreso y uso sin conexión.*?(?=\n## )", "", txt, flags=re.S)
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
    },
    "epub": {
        "toc": True, "toc-depth": 1, "toc-title": "Índice",
        "cover-image": "portada.png",
        "identifier": "doi:" + str(libro.get("doi")),
        "publisher": "Pablo Sánchez-Núñez",
        "rights": "CC BY 4.0",
        "subject": "Datos abiertos; reutilización de la información del sector público; R",
        "output-file": "reutilizacion-datos-abiertos.epub",
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


def portada(destino):
    """Portada sencilla para el EPUB (1600 × 2400 px)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
    fig = plt.figure(figsize=(8, 12), dpi=200)
    fig.patch.set_facecolor("#000e78")
    fig.text(0.08, 0.80, "Reutilización de datos\nabiertos y documentos", color="white",
             fontsize=34, fontweight="bold", va="top", linespacing=1.15)
    fig.text(0.08, 0.62, "Tutoriales interactivos en R (webR)", color="#c9d2ff", fontsize=20, va="top")
    for i, c in enumerate(["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]):
        fig.patches.append(matplotlib.patches.Rectangle((0.08 + i * 0.09, 0.47), 0.07, 0.07,
                           transform=fig.transFigure, facecolor=c, edgecolor="none"))
    fig.text(0.08, 0.235, "Pablo Sánchez-Núñez", color="white", fontsize=22, fontweight="bold")
    fig.text(0.08, 0.11, "Universidad Carlos III de Madrid", color="#c9d2ff", fontsize=15)
    fig.text(0.08, 0.205, "ORCID 0000-0001-7845-9506", color="#c9d2ff", fontsize=13)
    fig.text(0.08, 0.06, "DOI 10.5281/zenodo.24500934 · CC BY 4.0", color="#c9d2ff", fontsize=12)
    fig.savefig(destino, facecolor=fig.get_facecolor())
    plt.close(fig)

portada(BUILD / "portada.png")
SALIDA.parent.mkdir(exist_ok=True)
for formato, extension in (("typst", "pdf"), ("epub", "epub")):
    r = subprocess.run(["quarto", "render", "libro.qmd", "--to", formato], cwd=BUILD, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-3000:])
    if r.returncode != 0:
        sys.exit(r.returncode)
    destino = SALIDA.with_suffix("." + extension)
    shutil.copy(BUILD / ("reutilizacion-datos-abiertos." + extension), destino)
    print(extension.upper() + ":", destino, destino.stat().st_size // 1024, "KB")
