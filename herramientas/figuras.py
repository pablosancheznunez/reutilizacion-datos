"""Genera las figuras estáticas del libro (SVG) en figuras/.

Uso:  python3 herramientas/figuras.py .
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
"""
import sys, pathlib, csv, unicodedata
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch

RAIZ = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]   # series 1-5
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
AZUL_RAMP = ["#dbe8f8", "#b3cdf0", "#7eaae4", "#4a85d3", "#1f5fae"]  # secuencial, claro→oscuro

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": GRIS, "axes.labelcolor": TINTA2, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})

def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=110, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)

def rejilla(ax, eje="y"):
    ax.grid(axis=eje, color="#ecebe8", linewidth=0.8); ax.set_axisbelow(True)

# ---------------------------------------------------------------- Tema 0
def tema0():
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    niveles = [("★", "En la web con\nlicencia abierta", "PDF de la memoria"),
               ("★★", "Datos\nestructurados", "Excel (.xlsx)"),
               ("★★★", "Formato no\npropietario", "CSV"),
               ("★★★★", "URI para\nidentificar", "RDF con URI"),
               ("★★★★★", "Enlazados con\notros datos", "RDF + Wikidata")]
    for i, (est, req, ej) in enumerate(niveles):
        h = 1.5 + 0.85 * i
        ax.add_patch(FancyBboxPatch((i * 1.05, 0), 0.95, h, boxstyle="round,pad=0,rounding_size=0.06",
                                    fc=AZUL_RAMP[i], ec=SUP, lw=2))
        col = TINTA if i < 3 else "#ffffff"
        ax.text(i * 1.05 + 0.475, h - 0.32, est, ha="center", va="center", fontsize=12, color=col,
                fontfamily="DejaVu Sans")
        ax.text(i * 1.05 + 0.475, h - 0.9, req, ha="center", va="center", fontsize=9.5, color=col, linespacing=1.15)
        ax.text(i * 1.05 + 0.475, -0.32, ej, ha="center", va="center", fontsize=9, color=TINTA2)
    ax.annotate("El CSV de práctica", xy=(2 * 1.05 + 0.475, 3.25), xytext=(0.1, 4.3),
                fontsize=10, color=TINTA, arrowprops=dict(arrowstyle="-|>", color=TINTA2, lw=1))
    ax.set_xlim(-0.1, 5.2); ax.set_ylim(-0.6, 5.2); ax.axis("off")
    guardar(fig, "tema0_cinco_estrellas.svg")

# ---------------------------------------------------------------- Tema 1
def tema1():
    normas = [("Directiva 2003/98/CE", date(2003, 11, 17), "UE"), ("Ley 37/2007", date(2007, 11, 16), "ES"),
              ("RD 1495/2011", date(2011, 10, 24), "ES"), ("NTI-RISP", date(2013, 2, 19), "ES"),
              ("Directiva 2013/37/UE", date(2013, 6, 26), "UE"), ("Ley 19/2013", date(2013, 12, 9), "ES"),
              ("Ley 18/2015", date(2015, 7, 9), "ES"), ("Directiva (UE) 2019/1024", date(2019, 6, 20), "UE"),
              ("RDL 24/2021", date(2021, 11, 2), "ES"), ("Reglamento (UE) 2022/868", date(2022, 5, 30), "UE"),
              ("Reglamento de Ejecución\n(UE) 2023/138", date(2022, 12, 21), "UE"),
              ("Reglamento (UE) 2023/2854", date(2023, 12, 13), "UE"), ("Reglamento (UE) 2024/1689", date(2024, 6, 13), "UE")]
    normas = sorted(normas, key=lambda t: t[1])
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    n = len(normas)
    for k, (nom, d, a) in enumerate(normas):
        yk = n - 1 - k
        x = 1 if a == "UE" else 0
        c = S[0] if a == "UE" else S[1]
        ax.plot([0, 1], [yk, yk], color="#f1f0ed", lw=1, zorder=0)
        ax.plot(x, yk, "o", ms=10, color=c, mec=SUP, mew=2, zorder=3)
        ax.text(-0.12, yk, d.strftime("%d/%m/%Y"), ha="right", va="center", fontsize=9, color=TINTA2)
        lab = nom.replace("\n", " ")
        if a == "UE":
            ax.text(1.06, yk, lab, ha="left", va="center", fontsize=9.5, color=TINTA)
        else:
            ax.text(0.06, yk, lab, ha="left", va="center", fontsize=9.5, color=TINTA)
    ax.plot([0, 0], [-0.5, n - 0.5], color=S[1], lw=1, alpha=0.35, zorder=1)
    ax.plot([1, 1], [-0.5, n - 0.5], color=S[0], lw=1, alpha=0.35, zorder=1)
    ax.text(0, n - 0.1, "España", ha="center", fontsize=11, color=TINTA, fontweight="bold")
    ax.text(1, n - 0.1, "Unión Europea", ha="center", fontsize=11, color=TINTA, fontweight="bold")
    ax.set_xlim(-0.55, 2.05); ax.set_ylim(-0.7, n + 0.4); ax.axis("off")
    guardar(fig, "tema1_cronologia.svg")

