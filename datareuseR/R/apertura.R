#' Estrellas del esquema de cinco estrellas de los datos abiertos
#'
#' Aplica el esquema de Tim Berners-Lee: cada estrella exige las anteriores.
#'
#' @param licencia_abierta ¿Se publica con licencia abierta?
#' @param estructurado ¿Está en un formato estructurado (legible por máquina)?
#' @param no_propietario ¿El formato es abierto (no propietario)?
#' @param usa_uri ¿Identifica las cosas con URI?
#' @param enlazado ¿Enlaza con otros datos?
#' @return Número de estrellas, de 0 a 5.
#' @export
#' @examples
#' estrellas(TRUE, TRUE, FALSE, FALSE, FALSE)  # Excel con licencia abierta: 2
#' estrellas(TRUE, TRUE, TRUE, FALSE, FALSE)   # CSV con licencia abierta: 3
estrellas <- function(licencia_abierta, estructurado, no_propietario,
                      usa_uri, enlazado) {
  criterios <- c(licencia_abierta, estructurado, no_propietario, usa_uri, enlazado)
  if (!criterios[1]) return(0)
  sum(cumprod(criterios))
}

#' Evaluación FAIR simplificada de un registro de datos
#'
#' Lista de comprobación muy simplificada de los principios FAIR (Wilkinson et
#' al., 2016) para un conjunto de datos depositado.
#'
#' @param registro Lista con los elementos lógicos `identificador_persistente`,
#'   `metadatos_descriptivos`, `acceso_por_protocolo_abierto`,
#'   `formato_abierto`, `vocabulario_comun`, `licencia_declarada` y
#'   `procedencia_documentada`.
#' @return Vector lógico con nombres `F`, `A`, `I` y `R`.
#' @references Wilkinson, M. D. et al. (2016). The FAIR Guiding Principles for
#'   scientific data management and stewardship. *Scientific Data*, 3, 160018.
#'   \doi{10.1038/sdata.2016.18}
#' @export
#' @examples
#' evaluar_fair(list(
#'   identificador_persistente = TRUE, metadatos_descriptivos = TRUE,
#'   acceso_por_protocolo_abierto = TRUE, formato_abierto = TRUE,
#'   vocabulario_comun = FALSE, licencia_declarada = TRUE,
#'   procedencia_documentada = TRUE
#' ))
evaluar_fair <- function(registro) {
  campos <- c("identificador_persistente", "metadatos_descriptivos",
              "acceso_por_protocolo_abierto", "formato_abierto",
              "vocabulario_comun", "licencia_declarada",
              "procedencia_documentada")
  faltan <- setdiff(campos, names(registro))
  if (length(faltan)) {
    stop("Faltan elementos en el registro: ", paste(faltan, collapse = ", "),
         call. = FALSE)
  }
  c(F = registro$identificador_persistente && registro$metadatos_descriptivos,
    A = registro$acceso_por_protocolo_abierto,
    I = registro$formato_abierto && registro$vocabulario_comun,
    R = registro$licencia_declarada && registro$procedencia_documentada)
}

#' Sumar días hábiles
#'
#' Suma `n` días hábiles (de lunes a viernes) a una fecha, saltando también los
#' festivos indicados. Sirve para calcular plazos administrativos como los de
#' la Ley 37/2007.
#'
#' @param inicio Fecha de inicio (`Date` o texto `"AAAA-MM-DD"`).
#' @param n Número de días hábiles.
#' @param festivos Vector de fechas no hábiles adicionales.
#' @return Un objeto `Date`.
#' @export
#' @examples
#' sumar_habiles("2026-01-09", 3)  # viernes + 3 días hábiles = miércoles
sumar_habiles <- function(inicio, n, festivos = NULL) {
  dia <- as.Date(inicio)
  festivos <- as.Date(festivos)
  while (n > 0) {
    dia <- dia + 1
    laborable <- !(as.POSIXlt(dia)$wday %in% c(0, 6))
    if (laborable && !(dia %in% festivos)) n <- n - 1
  }
  dia
}
