
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import os

NAVY   = RGBColor(0x00, 0x33, 0x65)
NAVY2  = RGBColor(0x13, 0x2F, 0x57)
GOLD   = RGBColor(0xD4, 0xAF, 0x37)
GOLD2  = RGBColor(0xC0, 0x92, 0x1C)
RED    = RGBColor(0xB2, 0x2A, 0x2A)
GREEN  = RGBColor(0x05, 0x7A, 0x55)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DARK   = RGBColor(0x1C, 0x27, 0x39)
MUTED  = RGBColor(0x55, 0x66, 0x7D)
CREAM  = RGBColor(0xC3, 0xD3, 0xE6)

NAVY_L  = RGBColor(0xEC, 0xF3, 0xFC)
GREEN_L = RGBColor(0xEA, 0xF8, 0xF2)
RED_L   = RGBColor(0xFB, 0xEF, 0xEF)
GOLD_L  = RGBColor(0xFD, 0xF7, 0xE7)
GRAY_L  = RGBColor(0xF0, 0xF3, 0xF8)
NAVY_BD = RGBColor(0xBE, 0xD6, 0xF1)
GREEN_BD= RGBColor(0x9A, 0xE0, 0xCA)
RED_BD  = RGBColor(0xE6, 0xB6, 0xB6)
GOLD_BD = RGBColor(0xE8, 0xD5, 0x95)
GRAY_BD = RGBColor(0xD2, 0xDB, 0xE6)
AMBER   = RGBColor(0x86, 0x5F, 0x00)
PROG_OFF= RGBColor(0x9A, 0xA6, 0xB5) 
HAIR    = RGBColor(0xDD, 0xE3, 0xEC) 

FONT = "Times New Roman"
FIG  = "figures"

S_FOOT  = 11
S_PROG  = 11
S_CAP   = 13
S_CARDB = 16
S_CARDL = 16
S_BODY  = 20
S_CLAIM = 20
S_TITLE = 30
S_KICK  = 24
S_BIG   = 40
S_FORM  = 22
S_TAKE  = 16
S_SECTL = 30
S_SECNUM= 96
S_COVER = 40
S_QA    = 54

CONTENT_TOP = 1.90
FOOT_RULE   = 7.16

SECTIONS = ["Introduction", "Semantic Scaling", "Observational Scaling",
            "Search Scaling", "Conclusion & Future Work"]

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.50)
BLANK = prs.slide_layouts[6]


def _bg(s, c=WHITE):
    f = s.background.fill; f.solid(); f.fore_color.rgb = c


def rect(s, l, t, w, h, color, line_color=None, line_pt=0.75, rounded=False, adj=0.08):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(l), Inches(t), Inches(w), Inches(h))
    if rounded:
        try: shp.adjustments[0] = adj
        except Exception: pass
    shp.shadow.inherit = False
    if color is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = color
    if line_color: shp.line.color.rgb = line_color; shp.line.width = Pt(line_pt)
    else: shp.line.fill.background()
    return shp


def soft_shadow(shp, blur=0.030, dist=0.018, alpha=38, clr="9AA6B5"):
    spPr = shp._element.spPr
    for e in spPr.findall(qn("a:effectLst")): spPr.remove(e)
    el = spPr.makeelement(qn("a:effectLst"), {})
    sh = el.makeelement(qn("a:outerShdw"),
                        {"blurRad": str(int(blur*914400)), "dist": str(int(dist*914400)),
                         "dir": "5400000", "rotWithShape": "0"})
    c = sh.makeelement(qn("a:srgbClr"), {"val": clr})
    c.append(c.makeelement(qn("a:alpha"), {"val": str(alpha*1000)}))
    sh.append(c); el.append(sh); spPr.append(el)
    return shp


def hline(s, l, t, w, color=GOLD, pt=1.4):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Pt(pt))
    shp.shadow.inherit = False
    shp.fill.solid(); shp.fill.fore_color.rgb = color; shp.line.fill.background()
    return shp


def txt(s, l, t, w, h, text, size=S_BODY, bold=False, color=DARK,
        align=PP_ALIGN.LEFT, italic=False, wrap=True, anchor=None, spacing=1.02):
    b = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = wrap
    tf.margin_left = Pt(2); tf.margin_right = Pt(2); tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    if anchor is not None: tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.text = text; p.alignment = align; p.line_spacing = spacing
    p.font.size = Pt(size); p.font.bold = bold; p.font.italic = italic
    p.font.color.rgb = color; p.font.name = FONT
    return b


def rich(s, l, t, w, h, segs, size=S_BODY, align=PP_ALIGN.LEFT, anchor=None, spacing=1.02):
    b = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    if anchor is not None: tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align; p.line_spacing = spacing
    for sg in segs:
        text, bold, color = sg[0], sg[1], sg[2]
        italic = sg[3] if len(sg) > 3 else False
        r = p.add_run(); r.text = text
        r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color; r.font.name = FONT
    return b


def bullets(s, l, t, w, h, items, size=S_BODY, color=DARK, spacing=8, sub=MUTED):
    b = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    for i, it in enumerate(items):
        lvl, text, bd = 0, it, False
        if isinstance(it, tuple):
            if len(it) == 3: text, lvl, bd = it
            else: text, lvl = it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ("•  " + text) if lvl == 0 else ("–  " + text)
        p.font.size = Pt(size if lvl == 0 else size - 2)
        p.font.bold = bd
        p.font.color.rgb = color if lvl == 0 else sub
        p.font.name = FONT; p.space_after = Pt(spacing if lvl == 0 else 3); p.line_spacing = 1.02
    return b


def pic(s, fname, l, t, width=None, height=None, caption=None):
    rh = height or width or 8
    path = os.path.join(FIG, fname + ".png")
    kw = {}
    if width: kw["width"] = Inches(width)
    if height: kw["height"] = Inches(height)
    if not kw: kw["width"] = Inches(8)
    s.shapes.add_picture(path, Inches(l), Inches(t), **kw)
    if caption:
        txt(s, l, t + rh + 0.05, width or 8, 0.34, caption, S_CAP, False, MUTED, PP_ALIGN.CENTER)
    return rh


def notes(s, text): s.notes_slide.notes_text_frame.text = text


def _card(s, l, t, w, h, label, body, bg, bd, strip, lc, body_col=DARK,
          body_size=S_CARDB):
    rect(s, l, t, w, h, bg, line_color=bd, line_pt=1.0, rounded=True)
    rect(s, l + 0.02, t + 0.11, 0.09, h - 0.22, strip)
    if label:
        txt(s, l + 0.26, t + 0.11, w - 0.38, 0.34, label, S_CARDL, True, lc)
    if body:
        top = t + 0.50 if label else t + 0.15
        ht  = h - 0.60 if label else h - 0.26
        if isinstance(body, list):
            bullets(s, l + 0.26, top, w - 0.46, ht, body, body_size, body_col, spacing=5)
        else:
            txt(s, l + 0.26, top, w - 0.46, ht, body, body_size, False, body_col)

def info_card(s,l,t,w,h,lab,body,**k):   _card(s,l,t,w,h,lab,body,NAVY_L,NAVY_BD,NAVY,NAVY,**k)
def result_card(s,l,t,w,h,lab,body,**k): _card(s,l,t,w,h,lab,body,GREEN_L,GREEN_BD,GREEN,GREEN,**k)
def warn_card(s,l,t,w,h,lab,body,**k):   _card(s,l,t,w,h,lab,body,RED_L,RED_BD,RED,RED,**k)
def gold_card(s,l,t,w,h,lab,body,**k):   _card(s,l,t,w,h,lab,body,GOLD_L,GOLD_BD,GOLD,AMBER,**k)
def gray_card(s,l,t,w,h,lab,body,**k):   _card(s,l,t,w,h,lab,body,GRAY_L,GRAY_BD,MUTED,MUTED,**k)


def stat_card(s, l, t, w, h, big, label, sentence, accent=NAVY, bg=NAVY_L, bd=NAVY_BD):
    rect(s, l, t, w, h, bg, line_color=bd, line_pt=1.0, rounded=True)
    txt(s, l + 0.22, t + 0.16, w - 0.40, 0.66, big, S_KICK, True, accent)
    txt(s, l + 0.22, t + 0.86, w - 0.40, 0.36, label, S_CARDL, True, DARK)
    txt(s, l + 0.22, t + 1.26, w - 0.40, h - 1.36, sentence, S_CARDB, False, MUTED)


def chip(s, l, t, w, h, text, fill, tc, size=S_CARDB, bold=True, bd=None, italic=False):
    r = rect(s, l, t, w, h, fill, line_color=bd, line_pt=1.0, rounded=True)
    tf = r.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(4); tf.margin_right = Pt(4); tf.margin_top = Pt(2); tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; p.text = text
    p.font.size = Pt(size); p.font.bold = bold; p.font.italic = italic
    p.font.color.rgb = tc; p.font.name = FONT
    return r


