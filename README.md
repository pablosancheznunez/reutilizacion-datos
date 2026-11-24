# Reutilización de datos abiertos y documentos — tutoriales interactivos en R (webR)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24500934.svg)](https://doi.org/10.5281/zenodo.24500934)

**Autor:** Pablo Sánchez-Núñez · [ORCID 0000-0001-7845-9506](https://orcid.org/0000-0001-7845-9506) · [pablosancheznunez.com](https://pablosancheznunez.com)
Universidad Carlos III de Madrid, Departamento de Biblioteconomía y Documentación, OpenScienceLab

**Léelo en línea:** <https://pablosancheznunez.com/reutilizacion-datos/>

Libro en [Quarto](https://quarto.org) para la asignatura *Reutilización de datos abiertos y documentos* (17300) del Máster Universitario en Bibliotecas, Archivos y Continuidad Digital Online (UC3M). Cada tema sigue el temario oficial (objetivos y contenidos numerados) y termina con una práctica en R que se ejecuta en el navegador mediante [webR](https://docs.r-wasm.org/webr/latest/), con ejercicios autocorregidos.

## Cómo citar

> Sánchez-Núñez, P. (2026). *Reutilización de datos abiertos y documentos: tutoriales interactivos en R (webR)*. Universidad Carlos III de Madrid. Zenodo. https://doi.org/10.5281/zenodo.24500934

DOI de todas las versiones: 10.5281/zenodo.24500934 (siempre la última). DOI de v1.0.0: 10.5281/zenodo.24500935. GitHub muestra también la cita en «Cite this repository» (`CITATION.cff`).

## Generar el libro

```bash
quarto render    # genera _book/
```

No hace falta R: los capítulos usan `engine: markdown` y el código se ejecuta en el navegador. El motor webR (`webr/`) y los paquetes que usa el libro (`webr-repo/`) están incluidos, así que el sitio funciona sin depender de servidores externos. Debe servirse por HTTP(S).

La versión en línea se publica copiando `_book/` a la carpeta `reutilizacion-datos/` del repositorio `pablosancheznunez.github.io`.

## Estructura

| Fichero | Contenido |
|---|---|
| `index.qmd` | Presentación, mapa del libro, autoría y cita |
| `00a-primeros-pasos.qmd` | Introducción mínima a R |
| `00-datos-abiertos.qmd` … `05-infomediarias.qmd` | Temas 0 a 5 |
| `90-chuleta-r.qmd`, `91-guia-docente.qmd` | Apéndices |
| `datos/prestamos_bibliotecas_practica.csv` | CSV sintético de práctica con errores intencionados |
| `_extensions/r-wasm/live/` | Extensión quarto-live (MIT), con la plantilla de arranque modificada |
| `webr/`, `webr-repo/` | webR 0.6.0 y paquetes de R para WebAssembly |
| `.zenodo.json`, `CITATION.cff` | Metadatos para Zenodo y GitHub |

## Licencia

Textos y datos: CC BY 4.0. Código propio: MIT. Componentes de terceros con su propia licencia. Detalles en [LICENSE.md](LICENSE.md).