# ---------------------------------------------------------------- Tema 2
def tema2():
    usuario = ["Desarrolladores", "Empresas", "Ciudadanía", "Empresas", "Investigadores", "Desarrolladores",
               "Empresas", "Periodistas", "Administraciones", "Ciudadanía", "Investigadores", "Administraciones"]
    efecto = ["Social", "Económico", "Buen gobierno", "Económico", "Social", "Social",
              "Económico", "Buen gobierno", "Buen gobierno", "Social", "Social", "Social"]
    efectos = ["Económico", "Social", "Buen gobierno"]
    grupos = sorted(set(usuario), key=lambda u: -usuario.count(u))
    fig, ax = plt.subplots(figsize=(8, 3.8))
    izq = [0] * len(grupos)
    for j, e in enumerate(efectos):
        vals = [sum(1 for u, f in zip(usuario, efecto) if u == g and f == e) for g in grupos]
        bars = ax.barh(grupos, vals, left=izq, color=S[j], edgecolor=SUP, linewidth=2, height=0.62, label=e)
        for b, v in zip(bars, vals):
            if v: ax.text(b.get_x() + b.get_width() / 2, b.get_y() + b.get_height() / 2, str(v),
                          ha="center", va="center", fontsize=9.5, color=TINTA)
        izq = [a + b for a, b in zip(izq, vals)]
    ax.invert_yaxis(); ax.set_xlabel("Número de casos"); rejilla(ax, "x")
    ax.set_xticks(range(0, 5)); ax.tick_params(axis="y", length=0, labelcolor=TINTA)
    ax.legend(title="Efecto", frameon=False, loc="lower right", fontsize=9.5, title_fontsize=10)
    guardar(fig, "tema2_casos_usuario_efecto.svg")

