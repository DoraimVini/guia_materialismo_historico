#!/usr/bin/env python3
"""Converte as notas do cofre em dados JSON e monta a pagina unica (template.html)."""
import datetime
import json
import os
import re
import sys
import unicodedata

import markdown
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1])   # raiz do cofre (a raiz do repositório)
OUT = sys.argv[2]                    # arquivo HTML de saída

INCLUDE_DIRS = ["Autores", "Conceitos", "Correntes", "Obras"]
INCLUDE_FILES = ["Questões em aberto.md", "Trilha de leitura.md", "Livros/Fontes de Rosa Luxemburgo.md",
                 "Livros/Guia de fontes - epistemologia do materialismo histórico.md"]
MOC = "MOC - Materialismo histórico e dialético"

# Modulos do roteiro: (id, letra, titulo, descricao, cor, [titulos das notas em ordem])
MODULES = [
    ("a", "A", "Método e epistemologia",
     "Como Marx e Engels pensam o conhecimento: do ser social à crítica da ideologia. Comece aqui se a pergunta for \"com que método se estuda a história?\".", "epist",
     ["Materialismo histórico", "Materialismo dialético", "Epistemologia do materialismo histórico",
      "Epistemologia do método de Hobsbawm", "Hegel, a Fenomenologia e o materialismo histórico",
      "Prefácio à Fenomenologia do Espírito", "Manuscritos de 1844 - Crítica da dialética hegeliana",
      "Ludwig Feuerbach e o Fim da Filosofia Clássica Alemã",
      "Guia de fontes - epistemologia do materialismo histórico", "Prefácio de 1859",
      "Primazia do ser social", "A Ideologia Alemã", "Ideologia e ideias dominantes", "Teses sobre Feuerbach",
      "Introdução de 1857", "Do abstrato ao concreto pensado", "Prática como critério de verdade",
      "Crítica da ideologia e historicidade das categorias", "Ruptura epistemológica"]),
    ("b", "B", "Economia política",
     "Do valor à mais-valia, do salário à acumulação. A base para entender por que o capital é uma relação social e não uma coisa.", "econ",
     ["Economia política marxista", "Crítica da economia política", "Mercadoria e valor", "Trabalho concreto e trabalho abstrato",
      "Forma-valor e dinheiro", "Fetichismo da mercadoria", "Força de trabalho", "Mais-valia", "Trabalho Assalariado e Capital",
      "Salário, Preço e Lucro", "Luta salarial e sindicatos", "Acumulação de capital", "Queda tendencial da taxa de lucro",
      "Problema da transformação", "Debates sobre a teoria do valor", "O Capital - Livro I"]),
    ("c", "C", "Sociedade, Estado e comunismo",
     "Divisão do trabalho, família, Estado e a ideia de comunismo em Engels e Marx.", "soc",
     ["Divisões sociais do trabalho", "Família e reprodução social", "A Origem da Família, da Propriedade Privada e do Estado",
      "Teoria marxista do Estado", "Do socialismo utópico ao socialismo científico", "Princípios Básicos do Comunismo",
      "Comunismo como movimento real"]),
    ("d", "D", "Gramsci: hegemonia e cultura",
     "Como uma classe domina pelo consentimento e como se disputa o senso comum.", "grams",
     ["Cadernos do Cárcere", "Filosofia da práxis", "Senso comum e bom senso", "Hegemonia", "Intelectuais orgânicos e tradicionais",
      "Bloco histórico", "Historicismo absoluto", "Objetividade histórica"]),
    ("e", "E", "Organização, revolução e imperialismo",
     "Lênin, Lukács e Rosa Luxemburgo: espontaneidade e direção, reforma e revolução, imperialismo e dependência.", "org",
     ["Que Fazer (Lênin)", "Consciência de fora e espontaneidade", "Totalidade e consciência atribuída", "Reforma e revolução",
      "Greve de massas e espontaneidade", "Democracia socialista", "Imperialismo e militarismo", "Imperialismo - Lênin e Rosa",
      "Acumulação e ambientes não capitalistas", "Desenvolvimento desigual e combinado", "Socialismo ou barbárie"]),
    ("f", "F", "História do século XX",
     "O \"breve século XX\" de Hobsbawm: catástrofe, era de ouro e desmoronamento.", "hist",
     ["História do século XX", "Breve século XX", "Cronologia do breve século XX", "A Era dos Extremos", "Era da Catástrofe",
      "Era dos Extremos, cap. 1 - A era da guerra total", "Era dos Extremos, cap. 2 - A revolução mundial",
      "Era dos Extremos, cap. 3 - Rumo ao abismo econômico",
      "Era dos Extremos, cap. 4 - A queda do liberalismo", "Fascismo",
      "Genealogia - fascismo, Estado e hegemonia", "Era de Ouro",
      "Desmoronamento", "Socialismo real", "Hobsbawm lê Marx", "História social marxista"]),
    ("g", "G", "Rosa no Brasil",
     "Ponte para Florestan Fernandes: como Rosa Luxemburgo foi lida no Brasil e o que ela diz sobre comunidades tradicionais.", "br",
     ["Recepção de Rosa Luxemburgo no Brasil", "Comunismo primitivo e comunidades tradicionais", "Luxemburgo e Florestan Fernandes"]),
]
TAG_THEME = {"economia-politica": "econ", "epistemologia": "epist", "dialetica": "soc", "estado-hegemonia": "grams",
             "familia-reproducao": "soc", "historia": "hist", "organizacao-politica": "org", "imperialismo-dependencia": "org"}


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def slug(title):
    s = re.sub(r"[^a-z0-9]+", "-", deacc(title).lower()).strip("-")
    return s


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


