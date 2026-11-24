#' Ingresos mensuales de un servicio *freemium*
#'
#' @param usuarios Usuarios de la versión gratuita.
#' @param conversion Proporción que pasa a la versión de pago (0.04 = 4 \%).
#' @param precio Cuota mensual, en euros.
#' @return Ingresos mensuales, en euros.
#' @export
#' @examples
#' ingresos_mensuales(5000, 0.04, 9)
ingresos_mensuales <- function(usuarios, conversion, precio) {
  comprobar_conversion(conversion)
  usuarios * conversion * precio
}

#' Punto de equilibrio de un servicio *freemium*
#'
#' Usuarios gratuitos necesarios para que los ingresos cubran los costes fijos.
#'
#' @param costes_mes Costes fijos mensuales, en euros.
#' @param conversion Proporción que pasa a la versión de pago (0.04 = 4 \%).
#' @param precio Cuota mensual, en euros.
#' @return Número de usuarios (redondeado hacia arriba).
#' @export
#' @examples
#' punto_equilibrio(2700, 0.04, 9)  # 7500 usuarios
#' punto_equilibrio(2700, 0.08, 9)  # al doblar la conversión, la mitad
punto_equilibrio <- function(costes_mes, conversion, precio) {
  comprobar_conversion(conversion)
  ceiling(costes_mes / (conversion * precio))
}

comprobar_conversion <- function(conversion) {
  if (any(conversion > 1)) {
    stop("La conversi\u00f3n es una proporci\u00f3n: escribe 0.04 para un 4 %.",
         call. = FALSE)
  }
  invisible(conversion)
}

#' Obligaciones al combinar fuentes con distintas licencias
#'
#' Acumula las obligaciones de varias licencias según la tabla [licencias]:
#' basta con que una fuente exija atribución o compartir igual para que lo
#' exija el resultado, y el uso comercial solo es posible si todas lo permiten.
#'
#' @param fuentes Vector con los nombres de las licencias, tal como aparecen en
#'   `licencias$licencia`.
#' @return Vector lógico con nombres `atribucion`, `compartir_igual` y
#'   `uso_comercial`.
#' @export
#' @examples
#' obligaciones(c("CC BY 4.0", "ODbL 1.0"))
obligaciones <- function(fuentes) {
  desconocidas <- setdiff(fuentes, datareuseR::licencias$licencia)
  if (length(desconocidas)) {
    stop("Licencia no incluida en la tabla: ",
         paste(desconocidas, collapse = ", "), call. = FALSE)
  }
  l <- datareuseR::licencias[datareuseR::licencias$licencia %in% fuentes, ]
  c(atribucion      = any(l$atribucion),
    compartir_igual = any(l$compartir_igual),
    uso_comercial   = all(l$uso_comercial))
}