# ---------------------------------------------------------------- Tema 3
def leer_csv():
    with open(RAIZ / "datos" / "prestamos_bibliotecas_practica.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clave(m):
    m = m.strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", m) if unicodedata.category(c) != "Mn")

def tema3():
    filas = leer_csv(); cols = list(filas[0].keys())
    # (a) completitud por columna
    pct = [100 * sum(1 for r in filas if r[c].strip() not in ("", "n/d")) / len(filas) for c in cols]
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    bars = ax.barh(cols, pct, color=S[0], height=0.58, edgecolor=SUP, linewidth=2)
    for b, v in zip(bars, pct):
        ax.text(v + 1.5, b.get_y() + b.get_height() / 2, f"{v:.1f} %".replace(".", ","), va="center", fontsize=9.5, color=TINTA)
    ax.invert_yaxis(); ax.set_xlim(0, 112); ax.set_xlabel("Celdas completas (%)")
    rejilla(ax, "x"); ax.tick_params(axis="y", length=0, labelcolor=TINTA)
    guardar(fig, "tema3_completitud.svg")
    # (b) préstamos mensuales por municipio tras la limpieza
    vistos, limpias = set(), []
    for r in filas:
        k = tuple(r.values())
        if k in vistos: continue
        vistos.add(k); limpias.append(r)
    nombre = {"getafe": "Getafe", "leganes": "Leganés", "alcorcon": "Alcorcón", "mostoles": "Móstoles", "fuenlabrada": "Fuenlabrada"}
    serie = {}
    for r in limpias:
        p = r["prestamos"].strip()
        if p in ("", "n/d") or int(p) < 0: continue
        f = r["fecha"]
        mes = int(f.split("/")[1]) if "/" in f else int(f.split("-")[1])
        m = nombre[clave(r["municipio"])]
        serie.setdefault(m, {}).setdefault(mes, 0); serie[m][mes] += int(p)
    orden = ["Getafe", "Leganés", "Alcorcón", "Móstoles", "Fuenlabrada"]
    fig, ax = plt.subplots(figsize=(8, 3.9))
    meses = ["ene", "feb", "mar", "abr", "may", "jun"]
    finales = []
    for i, m in enumerate(orden):
        xs = list(range(1, 7)); ys = [serie[m].get(x, float("nan")) for x in xs]
        ax.plot(xs, ys, color=S[i], lw=2, marker="o", ms=5, mec=SUP, mew=1.5)
        finales.append([ys[-1], m])
    # separar etiquetas finales al menos 260 préstamos
    finales.sort()
    for j in range(1, len(finales)):
        if finales[j][0] - finales[j - 1][0] < 260: finales[j][0] = finales[j - 1][0] + 260
    for yv, m in finales:
        ax.text(6.12, yv, m, va="center", fontsize=9.5, color=TINTA)
    ax.set_xticks(range(1, 7)); ax.set_xticklabels(meses); ax.set_xlim(0.8, 6.9)
    ax.set_ylabel("Préstamos"); rejilla(ax, "y")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", ".")))
    ax.text(0.8, ax.get_ylim()[1], "Los huecos son meses sin dato válido (ausente o negativo)", fontsize=8.5, color=TINTA2, va="bottom")
    guardar(fig, "tema3_prestamos_municipio.svg")

# ---------------------------------------------------------------- Tema 4
def tema4():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    nodos = {"wd:Q8802\nGetafe": (0.5, 2.6), "wd:Q77433\nLeganés": (0.5, 1.2), "wd:Q10372\nAlcorcón": (0.5, 0.0),
             "ex:centro": (3.3, 3.1), "ex:sur": (3.3, 2.1), "ex:norte": (3.3, 1.2), "ex:parque": (3.3, 0.0),
             "Club de lectura\n(act1, act4)": (6.4, 2.9), "Taller de datos\nabiertos (act2, act6)": (6.4, 1.8),
             "Cuentacuentos (act3)": (6.4, 0.9), "Alfabetización\ndigital (act5)": (6.4, 0.0)}
    tipo = lambda n: 0 if n.startswith("wd:") else (1 if n.startswith("ex:") else 2)
    aristas = [("ex:centro", "wd:Q8802\nGetafe"), ("ex:sur", "wd:Q8802\nGetafe"), ("ex:norte", "wd:Q77433\nLeganés"),
               ("ex:parque", "wd:Q10372\nAlcorcón"),
               ("Club de lectura\n(act1, act4)", "ex:centro"), ("Club de lectura\n(act1, act4)", "ex:norte"),
               ("Taller de datos\nabiertos (act2, act6)", "ex:centro"), ("Taller de datos\nabiertos (act2, act6)", "ex:parque"),
               ("Cuentacuentos (act3)", "ex:sur"), ("Alfabetización\ndigital (act5)", "ex:centro")]
    for a, b in aristas:
        (x1, y1), (x2, y2) = nodos[a], nodos[b]
        ax.annotate("", xy=(x2 + (0.75 if tipo(b) == 0 else 0.55), y2), xytext=(x1 - (0.85 if tipo(a) == 2 else 0.5), y1),
                    arrowprops=dict(arrowstyle="-|>", color="#9a9893", lw=1, shrinkA=0, shrinkB=0))
    for n, (x, y) in nodos.items():
        t = tipo(n)
        ax.text(x, y, n, ha="center", va="center", fontsize=9, color=TINTA, linespacing=1.1,
                bbox=dict(boxstyle="round,pad=0.45", fc=["#e3eefb", "#fde6dc", "#d9f3e9"][t], ec=S[t], lw=1.5))
    for x, lab in [(0.5, "Municipios (Wikidata)"), (3.3, "Bibliotecas (schema:Library)"), (6.4, "Actividades (schema:Event)")]:
        ax.text(x, 3.85, lab, ha="center", fontsize=10, color=TINTA, fontweight="bold")
    ax.text(1.95, 3.45, "schema:containedInPlace", ha="center", fontsize=8.5, color=TINTA2, style="italic")
    ax.text(4.85, 3.45, "schema:location", ha="center", fontsize=8.5, color=TINTA2, style="italic")
    ax.set_xlim(-0.6, 7.6); ax.set_ylim(-0.5, 4.1); ax.axis("off")
    guardar(fig, "tema4_grafo.svg")

# ---------------------------------------------------------------- Tema 5
def tema5():
    precio, fijos = 9, 2700
    u = list(range(0, 12001, 250))
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (conv, lab) in enumerate([(0.04, "Conversión 4 %"), (0.06, "Conversión 6 %")]):
        ys = [x * conv * precio for x in u]
        ax.plot(u, ys, color=S[i], lw=2)
        ax.text(u[-1] + 150, ys[-1], lab, va="center", fontsize=9.5, color=TINTA)
        eq = fijos / (conv * precio)
        ax.plot(eq, fijos, "o", ms=8, color=S[i], mec=SUP, mew=2, zorder=4)
        ax.annotate(f"{int(eq):,} usuarios".replace(",", "."), (eq, fijos), xytext=((eq + 400, fijos - 700) if i == 0 else (eq - 3600, fijos + 900)),
                    fontsize=9, color=TINTA, arrowprops=dict(arrowstyle="-", color=GRIS, lw=0.8))
    ax.axhline(fijos, color=TINTA2, lw=1.2, ls=(0, (4, 3)))
    ax.text(150, fijos + 120, "Costes fijos: 2.700 € al mes", fontsize=9.5, color=TINTA2)
    ax.set_xlabel("Usuarios de la versión gratuita"); ax.set_ylabel("Ingresos (€ al mes)")
    ax.set_xlim(0, 13900); ax.set_ylim(0, 7000); rejilla(ax, "y")
    f = matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", "."))
    ax.xaxis.set_major_formatter(f); ax.yaxis.set_major_formatter(f)
    guardar(fig, "tema5_punto_equilibrio.svg")


# ====================================================================== v1.4
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
CAJA_, CAJA2_ = "#eef0f6", "#c9cfe0"


def _caja(ax, x, y, w, h, t, ec=CAJA2_, fc=CAJA_, fs=9.5, peso="normal", tc=TINTA):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08", fc=fc, ec=ec, lw=1.4))
    if t: ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=tc, fontweight=peso, linespacing=1.2)


