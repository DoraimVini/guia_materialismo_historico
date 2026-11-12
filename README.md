# Guia de Materialismo Histórico

Caderno de estudo coletivo sobre materialismo histórico e dialético, economia política marxista e história do século XX. As notas são um cofre do [Obsidian](https://obsidian.md) (fichamentos, conceitos, autores e perguntas em aberto) e viram um site de leitura a cada publicação.

**Site:** `https://<usuario>.github.io/<repositorio>/` (ativado em Settings > Pages > Source: GitHub Actions).

## Como ler
O site tem um **roteiro de leitura em 7 módulos** (A a G), um índice livre de todas as notas, busca e o mapa de ligações de cada nota. Cada nota diz de onde vêm as citações: *lido no PDF e conferido por script*, *lido online* ou *de memória (conferir)*. Marcas *(conferir)* indicam o que ainda não foi checado na fonte.

## Estrutura do repositório
| Pasta | Conteúdo |
| --- | --- |
| `Autores/`, `Conceitos/`, `Correntes/`, `Obras/` | as notas, uma por tema |
| `Livros/` | só notas sobre os livros. **PDFs e EPUBs não entram no repositório** (direitos autorais) |
| `Inbox/`, `Modelos/` | rascunhos e modelos de nota do Obsidian |
| `.site/` | gerador do site (`build_site.py`, `template.html`) e verificações (`check.py`) |
| `.github/workflows/` | verificação nos pull requests e publicação a partir da `main` |

## Ramos (branches)
- **`main`**: o que está no ar. Só recebe mudanças por pull request, vindas da `rascunho`. Cada push na `main` publica o site.
- **`rascunho`**: o dia a dia. É para onde o Obsidian (plugin Obsidian Git) envia as notas. Pode estar incompleto.
- **`estudo/<tema>`**: ramos curtos para um bloco de leitura (ex.: `estudo/hobsbawm-cap02`, `estudo/gramsci-caderno11`). Entram na `rascunho` por pull request e são apagados depois.
- **`site/<assunto>`**: mudanças no gerador ou no visual do site.

Todo pull request roda a verificação: confere que não há PDF/EPUB no repositório e monta a página; a página montada fica disponível como artefato do PR para pré-visualizar.

## Gerar o site localmente
```
pip install -r .site/requirements.txt
python .site/check.py .
python .site/build_site.py . _site/index.html
```
Abra `_site/index.html` no navegador.

## Licença e uso das fontes
As notas citam trechos curtos, sempre com fonte e página. Não envie livros inteiros: o `.gitignore` bloqueia PDF e EPUB e a verificação falha se algum aparecer.
