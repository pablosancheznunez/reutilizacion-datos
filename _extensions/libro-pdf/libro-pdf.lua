-- Adapta el libro a la versión impresa (PDF con Typst):
--  * celdas {webr}: muestra el código; oculta preparación y comprobación;
--    los ejercicios aparecen con su título y huecos.
--  * pistas y soluciones de los ejercicios: recuadros.
--  * soluciones de la autoevaluación: recuadro «Explicaciones».
--  * enlaces entre capítulos: anclas internas; descargas: URL de la web.

local WEB = "https://pablosancheznunez.com/reutilizacion-datos/"
local CAP = {
  ["index.qmd"] = "sec-presentacion", ["00a-primeros-pasos.qmd"] = "sec-primeros-pasos",
  ["00-datos-abiertos.qmd"] = "sec-tema0", ["01-risp.qmd"] = "sec-tema1", ["02-proyectos.qmd"] = "sec-tema2",
  ["03-calidad.qmd"] = "sec-tema3", ["04-interoperabilidad.qmd"] = "sec-tema4", ["05-infomediarias.qmd"] = "sec-tema5", ["06-caso-practico.qmd"] = "sec-caso",
  ["90-chuleta-r.qmd"] = "sec-chuleta", ["91-guia-docente.qmd"] = "sec-guia", ["92-glosario.qmd"] = "sec-glosario",
}

local function es_webr(el)
  for _, c in ipairs(el.classes) do
    if c == "webr" or c == "{webr}" then return true end
  end
  return false
end

local function callout(tipo, titulo, contenido)
  return quarto.Callout({ type = tipo, title = titulo, content = contenido, collapse = false })
end

function CodeBlock(el)
  for _, c in ipairs(el.classes) do
    if c == "ojs" or c == "{ojs}" then return {} end
  end
  if not es_webr(el) then return nil end
  local opts, code = {}, {}
  for line in (el.text .. "\n"):gmatch("(.-)\n") do
    if line:match("^#|") then table.insert(opts, line) else table.insert(code, line) end
  end
  local o = table.concat(opts, " ")
  if o:match("setup:%s*true") or o:match("check:%s*true") then return {} end
  if o:match("input:") then
    return callout("note", "Gráfica interactiva", pandoc.Blocks({ pandoc.Para({ pandoc.Str("Esta gráfica es interactiva en la versión web: "),
      pandoc.Link("pablosancheznunez.com/reutilizacion-datos", WEB) }) }))
  end
  local texto = table.concat(code, "\n"):gsub("^%s*\n", ""):gsub("\n%s*$", "")
  local bloque = pandoc.CodeBlock(texto, pandoc.Attr("", { "r" }))
  if o:match("exercise:") then
    return callout("note", "Ejercicio: completa los huecos ______", pandoc.Blocks({ bloque }))
  end
  return bloque
end

function Div(el)
  if el.classes:includes("hint") and el.attributes["exercise"] then
    return callout("note", "Pista", el.content)
  end
  if (el.classes:includes("solution") or el.classes:includes("solucion-ejercicio")) and el.attributes["exercise"] then
    return callout("tip", "Solución", el.content)
  end
  if el.classes:includes("webex-solution") then
    return callout("tip", "Explicaciones", el.content)
  end
end

function Link(el)
  local t = el.target
  if t:match("^https?://") or t:match("^mailto:") then return nil end
  local file, anchor = t:match("^([^#]*)#?(.*)$")
  if CAP[file] then
    el.target = "#" .. (anchor ~= "" and anchor or CAP[file])
    return el
  end
  if file:match("^plantillas/") or file:match("^datos/") then
    el.target = WEB .. file
    el.classes = {}
    el.attributes = {}
    return el
  end
end
