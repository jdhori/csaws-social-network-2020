# Accessible CSaWS Social Network brief - build pipeline
# All deliverables are generated from scripts/content.py (single source of truth).

PY      ?= python3
SCRIPTS := scripts
DOC     := document

.PHONY: all md html pdf export verify clean

all: export

md:
	cd $(SCRIPTS) && $(PY) build_md.py

html:
	cd $(SCRIPTS) && $(PY) build_html.py

pdf: html
	cd $(SCRIPTS) && $(PY) build_pdf.py

export: md html pdf

verify: pdf
	cd $(SCRIPTS) && $(PY) verify_pdf.py

clean:
	rm -f $(DOC)/CSaWS_SocialNetwork.md \
	      $(DOC)/CSaWS_SocialNetwork.html \
	      $(DOC)/CSaWS_SocialNetwork_accessible.pdf
