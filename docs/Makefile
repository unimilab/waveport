# Minimal Sphinx makefile. Install the docs dependency group before running make.
# -E rebuilds the environment from scratch: autodoc cannot track changes to
# docstrings defined in the compiled extension (src/main.cpp).
SPHINXOPTS ?= -W --keep-going -E
SPHINXBUILD ?= uv run --no-sync sphinx-build
SOURCEDIR = .
BUILDDIR = _build

.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
