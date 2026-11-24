"""Genera un script .R limpio por capítulo a partir de los bloques {webr} del .qmd."""
import re, sys, pathlib
LIBRO = pathlib.Path(sys.argv[1])
URL = "https://pablosancheznunez.com/reutilizacion-datos/datos/prestamos_bibliotecas_practica.csv"
CAPS = {
 "00a-primeros-pasos.qmd": ("primeros_pasos", "Primeros pasos con R"),
 "00-datos-abiertos.qmd": ("tema0_datos_abiertos", "Tema 0. Introducción a los datos abiertos y la reutilización de la información"),
 "01-risp.qmd": ("tema1_risp", "Tema 1. Reutilización de la información del sector público (RISP)"),
 "02-proyectos.qmd": ("tema2_proyectos", "Tema 2. Proyectos relevantes de reutilización de datos abiertos"),
 "03-calidad.qmd": ("tema3_calidad", "Tema 3. Gestión documental y open data"),
 "04-interoperabilidad.qmd": ("tema4_interoperabilidad", "Tema 4. Normalización e interoperabilidad"),
 "05-infomediarias.qmd": ("tema5_infomediarias", "Tema 5. Empresas infomediarias y oportunidades de negocio"),
}
blk = re.compile(r"^```\{webr\}\n(.*?)^```", re.S | re.M)
head = re.compile(r"^(#{2,3}) (.+)$", re.M)
for qmd, (slug, titulo) in CAPS.items():
    txt = (LIBRO / qmd).read_text()
    out = [f"# {titulo}",
           "# Reutilización de datos abiertos y documentos: tutoriales interactivos en R",
           "# Pablo Sánchez-Núñez (UC3M) · https://doi.org/10.5281/zenodo.24500934",
           "# Licencia del código: MIT · Libro: https://pablosancheznunez.com/reutilizacion-datos/",
           "#",
           "# Script limpio con todo el código del capítulo, para ejecutarlo en RStudio o Positron.",
           "# Los ejercicios tienen huecos (______): complétalos y compara con el libro.",
           ""]
    if "jsonlite" in txt:
        out += ["# Paquete necesario (solo la primera vez):", "# install.packages(\"jsonlite\")", ""]
    if "datos/prestamos" in txt:
        out += ["# Descarga del CSV de práctica a la carpeta datos/",
                f'url_csv <- "{URL}"',
                'dir.create("datos", showWarnings = FALSE)',
                'if (!file.exists("datos/prestamos_bibliotecas_practica.csv")) {',
                '  download.file(url_csv, "datos/prestamos_bibliotecas_practica.csv", mode = "wb")',
                '}', ""]
    pos = 0; ultimo_titulo = None
    for m in blk.finditer(txt):
        # título más reciente antes del bloque
        hs = [h for h in head.finditer(txt, 0, m.start())]
        if hs:
            t = re.sub(r"\s*\{[^}]*\}", "", hs[-1].group(2)).strip()
            if t != ultimo_titulo:
                out += ["", "# " + "-" * 70, f"# {t}", "# " + "-" * 70]
                ultimo_titulo = t
        body = m.group(1)
        opts = [l for l in body.splitlines() if l.startswith("#|")]
        code = "\n".join(l for l in body.splitlines() if not l.startswith("#|")).strip("\n")
        o = " ".join(opts)
        if "check: true" in o:
            continue
        if "setup: true" in o:
            out += ["# (preparación del ejercicio)", code, ""]
        elif "exercise:" in o:
            out += ["# EJERCICIO: completa los huecos ______", code, ""]
        else:
            out += [code, ""]
    (LIBRO / "plantillas" / f"{slug}.R").write_text("\n".join(out).rstrip() + "\n")
    print(slug, len(out))
