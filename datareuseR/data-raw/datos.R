# Genera los conjuntos de datos del paquete. Ejecutar desde la carpeta del paquete.
prestamos_practica <- utils::read.csv("inst/extdata/prestamos_bibliotecas_practica.csv",
                                      colClasses = "character", encoding = "UTF-8")

source("R/lectura.R")
bibliotecas_madrid <- leer_csv_abierto("inst/extdata/bibliotecas_madrid_2026-11-24.csv")
attr(bibliotecas_madrid, "lectura") <- NULL
for (v in names(bibliotecas_madrid)) {
  if (is.character(bibliotecas_madrid[[v]])) {
    bibliotecas_madrid[[v]] <- enc2utf8(bibliotecas_madrid[[v]])
  }
}

casos_reutilizacion <- data.frame(
  caso = c("App de horarios de bibliotecas", "Mapa de wifi público", "Visor de presupuestos municipales",
           "Recomendador de lecturas", "Estudio de brecha digital", "Alertas de calidad del aire",
           "Buscador de ayudas públicas", "Reportaje sobre contratos", "Panel de préstamos regionales",
           "Planificador de rutas accesibles", "Análisis de citas a datasets", "Catálogo enriquecido con Wikidata"),
  usuario = c("Desarrolladores", "Empresas", "Ciudadanía", "Empresas", "Investigadores", "Desarrolladores",
              "Empresas", "Periodistas", "Administraciones", "Ciudadanía", "Investigadores", "Administraciones"),
  utilizacion = c("Servicio", "Servicio", "Visualización", "Servicio", "Análisis", "Servicio",
                  "Servicio", "Fiscalización", "Visualización", "Servicio", "Análisis", "Servicio"),
  efecto = c("Social", "Económico", "Buen gobierno", "Económico", "Social", "Social",
             "Económico", "Buen gobierno", "Buen gobierno", "Social", "Social", "Social"),
  ambito = c("Local", "Local", "Local", "Nacional", "Nacional", "Local",
             "Nacional", "Nacional", "Autonómico", "Local", "Europeo", "Autonómico")
)

licencias <- data.frame(
  licencia        = c("CC0 1.0", "CC BY 4.0", "CC BY-SA 4.0", "ODbL 1.0", "CC BY-NC 4.0"),
  atribucion      = c(FALSE, TRUE, TRUE, TRUE, TRUE),
  compartir_igual = c(FALSE, FALSE, TRUE, TRUE, FALSE),
  uso_comercial   = c(TRUE, TRUE, TRUE, TRUE, FALSE)
)

marcar_utf8 <- function(d) {
  for (v in names(d)) if (is.character(d[[v]])) Encoding(d[[v]]) <- "UTF-8"
  d
}
prestamos_practica <- marcar_utf8(prestamos_practica)
bibliotecas_madrid <- marcar_utf8(bibliotecas_madrid)
casos_reutilizacion <- marcar_utf8(casos_reutilizacion)

dir.create("data", showWarnings = FALSE)
for (obj in c("prestamos_practica", "bibliotecas_madrid", "casos_reutilizacion", "licencias")) {
  save(list = obj, file = file.path("data", paste0(obj, ".rda")), compress = "xz")
}
