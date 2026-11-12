#!/usr/bin/env python3
"""Verificacoes antes de publicar: nada de PDF/EPUB no repositorio e frontmatter legivel."""
import os, re, sys
ROOT = os.path.abspath(sys.argv[1]); erros = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in (".git", ".github", ".site", ".obsidian")]
    for f in fn:
        p = os.path.join(dp, f)
        if f.lower().endswith((".pdf", ".epub", ".mobi", ".djvu")):
            erros.append("arquivo de livro no repositorio (direitos autorais): " + os.path.relpath(p, ROOT))
        if f.endswith(".md"):
            t = open(p, encoding="utf-8").read()
            if t.startswith("---") and not re.match(r"^---\n.*?\n---\n", t, re.S):
                erros.append("frontmatter sem fechamento: " + os.path.relpath(p, ROOT))
if erros:
    print("\n".join("ERRO: " + e for e in erros)); sys.exit(1)
print("verificacoes ok")