paths = []
for d in INCLUDE_DIRS:
    for f in sorted(os.listdir(os.path.join(ROOT, d))):
        if f.endswith(".md"):
            paths.append(os.path.join(d, f))
paths += INCLUDE_FILES

raw = {}
for rel in paths:
    txt = read(os.path.join(ROOT, rel))
    title = unicodedata.normalize("NFC", os.path.basename(rel)[:-3])
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    fmeta = yaml.safe_load(m.group(1)) if m else {}
    body = txt[m.end():] if m else txt
    body = re.sub(r"^\s*# .*\n", "", body, count=1)
    raw[title] = {"rel": rel, "meta": fmeta or {}, "body": body}

ids = {t: "n-" + slug(t) for t in raw}
assert len(set(ids.values())) == len(ids), "slug duplicado"
for mod in MODULES:
    for t in mod[5]:
        assert t in raw, ("nota do modulo nao existe", t)

module_of = {}
for mod in MODULES:
    for t in mod[5]:
        module_of.setdefault(t, mod[5] and mod[4])

md = markdown.Markdown(extensions=["tables", "sane_lists"])


def plain(s):
    s = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]", lambda m: (m.group(2) or m.group(1)), s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`>#]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def blurb_of(body):
    for head in ("Em uma frase", "Por que ler"):
        m = re.search(r"^## " + head + r"\s*\n+(.+?)(?:\n\n|\Z)", body, re.S | re.M)
        if m:
            return plain(m.group(1))[:300]
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if len(p) > 50 and not re.match(r"^(>|#|-|\||Autor|Corrente|\d+\.)", p):
            return plain(p)[:300]
    return ""


out_links = {}
MISSING = set()


def convert_wikilinks(title, body):
    outs = []

    def rep(m):
        target, alias = m.group(1).strip(), m.group(2)
        if target.lower().endswith(".pdf") or target.lower().endswith(".epub"):
            label = alias or target
            return f'<span class="wl-pdf" title="Arquivo do cofre, não incluído nesta versão online">{label}</span>'
        if target == MOC:
            return f'<a class="wl" href="#inicio">{alias or "Início"}</a>'
        label = alias or target
        if target in ids:
            if ids[target] not in outs and target != title:
                outs.append(ids[target])
            return f'<a class="wl" href="#{ids[target]}">{label}</a>'
        MISSING.add(target)
        return f'<span class="wl-miss" title="Nota ainda não incluída">{label}</span>'

    body = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]", rep, body)
    return body, outs


def render(title, body):
    body = re.sub(r"\n## Minhas anotações\s*$", "\n", body.rstrip() + "\n")
    body = re.sub(r"\n## Para a confer[^\n]*\n.*?(?=\n## |\Z)", "\n", body, flags=re.S)
    body, outs = convert_wikilinks(title, body)
    md.reset()
    html = md.convert(body)
    # callouts
    def callout(m):
        kind, head, rest = m.group(1), m.group(2).strip(), m.group(3)
        inner = f"<p>{rest.strip()}</p>" if rest.strip() else ""
        more = m.group(4) or ""
        if kind == "info":
            return f'<details class="callout c-info"><summary>{head}</summary>{inner}{more}</details>'
        return f'<aside class="callout c-{kind}"><div class="ch">{head}</div>{inner}{more}</aside>'
    html = re.sub(r"<blockquote>\s*<p>\[!(\w+)\]\s*([^\n<]*)\n?(.*?)</p>(.*?)</blockquote>",
                  lambda m: callout(m), html, flags=re.S)
    html = re.sub(r"<em>(\(conferir[^<]*)</em>", r'<em class="tbc">\1</em>', html)
    html = re.sub(r"<em>(\((?:leitura minha|pergunta)[^<]*)</em>", r'<em class="mine">\1</em>', html)
    html = html.replace("<li>[ ] ", '<li class="todo">').replace("<li>[x] ", '<li class="done">')
    html = html.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    html = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener noreferrer"', html)
    return html, outs


KIND = {"obra": "obra", "conceito": "conceito", "autor": "autor", "corrente": "corrente", "trilha": "guia", "questoes": "guia"}
notes = []
for title, d in raw.items():
    html, outs = render(title, d["body"])
    tipo = d["meta"].get("tipo", "")
    kind = KIND.get(tipo, "guia" if title in ("Questões em aberto", "Trilha de leitura") else ("fonte" if title.startswith("Fontes") else "nota"))
    tags = d["meta"].get("tags") or []
    theme = module_of.get(title)
    if not theme:
        for tg in tags:
            if tg in TAG_THEME:
                theme = TAG_THEME[tg]
                break
    textplain = plain(re.sub(r"<[^>]+>", " ", html))
    stub = len(re.sub(r"\s+", "", textplain)) < 420 and kind in ("autor", "corrente")
    notes.append({
        "id": ids[title], "t": title, "k": kind, "th": theme or "", "stub": stub,
        "bl": blurb_of(d["body"]), "h": html, "x": deacc(textplain).lower(), "o": outs,
    })

mods = [{"id": m[0], "l": m[1], "t": m[2], "d": m[3], "th": m[4], "s": [ids[t] for t in m[5]]} for m in MODULES]
data = {"notes": notes, "mods": mods, "built": datetime.date.today().strftime("%d/%m/%Y")}
js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
tpl = read(os.path.join(HERE, "template.html"))
assert "/*__DATA__*/null" in tpl
page = tpl.replace("/*__DATA__*/null", js)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print("links sem nota (aparecem como texto simples):", len(MISSING))
print("notas:", len(notes), "| modulos:", len(mods), "| bytes:", len(page.encode("utf-8")))
print("sem tema:", sum(1 for n in notes if not n["th"]), "| esbocos:", sum(1 for n in notes if n["stub"]))
