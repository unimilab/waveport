Contributing to the documentation
=================================

Build locally
-------------

From the repository root, install the locked documentation dependencies:

.. code-block:: console

   uv sync --locked --only-group docs
   uv run --no-sync sphinx-build -M html docs docs/_build -W --keep-going

Open ``docs/_build/html/index.html`` in a browser. ``--only-group docs``
installs the documentation tools without building WavePort's native extension.
For an environment that also needs the package and development tools, use
``uv sync --locked --group docs`` instead.

Convenience commands after installing the tools:

.. code-block:: console

   make -C docs html
   make -C docs clean

On Windows, use ``docs\make.bat html``. To check external links separately:

.. code-block:: console

   uv run --no-sync sphinx-build -b linkcheck docs docs/_build/linkcheck -W --keep-going

The HTML build treats warnings as errors, including unresolved internal
references. The link check requires network access and is a separate manual
check. Generated files belong in ``docs/_build/`` and are ignored by Git.

Organization and style
----------------------

Write pages in reStructuredText and add them to a ``toctree``. The layout
separates tutorials (guided learning), how-to guides (specific tasks),
explanation (concepts), and reference (API details). Keep installation and
contributor instructions at the top level. Split section landing pages into
smaller pages as the documentation grows.

Use Sphinx roles such as ``:doc:`` for pages and ``:func:`` for API objects,
and specify a language on code blocks. Version and author metadata come from
``pyproject.toml``. The API reference uses Python-domain directives rather
than imports; update it alongside API changes. Code examples are rendered
but are not executed by the documentation build.

Publish to GitHub Pages
-----------------------

The workflow in ``.github/workflows/docs.yml`` builds HTML on pull requests,
pushes to ``master``, and manual runs. Only successful builds from the
repository's default branch can deploy. Pull requests have read-only
permissions and never deploy.

To enable publishing for this repository:

#. In GitHub, open **Settings → Pages → Build and deployment** and set
   **Source** to **GitHub Actions**.
#. Ensure the ``github-pages`` environment allows deployment from the default
   branch. GitHub creates this environment on the first deployment if needed.
#. Merge the documentation setup into ``master`` or run the **Documentation**
   workflow manually on the default branch.

The deployment uploads ``docs/_build/html`` using the official Pages actions
and publishes it at https://ziotom78.github.io/waveport/. The workflow uses
``GITHUB_TOKEN`` with deployment permissions scoped to the deployment job;
no personal access token or ``gh-pages`` branch is needed. Sphinx generates
``.nojekyll`` so GitHub Pages serves Sphinx's underscored asset directories.

If the default branch is renamed, update the workflow's push branch filter.
For a fork, also update the documentation URL and repository links.

See the `Sphinx getting-started guide
<https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_ and
`GitHub's custom Pages workflow documentation
<https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>`_
for the underlying tooling.
