# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import pathlib
import sys

PROJECT = pathlib.Path(__file__).parents[2].resolve().as_posix()
print(f"- Project: {PROJECT}")
PROJECT_SRC = pathlib.Path(os.path.join(PROJECT, "apc_lemmy_bot")).as_posix()
print(f"- Source code: {PROJECT_SRC}")

sys.path.insert(0, pathlib.Path(PROJECT).as_posix())
# sys.path.insert(0, pathlib.Path(PROJECT_SRC).as_posix())

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "apc-lemmy-bot"
copyright = "2023, Carles Muñoz Gorriz"
author = "Carles Muñoz Gorriz"
release = "0.4.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "numpydoc",
    "sphinx_automodapi.automodapi",
    "autoapi.extension",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
# html_theme = 'sphinx_rtd_theme'
html_static_path = ["_static"]


# -- Options for extensions --------------------------------------------------

# Numpydoc settings
# See: https://numpydoc.readthedocs.io/en/latest/install.html
numpydoc_use_plots = False
numpydoc_show_inherited_class_members = True
numpydoc_class_members_toctree = True
# numpydoc_citation_re = "[\w-]+"
numpydoc_attributes_as_param_list = True
numpydoc_xref_param_typebool = True
# numpydoc_xref_aliases = {}
# numpydoc_xref_ignore = {}
numpydoc_validation_checks = {"all"}
# numpydoc_validation_exclude = {}

# Autoapi settings:
# See: https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
autoapi_type = "python"
autoapi_dirs = [PROJECT_SRC]
templates_path = ["_templates"]
autoapi_file_patterns = ["py", "pyi"]  # using default
autoapi_generate_api_docs = True  # using default
# autoapi_options = [...]  # using defalut
autoapi_ignore = ["*migrations*"]  # using default
# autoapi_root = "autoapi"  # using default
autoapi_add_toctree_entry = True  # using default
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
# autoapi_python_use_implicit_namespaces
# autoapi_prepare_jinja_env
autoapi_keep_files = False  # using default
# suppress_warnings
