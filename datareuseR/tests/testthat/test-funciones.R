test_that("leer_csv_abierto detecta Latin-1 y punto y coma", {
  f <- system.file("extdata", "bibliotecas_madrid_2026-11-24.csv", package = "datareuseR")
  bib <- leer_csv_abierto(f)
  expect_equal(attr(bib, "lectura"), list(encoding = "latin1", sep = ";"))
  expect_equal(nrow(bib), 52)
  expect_true(any(grepl("Mingote", bib$NOMBRE)))
})

test_that("leer_csv_abierto detecta UTF-8 y coma", {
  f <- system.file("extdata", "prestamos_bibliotecas_practica.csv", package = "datareuseR")
  p <- leer_csv_abierto(f, colClasses = "character")
  expect_equal(attr(p, "lectura"), list(encoding = "UTF-8", sep = ","))
  expect_equal(nrow(p), nrow(prestamos_practica))
})

test_that("completitud coincide con el libro", {
  expect_equal(round(completitud(bibliotecas_madrid), 2), 84.13)
  por_col <- completitud(prestamos_practica, por = "columna")
  expect_equal(unname(por_col["id"]), 100)
  expect_lt(unname(por_col["usuarios_activos"]), 100)
})

test_that("celda_vacia reconoce códigos de ausencia", {
  expect_equal(celda_vacia(c("1", "", " ", NA, "n/d")), c(FALSE, TRUE, TRUE, TRUE, TRUE))
})

test_that("informe_calidad cuenta duplicados", {
  inf <- informe_calidad(prestamos_practica)
  expect_s3_class(inf, "informe_calidad")
  expect_equal(inf$duplicadas, sum(duplicated(prestamos_practica)))
  expect_output(print(inf), "Completitud total")
})

test_that("clave_agrupacion unifica variantes", {
  expect_equal(unique(clave_agrupacion(c("Leganés", " leganes", "LEGANES "))), "leganes")
})

test_that("estrellas sigue el esquema", {
  expect_equal(estrellas(TRUE, TRUE, FALSE, FALSE, FALSE), 2)
  expect_equal(estrellas(TRUE, TRUE, TRUE, FALSE, FALSE), 3)
  expect_equal(estrellas(FALSE, TRUE, TRUE, TRUE, TRUE), 0)
})

test_that("evaluar_fair da el resultado del ejercicio 2.4", {
  r <- list(identificador_persistente = FALSE, metadatos_descriptivos = TRUE,
            acceso_por_protocolo_abierto = TRUE, formato_abierto = TRUE,
            vocabulario_comun = TRUE, licencia_declarada = FALSE,
            procedencia_documentada = FALSE)
  expect_equal(sum(evaluar_fair(r)), 2)
  expect_error(evaluar_fair(list(formato_abierto = TRUE)), "Faltan")
})

test_that("sumar_habiles salta fines de semana y festivos", {
  expect_equal(sumar_habiles("2026-01-09", 3), as.Date("2026-01-14"))
  expect_equal(sumar_habiles("2026-01-09", 3, festivos = "2026-01-12"), as.Date("2026-01-15"))
})

test_that("punto_equilibrio coincide con el simulador del Tema 5", {
  expect_equal(punto_equilibrio(2700, 0.04, 9), 7500)
  expect_equal(punto_equilibrio(2700, 0.08, 9), 3750)
  expect_equal(ingresos_mensuales(5000, 0.04, 9), 1800)
  expect_error(punto_equilibrio(2700, 4, 9), "proporci")
})

test_that("obligaciones combina licencias", {
  expect_equal(obligaciones(c("CC BY 4.0", "ODbL 1.0")),
               c(atribucion = TRUE, compartir_igual = TRUE, uso_comercial = TRUE))
  expect_false(obligaciones(c("CC0 1.0", "CC BY-NC 4.0"))[["uso_comercial"]])
  expect_error(obligaciones("GPL"), "no incluida")
})

test_that("normalizar_formato unifica URI y MIME", {
  expect_equal(normalizar_formato("http://publications.europa.eu/resource/authority/file-type/CSV"), "CSV")
  expect_equal(normalizar_formato(list(value = "text/csv")), "CSV")
  expect_equal(normalizar_formato(list(value = "application/vnd.ms-excel")), "XLS")
})

test_that("la copia de datos.gob.es se lee y se tabula", {
  f <- system.file("extdata", "datosgob_bibliotecas.json", package = "datareuseR")
  items <- jsonlite::fromJSON(f, simplifyVector = FALSE)$result$items
  expect_length(items, 50)
  t <- tabla_datosgob(items)
  expect_equal(t$titulo[1], "Bibliotecas de Vigo")
  expect_true("CSV" %in% formatos_de(items[[1]]))
  expect_equal(nrow(t), 50)
})

test_that("titulo_es admite texto, objeto o lista", {
  expect_equal(titulo_es(list(title = "Uno")), "Uno")
  expect_equal(titulo_es(list(title = list(`_value` = "Dos", `_lang` = "es"))), "Dos")
  expect_equal(titulo_es(list(title = list(list(`_value` = "Tres", `_lang` = "gl"),
                                           list(`_value` = "Tres es", `_lang` = "es")))), "Tres es")
})
