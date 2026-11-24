#' ¿Está vacía una celda?
#'
#' Considera vacías las celdas `NA`, las cadenas vacías o formadas solo por
#' espacios y, opcionalmente, códigos de ausencia como `"n/d"`.
#'
#' @param x Vector.
#' @param ausentes Cadenas que también se tratan como valor ausente.
#' @return Vector lógico del mismo tamaño que `x`.
#' @export
#' @examples
#' celda_vacia(c("12", "", " ", NA, "n/d"))
celda_vacia <- function(x, ausentes = c("n/d", "N/D", "NA")) {
  texto <- trimws(as.character(x))
  is.na(x) | texto == "" | texto %in% ausentes
}

#' Completitud de un conjunto de datos
#'
#' Porcentaje de celdas no vacías, la métrica de completitud de Vetrò et al.
#' (2016).
#'
#' @param datos Un `data.frame`.
#' @param por `"total"` para el porcentaje de todo el conjunto o `"columna"`
#'   para un porcentaje por columna.
#' @param ... Otros argumentos para [celda_vacia()].
#' @return Un número o un vector con nombres, en porcentaje.
#' @references Vetrò, A. et al. (2016). Open data quality measurement
#'   framework. *Government Information Quarterly*, 33(2), 325-337.
#'   \doi{10.1016/j.giq.2016.02.001}
#' @export
#' @examples
#' completitud(prestamos_practica)
#' completitud(prestamos_practica, por = "columna")
completitud <- function(datos, por = c("total", "columna"), ...) {
  por <- match.arg(por)
  vacias <- vapply(datos, function(col) sum(celda_vacia(col, ...)), numeric(1))
  if (por == "columna") {
    return(100 * (1 - vacias / nrow(datos)))
  }
  100 * (1 - sum(vacias) / (nrow(datos) * ncol(datos)))
}

#' Informe rápido de calidad
#'
#' Resume filas, filas duplicadas, columnas vacías y completitud por columna.
#'
#' @param datos Un `data.frame`.
#' @param ... Otros argumentos para [celda_vacia()].
#' @return Un objeto de clase `informe_calidad` (una lista) con método de
#'   impresión.
#' @export
#' @examples
#' informe_calidad(prestamos_practica)
informe_calidad <- function(datos, ...) {
  por_columna <- completitud(datos, por = "columna", ...)
  informe <- list(
    filas = nrow(datos),
    columnas = ncol(datos),
    duplicadas = sum(duplicated(datos)),
    columnas_vacias = names(por_columna)[por_columna == 0],
    completitud_total = completitud(datos, ...),
    completitud_columnas = por_columna
  )
  class(informe) <- "informe_calidad"
  informe
}

#' @export
print.informe_calidad <- function(x, ...) {
  cat("Informe de calidad\n")
  cat("  Filas:", x$filas, "| columnas:", x$columnas,
      "| filas duplicadas:", x$duplicadas, "\n")
  cat("  Completitud total:", sprintf("%.2f %%", x$completitud_total), "\n")
  if (length(x$columnas_vacias)) {
    cat("  Columnas vac\u00edas:", paste(x$columnas_vacias, collapse = ", "), "\n")
  }
  incompletas <- x$completitud_columnas[x$completitud_columnas < 100]
  if (length(incompletas)) {
    cat("  Columnas incompletas (%):\n")
    print(round(sort(incompletas), 1))
  }
  invisible(x)
}

#' Clave de agrupación al estilo *fingerprint* de OpenRefine
#'
#' Quita espacios sobrantes, pasa a minúsculas y elimina tildes, para detectar
#' variantes de un mismo valor ("Leganés", " leganes").
#'
#' @param x Vector de texto.
#' @return Vector de texto normalizado.
#' @export
#' @examples
#' clave_agrupacion(c("Leganés", " leganes", "LEGANES "))
clave_agrupacion <- function(x) {
  x <- tolower(trimws(x))
  chartr("\u00e1\u00e9\u00ed\u00f3\u00fa\u00fc\u00f1", "aeiouun", x)
}
