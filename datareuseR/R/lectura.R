#' Leer un CSV de datos abiertos con codificación y separador desconocidos
#'
#' Los portales publican CSV en UTF-8 o en Latin-1, separados por comas o por
#' punto y coma. `leer_csv_abierto()` prueba la codificación y el separador antes
#' de leer, y guarda lo que ha detectado en el atributo `"lectura"` para que
#' quede documentado.
#'
#' @param archivo Ruta o URL del fichero CSV.
#' @param encoding Codificación. Por defecto (`NULL`) se detecta: UTF-8 si el
#'   texto es UTF-8 válido y, si no, Latin-1.
#' @param sep Separador. Por defecto (`NULL`) se elige el más frecuente en la
#'   primera línea entre `;`, `,`, tabulador y `|`.
#' @param ... Otros argumentos para [utils::read.csv()].
#' @return Un `data.frame` con el atributo `"lectura"`: una lista con
#'   `encoding` y `sep`.
#' @export
#' @examples
#' f <- system.file("extdata", "bibliotecas_madrid_2026-11-24.csv",
#'                  package = "datareuseR")
#' bib <- leer_csv_abierto(f)
#' attr(bib, "lectura")
#' dim(bib)
leer_csv_abierto <- function(archivo, encoding = NULL, sep = NULL, ...) {
  con <- if (grepl("^https?://", archivo)) url(archivo, "rb") else file(archivo, "rb")
  bytes <- tryCatch(readBin(con, "raw", n = 1e8), finally = close(con))
  # Quita la marca de orden de bytes (BOM) de UTF-8, si la hay
  if (length(bytes) >= 3 && identical(bytes[1:3], as.raw(c(0xef, 0xbb, 0xbf)))) {
    bytes <- bytes[-(1:3)]
  }
  texto <- rawToChar(bytes)
  if (is.null(encoding)) {
    encoding <- if (validUTF8(texto)) "UTF-8" else "latin1"
  }
  texto <- iconv(texto, from = encoding, to = "UTF-8")
  Encoding(texto) <- "UTF-8"
  if (is.null(sep)) {
    primera <- sub("[\r\n].*$", "", texto)
    candidatos <- c(";", ",", "\t", "|")
    cuenta <- vapply(candidatos, function(s) {
      lengths(regmatches(primera, gregexpr(s, primera, fixed = TRUE)))
    }, numeric(1))
    sep <- candidatos[which.max(cuenta)]
  }
  datos <- utils::read.csv(text = texto, sep = sep, encoding = "UTF-8",
                           check.names = FALSE, ...)
  attr(datos, "lectura") <- list(encoding = encoding, sep = sep)
  datos
}
