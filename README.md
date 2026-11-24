# Reutilización de datos abiertos y documentos — tutoriales interactivos en R (webR)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24500934.svg)](https://doi.org/10.5281/zenodo.24500934)

**Autor:** Pablo Sánchez-Núñez · [ORCID 0000-0001-7845-9506](https://orcid.org/0000-0001-7845-9506) · [pablosancheznunez.com](https://pablosancheznunez.com)
Universidad Carlos III de Madrid

**Léelo en línea:** <https://pablosancheznunez.com/reutilizacion-datos/> · **PDF:** [reutilizacion-datos-abiertos.pdf](pdf/reutilizacion-datos-abiertos.pdf) · **EPUB:** [reutilizacion-datos-abiertos.epub](pdf/reutilizacion-datos-abiertos.epub)

Libro en [Quarto](https://quarto.org) para la asignatura *Reutilización de datos abiertos y documentos* (17300) del Máster Universitario en Bibliotecas, Archivos y Continuidad Digital Online (UC3M). Cada tema sigue el temario oficial (objetivos y contenidos numerados) y termina con una práctica en R que se ejecuta en el navegador mediante [webR](https://docs.r-wasm.org/webr/latest/), con ejercicios autocorregidos, retos evaluables, progreso del estudiante, modo oscuro y uso sin conexión.

El paquete de R [`datareuseR`](datareuseR/) reúne los datos y las funciones del libro para trabajar en RStudio o Positron:

```r
remotes::install_github("pablosancheznunez/reutilizacion-datos", subdir = "datareuseR")
```

## Cómo citar

> Sánchez-Núñez, P. (2026). *Reutilización de datos abiertos y documentos: tutoriales interactivos en R (webR)*. Universidad Carlos III de Madrid. Zenodo. https://doi.org/10.5281/zenodo.24500934

DOI de todas las versiones: 10.5281/zenodo.24500934 (siempre la última). DOI de v1.0.0: 10.5281/zenodo.24500935. GitHub muestra también la cita en «Cite this repository» (`CITATION.cff`).

## Generar el libro

```bash
python3 herramientas/extraer_r.py .   # scripts .R
python3 herramientas/figuras.py .     # figuras
python3 herramientas/moodle.py .      # banco de preguntas (Moodle XML)
python3 herramientas/datareuser_webr.py  # funciones de datareuseR para webR
python3 herramientas/pdf.py           # PDF (Typst) y EPUB
quarto render                         # sitio web en _book/
```

No hace falta R: los capítulos usan `engine: markdown` y el código se ejecuta en el navegador. El motor webR (`webr/`) y los paquetes que usa el libro (`webr-repo/`) están incluidos, así que el sitio funciona sin depender de servidores externos. Debe servirse por HTTP(S).

La versión en línea se publica copiando `_book/` a la carpeta `reutilizacion-datos/` del repositorio `pablosancheznunez.github.io`.

## Estructura

| Fichero | Contenido |
|---|---|
| `index.qmd` | Presentación, mapa del libro, autoría y cita |
| `00a-primeros-pasos.qmd` | Introducción mínima a R |
| `00-datos-abiertos.qmd` … `05-infomediarias.qmd` | Temas 0 a 5 |
| `90-chuleta-r.qmd`, `91-guia-docente.qmd`, `92-glosario.qmd` | Apéndices: chuleta de R, guía docente y glosario por temas |
| `plantillas/` | Scripts `.R` por capítulo, plantilla de informe `.qmd` y tema `.scss` descargables |
| `_extensions/webex/` | Preguntas autoevaluables con el formato de webexercises |
| `06-caso-practico.qmd` | Caso práctico con datos reales (Bibliotecas de Madrid, CC BY 4.0) |
| `figuras/` | Figuras de cada tema (SVG) |
| `moodle/` | Preguntas de autoevaluación en Moodle XML para Aula Global |
| `herramientas/pruebas/` | Pruebas en navegador: ejercicios, autoevaluación y accesibilidad |
| `.github/workflows/comprobar.yml` | Comprobación automática en cada cambio |
| `pdf/` | Versiones del libro en PDF y EPUB |
| `herramientas/` | Scripts para generar los `.R` de cada capítulo (`extraer_r.py`), las figuras (`figuras.py`) y el PDF (`pdf.py`) |
| `_extensions/libro-pdf/` | Filtro que adapta el libro al PDF |
| `datos/prestamos_bibliotecas_practica.csv` | CSV sintético de práctica con errores intencionados |
| `_extensions/r-wasm/live/` | Extensión quarto-live (MIT), con la plantilla de arranque modificada |
| `webr/`, `webr-repo/` | webR 0.6.0 y paquetes de R para WebAssembly |
| `.zenodo.json`, `CITATION.cff` | Metadatos para Zenodo y GitHub |
| `datareuseR/` | Paquete de R con los datos y funciones del libro (pruebas y viñeta incluidas) |
| `datos/datareuseR.R`, `datos/datosgob_bibliotecas.json` | Funciones del paquete para webR y copia de la API de datos.gob.es |
| `progreso.html`, `sw.js` | Progreso del estudiante (en el navegador) y uso sin conexión |
| `estilos-oscuro.scss` | Tema oscuro |
| `.github/workflows/semanal.yml` | Comprobación semanal de enlaces, datos de Madrid, API y paquete |

## Licencia

Textos y datos: CC BY 4.0. Código propio: MIT. Componentes de terceros con su propia licencia. Detalles en [LICENSE.md](LICENSE.md).
