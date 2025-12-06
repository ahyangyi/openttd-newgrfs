# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Ahyangyi's OpenTTD NewGRFs"
copyright = '2025, Yi Yang (ahyangyi)'
author = 'Yi Yang (ahyangyi)'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinxcontrib.mermaid"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = [".rst", ".md"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#006590",
        "color-brand-content": "#006590",
        "color-brand-visited": "#006590",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4898c9",
        "color-brand-content": "#4898c9",
        "color-brand-visited": "#4898c9",
    },
}