def _flecha(ax, a, b, color=TINTA2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3, shrinkA=2, shrinkB=2))


def v14_fair():
    fig, ax = plt.subplots(figsize=(10, 3.4)); ax.set_xlim(0, 16); ax.set_ylim(0, 5.2); ax.axis("off")
    ps = [("F", "Localizables", "identificador persistente\ny metadatos ricos,\nindexados en un catálogo"),
          ("A", "Accesibles", "se recuperan por su\nidentificador con un\nprotocolo abierto"),
          ("I", "Interoperables", "formatos y vocabularios\ncompartidos que\nlas máquinas entienden"),
          ("R", "Reutilizables", "licencia clara,\nprocedencia y normas\nde la comunidad")]
    for i, (l, t, d) in enumerate(ps):
        x = 0.2 + i * 4.0
        _caja(ax, x, 0.3, 3.6, 4.5, None, fc=SUP, ec=S[i])
        ax.add_patch(Circle((x + 1.8, 4.0), 0.45, fc=S[i], ec="none"))
        ax.text(x + 1.8, 4.0, l, ha="center", va="center", fontsize=15, fontweight="bold", color=TINTA)
        ax.text(x + 1.8, 3.05, t, ha="center", va="center", fontsize=11, fontweight="bold", color=TINTA)
        ax.text(x + 1.8, 1.6, d, ha="center", va="center", fontsize=9, color=TINTA2)
    guardar(fig, "v14_fair.svg")


