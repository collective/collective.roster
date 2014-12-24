# -*- coding: utf-8 -*-
import os

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinxcontrib_robotframework',
]

# Enable Robot Framework tests during Sphinx compilation.
sphinxcontrib_robotframework_enabled = True
sphinxcontrib_robotframework_quiet = True

# Configure Robot Framework tests to use PhantomJS
sphinxcontrib_robotframework_variables = {
    'BROWSER': 'firefox'
}

# The language
language = 'en'

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = os.environ.get('SPHINX_PROJECT', u'collective.roster')
copyright = os.environ.get('SPHINX_COPYRIGHT', u'University of Jyväskylä and contributors')

# General information about the project.

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '2.0'
# The full version, including alpha/beta/rc tags.
release = '2.0.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_*.rst', 'README']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['_static']
templates_path = ['_templates']

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
}

latex_documents = [
    # (source target file, target latex name, document title,
    #  author, document clas [howto/manual]),
    ('index', 'collective.roster.tex', u'collective.roster',
     u'University of Jyväskylä and contributors', 'manual'),
]
