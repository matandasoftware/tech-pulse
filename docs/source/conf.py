# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tech Pulse'
copyright = '2026, Mudau Pfarelo Channel'
author = 'Mudau Pfarelo Channel'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # Auto-generate docs from docstrings
    'sphinx.ext.viewcode',      # Add links to source code
    'sphinx.ext.napoleon',      # Support Google/NumPy docstring styles
    'sphinxcontrib.httpdomain', # HTTP API documentation
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Path setup for Django
import os
import sys
import django

# Add project root to Python path
sys.path.insert(0, os.path.abspath('../..'))

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()

# HTML theme options
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
}

# Logo and favicon (optional)
# html_logo = '_static/logo.png'
# html_favicon = '_static/favicon.ico'
