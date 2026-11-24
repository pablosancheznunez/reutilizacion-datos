"""Genera datos/datareuseR.R: las funciones del paquete datareuseR en un solo
fichero que los capítulos cargan con source() dentro de webR (el paquete no
está compilado para WebAssembly). Ejecutar desde la raíz del libro."""
import pathlib, re, shutil

raiz = pathlib.Path(__file__).resolve().parent.parent
pkg = raiz / "datareuseR"
partes = ["# datareuseR para webR: generado por herramientas/datareuser_webr.py.",
          "# No editar: el código fuente está en datareuseR/R/.",
          "# En tu ordenador, instala el paquete y usa library(datareuseR).", ""]
for f in sorted((pkg / "R").glob("*.R")):
    if f.name == "datos.R":
        continue
    codigo = [l for l in f.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#'")]
    texto = "\n".join(codigo)
    texto = texto.replace('system.file("extdata", "datosgob_bibliotecas.json", package = "datareuseR")',
                          '"datos/datosgob_bibliotecas.json"')
    texto = texto.replace("datareuseR::licencias", "licencias")
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    partes += [f"# ---- {f.name} ----", texto, ""]
partes += ["# ---- tabla de licencias ----",
           'licencias <- data.frame(',
           '  licencia        = c("CC0 1.0", "CC BY 4.0", "CC BY-SA 4.0", "ODbL 1.0", "CC BY-NC 4.0"),',
           '  atribucion      = c(FALSE, TRUE, TRUE, TRUE, TRUE),',
           '  compartir_igual = c(FALSE, FALSE, TRUE, TRUE, FALSE),',
           '  uso_comercial   = c(TRUE, TRUE, TRUE, TRUE, FALSE)',
           ')', ""]
(raiz / "datos" / "datareuseR.R").write_text("\n".join(partes), encoding="utf-8")
shutil.copy(pkg / "inst" / "extdata" / "datosgob_bibliotecas.json", raiz / "datos" / "datosgob_bibliotecas.json")
print("datos/datareuseR.R:", len("\n".join(partes)), "caracteres")
