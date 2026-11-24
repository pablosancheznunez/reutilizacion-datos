#' Préstamos de bibliotecas: fichero de práctica con errores
#'
#' Datos **sintéticos** de préstamos mensuales de seis bibliotecas municipales
#' del sur de Madrid (enero a junio de 2025), con errores de calidad
#' introducidos a propósito: filas duplicadas, municipios escritos de varias
#' formas, fechas en dos formatos, valores ausentes codificados como `"n/d"` y
#' un número de préstamos negativo. Todas las columnas se guardan como texto,
#' tal como se leerían sin limpiar.
#'
#' @format Un `data.frame` con 6 columnas de texto: `id`, `biblioteca`,
#'   `municipio`, `fecha`, `prestamos` y `usuarios_activos`. El fichero
#'   original está en `system.file("extdata", "prestamos_bibliotecas_practica.csv",
#'   package = "datareuseR")`.
#' @source Elaboración propia para el libro *Reutilización de datos abiertos y
#'   documentos*.
"prestamos_practica"

#' Bibliotecas públicas municipales de Madrid
#'
#' Copia fechada (24 de noviembre de 2026) del directorio de bibliotecas
#' públicas municipales publicado por el Ayuntamiento de Madrid. El fichero
#' original, en Latin-1 y separado por punto y coma, está en
#' `system.file("extdata", "bibliotecas_madrid_2026-11-24.csv",
#' package = "datareuseR")`.
#'
#' @format Un `data.frame` con 52 filas (una por biblioteca) y 32 columnas,
#'   entre ellas `NOMBRE`, `HORARIO`, `DISTRITO`, `LATITUD` y `LONGITUD`.
#' @source Ayuntamiento de Madrid, Portal de Datos Abiertos. Licencia CC BY 4.0.
#'   \url{https://datos.madrid.es}
"bibliotecas_madrid"

#' Casos ilustrativos de reutilización de datos abiertos
#'
#' Doce casos **inventados**, inspirados en tipos de proyecto frecuentes, y
#' clasificados con las dimensiones de Safarov, Meijer y Grimmelikhuijsen
#' (2017): tipo de usuario, tipo de utilización y efecto.
#'
#' @format Un `data.frame` con 12 filas y las columnas `caso`, `usuario`,
#'   `utilizacion`, `efecto` y `ambito`.
#' @source Elaboración propia. Marco de análisis: Safarov, I., Meijer, A. y
#'   Grimmelikhuijsen, S. (2017). \doi{10.3233/IP-160012}
"casos_reutilizacion"

#' Obligaciones de algunas licencias abiertas
#'
#' Tabla simplificada de obligaciones de cinco licencias habituales en datos
#' abiertos. Se usa en [obligaciones()].
#'
#' @format Un `data.frame` con 5 filas y las columnas `licencia`,
#'   `atribucion`, `compartir_igual` y `uso_comercial`.
#' @source Textos de las licencias Creative Commons y ODbL.
"licencias"