def v14_ciclo():
    import math
    fig, ax = plt.subplots(figsize=(7, 5.4)); ax.set_xlim(-6, 6); ax.set_ylim(-4.6, 4.6); ax.set_aspect("equal"); ax.axis("off")
    fases = ["Planificar", "Recoger o crear", "Describir\n(metadatos)", "Publicar", "Reutilizar", "Preservar\ny actualizar"]
    pos = []
    for i, f in enumerate(fases):
        a = math.pi / 2 - i * 2 * math.pi / len(fases); x, y = 3.4 * math.cos(a), 3.4 * math.sin(a); pos.append((x, y))
        _caja(ax, x - 1.25, y - 0.6, 2.5, 1.2, f, ec=S[i % 5], fc=SUP, fs=9.5, peso="bold")
    for i in range(len(fases)):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % len(fases)]
        _flecha(ax, (x1 + (x2 - x1) * .32, y1 + (y2 - y1) * .32), (x1 + (x2 - x1) * .68, y1 + (y2 - y1) * .68))
    ax.text(0, 0, "Ciclo de vida\nde los datos", ha="center", va="center", fontsize=12, color=TINTA2)
    guardar(fig, "v14_ciclo.svg")


def v14_dcat():
    fig, ax = plt.subplots(figsize=(10, 3.6)); ax.set_xlim(0, 16); ax.set_ylim(0, 5.4); ax.axis("off")
    nodos = [(0.3, "dcat:Catalog", "Catálogo\n(datos.gob.es)", S[0]), (5.6, "dcat:Dataset", "Conjunto de datos\n(préstamos de bibliotecas)", S[1]),
             (10.9, "dcat:Distribution", "Distribución\n(fichero CSV, API JSON…)", S[2])]
    for x, c, d, col in nodos:
        _caja(ax, x, 2.4, 4.8, 1.8, None, fc=SUP, ec=col)
        ax.text(x + 2.4, 3.65, c, ha="center", va="center", fontsize=10.5, fontweight="bold", color=TINTA, family="monospace")
        ax.text(x + 2.4, 2.95, d, ha="center", va="center", fontsize=9, color=TINTA2)
    _flecha(ax, (5.1, 3.3), (5.6, 3.3)); ax.text(5.35, 4.45, "dcat:dataset", ha="center", fontsize=8.5, color=TINTA2, family="monospace")
    _flecha(ax, (10.4, 3.3), (10.9, 3.3)); ax.text(10.65, 4.45, "dcat:distribution", ha="center", fontsize=8.5, color=TINTA2, family="monospace")
    props = ["dct:title · dct:description · dct:publisher · dct:license · dcat:theme · dct:modified", "", "dcat:accessURL · dcat:downloadURL · dct:format · dcat:mediaType"]
    ax.text(8.0, 1.5, "Propiedades del conjunto: " + props[0], ha="center", fontsize=8.5, color=TINTA, family="monospace")
    ax.text(8.0, 0.8, "Propiedades de la distribución: " + props[2], ha="center", fontsize=8.5, color=TINTA, family="monospace")
    guardar(fig, "v14_dcat.svg")


def v14_valor():
    fig, ax = plt.subplots(figsize=(10, 2.8)); ax.set_xlim(0, 16); ax.set_ylim(0, 4); ax.axis("off")
    pasos = [("Datos públicos\nen abierto", S[0]), ("Captura y\nlimpieza", S[1]), ("Integración\ncon otras fuentes", S[2]), ("Análisis y\nvisualización", S[3]), ("Producto o\nservicio", S[4])]
    for i, (t, c) in enumerate(pasos):
        x = 0.2 + i * 3.2
        _caja(ax, x, 1.2, 2.7, 1.6, t, ec=c, fc=SUP, fs=9.5, peso="bold")
        if i < 4: _flecha(ax, (x + 2.72, 2.0), (x + 3.18, 2.0))
    ax.text(8, 0.45, "Cada eslabón añade valor: ahí está el modelo de negocio de una infomediaria.", ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "v14_valor.svg")

for fn in (tema0, tema1, tema2, tema3, tema4, tema5, v14_fair, v14_ciclo, v14_dcat, v14_valor):
    fn()
