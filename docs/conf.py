#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Parselmouth documentation build configuration file, created by
# sphinx-quickstart on Tue Sep 12 00:08:01 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
import subprocess
import sys

on_rtd = os.environ.get('READTHEDOCS') == 'True'

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
sys.path.insert(1, os.path.abspath(os.path.dirname(__file__)))
extensions = ['sphinx.ext.napoleon',
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.doctest',
              'sphinx.ext.intersphinx',
              'sphinx.ext.todo',
              'sphinx.ext.coverage',
              'nbsphinx',
              'pybind11_docstrings',
              'praat_manual']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Parselmouth'
copyright = '2017-2019, Yannick Jadoul'
author = 'Yannick Jadoul'

if on_rtd:
    rtd_version = os.environ.get('READTHEDOCS_VERSION')
    setup_py_version = subprocess.check_output([sys.executable, os.path.abspath(os.path.join('..', 'setup.py')), '--version']).decode('ascii').strip()

    if rtd_version == 'stable':
        branch = None
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'praat-parselmouth=={}'.format(setup_py_version)])
        except subprocess.CalledProcessError:
            branch = 'stable'
    else:
        branch = 'master' if rtd_version == 'latest' else rtd_version

    if branch is not None:
        # PEP 425 tags
        rtd_impl_tag = 'cp{}{}'.format(sys.version_info.major, sys.version_info.minor)
        rtd_abi_tag = rtd_impl_tag + 'm'
        rtd_platform_tag = 'manylinux1_x86_64'
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'https://dl.bintray.com/yannickjadoul/Parselmouth/{}/praat_parselmouth-{}-{}-{}-{}.whl'.format(branch, setup_py_version, rtd_impl_tag, rtd_abi_tag, rtd_platform_tag)])
else:
    sys.path.insert(0, os.path.abspath(os.path.join('..', 'installed')))

import parselmouth

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '.'.join(parselmouth.__version__.split('.')[:2])
# The full version, including alpha/beta/rc tags.
release = parselmouth.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Autodoc configuration
autodoc_member_order = 'groupwise'

# Intersphinx configuration
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'numpy': ('https://docs.scipy.org/doc/numpy', None),
                       'tgt': ('https://textgridtools.readthedocs.io/en/stable', None)}

default_role = 'py:obj'
nitpicky = True
nitpick_ignore = [('py:class', 'pybind11_builtins.pybind11_object'),
                  ('py:class', 'List'),
                  ('py:obj', 'List')]


if on_rtd:
    branch_or_tag = branch or 'v{}'.format(release)
else:
    rev_parse_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('ascii').strip()
    branch_or_tag = rev_parse_name if rev_parse_name != 'HEAD' else 'v{}'.format(release)

rst_epilog = """
.. |binder_badge_examples| image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/YannickJadoul/Parselmouth/{branch_or_tag}?urlpath=lab/tree/docs/examples
""".format(branch_or_tag=branch_or_tag)

nbsphinx_prolog = """
{{% set docname = env.doc2path(env.docname, base='docs') %}}

.. only:: html

    .. note::

        An online, interactive version of this example is available at Binder: |binder|

.. |binder| image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/YannickJadoul/Parselmouth/{branch_or_tag}?urlpath=lab/tree/{{{{ docname }}}}
""".format(branch_or_tag=branch_or_tag)


def setup(app):
    app.add_stylesheet('css/custom.css')


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'default' if on_rtd else 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
# html_sidebars = {
#     '**': [
#         'about.html',
#         'navigation.html',
#         'relations.html',  # needs 'show_related': True theme option to display
#         'searchbox.html',
#         'donate.html',
#     ]
# }


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Parselmouthdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Parselmouth.tex', 'Parselmouth Documentation',
     'Yannick Jadoul', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'parselmouth', 'Parselmouth Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Parselmouth', 'Parselmouth Documentation',
     author, 'Parselmouth', 'One line description of project.',
     'Miscellaneous'),
]



# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


