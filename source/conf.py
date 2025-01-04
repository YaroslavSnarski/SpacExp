# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SpacExp'
copyright = '2024, Y. Snarski'
author = 'Y. Snarski'
release = '01.01.2015'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os, sys, glob
sys.path.insert(0, os.path.abspath('../../SpacExp'))
sys.path.insert(1, os.path.abspath('../../SpacExp/SpacExp'))
sys.path.insert(2, os.path.abspath('../../SpacExp/SpacExpWeb'))
sys.path.insert(3, os.path.abspath('../../SpacExp/utils'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'SpacExpWeb.settings'
import django
django.setup()

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autosummary']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
