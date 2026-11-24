#' Consultar el catálogo nacional de datos abiertos (datos.gob.es)
#'
#' Busca conjuntos de datos por palabra del título en la API de datos.gob.es.
#' Si no hay conexión y se busca `"bibliotecas"`, devuelve la copia guardada
#' en el paquete (consultada el 24 de noviembre de 2026), para que los
#' ejercicios funcionen sin red.
#'
#' @param titulo Palabra que debe aparecer en el título.
#' @param n Número máximo de resultados (la API admite hasta 50 por página).
#' @param copia Si es `TRUE`, usa la copia local cuando falla la consulta.
#' @return Lista de conjuntos de datos (uno por elemento), con el atributo
#'   `"origen"`: `"api"` o `"copia"`.
#' @seealso [tabla_datosgob()] para pasar el resultado a un `data.frame`.
#' @export
#' @examples
#' items <- consultar_datosgob("bibliotecas")
#' attr(items, "origen")
#' length(items)
consultar_datosgob <- function(titulo = "bibliotecas", n = 50, copia = TRUE) {
  url <- sprintf(
    "https://datos.gob.es/apidata/catalog/dataset/title/%s.json?_pageSize=%d",
    utils::URLencode(titulo, reserved = TRUE), as.integer(n))
  respuesta <- tryCatch({
    con <- url(url, encoding = "UTF-8")
    on.exit(close(con), add = TRUE)
    jsonlite::fromJSON(paste(readLines(con, warn = FALSE), collapse = "\n"),
                       simplifyVector = FALSE)
  }, error = function(e) NULL, warning = function(w) NULL)
  origen <- "api"
  if (is.null(respuesta)) {
    if (!copia || !identical(titulo, "bibliotecas")) {
      stop("No se ha podido consultar datos.gob.es.", call. = FALSE)
    }
    message("Sin conexi\u00f3n con datos.gob.es: se usa la copia del 24/11/2026.")
    f <- system.file("extdata", "datosgob_bibliotecas.json", package = "datareuseR")
    respuesta <- jsonlite::fromJSON(f, simplifyVector = FALSE)
    origen <- "copia"
  }
  items <- respuesta$result$items
  attr(items, "origen") <- origen
  items
}

# La API devuelve a veces un objeto y a veces una lista de objetos.
como_lista <- function(x) {
  if (is.null(x)) return(list())
  if (is.list(x) && !is.null(names(x))) list(x) else as.list(x)
}

#' Título en español de un conjunto de datos de datos.gob.es
#'
#' @param item Un elemento devuelto por [consultar_datosgob()].
#' @return Texto.
#' @export
#' @examples
#' titulo_es(consultar_datosgob()[[1]])
titulo_es <- function(item) {
  titulos <- como_lista(item$title)
  for (t in titulos) {
    if (is.character(t)) return(t[[1]])
    if (identical(t[["_lang"]], "es")) return(t[["_value"]])
  }
  t <- titulos[[1]]
  if (is.character(t)) t else t[["_value"]]
}

#' Normalizar la etiqueta de formato de una distribución
#'
#' datos.gob.es expresa los formatos de dos maneras: con el vocabulario de
#' tipos de fichero de la Oficina de Publicaciones de la UE
#' (`.../file-type/CSV`) o con un tipo MIME (`text/csv`). Esta función los lleva
#' a una etiqueta común en mayúsculas.
#'
#' @param formato Valor del campo `format` de una distribución (texto o lista
#'   con el elemento `value`).
#' @return Etiqueta en mayúsculas, como `"CSV"` o `"XLSX"`.
#' @export
#' @examples
#' normalizar_formato("http://publications.europa.eu/resource/authority/file-type/CSV")
#' normalizar_formato(list(value = "text/csv"))
normalizar_formato <- function(formato) {
  if (is.list(formato)) formato <- formato[["value"]]
  mime <- c(
    "text/csv" = "CSV", "application/json" = "JSON", "text/html" = "HTML",
    "application/xml" = "XML", "text/xml" = "XML", "application/pdf" = "PDF",
    "application/vnd.ms-excel" = "XLS",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" = "XLSX",
    "application/vnd.oasis.opendocument.spreadsheet" = "ODS",
    "text/pc-axis" = "PC-AXIS", "application/rdf+xml" = "RDF_XML",
    "application/geo+json" = "GEOJSON"
  )
  if (formato %in% names(mime)) return(unname(mime[formato]))
  toupper(sub(".*/", "", formato))
}

#' Formatos de las distribuciones de un conjunto de datos
#'
#' @param item Un elemento devuelto por [consultar_datosgob()].
#' @return Vector de etiquetas de formato sin repetir.
#' @export
#' @examples
#' formatos_de(consultar_datosgob()[[1]])
formatos_de <- function(item) {
  dist <- como_lista(item$distribution)
  unique(vapply(dist, function(d) normalizar_formato(d$format), character(1)))
}

#' Pasar los resultados de datos.gob.es a una tabla
#'
#' @param items Lista devuelta por [consultar_datosgob()].
#' @return `data.frame` con `titulo`, `publicador` (código del organismo),
#'   `n_distribuciones` y `formatos`.
#' @export
#' @examples
#' head(tabla_datosgob(consultar_datosgob()))
tabla_datosgob <- function(items) {
  data.frame(
    titulo = vapply(items, titulo_es, character(1)),
    publicador = vapply(items, function(it) sub(".*/", "", it$publisher), character(1)),
    n_distribuciones = vapply(items, function(it) length(como_lista(it$distribution)), integer(1)),
    formatos = vapply(items, function(it) paste(formatos_de(it), collapse = ", "), character(1))
  )
}
