"""Config file for sphinx."""
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# ----------------------------------------------------------------------------
# -- Path setup --------------------------------------------------------------
# ----------------------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here.
import pathlib
import sys

PROJECT = pathlib.Path(__file__).parents[2].resolve().as_posix()
print(f"- Project: {PROJECT}")
PROJECT_SRC = pathlib.Path(PROJECT) / "apc_lemmy_bot"
print(f"- Source code: {PROJECT_SRC}")

sys.path.insert(0, pathlib.Path(PROJECT).as_posix())

# ----------------------------------------------------------------------------
# -- Project information -----------------------------------------------------
# ----------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "apc-lemmy-bot"
project_copyright = "2023-2025, Carles Muñoz Gorriz"
author = "Carles Muñoz Gorriz"
release = "0.5.4"

# ----------------------------------------------------------------------------
# -- General configuration ---------------------------------------------------
# ----------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    "autoapi.extension",
    "numpydoc",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]
templates_path = ["_templates"]
exclude_patterns: list[str] = []


# ----------------------------------------------------------------------------
# -- Options for manpage output ----------------------------------------------
# ----------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-man_pages
man_pages = [
    (
        "usage",
        "apc-lemmy-bot",
        "Post supabase events to a Lemmy instance or show them",
        [author],
        "1",
    )
]
man_show_urls = False
man_make_section_directory = True

# ----------------------------------------------------------------------------
# -- Options for HTML output -------------------------------------------------
# ----------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_context = {
    "display_github": False,  # Integrate GitHub
    "github_user": "carlesmu",  # Username
    "github_repo": "apc-lemmy-bot",  # Repo name
    "github_version": "main",  # Version
    "conf_py_path": "/docs/source/",  # Path in the checkout to the docs root
}


# ----------------------------------------------------------------------------
# -- Options for the theme ---------------------------------------------------
# ----------------------------------------------------------------------------
# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
html_theme_options = {
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "vcs_pageview_mode": "",
    "flyout_display": "hidden",
    "version_selector": True,
    "language_selector": True,
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# ----------------------------------------------------------------------------
# -- Options for extensions --------------------------------------------------
# ----------------------------------------------------------------------------

# autoapi.extension settings -------------------------------------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
autoapi_dirs = [
    PROJECT_SRC,
]

# numpydoc settings ----------------------------------------------------------
# https://numpydoc.readthedocs.io/en/latest/install.html
numpydoc_use_plots = False
numpydoc_show_inherited_class_members = True
numpydoc_class_members_toctree = True
numpydoc_attributes_as_param_list = True
numpydoc_xref_param_typebool = True
numpydoc_validation_checks = {"all"}

# sphinx.ext.intersphinx settings --------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


# ----------------------------------------------------------------------------
# -- End of file -------------------------------------------------------------
# ----------------------------------------------------------------------------
