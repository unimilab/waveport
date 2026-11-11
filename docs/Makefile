# Minimal Sphinx makefile. Install the docs dependency group before running make.
SPHINXOPTS ?= -W --keep-going
SPHINXBUILD ?= uv run --no-sync sphinx-build
SOURCEDIR = .
BUILDDIR = _build

.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