def arrow(s, l, t, text="→", size=22, color=GOLD2):
    txt(s, l, t, 0.44, 0.44, text, size, True, color, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def mathbox(s, l, t, w, h, expr, label=None, expr_size=S_FORM, accent=NAVY):
    rect(s, l, t, w, h, GRAY_L, line_color=GRAY_BD, line_pt=1.0, rounded=True)
    rect(s, l + 0.02, t + 0.10, 0.09, h - 0.20, accent)
    if label:
        txt(s, l + 0.26, t + 0.10, w - 0.40, 0.30, label, S_CARDL, True, accent)
        txt(s, l + 0.26, t + 0.44, w - 0.52, h - 0.54, expr, expr_size, False, DARK,
            PP_ALIGN.CENTER, italic=True, anchor=MSO_ANCHOR.MIDDLE)
    else:
        txt(s, l + 0.26, t + 0.06, w - 0.52, h - 0.12, expr, expr_size, False, DARK,
            PP_ALIGN.CENTER, italic=True, anchor=MSO_ANCHOR.MIDDLE)


def progbar(s, active):
    x0, y0, total = 0.55, 0.23, 11.05
    seg = (total - 4*0.08) / 5
    for i, name in enumerate(SECTIONS):
        lx = x0 + i * (seg + 0.08)
        on = (i == active)
        c = chip(s, lx, y0, seg, 0.26, name,
                 NAVY if on else WHITE, WHITE if on else MUTED,
                 size=S_PROG, bold=on, bd=None if on else HAIR)
        soft_shadow(c, alpha=(46 if on else 20))


def footer(s):
    hline(s, 0.55, FOOT_RULE, 12.23, GRAY_BD, 0.8)
    txt(s, 0.55, FOOT_RULE + 0.04, 9.0, 0.26,
        "Towards Scalable and Generalizable Video Retrieval", 9, False, MUTED)
    txt(s, 10.3, FOOT_RULE + 0.04, 2.48, 0.26, "Zhuoning Guo · HKUST(GZ)", 9, False, MUTED, PP_ALIGN.RIGHT)


PAGE = {"n": 0}
def _pg(): PAGE["n"] += 1; return PAGE["n"]


def base(active, title, claim=None):
    s = prs.slides.add_slide(BLANK); _bg(s)
    progbar(s, active)
    txt(s, 11.75, 0.22, 1.03, 0.30, str(_pg()), S_FOOT, False, MUTED, PP_ALIGN.RIGHT,
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 0.55, 0.66, 12.23, 0.62, title, S_TITLE, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, 0.57, 1.36, 2.10, GOLD, 3.0)
    if claim:
        txt(s, 0.55, 1.42, 12.23, 0.36, claim, S_CLAIM, False, MUTED, italic=True)
    footer(s)
    return s


def take(s, text, y=6.40):
    rect(s, 0.55, y, 12.23, 0.54, NAVY, rounded=True)
    rich(s, 0.80, y + 0.02, 11.8, 0.50, [("Takeaway   ", True, GOLD), (text, False, WHITE)],
         size=S_TAKE, anchor=MSO_ANCHOR.MIDDLE)


def caption(s, text, y=6.52, w=12.23):
    hline(s, 0.57, y, 1.6, GOLD, 1.4)
    txt(s, 0.55, y + 0.09, w, 0.36, text, S_CAP, False, MUTED, italic=True)


def flatcol(s, l, t, w, label, body, accent=NAVY, body_size=S_CARDB, bh=1.20):
    rect(s, l, t + 0.02, 0.08, 0.30, accent)
    txt(s, l + 0.20, t, w - 0.20, 0.34, label, S_CARDL, True, NAVY)
    if isinstance(body, list):
        bullets(s, l + 0.20, t + 0.42, w - 0.24, bh, body, body_size, MUTED, spacing=4)
    else:
        txt(s, l + 0.20, t + 0.42, w - 0.24, bh, body, body_size, False, MUTED)


def add_table(s, headers, rows, l, t, w, h, best_row=-1, hi_col=None,
              col_widths=None, fs=14, hfs=14):
    nc, nr = len(headers), len(rows) + 1
    shp = s.shapes.add_table(nr, nc, Inches(l), Inches(t), Inches(w), Inches(h))
    tb = shp.table
    try: tb.first_row = False; tb.horz_banding = False
    except Exception: pass
    if col_widths:
        tot = Inches(w)
        for j, cwd in enumerate(col_widths): tb.columns[j].width = int(tot * cwd)
    for j, hd in enumerate(headers):
        c = tb.cell(0, j); c.text = hd; c.fill.solid(); c.fill.fore_color.rgb = NAVY
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        for p in c.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT
            p.font.size = Pt(hfs); p.font.bold = True; p.font.color.rgb = WHITE; p.font.name = FONT
    for i, row in enumerate(rows):
        best = (i == best_row)
        for j, val in enumerate(row):
            c = tb.cell(i + 1, j); c.text = str(val); c.fill.solid()
            c.fill.fore_color.rgb = GREEN_L if best else (GRAY_L if i % 2 else WHITE)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in c.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT
                p.font.size = Pt(fs); p.font.name = FONT
                if best: p.font.bold = True; p.font.color.rgb = GREEN
                elif hi_col and j in hi_col: p.font.bold = True; p.font.color.rgb = NAVY
                else: p.font.color.rgb = DARK
    return tb


def section(num, label, title, question, sub=None):
    s = prs.slides.add_slide(BLANK); _bg(s)
    rect(s, 0, 0, 4.6, 7.50, NAVY2)
    rect(s, 4.6, 0, 0.10, 7.50, GOLD)
    txt(s, 0.45, 1.30, 3.95, 2.0, num, S_SECNUM, True, GOLD, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, 0.58, 3.55, 1.75, WHITE, 2.0)
    txt(s, 0.58, 3.76, 3.7, 0.4, label.upper(), S_FOOT + 1, True, CREAM)
    txt(s, 0.58, 4.18, 3.75, 1.7, title, S_SECTL, True, WHITE)
    txt(s, 5.35, 2.55, 7.4, 0.4, "GUIDING QUESTION", S_FOOT, True, GOLD)
    txt(s, 5.35, 3.02, 7.5, 2.3, question, 26, False, DARK)
    if sub:
        txt(s, 5.35, 5.25, 7.4, 1.4, sub, S_CARDB, False, MUTED)
    txt(s, 11.75, 0.22, 1.03, 0.30, str(_pg()), S_FOOT, False, MUTED, PP_ALIGN.RIGHT)
    notes(s, question)
    return s


s = prs.slides.add_slide(BLANK); _bg(s)
rect(s, 0.55, 0.55, 0.62, 0.62, NAVY)
rect(s, 12.16, 6.33, 0.62, 0.62, GOLD)
hline(s, 1.30, 3.40, 10.73, GOLD, 2.0)
txt(s, 0.70, 1.78, 11.93, 1.55, "Towards Scalable and Generalizable\nVideo Retrieval",
    S_COVER, True, NAVY, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.70, 3.52, 11.93, 0.44, "PhD Thesis Defense", 16, False, MUTED, PP_ALIGN.CENTER)
txt(s, 0.70, 4.14, 11.93, 0.62, "Zhuoning Guo", 26, True, NAVY, PP_ALIGN.CENTER)
txt(s, 0.70, 4.88, 11.93, 0.40, "Thrust of Artificial Intelligence, HKUST(GZ)", 14, False, DARK, PP_ALIGN.CENTER)
rich(s, 0.70, 5.36, 11.93, 0.40,
     [("Advisors:  ", False, MUTED), ("Prof. Xiaowen Chu", True, NAVY),
      ("   &   ", False, MUTED), ("Prof. Renjing Xu", True, NAVY)], size=14, align=PP_ALIGN.CENTER)
txt(s, 0.70, 5.86, 11.93, 0.36, "July 29, 2026", 12, False, MUTED, PP_ALIGN.CENTER)
txt(s, 0.70, 6.46, 11.93, 0.5,
    "“How can video retrieval stay generalizable as semantic capability, visual observation, and search scale all grow?”",
    14, False, GOLD2, PP_ALIGN.CENTER, italic=True)
notes(s, "Good morning. I am Zhuoning Guo. This thesis studies video retrieval as a pipeline-level "
         "scaling problem, advised by Prof. Xiaowen Chu and Prof. Renjing Xu.")

s = base(0, "Video Retrieval Underpins Modern Multimedia Systems",
         "Search, recommendation, and discovery all reduce to matching a query to a video corpus.")
apps = [("Search", "Find videos from text, an image, or a clip across a massive corpus."),
        ("Recommendation", "Match evolving user intent to a fast-growing item catalog."),
        ("Discovery & personalization", "Surface relevant long-form content under strict latency.")]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (h, b) in enumerate(apps):
    flatcol(s, x0 + i*(cw+cg), 2.05, cw, h, b, bh=2.05)
for vx in (4.62, 8.77):
    rect(s, vx, 2.10, 0.012, 2.30, HAIR)
gold_card(s, 0.55, 4.85, 12.23, 1.35, "The shift",
          "As corpora, query forms, and serving traffic all grow, retrieval stops being a single "
          "benchmark task and becomes a pipeline-level scaling problem — the subject of this thesis.")
notes(s, "Video retrieval is foundational to search, recommendation, and discovery — and it is scaling.")

s = base(0, "Roadmap: From Representation to Observation to Search",
         "One pipeline, three sequential scaling bottlenecks, three studies.")
road = [
    ("01", "Motivation", "Video retrieval is a pipeline-level scaling problem", NAVY),
    ("02", "Study 1 · Semantic Scaling — GVE", "Diagnose capabilities → synthesize data → unified embedding", GOLD2),
    ("03", "Study 2 · Observational Scaling — MG-LVR & VEterfall", "Granularity-aware evidence → scaling laws → distillation", GOLD2),
    ("04", "Study 3 · Search Scaling — GMP-GR", "Search-compatible metric → graph traversal → GPU execution", GOLD2),
    ("05", "Conclusion & Future Work", "Structure-aware scaling across the pipeline", NAVY),
]
y = 2.02
for num, lab, desc, col in road:
    rect(s, 0.95, y, 0.64, 0.64, col, rounded=True)
    txt(s, 0.95, y, 0.64, 0.64, num, 18, True, WHITE, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 1.80, y - 0.02, 10.9, 0.40, lab, S_BODY, True, NAVY)
    txt(s, 1.80, y + 0.36, 10.9, 0.32, desc, S_CARDB, False, MUTED)
    if num != "05": rect(s, 1.24, y + 0.66, 0.05, 0.32, GRAY_BD)
    y += 0.98
notes(s, "The talk follows the retrieval pipeline; three studies attack three successive bottlenecks.")

s = base(0, "Video Retrieval Is a Pipeline, Not a Single Benchmark Task",
         "A query is answered by a chain of decisions, each with its own scaling pressure.")
stages = [("Query", "text / image /\ncomposed"), ("Representation", "embed query\n& video"),
          ("Observation", "sample frames\n& tokens"), ("Search", "billion-scale\nANNS"),
          ("Candidates", "ranked\nresult set")]
sw, gap, x0, y0 = 2.16, 0.30, 0.62, 2.10
for i, (h, b) in enumerate(stages):
    active = i in (1, 2, 3); lx = x0 + i*(sw+gap)
    chip(s, lx, y0, sw, 1.20, h, NAVY if active else GRAY_L, WHITE if active else MUTED,
         size=S_BODY, bd=None if active else GRAY_BD)
    txt(s, lx, y0 + 1.24, sw, 0.50, b, S_CARDB, False, MUTED, PP_ALIGN.CENTER)
    if i < 4: arrow(s, lx + sw, y0 + 0.50, size=24)
for i, lab in [(1, "semantic\ncapability gap"), (2, "visual\nevidence gap"), (3, "searchability\ngap")]:
    lx = x0 + i*(sw+gap)
    arrow(s, lx + sw/2 - 0.22, 3.92, text="↓", size=22, color=RED)
    chip(s, lx, 4.18, sw, 0.90, lab, RED_L, RED, size=S_CARDB, bd=RED_BD)
gold_card(s, 0.62, 5.30, 12.16, 0.80, None,
          "Modern retrieval fails not because one benchmark is hard, but because different pipeline "
          "stages expose different scaling bottlenecks.")
notes(s, "Retrieval is a chain: represent, observe, search — each stage has a distinct bottleneck.")

s = base(0, "Problem Formulation: Embedding-Based Video Retrieval",
         "A shared embedding space ranks a corpus by similarity to any query form.")
info_card(s, 0.55, 1.98, 6.05, 2.15, "Objective",
          "Learn an encoder E_θ mapping a query q (text, visual, or composed) and every video v "
          "into a shared space, so relevant pairs rank above irrelevant ones and a compact "
          "candidate set is returned for downstream ranking.")
mathbox(s, 0.55, 4.28, 6.05, 1.15,
        "s(q → v)  =  cos( E_θ(q),  E_θ(v) )", label="Relevance score", expr_size=24)
info_card(s, 6.75, 1.98, 6.03, 3.45, "Two axes of universality",
          ["Query format:  Textual (TXT), Composed (CMP), Visual (VIS)",
           "Data domain:  Coarse-grained (CG), Fine-grained (FG), Long-context (LC)",
           "Fine-grained splits:  Spatial (S), Temporal (T), Partial Relevance (PR)"])
gold_card(s, 6.75, 5.42, 6.03, 1.45, "Why it is hard",
          "A model may excel on one axis (e.g. text–video) yet fail on composed, visual-only, or "
          "partially-relevant retrieval — leaderboards hide this.")
gray_card(s, 0.55, 5.42, 6.05, 1.45, "Scope",
          "Studies 1–2 target text/visual→video retrieval; Study 3 targets web-scale user→item "
          "retrieval under the same searchable-signal principle.")
notes(s, "Formal setup: one embedding space, cosine relevance, evaluated across query formats and domains.")

s = base(0, "The Benchmark–Reality Gap Is Structural",
         "Leaderboard conditions differ from deployment along every axis that matters.")
txt(s, 0.75, 2.02, 5.9, 0.4, "BENCHMARK WORLD", S_CARDL, True, MUTED)
txt(s, 7.05, 2.02, 5.7, 0.4, "PRODUCTION REALITY", S_CARDL, True, RED)
rows = [("Video length", "Short clips (10–30 s)", "Minutes to hours"),
        ("Query form", "Single type (text)", "Text · image · composed"),
        ("Corpus size", "1K–10K videos", "Billion-scale pools"),
        ("Serving", "Offline evaluation", "Sub-10 ms latency budget")]
y = 2.52
for axis, be, pr in rows:
    txt(s, 0.55, y + 0.10, 1.95, 0.5, axis, S_CARDB, True, NAVY)
    chip(s, 2.55, y, 4.05, 0.66, be, GRAY_L, MUTED, size=S_CARDB, bold=False, bd=GRAY_BD)
    chip(s, 6.90, y, 5.88, 0.66, pr, RED_L, DARK, size=S_CARDB, bold=False, bd=RED_BD)
    y += 0.80
gold_card(s, 0.55, 5.92, 12.23, 0.9, None,
          "Each production stage exposes a bottleneck that short-clip benchmarks make invisible.")
notes(s, "The gap is structural — along length, query form, corpus size, and serving.")

s = base(0, "Three Bottlenecks Structure the Thesis",
         "Representation, observation, and search each need structure-aware scaling.")
pic(s, "thesis-framework", 2.915, 2.02, width=7.5)
_stages = [
    ("Semantic Scaling",       "Capability gaps across query forms & relevance types"),
    ("Observational Scaling",  "Evidence gaps under limited frame/token budgets"),
    ("Search Scaling",         "Metric–graph–GPU incompatibility at scale"),
]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (lab, desc) in enumerate(_stages):
    lx = x0 + i * (cw + cg)
    txt(s, lx, 6.07, cw, 0.26, lab,  S_CARDB, True,  NAVY)
    txt(s, lx, 6.33, cw, 0.22, desc, S_CAP,   False, MUTED)
for vx in (4.74, 8.93):
    rect(s, vx, 6.07, 0.012, 0.48, HAIR)
take(s, "Generalizability is the evidence that scaling has addressed the right bottleneck.", y=6.60)
notes(s, "Thesis Figure 1.1: three-stage pipeline with structural bottlenecks and structure-aware solutions.")

s = base(0, "Naive Scaling Fails Differently at Each Stage",
         "More parameters, more frames, or higher offline AUC each hit a different wall.")
cwid = [0.15, 0.24, 0.33, 0.28]; xs = [0.55]
for f in cwid[:-1]: xs.append(xs[-1] + f*12.23)
head = [("Stage", MUTED), ("Naive scaling", MUTED), ("Why it fails", RED), ("Structure-aware fix", GREEN)]
for k, (hd, col) in enumerate(head):
    txt(s, xs[k], 2.02, cwid[k]*12.23, 0.36, hd, S_CARDL, True, col)
rowd = [("Semantic", "More params /\ngeneric data", "Capability gaps persist even at 8B parameters",
         "Diagnose → synthesize → curriculum"),
        ("Observation", "More frames /\ntokens", "Fine recall barely moves with 16× more frames",
         "Granularity-aware allocation + distillation"),
        ("Search", "Higher offline\nmetric AUC", "Neural metrics break greedy graph traversal",
         "Metric–graph–GPU co-design")]
y = 2.48
for st, na, fa, fx in rowd:
    chip(s, xs[0], y, cwid[0]*12.23-0.15, 1.06, st, NAVY, WHITE, size=S_CARDB)
    chip(s, xs[1], y, cwid[1]*12.23-0.15, 1.06, na, GRAY_L, MUTED, size=S_CARDB, bold=False, bd=GRAY_BD)
    chip(s, xs[2], y, cwid[2]*12.23-0.15, 1.06, fa, RED_L, DARK, size=S_CARDB, bold=False, bd=RED_BD)
    chip(s, xs[3], y, cwid[3]*12.23, 1.06, fx, GREEN_L, DARK, size=S_CARDB, bold=False, bd=GREEN_BD)
    y += 1.20
notes(s, "Failure modes are qualitatively different, so no single scaling recipe fixes all three.")

s = base(0, "Three Studies Address Three Pipeline Bottlenecks",
         "Each study delivers a diagnosis, a method, and generalization evidence.")
contrib = [("Study 1 · Semantic Scaling",
            ["UVRB: unified diagnosis, 16 datasets × 14 models",
             "V-SynFlow → UVRD: 1.55M capability-targeted pairs",
             "GVE: SOTA zero-shot generalization (0.573 / 0.600)"]),
           ("Study 2 · Observational Scaling",
            ["MG-LVR: 9,971 queries over 4,844 long videos (706 s)",
             "Spatiotemporal scaling laws for frame/token budgets",
             "VEterfall: +20% fine-grained at 4–16× efficiency"]),
           ("Study 3 · Search Scaling",
            ["MUIRML + SCL: search-compatible neural metric",
             "HiPANNS: parallel graph traversal on GPU",
             "GMP-GR: +20.9% coverage; validated in two A/B services"])]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (name, items) in enumerate(contrib):
    lx = x0 + i*(cw+cg)
    rect(s, lx, 2.00, cw, 4.55, WHITE, line_color=NAVY_BD, line_pt=1.0, rounded=True)
    rect(s, lx, 2.00, cw, 0.68, NAVY, rounded=True)
    txt(s, lx, 2.00, cw, 0.68, name, S_CARDL, True, WHITE, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    bullets(s, lx + 0.24, 2.86, cw - 0.44, 3.6, items, S_CARDB, DARK, spacing=11)
notes(s, "Three studies, one argument: structure-aware scaling along the retrieval pipeline.")


section("01", "Study 1 · Semantic Scaling", "General Video\nEmbedding (GVE)",
        "What capabilities should a video retrieval model possess, and how do we scale toward them?",
        "Chapter 3 · submitted to ACM MM 2026")

s = base(1, "Universal Video Retrieval Requires Capability Coverage",
         "Generalization means covering query forms, domains, and relevance types.")
flatcol(s, 0.55, 1.98, 6.05, "Query formats",
        ["Textual (TXT) — natural-language prompts",
         "Composed (CMP) — text + visual reference",
         "Visual (VIS) — reference frame or clip"], bh=1.65)
flatcol(s, 6.73, 1.98, 6.05, "Domains & relevance",
        ["Coarse (CG) vs. fine-grained (FG) vs. long-context (LC)",
         "Fine-grained splits: Spatial (S), Temporal (T)",
         "Partial Relevance (PR) — only part of a video matches"], bh=1.65)
rect(s, 6.58, 2.02, 0.012, 1.90, HAIR)
warn_card(s, 0.55, 4.10, 12.23, 1.15, "The trap",
          "A model can top MSR-VTT yet fail on composed, visual-only, or partially-relevant "
          "retrieval — a single leaderboard score hides the capabilities that matter.")
gold_card(s, 0.55, 5.40, 12.23, 1.20, "Core insight",
          "Semantic scaling means scaling toward broader capability coverage across formats, "
          "domains, and relevance types — not merely adding parameters or generic pairs.")
notes(s, "Universal retrieval is defined by capability coverage, not a single benchmark.")

s = base(1, "UVRB: One Protocol to Diagnose 14 Models on 16 Datasets",
         "A standardized diagnostic that measures what a model lacks, not just its rank.")
pic(s, "gve/uvrb", 0.965, 2.00, width=11.4,
    caption="UVRB unifies 16 public datasets into one evaluation space with six capability labels.")
cols12 = [(0.62, "Unified protocol",
           ["16 datasets, identical preprocessing", "Frozen embeddings, cosine similarity",
            "No task-specific fine-tuning"]),
          (4.77, "14 baselines",
           ["87M → 8.3B parameters", "CLIP- & MLLM-based families", "GME · UNITE · VLM2Vec · UniME · B3"]),
          (8.92, "Diagnostic power",
           "Maps the capability a model is missing — not just its leaderboard rank.")]
for cx, lab, bd in cols12:
    flatcol(s, cx, 5.12, 3.85, lab, bd)
for vx in (4.62, 8.77):
    rect(s, vx, 5.16, 0.012, 1.34, HAIR)
notes(s, "UVRB is a diagnostic, not a leaderboard: one protocol isolating six capability dimensions.")

s = base(1, "UVRB Reveals Structured, Not Random, Capability Gaps",
         "Weaknesses track the training distribution and cluster on the same hard skills.")
pic(s, "gve/uvrb_dual_radar", 0.55, 2.02, width=8.7,
    caption="Per-dataset (left) and per-ability (right) coverage; GVE-7B forms the outer envelope.")
flatcol(s, 9.45, 2.05, 3.35, "GVE-7B",
        "Fills the largest area across both datasets and abilities.", accent=GREEN, bh=0.90)
flatcol(s, 9.45, 3.55, 3.35, "Shared blind spots",
        "Temporal, composed, and partial-relevance retrieval stay weak across all 14 models — "
        "even at 8.3B parameters.", accent=RED, bh=1.40)
flatcol(s, 9.45, 5.45, 3.35, "Structured, not random",
        "Gaps can be diagnosed and targeted, not scaled away by size.", accent=GOLD2)
notes(s, "The radar is the evidence: gaps are systematic and tied to data coverage.")

s = base(1, "Three Non-Trivial Capability Gaps Emerge",
         "Diagnosis surfaces one proxy, one decoupling, and one scaling paradox.")
stat_card(s, 0.55, 1.98, 3.95, 3.15, "ρ ≈ 0.97", "PR predicts universality",
          "Partial-relevance retrieval correlates with overall UVR far more than MSR-VTT "
          "(ρ ≈ 0.58) — a lightweight universality proxy.")
stat_card(s, 4.69, 1.98, 3.95, 3.15, "ρ ≈ 0.12", "Spatial ⟂ Temporal",
          "Spatial and temporal skills are near-independent; temporal drives fine-grained recall "
          "(ρ ≈ 0.98), spatial does not (ρ ≈ 0.39).")
stat_card(s, 8.83, 1.98, 3.95, 3.15, "87M > 8B", "Scaling paradox (VIS)",
          "On visual-only retrieval an 87M CLIP model (0.714) beats an 8B MLLM (0.702) — "
          "perceptual breadth over raw capacity.", accent=RED, bg=RED_L, bd=RED_BD)
take(s, "Bigger is not broader — targeted, diverse data, not parameter count, closes these gaps.", y=5.42)
notes(s, "Three findings: PR proxy, spatial/temporal decoupling, and the visual-only scaling paradox.")

s = base(1, "V-SynFlow: Capability-Guided Data Synthesis",
         "A three-stage pipeline synthesizes exactly the skills diagnosis flagged as weak.")
pic(s, "gve/v-synflow", 0.55, 1.98, width=12.23)
steps = [("① Quality control", "Filter web video by quality, cross-modal consistency, and temporal dynamics."),
         ("② Information enrichment", "MLLM captioning skewed to under-represented temporal & spatial skills."),
         ("③ Task extension", "Synthesize composed and visual tasks covering all UVRB dimensions.")]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (h, b) in enumerate(steps):
    flatcol(s, x0 + i*(cw+cg), 4.88, cw, h, b, bh=1.00)
for vx in (4.62, 8.77):
    rect(s, vx, 4.92, 0.012, 1.20, HAIR)
caption(s, "Capability-skewed synthesis — 60% temporal · 30% spatial · 10% partial/abstract — targets diagnosed gaps.", y=6.52)
notes(s, "V-SynFlow turns the diagnosis into data: control quality, enrich toward gaps, extend tasks.")

s = base(1, "UVRD Is Capability-Targeted, Not Merely Large",
         "1.55M synthetic pairs, skewed to diagnosed gaps and audited for quality.")
stat_card(s, 0.55, 1.98, 3.02, 2.55, "1.55M", "Training pairs",
          "A multi-task corpus built for the capabilities models actually lack.")
stat_card(s, 3.71, 1.98, 3.02, 2.55, "95%", "Sample audit",
          "Factual accuracy on a 100-sample human audit; downstream gains confirm quality at scale.",
          accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
stat_card(s, 6.87, 1.98, 3.02, 2.55, "60/30/10", "Gap-targeted skew",
          "Temporal / spatial / partial-abstract emphasis over generic coverage.")
add_table(s, ["UVRD task", "Pairs"],
          [["T2V  text→video", "879K"], ["T2I  text→image", "210K"],
           ["I2V  image→video", "200K"], ["T2T / TI2V / TV2V / V2V", "260K"]],
          10.03, 1.98, 2.75, 2.55, fs=13, hfs=13, col_widths=[0.66, 0.34])
gold_card(s, 0.55, 4.72, 12.23, 1.10, "Design principle",
          "Skew beats naive scale: UVRD is not the largest corpus, but the most effective for "
          "filling the capability gaps UVRB diagnosed.")
notes(s, "UVRD embodies capability-first data design: targeted skew plus audited quality.")

s = base(1, "GVE: A Unified Embedding Trained by Contrastive Learning",
         "One Qwen2.5-VL backbone maps every query form into a shared retrieval space.")
pic(s, "gve/model", 0.55, 1.98, width=8.4,
    caption="GVE encodes text, image, video, and composed queries into one aligned embedding space.")
info_card(s, 9.15, 1.98, 3.63, 1.65, "Backbone",
          "Qwen2.5-VL MLLM; parameter-efficient LoRA fine-tuning; last-token pooling + ℓ2 norm.")
mathbox(s, 9.15, 3.75, 3.63, 1.55,
        "ℒ = −log  exp(s⁺/τ)\n———————————\nΣ exp(s/τ) + Σ exp(s⁻/τ)",
        label="Symmetric InfoNCE", expr_size=15)
result_card(s, 9.15, 5.42, 3.63, 1.40, "Objective",
            "Align matched pairs against in-batch + mined hard negatives (τ = 0.03), symmetrized q↔v.")
notes(s, "GVE is one unified embedding model; training is symmetric InfoNCE with hard negatives.")

s = base(1, "The Modality Pyramid Curriculum Stabilizes Training",
         "A difficulty-ordered schedule prevents gradient interference across tasks.")
pic(s, "gve/modality-pyramid", 0.55, 1.98, width=5.0,
    caption="Pyramid: easy atomic alignment → text-video → composed retrieval.")
info_card(s, 5.80, 1.98, 6.98, 1.55, "Bottom-up curriculum",
          "Text–image alignment → text–video matching → composed video retrieval, building "
          "capability incrementally rather than mixing all tasks at once.")
mathbox(s, 5.80, 3.65, 6.98, 1.75,
        "P⁽ᵗ⁾(k)  ∝  exp( R_k⁽ᵗ⁾ / σ(t) ),    R_k = (1/Nₚ) Σ cos( Ψ(xᵢ), Ψ(yᵢ) )",
        label="Alignment-aware dynamic scheduling", expr_size=18)
gold_card(s, 5.80, 5.52, 6.98, 1.05, "Mechanism",
          "A prober Ψ scores per-task alignment; temperature σ(t) rises 0.1→1.0 across epochs, "
          "shifting sampling from easy to hard tasks.")
notes(s, "The curriculum orders tasks by measured alignment, stabilizing multi-task training.")

s = base(1, "GVE Improves Zero-Shot Retrieval Generalization",
         "New SOTA on both dataset-level and ability-level averages across 16 datasets.")
add_table(s, ["Model", "Dataset AVG", "Ability AVG"],
          [["CLIP4Clip (87M)", "0.390", "0.416"],
           ["Unite-7B (prev. best)", "0.538", "0.559"],
           ["GVE-3B (ours, 3.8B)", "0.544", "0.571"],
           ["GVE-7B (ours, 8.3B)", "0.573", "0.600"]],
          0.55, 1.98, 6.55, 2.55, best_row=3, hi_col=[1, 2], fs=15, col_widths=[0.44, 0.28, 0.28])
stat_card(s, 7.35, 1.98, 2.62, 2.55, "+6.5%", "Dataset AVG",
          "vs Unite-7B, over 16 datasets.", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
stat_card(s, 10.16, 1.98, 2.62, 2.55, "+7.3%", "Ability AVG",
          "vs Unite-7B, over 8 abilities.", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
gold_card(s, 0.55, 4.66, 12.23, 1.28, "Efficiency",
          "GVE-3B (3.8B) already outperforms the larger Unite-7B — data quality beats parameter "
          "count, while GVE-7B remains the strongest variant.")
take(s, "Capability-targeted data lifts a smaller model above a larger baseline.", y=6.12)
notes(s, "GVE sets new SOTA on both averages; GVE-3B beats Unite-7B; GVE-7B is strongest.")

s = base(1, "Where the Gains Come From: Ability Breakdown",
         "GVE-7B leads on the hard skills UVRB flagged, while staying competitive elsewhere.")
add_table(s, ["Ability", "Unite-7B", "GVE-7B", "Δ"],
          [["Text (TXT)", "0.609", "0.657", "+0.048"],
           ["Composed (CMP)", "0.254", "0.312", "+0.058"],
           ["Long-context (LC)", "0.746", "0.814", "+0.068"],
           ["Temporal (T)", "0.412", "0.469", "+0.057"],
           ["Fine-grained (FG)", "0.539", "0.570", "+0.031"],
           ["Visual-only (VIS)", "0.666", "0.657", "−0.009"]],
          0.55, 1.98, 7.35, 3.75, hi_col=[2], fs=14, col_widths=[0.40, 0.20, 0.20, 0.20])
info_card(s, 8.10, 1.98, 4.68, 1.75, "Largest gains",
          "Composed, long-context, and temporal — exactly the capabilities diagnosis identified "
          "as under-served.")
warn_card(s, 8.10, 3.86, 4.68, 1.87, "Honest boundary",
          "Visual-only retrieval stays flat: the scaling-paradox skill where a compact CLIP "
          "encoder remains hard to beat.")
caption(s, "Targeted synthesis raises the diagnosed weak skills without sacrificing the strong ones.", y=6.55)
notes(s, "The gains land on the diagnosed gaps; VIS remains the honest exception.")

s = base(1, "UVRD and Curriculum Provide Complementary Gains",
         "Targeted data and ordered training each contribute; together they compound.")
add_table(s, ["3B variant", "Dataset AVG", "Ability AVG", "Composed (CMP)"],
          [["GVE-i  (public data)", "0.528", "0.558", "0.237"],
           ["GVE-s  (+ UVRD)", "0.537", "0.564", "0.301"],
           ["GVE  (+ Modality Pyramid)", "0.544", "0.571", "0.304"]],
          0.55, 1.98, 8.05, 2.15, best_row=2, hi_col=[3], fs=14, col_widths=[0.40, 0.20, 0.20, 0.20])
stat_card(s, 8.80, 1.98, 3.98, 2.15, "+27%", "on Composed",
          "Relative CMP gain from adding UVRD (0.237 → 0.301).", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
gold_card(s, 0.55, 4.35, 12.23, 1.45, "Reading the table",
          "UVRD lifts overall R@1 by +2.3% and composed retrieval by +27% relative; the Modality "
          "Pyramid curriculum adds further ordering gains on top — diagnosis → data → curriculum "
          "is additive.")
caption(s, "Each component targets a distinct part of the semantic bottleneck.", y=6.55)
notes(s, "Ablations isolate targeted data (UVRD) and curriculum ordering (Modality Pyramid).")

s = base(1, "Correlation Analysis Explains the Capability Structure",
         "Partial relevance predicts universality; spatial and temporal skills are decoupled.")
pic(s, "gve/corr_ability_and_data", 1.165, 1.98, width=11.0,
    caption="Correlation of each ability with overall UVR performance (and with training-data mix).")
info_card(s, 0.55, 5.22, 3.97, 1.45, "PR ↔ universality",
          "Partial-relevance retrieval has the highest correlation with overall UVR (ρ ≈ 0.97).")
info_card(s, 4.68, 5.22, 3.97, 1.45, "Spatial ⟂ Temporal",
          "Spatial and temporal abilities correlate only ρ ≈ 0.12 — learned separately.")
info_card(s, 8.81, 5.22, 3.97, 1.45, "Temporal → fine-grained",
          "Temporal ability drives fine-grained recall (ρ ≈ 0.98); spatial does not (ρ ≈ 0.39).")
notes(s, "The correlation figure is the quantitative backing for the three capability findings.")

s = base(1, "GVE Transfers to Zero-Shot Video Classification",
         "A retrieval embedding generalizes to classification with no task-specific tuning.")
add_table(s, ["Model", "Zero-shot classification AVG"],
          [["GVE-3B (ours)", "0.476"],
           ["Unite-7B", "0.519"],
           ["InternVideo2-6B (video specialist)", "0.526"],
           ["GVE-7B (ours)", "0.526"]],
          0.55, 1.98, 7.35, 2.55, best_row=3, hi_col=[1], fs=15, col_widths=[0.62, 0.38])
info_card(s, 8.10, 1.98, 4.68, 1.20, "Result",
          "GVE-7B matches a specialist 6B video model, zero-shot.")
result_card(s, 8.10, 3.32, 4.68, 1.21, "Why it matters",
            "Retrieval-trained geometry is genuinely general, not benchmark-specific.")
gold_card(s, 0.55, 4.72, 12.23, 1.10, "Reading",
          "Averaged over K700, UCF101, HMDB51, SSV2, and Breakfast: capability-guided retrieval "
          "training yields embeddings that transfer beyond retrieval itself.")
notes(s, "GVE's embedding transfers to classification, matching InternVideo2-6B zero-shot.")

s = base(1, "Study 1 Takeaway: Capability-Guided Semantic Scaling",
         "Scaling begins with diagnosis: build and train for the capabilities the model lacks.")
flow = ["Diagnose\n(UVRB)", "Synthesize\n(V-SynFlow → UVRD)", "Curriculum\n(Modality Pyramid)", "Generalize\n(GVE)"]
cw, cg, x0 = 2.86, 0.30, 0.62
for i, step in enumerate(flow):
    chip(s, x0 + i*(cw+cg), 2.20, cw, 1.10, step, GREEN if i == 3 else NAVY, WHITE, size=S_CARDB)
    if i < 3: arrow(s, x0 + i*(cw+cg) + cw, 2.55, size=22, color=GOLD2)
result_card(s, 0.55, 3.75, 12.23, 1.45, "Evidence",
            "GVE reaches 0.573 dataset-AVG and 0.600 ability-AVG (SOTA zero-shot across 16 datasets), "
            "with GVE-3B already beating the 7B baseline.")
take(s, "Semantic scaling needs capability diagnosis, not just more parameters or data.", y=5.55)
notes(s, "Study 1 in one line: capability diagnosis drives effective semantic scaling.")


section("02", "Study 2 · Observational Scaling", "MG-LVR &\nVEterfall",
        "What visual evidence should be observed, under limited frame and token budgets?",
        "Chapter 4 · submitted to ECCV 2026")

s = base(2, "A Video Embedding Can Only Represent What It Observes",
         "For long videos, frame sampling is part of retrieval — not a preprocessing detail.")
tl_l, tl_w, tl_y = 0.90, 11.5, 2.85
rect(s, tl_l, tl_y, tl_w, 0.72, GRAY_L, line_color=GRAY_BD, rounded=True)
txt(s, tl_l, tl_y - 0.38, 4.0, 0.34, "one 706-second video", S_CAP, False, MUTED)
for fx in [0.06, 0.20, 0.34, 0.48, 0.78, 0.92]:
    rect(s, tl_l + tl_w*fx, tl_y + 0.06, 0.05, 0.60, GOLD)
rmx = tl_l + tl_w*0.63
rect(s, rmx, tl_y - 0.18, 0.09, 1.08, RED)
txt(s, rmx - 1.35, tl_y - 0.62, 2.8, 0.4, "relevant moment", S_CAP, True, RED, PP_ALIGN.CENTER)
txt(s, tl_l, tl_y + 0.82, tl_w, 0.34, "gold = sampled frames    ·    red = the few relevant seconds",
    S_CAP, False, MUTED)
warn_card(s, 0.90, 4.30, 11.5, 1.05, None,
          "If the relevant moment is never sampled, retrieval fails before modeling even begins — "
          "and encoding every frame of an hour-long video is infeasible.")
gold_card(s, 0.90, 5.50, 11.5, 1.10, "Open question",
          "How does sampling density interact with query granularity? Standard benchmarks never "
          "isolate this, so it has stayed unmeasured — the gap MG-LVR fills.")
notes(s, "The hook: observation bounds representation; sampling decides what evidence exists.")

s = base(2, "Granularity Defines How Much Evidence a Query Needs",
         "G is the fraction of a video that is relevant — from one moment to the whole clip.")
mathbox(s, 0.55, 1.98, 6.05, 1.20,
        "G  =  | S(v*, q) |  /  d_video     ∈  (0, 1]",
        label="Temporal granularity", expr_size=22)
mathbox(s, 0.55, 3.34, 6.05, 1.20,
        "C  =  Σ (eᵢ − sᵢ)  /  (e_k − s₁)     ∈  (0, 1]",
        label="Temporal continuity", expr_size=22)
info_card(s, 0.55, 4.70, 6.05, 1.55, "Reading the definitions",
          "G measures how localized the evidence is; C measures whether it is one contiguous event "
          "or scattered across the video.")
grn = [("Fine (FN)", "a brief moment · G ∈ [0.001, 0.01]", RED, 0.12),
       ("Medium (MD)", "several segments · G ∈ [0.1, 0.3]", GOLD2, 0.45),
       ("Coarse (CR)", "broad, video-level coverage", GREEN, 0.92)]
y = 2.05
for name, desc, col, frac in grn:
    txt(s, 6.85, y + 0.02, 2.5, 0.36, name, S_BODY, True, col)
    txt(s, 6.85, y + 0.42, 2.60, 0.56, desc, S_CARDB, False, MUTED)
    rect(s, 9.55, y + 0.06, 3.23, 0.52, GRAY_L, line_color=GRAY_BD, rounded=True)
    rect(s, 9.55, y + 0.06, max(0.22, 3.23*frac), 0.52, col, rounded=True)
    y += 1.05
gold_card(s, 6.85, 5.30, 5.93, 1.20, "Why it matters",
          "Granularity sets the frame/token budget a query truly needs — coarse and fine queries "
          "want opposite allocations.")
notes(s, "Granularity G and continuity C make the observation problem measurable.")

s = base(2, "MG-LVR: A Multi-Granularity Long-Video Benchmark",
         "A long-video benchmark that varies query granularity under controlled sampling.")
stat_card(s, 0.55, 1.98, 3.02, 2.35, "9,971", "Queries",
          "Fine 4,706 · Medium 4,142 · Coarse 1,123.")
stat_card(s, 3.71, 1.98, 3.02, 2.35, "4,844", "Long videos",
          "Average duration ≈ 706 s — genuinely long-form.")
stat_card(s, 6.87, 1.98, 3.02, 2.35, "23", "Models",
          "6 CLIP-based + 17 MLLM-based, one protocol.")
stat_card(s, 10.03, 1.98, 2.75, 2.35, "96%", "Audited",
          "Human-validated on 50 pairs.", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
add_table(s, ["Benchmark", "#Query", "#Corpus", "Avg dur", "Granularity"],
          [["MSR-VTT", "1,000", "1,000", "15 s", "Coarse"],
           ["ActivityNet Cap.", "18,000", "4,917", "118 s", "FN, MD"],
           ["LoVR", "100", "467", "1,560 s", "Coarse"],
           ["MG-LVR (ours)", "9,971", "4,844", "706 s", "All + both C"]],
          0.55, 4.50, 12.23, 2.0, best_row=3, hi_col=[1, 4], fs=14,
          col_widths=[0.28, 0.16, 0.16, 0.18, 0.22])
notes(s, "MG-LVR is the measurement instrument: only benchmark with all granularities on long videos.")

s = base(2, "Fine-Grained Retrieval Exposes the Observation Bottleneck",
         "Under sparse sampling, coarse queries are easy and fine queries collapse.")
rect(s, 0.55, 1.98, 5.95, 2.55, GREEN_L, line_color=GREEN_BD, line_pt=1.0, rounded=True)
txt(s, 0.55, 2.22, 5.95, 1.05, "0.856", 60, True, GREEN, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.55, 3.42, 5.95, 0.44, "Coarse R@1  ·  8 frames", S_BODY, True, DARK, PP_ALIGN.CENTER)
txt(s, 0.55, 3.92, 5.95, 0.44, "broad themes are easy to match", S_CARDB, False, MUTED, PP_ALIGN.CENTER)
rect(s, 6.83, 1.98, 5.95, 2.55, RED_L, line_color=RED_BD, line_pt=1.0, rounded=True)
txt(s, 6.83, 2.22, 5.95, 1.05, "0.210", 60, True, RED, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 6.83, 3.42, 5.95, 0.44, "Fine R@1  ·  8 frames", S_BODY, True, DARK, PP_ALIGN.CENTER)
txt(s, 6.83, 3.92, 5.95, 0.44, "a > 75% drop — evidence is missed", S_CARDB, False, MUTED, PP_ALIGN.CENTER)
add_table(s, ["Best model (Qwen3-VL-Emb-8B)", "Coarse R@1", "Fine R@1"],
          [["8 frames", "0.856", "0.210"],
           ["128 frames  (16× more)", "0.903", "0.287"]],
          0.55, 4.68, 8.6, 1.25, hi_col=[2], fs=14, col_widths=[0.52, 0.24, 0.24])
warn_card(s, 9.30, 4.68, 3.48, 1.25, None,
          "16× more frames lifts fine R@1 by < 8 points — naive frame scaling cannot close the gap.")
take(s, "Fine-grained retrieval fails under sparse sampling and barely recovers with more frames.", y=6.10)
notes(s, "The granularity gap is the core empirical finding of Study 2.")

s = base(2, "Temporal Scaling Is Architecture-Dependent",
         "MLLMs keep improving with frames; CLIP-style models saturate, then degrade.")
pic(s, "mglvr/mglvr_testtime_temporal_scaling", 0.55, 1.98, width=12.23,
    caption="Test-time R@1 vs. frame count, by architecture family.")
info_card(s, 0.55, 4.70, 6.05, 1.55, "MLLM-based",
          "Improve up to ~128 frames — useful for fine-grained queries that need dense temporal "
          "evidence.")
warn_card(s, 6.73, 4.70, 6.05, 1.55, "CLIP-based",
          "Saturate near 16 frames, then degrade: mean-pooling dilutes the signal as frames grow.")
caption(s, "More frames help only architectures that can actually use them.", y=6.55)
notes(s, "There is no single 'more frames is better' law — it depends on the architecture.")

s = base(2, "Fixed Token Budgets Require Granularity-Aware Allocation",
         "Under a fixed budget N = F × T, coarse and fine queries prefer opposite splits.")
pic(s, "mglvr/st_tradeoff", 0.55, 1.98, width=12.23,
    caption="Spatial–temporal trade-off at fixed token budget across query granularities.")
result_card(s, 0.55, 4.70, 6.05, 1.55, "Coarse queries",
            "Prefer high spatial resolution with fewer frames — scene-level cues dominate.")
info_card(s, 6.73, 4.70, 6.05, 1.55, "Fine-grained queries",
          "Prefer more frames over spatial detail — temporal coverage locates the moment.")
caption(s, "Spatial and temporal tokens are not interchangeable; allocation must follow granularity.", y=6.55)
notes(s, "At fixed budget, allocation should be granularity-aware.")

s = base(2, "Training Choices Constrain What Inference Can Recover",
         "Two training-time laws: resolution transfers, but frame count is anchored.")
info_card(s, 0.55, 1.98, 6.05, 2.65, "Resolution robustness",
          "Training at high spatial resolution transfers to low-resolution inference — models "
          "trained at 400 tokens still lead when tested at 50 tokens.")
warn_card(s, 6.73, 1.98, 6.05, 2.65, "Frame-count anchoring",
          "Temporal ability peaks when the inference frame count matches training; a train-32 / "
          "test-4 mismatch loses fine-grained recall, and vice-versa.")
gold_card(s, 0.55, 4.80, 12.23, 1.45, "Consequence for deployment",
          "Efficient serving demands sparse inference, yet anchoring ties fine-grained skill to "
          "dense training — motivating an explicit dense-to-sparse transfer method (VEterfall).")
caption(s, "Sparse inference must inherit dense-trained temporal skill — not relearn it.", y=6.55)
notes(s, "Training-time laws set rigid inference constraints, motivating VEterfall.")

s = base(2, "VEterfall: Dense-to-Sparse Self-Distillation",
         "A cascade transfers temporal knowledge down the sampling-density axis.")
pic(s, "mglvr/d2s", 0.55, 2.02, width=6.7,
    caption="Dense-to-sparse cascade: temporal knowledge distilled to progressively fewer frames and tokens.")
mathbox(s, 7.45, 2.10, 5.33, 1.35, "ℒ  =  MSE( zₛ , zₜ )  +  λ · InfoNCE",
        label="Per-step distillation objective", expr_size=18)
gold_card(s, 7.45, 3.66, 5.33, 1.88, "Learn dense, deploy sparse",
          "Skill for low-density inference is latent in dense models but does not transfer "
          "automatically — VEterfall distills it explicitly, one step at a time "
          "(λ = 0.5, K = 2, 16× fewer tokens).")
caption(s, "The architecture is unchanged; only observation density decreases.", y=6.55)
notes(s, "VEterfall is cascaded self-distillation: MSE to the denser teacher plus an InfoNCE anchor.")

s = base(2, "VEterfall Recovers Fine-Grained Sparse Performance",
         "Large fine-grained gains at the tightest budget, over the sparse baseline.")
add_table(s, ["Model  ·  4F–100T", "Overall", "Fine", "Medium", "Coarse"],
          [["V⁰  (sparse baseline)", "0.300", "0.132", "0.391", "0.664"],
           ["V¹", "0.300", "0.130", "0.394", "0.664"],
           ["V²  (VEterfall)", "0.325", "0.158", "0.423", "0.667"]],
          0.55, 1.98, 8.05, 2.15, best_row=2, hi_col=[2], fs=14,
          col_widths=[0.36, 0.16, 0.16, 0.16, 0.16])
stat_card(s, 8.80, 1.98, 3.98, 2.15, "+20%", "Fine R@1 (relative)",
          "0.132 → 0.158 at 4F–100T, over the sparse baseline.", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
gold_card(s, 0.55, 4.35, 12.23, 1.45, "Reading the result",
          "The +20% relative fine-grained gain is measured over the sparse baseline (V⁰) at the "
          "same 4F–100T budget: VEterfall improves sparse inference by transferring dense knowledge "
          "at 4–16× efficiency — not by outperforming the dense teacher directly.")
take(s, "Dense-trained temporal skill is recovered under a 16× smaller token budget.", y=5.92)
notes(s, "VEterfall lifts fine-grained R@1 ~20% over the sparse baseline at 4–16× efficiency.")

s = base(2, "Spatial Resolution Helps Most When Frames Are Scarce",
         "Spatial and temporal budgets are complementary, not interchangeable.")
pic(s, "mglvr/mglvr_testtime_spatial_scaling_1", 2.665, 1.88, width=8.0,
    caption="Test-time R@1 vs. spatial tokens per frame, by frame count.")
info_card(s, 0.55, 4.95, 6.05, 1.35, "Low frame counts (F ≤ 8)",
          "Spatial resolution is critical — more tokens per frame recover detail sparse frames miss.")
warn_card(s, 6.73, 4.95, 6.05, 1.35, "High frame counts (F > 32)",
          "Extra spatial tokens add little; coarse queries can even suffer token redundancy.")
caption(s, "Spend spatial detail when frames are scarce; spend frames when the query is fine-grained.", y=6.55)
notes(s, "Spatial scaling matters most at low frame counts — complementary to temporal scaling.")

s = base(2, "Study 2 Takeaway: Observation-Aware Retrieval Scaling",
         "MG-LVR reveals the bottleneck; scaling laws explain it; VEterfall intervenes.")
flow = ["Measure\n(MG-LVR)", "Explain\n(scaling laws)", "Intervene\n(VEterfall)"]
cw, cg, x0 = 3.85, 0.35, 0.62
for i, step in enumerate(flow):
    chip(s, x0 + i*(cw+cg), 2.20, cw, 1.10, step, GREEN if i == 2 else NAVY, WHITE, size=S_BODY)
    if i < 2: arrow(s, x0 + i*(cw+cg) + cw, 2.55, size=22, color=GOLD2)
result_card(s, 0.55, 3.75, 12.23, 1.45, "Evidence",
            "Fine-grained retrieval drops > 75% under sparse sampling; VEterfall recovers +20% at "
            "4–16× efficiency by transferring dense knowledge to sparse inference.")
take(s, "Observational scaling needs granularity-aware evidence acquisition, not just more frames.", y=5.55)
notes(s, "Study 2 in one line: observe granularity-aware, then distill dense skill into sparse inference.")


section("03", "Study 3 · Search Scaling", "GMP-GR",
        "How can a learned retrieval signal be searched at deployment scale?",
        "Chapter 5 · published at ACM Web Conference 2026")

s = base(3, "Web-Scale Retrieval: Reduce Billions to a Searchable Candidate Set",
         "Deployment must return the top candidates under strict latency, from a huge corpus.")
pipe = [("Billion-scale\ncorpus", GRAY_L, MUTED), ("Learned metric\nδ(u, v)", NAVY, WHITE),
        ("Graph traversal\n(ANNS)", NAVY, WHITE), ("GPU serving\n< 10 ms", NAVY, WHITE),
        ("Candidate set\n~10³", GREEN, WHITE)]
sw, gap, x0, y0 = 2.16, 0.30, 0.62, 2.05
for i, (lab, bg, fg) in enumerate(pipe):
    lx = x0 + i*(sw+gap)
    chip(s, lx, y0, sw, 1.05, lab, bg, fg, size=S_CARDB, bd=GRAY_BD if i == 0 else None)
    if i < 4: arrow(s, lx + sw, y0 + 0.32, size=24)
mathbox(s, 0.62, 3.45, 6.05, 1.15,
        "Vᵤ*  =  arg max   Σ  δ(u, v)\nover candidate sets  Vᵤ ⊆ V ,   v ∈ Vᵤ",
        label="Search objective", expr_size=17)
warn_card(s, 6.85, 3.45, 5.93, 1.45, "The catch",
          "A more accurate neural metric δ is worthless if it cannot be searched: expressive "
          "metrics can violate the regularity graph traversal relies on.")
gold_card(s, 0.62, 5.06, 12.16, 1.10, "Reframing",
          "Study 3 is search scaling for a learned signal — making accuracy compatible with graph "
          "and GPU execution. (Here queries are users and items; the searchable-signal principle "
          "is the same as for video.)")
notes(s, "Search scaling: the learned signal must be accurate AND searchable under latency.")

s = base(3, "Search Scaling Couples Metric, Graph, and GPU Bottlenecks",
         "Isolated optimization of any one component cannot deliver end-to-end efficiency.")
b3 = [("Metric", "A neural metric captures multi-relational user behavior but can break search regularity."),
      ("Graph", "Metrics that violate the triangle inequality trap greedy HNSW traversal in local optima."),
      ("GPU", "Irregular neural ops trigger many kernel launches; high concurrency underutilizes the GPU.")]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (name, desc) in enumerate(b3):
    warn_card(s, x0 + i*(cw+cg), 1.98, cw, 2.7, name + " bottleneck", desc)
gold_card(s, 0.55, 4.90, 12.23, 1.25, "Why co-design",
          "The three bottlenecks are intertwined: a searchable metric, a broader graph search, and "
          "GPU-aware execution must be designed together — GMP-GR does exactly this.")
notes(s, "Three coupled bottlenecks — metric, graph, GPU — demand joint co-design.")

s = base(3, "Expressive Neural Metrics Can Break Graph Traversal",
         "Greedy graph search relies on distance regularity that neural metrics may violate.")
result_card(s, 0.55, 1.98, 6.05, 2.55, "Regular (Euclidean) metric",
            "The triangle inequality holds, so every greedy hop provably moves closer to the "
            "target — graph traversal reaches the true nearest neighbors.")
warn_card(s, 6.73, 1.98, 6.05, 2.55, "Expressive neural metric",
          "Ranking can be inconsistent with distance, so greedy traversal stalls in local optima "
          "and misses relevant items — accuracy gains are lost at search time.")
mathbox(s, 0.55, 4.72, 6.05, 1.10,
        "d(a, c)  ≤  d(a, b)  +  d(b, c)", label="Triangle inequality", expr_size=22)
gold_card(s, 6.73, 4.72, 6.05, 1.20, "The fix (SCL)",
          "Transplant Euclidean ranking regularity into the learned metric — accuracy and "
          "searchability hold together.")
take(s, "Better offline relevance is useless unless the signal stays searchable.", y=6.06)
notes(s, "The core insight: expressive metrics can violate regularity and trap graph traversal.")

s = base(3, "GMP-GR Co-Designs Metric, Graph, and GPU Execution",
         "One framework aligns learned relevance with graph search and GPU serving.")
pic(s, "gmpgr/GMP-GR", 1.00, 1.92, width=10.0)
blocks = [("① Metric — MUIRML + SCL", "Accurate and searchable: SCL enforces rank–distance consistency."),
          ("② Graph — C-HiPANNS", "Multi-seed parallel traversal widens the search space, escaping traps."),
          ("③ GPU — Q-HiPANNS + system", "Query batching, compilation, and quantization cut latency.")]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (h, b) in enumerate(blocks):
    flatcol(s, x0 + i*(cw+cg), 5.95, cw, h, b, bh=0.72)
for vx in (4.62, 8.77):
    rect(s, vx, 5.99, 0.012, 0.90, HAIR)
notes(s, "GMP-GR co-design: searchable metric, parallel graph traversal, GPU-aware execution.")

s = base(3, "MUIRML and the Self-Covariant Loss Make Relevance Searchable",
         "A multi-relational metric, regularized to preserve graph-search regularity.")
info_card(s, 0.55, 1.98, 6.05, 2.45, "MUIRML metric",
          "A lightweight DNN predicts a multi-interaction relevance δ(u, v) from concatenated "
          "user/item features (with a serendipity term), capturing behaviors a single dot-product "
          "cannot.")
mathbox(s, 6.73, 1.98, 6.05, 2.45,
        "ρ(u,v) = Σ (δ − δ̄)(δ′ − δ̄′)\n————————————————\nVAR(δ) · VAR(δ′)",
        label="Self-Covariant Loss (SCL)", expr_size=17)
mathbox(s, 0.55, 4.62, 12.23, 1.15,
        "ℒ  =  Σ ‖ Z − Ẑ ‖₂   +   Σ  1 / ( ρ + 1 )         "
        "( δ = learned relevance,  δ′ = Euclidean distance )",
        label="Multi-objective training", expr_size=18)
take(s, "SCL transplants Euclidean ranking regularity into the learned metric, retaining an approximate triangle inequality property.", y=6.00)
notes(s, "MUIRML learns multi-relational relevance; SCL regularizes it toward graph-searchable geometry.")

s = base(3, "HiPANNS: Parallel Graph Traversal on the GPU",
         "Two levels of parallelism raise recall and throughput together.")
info_card(s, 0.55, 1.98, 6.05, 2.75, "C-HiPANNS — inter-candidate",
          ["k parallel searches per query with different seeds",
           "Share one K-size max-heap across processes",
           "k-fold search-space expansion escapes local optima → higher recall"])
info_card(s, 6.73, 1.98, 6.05, 2.75, "Q-HiPANNS — inter-query",
          ["Aggregate irregular neural computations into GPU batches",
           "Adaptive batch splitting under a max batch size",
           "Amortizes kernel-launch overhead → higher throughput"])
gold_card(s, 0.55, 4.92, 12.23, 1.20, "Together",
          "C-HiPANNS broadens the search for accuracy while Q-HiPANNS batches computation for "
          "speed — the graph and GPU layers reinforce, rather than trade off against, each other.")
notes(s, "HiPANNS parallelizes across candidates (recall) and across queries (throughput).")

s = base(3, "GMP-GR Improves Coverage, Recall, and Speed Together",
         "Search-compatible learning lifts accuracy and throughput at the same time.")
add_table(s, ["Method (Video)", "Coverage", "Rec@10", "Rec@100"],
          [["D-NSW", "0.408", "0.553", "0.609"],
           ["SL2G", "0.441", "0.578", "0.612"],
           ["NANN (best baseline)", "0.537", "0.672", "0.664"],
           ["GMP-GR (ours)", "0.649", "0.824", "0.805"]],
          0.55, 1.98, 7.35, 2.6, best_row=3, hi_col=[1, 2], fs=14,
          col_widths=[0.40, 0.20, 0.20, 0.20])
pic(s, "gmpgr/efficiency_Video", 8.15, 1.98, width=4.6,
    caption="Recall vs. latency — GMP-GR sits on the efficient frontier.")
for lx, big, lab in [(0.55, "+20.9%", "Coverage  ·  vs NANN (Video)"),
                     (4.62, "+22.7%", "Recall@10  ·  vs NANN (Video)")]:
    rect(s, lx, 4.72, 3.90, 1.35, GREEN_L, line_color=GREEN_BD, line_pt=1.0, rounded=True)
    txt(s, lx + 0.24, 4.86, 3.5, 0.66, big, S_KICK, True, GREEN)
    txt(s, lx + 0.24, 5.56, 3.5, 0.40, lab, S_CARDL, True, DARK)
take(s, "Video dataset shown; full four-dataset results in backup. Metric and graph co-design jointly improve coverage, recall, and speed.", y=6.28)
notes(s, "Offline: GMP-GR jointly improves coverage, recall, and speed across four datasets.")

s = base(3, "Online A/B Tests Validate Production Impact",
         "Two live services show consistent, significant engagement gains.")
add_table(s, ["Online A/B service", "Time-on-page", "DAU"],
          [["Main feed", "+1.13%", "+0.23%"],
           ["Short video", "+1.19%", "+0.50%"]],
          0.55, 1.98, 7.35, 1.6, hi_col=[1, 2], fs=16, hfs=15, col_widths=[0.50, 0.25, 0.25])
info_card(s, 8.15, 1.98, 4.63, 1.60, "Component attribution",
          "MUIRML and HiPANNS add +0.57% and +0.23% time-on-page respectively.")
gold_card(s, 0.55, 3.78, 12.23, 1.10, "Deployment scope",
          "Validated by two online A/B services (main feed and short video), then subsequently "
          "extended across 20+ Baidu applications — the broader rollout is deployment, not a "
          "single A/B result.")
result_card(s, 0.55, 5.00, 12.23, 1.10, "Interpretation",
            "Retrieval gains matter only when relevance improves without latency regression — which "
            "these online tests confirm.")
caption(s, "A searchable learned signal delivers measurable, latency-safe engagement gains in production.", y=6.55)
notes(s, "Two-service A/B: +1.13%/+1.19% time-on-page; later deployed across 20+ apps. No p-values in source.")

s = base(3, "System-Level Execution Makes the Signal Deployable",
         "Engineering co-design turns a searchable metric into a production service.")
stat_card(s, 0.55, 1.98, 3.95, 2.35, "+74%", "Throughput",
          "from compilation optimization of the serving graph.", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
stat_card(s, 4.69, 1.98, 3.95, 2.35, "+26%", "Throughput",
          "from 32→16-bit model quantization.", accent=GREEN, bg=GREEN_L, bd=GREEN_BD)
stat_card(s, 8.83, 1.98, 3.95, 2.35, "20+", "Baidu apps",
          "News, Tieba, Shorts and more, on 165 + 119 A30 GPUs.")
info_card(s, 0.55, 4.55, 12.23, 1.6, "Freshness & serving",
          "Streaming index updates keep embeddings current under dynamic catalogs; two services on "
          "five servers each sustain production-scale traffic within the P99 latency budget.")
notes(s, "System optimizations (compilation, quantization, streaming) make GMP-GR production-ready.")

s = base(3, "Ablation: Metric and Graph Are Both Necessary",
         "Removing MUIRML or HiPANNS degrades accuracy or throughput.")
pic(s, "gmpgr/ablation_Cov", 1.15, 1.98, width=4.5, caption="Coverage under component removal.")
pic(s, "gmpgr/ablation_Rec10", 7.68, 1.98, width=4.5, caption="Recall@10 under component removal.")
caption(s, "Each component is irreplaceable — the metric, graph, and GPU layers reinforce one another.", y=6.55)
notes(s, "Ablation figures: removing MUIRML or HiPANNS drops accuracy and throughput.")

s = base(3, "Study 3 Takeaway: Search-Compatible Retrieval Scaling",
         "Accuracy, searchability, and throughput must be optimized as one system.")
flow = ["Searchable metric\n(MUIRML + SCL)", "Parallel graph\n(C-HiPANNS)", "GPU execution\n(Q-HiPANNS)"]
cw, cg, x0 = 3.85, 0.35, 0.62
for i, step in enumerate(flow):
    chip(s, x0 + i*(cw+cg), 2.20, cw, 1.10, step, GREEN if i == 2 else NAVY, WHITE, size=S_CARDB)
    if i < 2: arrow(s, x0 + i*(cw+cg) + cw, 2.55, size=22, color=GOLD2)
result_card(s, 0.55, 3.75, 12.23, 1.45, "Evidence",
            "GMP-GR raises coverage +20.9% and Recall@10 +22.7% while improving throughput, and lifts "
            "engagement +1.13%/+1.19% time-on-page in two online A/B services.")
take(s, "Search scaling needs metric–graph–GPU compatibility, not just better offline metrics.", y=5.55)
notes(s, "Study 3 in one line: make the learned signal searchable, then execute it efficiently.")


s = base(4, "Structure-Aware Scaling Explains All Three Studies",
         "The same principle — align scaling with the bottleneck — recurs at every stage.")
add_table(s, ["Stage", "Naive scaling", "Structural bottleneck", "Structure-aware solution"],
          [["Semantic", "More params / generic data", "Capability gaps across tasks",
            "Diagnose → synthesize → curriculum"],
           ["Observation", "More frames / tokens", "Granularity vs. evidence coverage",
            "Granularity-aware allocation + distillation"],
           ["Search", "Higher offline AUC", "Metric–graph–GPU mismatch",
            "Search-compatible metric + GPU co-design"]],
          0.55, 2.02, 12.23, 3.05, hi_col=[3], fs=15,
          col_widths=[0.14, 0.24, 0.28, 0.34])
take(s, "Scaling capacity alone is insufficient unless aligned with the structure of the bottleneck.",
     y=5.55)
notes(s, "One table, one thesis: structure-aware scaling unifies the three studies.")

s = base(4, "Generalizability Confirms the Right Bottleneck",
         "The opening framework, now filled with evidence from each study.")
cols = [("Semantic", "GVE", "SOTA zero-shot across 16 datasets\n(0.573 dataset · 0.600 ability AVG)"),
        ("Observational", "VEterfall", "+20% fine-grained recall over the\nsparse baseline at 4–16× efficiency"),
        ("Search", "GMP-GR", "+20.9% coverage, +22.7% recall;\n+1.1–1.2% online time-on-page")]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (name, model, ev) in enumerate(cols):
    lx = x0 + i*(cw+cg)
    chip(s, lx, 2.02, cw, 0.64, name + " Scaling", NAVY, WHITE, size=S_BODY)
    chip(s, lx, 2.78, cw, 0.58, model, GOLD, NAVY, size=S_BODY)
    result_card(s, lx, 3.52, cw, 1.95, "Evidence", ev)
    if i < 2: arrow(s, lx + cw, 2.18, size=22, color=NAVY)
take(s, "Generalizability is the evidence that scaling has addressed the right bottleneck.", y=5.78)
notes(s, "The framework returns, now backed by concrete generalization evidence per study.")

s = base(4, "Research Outputs and Reusable Artifacts",
         "Each study leaves behind a benchmark, a method, and a deployable system.")
info_card(s, 0.55, 2.02, 3.97, 4.35, "Benchmarks & data",
          ["UVRB — 16-dataset capability diagnosis",
           "UVRD — 1.55M targeted pairs",
           "MG-LVR — long-video, multi-granularity"])
info_card(s, 4.68, 2.02, 3.97, 4.35, "Models & methods",
          ["GVE — unified video embedding",
           "V-SynFlow — capability-guided synthesis",
           "VEterfall — dense-to-sparse distillation"])
info_card(s, 8.81, 2.02, 3.97, 4.35, "Systems",
          ["GMP-GR — search-scaling framework",
           "MUIRML + SCL — searchable metric",
           "HiPANNS — parallel graph traversal"])
notes(s, "The thesis produces reusable artifacts across all three stages.")

s = base(4, "Boundaries of Evidence",
         "Where the current evidence stops — and where structure-aware scaling extends next.")
gray_card(s, 0.55, 2.02, 3.97, 3.35, "Stage-wise validation",
          "The three studies cover successive pipeline stages but are not yet jointly optimized "
          "end-to-end — an integration this thesis motivates rather than claims.")
gray_card(s, 4.68, 2.02, 3.97, 3.35, "Synthetic supervision",
          "UVRD and MG-LVR rely on synthesized and caption-based signals; larger audits and finer "
          "temporal grounding are natural extensions.")
gray_card(s, 8.81, 2.02, 3.97, 3.35, "Deployment context",
          "GMP-GR is validated in Baidu infrastructure; the algorithmic principles are general, but "
          "absolute throughput depends on hardware and traffic.")
gold_card(s, 0.55, 5.55, 12.23, 0.92, None,
          "These boundaries define where structure-aware scaling should be extended next — the frontier, not weaknesses.")
notes(s, "Framed as boundaries of evidence: honest, controlled, forward-looking.")

s = base(4, "Future Work I: Retrieval-Native Multimodal Models",
         "Retrieval should be built into the model, not extracted from generation states.")
chip(s, 4.9, 2.10, 3.53, 0.75, "Shared vision–language backbone", NAVY, WHITE, size=S_CARDB)
arrow(s, 3.7, 3.05, text="↙", size=22, color=GOLD2); arrow(s, 9.0, 3.05, text="↘", size=22, color=GOLD2)
chip(s, 1.4, 3.35, 4.2, 0.9, "Generative objective\n(today's MLLM)", GRAY_L, MUTED, size=S_CARDB, bd=GRAY_BD)
chip(s, 7.7, 3.35, 4.2, 0.9, "Retrieval objective\n+ retrieval token / routing", GREEN, WHITE, size=S_CARDB)
info_card(s, 0.55, 4.65, 12.23, 1.7, "Direction",
          "MLLM hidden states are optimized for generation, not retrieval geometry. Native "
          "architectures with retrieval-specific objectives, tokens, and routing could align "
          "generative and retrieval representations from the start — extending semantic scaling "
          "into the model design itself.")
notes(s, "Future I: models purpose-built for retrieval, not repurposed generators.")

s = base(4, "Future Work II: Video Retrieval as Agent Memory",
         "Retrieval becomes the interface to an agent's long-horizon visual experience.")
flow = ["Streaming\nobservations", "Indexed\nvisual memory", "Query", "Recalled\nepisode", "Action"]
sw, gap, x0, y0 = 2.16, 0.30, 0.62, 2.30
for i, lab in enumerate(flow):
    col = GREEN if i == 1 else NAVY
    chip(s, x0 + i*(sw+gap), y0, sw, 1.05, lab, col, WHITE, size=S_CARDB)
    if i < 4: arrow(s, x0 + i*(sw+gap) + sw, y0 + 0.32, size=24)
info_card(s, 0.55, 4.05, 12.23, 2.0, "Direction",
          "Agents need memory that spans long visual histories. Casting retrieval as the memory "
          "interface — over past observations, object locations, and event context — turns the "
          "embedding and search machinery of this thesis into the substrate for embodied and "
          "multimodal agents.")
notes(s, "Future II: retrieval as the memory layer for agents.")

s = base(4, "Future Work III: Self-Evolving Retrieval Systems",
         "The thesis pipeline can become a self-improving loop.")
loop = ["Evaluate", "Diagnose", "Synthesize", "Train", "Deploy"]
sw, gap, x0, y0 = 2.16, 0.30, 0.62, 2.35
for i, lab in enumerate(loop):
    chip(s, x0 + i*(sw+gap), y0, sw, 1.0, lab, NAVY, WHITE, size=S_BODY)
    if i < 4: arrow(s, x0 + i*(sw+gap) + sw, y0 + 0.30, size=24)
txt(s, 3.2, 3.66, 6.9, 0.4, "↺   re-evaluate on new evidence", 16, True, GOLD2, PP_ALIGN.CENTER)
info_card(s, 0.55, 4.35, 12.23, 1.85, "Direction",
          "UVRB-style evaluation, V-SynFlow-style synthesis, curriculum scheduling, and model "
          "updating can form a closed loop: the system diagnoses its own weaknesses, generates "
          "targeted data, and retrains — reducing reliance on static benchmarks.")
notes(s, "Future III: evaluation → synthesis → curriculum → training as an autonomous loop.")

s = prs.slides.add_slide(BLANK); _bg(s)
txt(s, 11.75, 0.22, 1.03, 0.30, str(_pg()), S_FOOT, False, MUTED, PP_ALIGN.RIGHT,
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.55, 0.66, 12.23, 0.62, "Structure-Aware Scaling Connects the Three Studies",
    S_TITLE, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
hline(s, 0.57, 1.36, 2.10, GOLD, 3.0)
txt(s, 0.55, 1.42, 12.23, 0.36,
    "Modern video retrieval is a pipeline-level scaling problem — solved stage by stage.",
    S_CLAIM, False, MUTED, italic=True)
footer(s)
three = [("Semantic scaling", "needs capability diagnosis."),
         ("Observational scaling", "needs granularity-aware evidence acquisition."),
         ("Search scaling", "needs metric–graph–GPU compatibility.")]
y = 2.20
for a, b in three:
    rect(s, 0.55, y, 0.11, 0.66, GOLD)
    rich(s, 0.85, y, 11.9, 0.66, [(a + "  ", True, NAVY), (b, False, DARK)],
         size=24, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.86
take(s, "Scaling becomes effective only when aligned with the structure of the bottleneck it addresses.",
     y=5.20)
txt(s, 0.55, 6.02, 12.23, 0.7,
    "Scalable and generalizable video retrieval requires structure-aware scaling across semantic "
    "capability, visual observation, and search execution.", S_CARDB, False, MUTED, italic=True)
notes(s, "The three sentences to remember, and the unifying thesis statement.")

s = base(4, "Publications and Research Outputs",
         "The three studies correspond to three papers and reusable public artifacts.")
pubs = [("Study 1 · GVE", "Universal Video Retrieval via\nGeneral Video Embedding", "Submitted · ACM MM 2026"),
        ("Study 2 · MG-LVR & VEterfall", "Multi-Granularity Long-Video\nRetrieval & Scaling Laws", "Submitted · ECCV 2026"),
        ("Study 3 · GMP-GR", "Searchable Learned Metrics for\nWeb-Scale Retrieval", "Published · ACM WebConf 2026")]
cw, cg, x0 = 3.97, 0.22, 0.55
for i, (name, ttl, venue) in enumerate(pubs):
    rect(s, x0 + i*(cw+cg), 2.05, cw, 3.15, WHITE, line_color=NAVY_BD, line_pt=1.0, rounded=True)
    rect(s, x0 + i*(cw+cg), 2.05, cw, 0.66, NAVY, rounded=True)
    txt(s, x0 + i*(cw+cg), 2.05, cw, 0.66, name, S_CARDL, True, WHITE, PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x0 + i*(cw+cg) + 0.22, 2.90, cw - 0.44, 1.4, ttl, S_CARDB, False, DARK)
    chip(s, x0 + i*(cw+cg) + 0.22, 4.45, cw - 0.44, 0.55, venue, GOLD_L, AMBER, size=S_CARDB, bd=GOLD_BD)
gold_card(s, 0.55, 5.55, 12.23, 0.95, "Reusable artifacts",
          "UVRB, UVRD, and MG-LVR benchmarks/data; GVE, VEterfall, and GMP-GR methods — released to "
          "support reproducible video-retrieval research.")
notes(s, "Three papers, one per study, plus public benchmarks, data, and methods.")

s = prs.slides.add_slide(BLANK); _bg(s)
rect(s, 0.55, 0.55, 0.62, 0.62, NAVY)
rect(s, 12.16, 6.33, 0.62, 0.62, GOLD)
txt(s, 0.70, 2.05, 11.93, 1.2, "Questions?", S_QA, True, NAVY, PP_ALIGN.CENTER)
txt(s, 0.70, 3.45, 11.93, 0.6, "Thank you for your time and attention.", 24, True, MUTED, PP_ALIGN.CENTER)
hline(s, 3.9, 4.40, 5.53, GOLD, 2.0)
rich(s, 0.70, 4.62, 11.93, 0.6,
     [("Capability diagnosis   ·   ", True, NAVY), ("granularity-aware evidence   ·   ", True, NAVY),
      ("searchable signals", True, NAVY)], size=17, align=PP_ALIGN.CENTER)
txt(s, 0.70, 5.55, 11.93, 0.4, "Zhuoning Guo   ·   HKUST(GZ)   ·   July 29, 2026",
    13, False, MUTED, PP_ALIGN.CENTER)
notes(s, "Standby Q&A page — three memorable phrases anchor the thesis.")


BP = {"n": 0}
def _bp(): BP["n"] += 1; return "B" + str(BP["n"])

def bslide(title, claim=None):
    s = prs.slides.add_slide(BLANK); _bg(s)
    txt(s, 0.55, 0.30, 10.0, 0.34, "APPENDIX · BACKUP", S_FOOT, True, GOLD2)
    txt(s, 11.75, 0.30, 1.03, 0.30, _bp(), S_FOOT, False, MUTED, PP_ALIGN.RIGHT)
    txt(s, 0.55, 0.66, 12.23, 0.62, title, S_TITLE, True, NAVY, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, 0.57, 1.36, 2.10, GOLD, 3.0)
    if claim: txt(s, 0.55, 1.42, 12.23, 0.36, claim, S_CLAIM, False, MUTED, italic=True)
    footer(s)
    return s

sB = prs.slides.add_slide(BLANK); _bg(sB)
rect(sB, 0, 0, 4.6, 7.50, NAVY2); rect(sB, 4.6, 0, 0.10, 7.50, GOLD)
txt(sB, 0.45, 2.55, 3.95, 1.5, "A", S_SECNUM, True, GOLD, anchor=MSO_ANCHOR.MIDDLE)
txt(sB, 0.58, 4.26, 3.7, 0.36, "APPENDIX", S_FOOT + 1, True, CREAM)
txt(sB, 0.58, 4.70, 3.7, 1.2, "Backup &\nQ&A", S_SECTL, True, WHITE)
txt(sB, 5.35, 2.9, 7.4, 2.6,
    "Full tables, protocol details, related work, and prepared answers.\n\n"
    "Several slides here are optional material that can be promoted into the main deck.",
    22, False, DARK)
notes(sB, "Backup: full evidence and prepared committee answers.")

s = bslide("GVE — Full Ability-Level Results (excerpt)",
           "By-ability averages; GVE-7B leads the overall ability average.")
add_table(s, ["Model", "AVG", "TXT", "CMP", "VIS", "CG", "FG", "LC", "S", "T", "PR"],
          [["VideoCLIP-XL", "0.510", "0.550", "0.227", "0.632", "0.558", "0.493", "0.600", "0.787", "0.381", "0.310"],
           ["VLM2Vec-V2", "0.538", "0.587", "0.263", "0.613", "0.498", "0.502", "0.762", "0.809", "0.348", "0.348"],
           ["UniME-7B", "0.542", "0.561", "0.308", "0.702", "0.500", "0.518", "0.664", "0.785", "0.396", "0.373"],
           ["GME-7B", "0.562", "0.604", "0.341", "0.615", "0.518", "0.507", "0.788", "0.749", "0.373", "0.398"],
           ["Unite-7B", "0.559", "0.609", "0.254", "0.666", "0.541", "0.539", "0.746", "0.779", "0.412", "0.425"],
           ["GVE-3B", "0.571", "0.619", "0.304", "0.647", "0.552", "0.541", "0.764", "0.816", "0.430", "0.377"],
           ["GVE-7B", "0.600", "0.657", "0.312", "0.657", "0.587", "0.570", "0.814", "0.821", "0.469", "0.419"]],
          0.55, 2.02, 12.23, 3.9, best_row=6, fs=13, hfs=13,
          col_widths=[0.19]+[0.081]*10)
txt(s, 0.55, 6.05, 12.23, 0.5,
    "Source: Chapter 3, Table (by abilities). CLIP4Clip retains the best VIS (0.714) — the scaling paradox.",
    S_CAP, False, MUTED)

s = bslide("UVRB Protocol and Model Families",
           "Frozen embeddings, one protocol, 14 models across two families.")
add_table(s, ["Family", "Representative models", "Strengths", "Key limitation"],
          [["CLIP-based", "CLIP4Clip, InternVideo2, VideoCLIP-XL", "Fast; strong T2V", "Modality gaps; limited reasoning"],
           ["MLLM-based", "GME, UNITE, VLM2Vec, B3, UniME", "Unified reasoning; balanced", "Gradient interference; data-hungry"],
           ["GVE (ours)", "Qwen2.5-VL variants", "Targeted coverage; no gaps", "Needs high-quality curricula"]],
          0.55, 2.02, 12.23, 2.1, best_row=2, fs=14, col_widths=[0.15, 0.32, 0.27, 0.26])
info_card(s, 0.55, 4.45, 12.23, 1.55, "Protocol",
          "16 public datasets, identical preprocessing, frozen embeddings with cosine similarity, no "
          "task-specific fine-tuning. Capability gaps persist even at 8.3B parameters, motivating "
          "targeted synthesis rather than pure scale.")

s = bslide("Targeted Data Scaling Follows a Logarithmic Law  (promotable to main)",
           "More data helps logarithmically; smaller models gain more per decade.")
pic(s, "gve/scaling_avg", 0.55, 2.02, width=7.2, caption="Average performance vs. training-data volume (log scale).")
mathbox(s, 8.05, 2.02, 4.73, 1.0, "y  =  a · ln(x)  +  b", label="Data scaling law", expr_size=20)
result_card(s, 8.05, 3.20, 4.73, 1.4, "Efficiency gap",
            "GVE-3B gains +7.4% per 10× data vs. +5.4% for GVE-7B — smaller models scale more "
            "efficiently.")
info_card(s, 8.05, 4.75, 4.73, 1.35, "Reading",
          "Gains diminish with scale, so capability-targeted data (UVRD) matters more than sheer volume.")

s = bslide("MG-LVR — Results at 128 Frames (excerpt)",
           "Even with 16× more frames, the coarse–fine gap persists across 23 models.")
add_table(s, ["Model  ·  128 frames", "Overall R@1", "Fine R@1", "Coarse R@1"],
          [["GVE-3B", "0.491", "0.243", "0.835"],
           ["Unite-7B", "0.474", "0.234", "0.828"],
           ["GVE-7B", "0.508", "0.266", "0.845"],
           ["Qwen3-VL-Emb-8B (best)", "0.549", "0.287", "0.903"]],
          0.55, 2.02, 9.0, 2.6, best_row=3, hi_col=[2], fs=14, col_widths=[0.40, 0.20, 0.20, 0.20])
warn_card(s, 9.75, 2.02, 3.03, 2.6, "Persistent gap",
          "Best fine R@1 is still 0.287 vs 0.903 coarse — the observation bottleneck is structural, "
          "not a capacity issue.")
info_card(s, 0.55, 4.85, 12.23, 1.25, "Frame-count anchoring (training-time)",
          "Temporal ability peaks when inference frames match training; a train-32 / test-4 mismatch "
          "measurably lowers fine-grained recall — see Chapter 4 scaling tables.")

s = bslide("VEterfall — Frame and Token Efficiency (excerpt)",
           "Distillation gains hold under both frame and token compression.")
add_table(s, ["Frame-eff. (T=200)", "Overall", "Fine", "Coarse"],
          [["8F  V⁰", "0.369", "0.148", "0.782"],
           ["8F  V¹", "0.398", "0.182", "0.780"],
           ["4F  V⁰", "0.303", "0.125", "0.677"],
           ["4F  V¹", "0.319", "0.138", "0.706"]],
          0.55, 2.02, 6.0, 2.7, hi_col=[1], fs=13, col_widths=[0.4, 0.2, 0.2, 0.2])
add_table(s, ["Token-eff. (F=8)", "Overall", "Fine", "Coarse"],
          [["400T  V⁰", "0.404", "0.179", "0.801"],
           ["400T  V¹", "0.412", "0.191", "0.800"],
           ["100T  V⁰", "0.375", "0.158", "0.772"],
           ["100T  V¹", "0.380", "0.171", "0.758"]],
          6.78, 2.02, 6.0, 2.7, hi_col=[1], fs=13, col_widths=[0.4, 0.2, 0.2, 0.2])
info_card(s, 0.55, 4.95, 12.23, 1.15, "Takeaway",
          "Reducing frames or tokens with VEterfall beats the un-distilled model at the same budget; "
          "the advantage widens as budgets tighten (λ = 0.5, K = 2 rounds).")

s = bslide("GMP-GR — Full Offline Results (four datasets)",
           "Coverage / Recall@10 across all evaluated datasets vs. the best baseline.")
add_table(s, ["Coverage", "Video", "MVideo", "Explore", "Fresh"],
          [["NANN (best baseline)", "0.537", "0.502", "0.503", "0.613"],
           ["GMP-GR (ours)", "0.649", "0.604", "0.628", "0.691"]],
          0.55, 2.02, 12.23, 1.4, best_row=1, hi_col=[1,2,3,4], fs=15, col_widths=[0.32,0.17,0.17,0.17,0.17])
add_table(s, ["Recall@10", "Video", "MVideo", "Explore", "Fresh"],
          [["NANN (best baseline)", "0.672", "0.649", "0.604", "0.732"],
           ["GMP-GR (ours)", "0.824", "0.718", "0.800", "0.842"]],
          0.55, 3.70, 12.23, 1.4, best_row=1, hi_col=[1,2,3,4], fs=15, col_widths=[0.32,0.17,0.17,0.17,0.17])
info_card(s, 0.55, 5.35, 12.23, 1.05, "Speed",
          "GMP-GR retrieves 321K items/s on Video — fastest among DNN-based methods; C-NSW is faster "
          "only by dropping to a lightweight cosine metric with far lower accuracy.")

qa = [
    ("Q1 · GVE vs. GPT-4o / Gemini for retrieval",
     "Generation vs. retrieval geometry",
     "Foundation models optimize open-ended generation, not dense retrieval embeddings. GVE is "
     "trained with retrieval objectives and capability-targeted data, aligning query and video "
     "geometry rather than reusing generic hidden states."),
    ("Q2 · Is a 100-sample validation enough?",
     "Statistical limit vs. functional evidence",
     "A 100-sample audit has a wide confidence interval, which we acknowledge. The functional proof "
     "is downstream: consistent zero-shot gains across 16 UVRB datasets — systematic noise would "
     "not produce broad, cross-dataset improvements."),
    ("Q3 · Is the granularity gap a benchmark artifact?",
     "Universal across 23 models",
     "The gap persists across all 23 evaluated models and both continuity types. Its cause is "
     "structural — sparse sampling misses brief frame-level evidence — and short-clip benchmarks "
     "simply mask it."),
    ("Q4 · How would GVE + VEterfall combine?",
     "Promising, not yet evaluated",
     "Open future work. Hypothesis: a stronger dense teacher (GVE) yields higher-quality sparse "
     "distillation signals for VEterfall, improving fine-grained efficiency — a concrete "
     "cross-model experiment."),
    ("Q5 · Does SCL hurt DNN metric expressiveness?",
     "Soft rank regularizer",
     "SCL constrains ranking order, not raw score magnitudes. It aligns output ranking with "
     "Euclidean distance to remove degenerate graph-navigation cases while preserving fine-grained "
     "relevance — regularizing relative order, not absolute expressiveness."),
    ("Q6 · Can GMP-GR generalize beyond Baidu?",
     "Algorithmic generality vs. platform metrics",
     "The core logic is HNSW-compatible and architecture-agnostic, so accuracy gains transfer. "
     "Absolute throughput depends on hardware and traffic — we separate universal algorithmic "
     "value from platform-specific engineering numbers."),
]
for title, label, body in qa:
    s = bslide(title)
    info_card(s, 0.55, 2.15, 12.23, 2.0, label, body)
    gold_card(s, 0.55, 4.35, 12.23, 1.55, "Response strategy",
              "Acknowledge the limit honestly, then redirect to the empirical evidence that answers "
              "the underlying concern.")
    notes(s, body)


s = bslide("MG-LVR Controls Granularity Through Clip Relation Graphs",
           "Clip Relation Graph makes query granularity measurable, not manually assumed.")
pic(s, "mglvr/mg-lvr", 0.915, 2.02, width=11.5,
    caption="Isolated nodes → Fine queries (G)  ·  Louvain communities → Coarse queries (C)  ·  Granularity made measurable, not assumed.")
notes(s, "Backup (promotable): Figure 4.2 — MG-LVR construction pipeline. "
         "Isolated nodes = semantically unique clips → fine-grained retrieval targets (G label). "
         "Louvain communities = thematically connected multi-clip groups → coarse-grained targets (C label). "
         "This structural approach makes granularity measurable rather than manually assumed.")


def _force(rpr, name=FONT):
    for tag in ("a:latin", "a:ea", "a:cs"):
        for e in rpr.findall(qn(tag)): rpr.remove(e)
    for tag in ("a:latin", "a:ea", "a:cs"):
        rpr.append(rpr.makeelement(qn(tag), {"typeface": name}))

def _tf(tf):
    for p in tf.paragraphs:
        pPr = p._p.get_or_add_pPr()
        d = pPr.find(qn("a:defRPr"))
        if d is None:
            d = pPr.makeelement(qn("a:defRPr"), {}); pPr.insert(0, d)
        _force(d)
        for r in p.runs: _force(r._r.get_or_add_rPr())

def _walk(shapes):
    for sh in shapes:
        if sh.has_text_frame: _tf(sh.text_frame)
        if sh.shape_type == 6: _walk(sh.shapes)
        try:
            if sh.has_table:
                for row in sh.table.rows:
                    for c in row.cells: _tf(c.text_frame)
        except Exception: pass

for slide in prs.slides: _walk(slide.shapes)

OUT = "thesis-slides-v0.3.pptx"
prs.save(OUT)
print("Saved", OUT, "| slides:", len(prs.slides._sldIdLst))
