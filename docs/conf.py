# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, '..')

import shapash

# -- Project information -----------------------------------------------------

project = 'Shapash'
copyright = '2020, Maif'
author = 'Maif'

# The short X.Y version
version = shapash.__version__

# The full version, including alpha/beta/rc tags
release = shapash.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',
    'nbsphinx',
]

nbsphinx_execute = 'never'
master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_material'
#html_logo = './assets/images/svg/shapash-github.svg'

# Material theme options (see theme.conf for more information)
html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'Shapash',
    # Set the color and the accent color
    'color_primary': 'amber',
    'color_accent': 'deep-orange',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/MAIF/shapash',
    'repo_name': 'shapash',

    # Icon of the navbar
    'logo_icon': '&#xe873',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 3,
    # If False, expand all TOC entries
    'globaltoc_collapse': True,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Additional html pages  -------------------------------------------------
import subprocess
# Generates the report example in the documentation
subprocess.call(['python', '../tutorial/report/shapash_report_example.py'])
html_extra_path = ['../tutorial/report/output/report.html']


def setup_tutorials():
    import pathlib
    import shutil

    def _copy_notebooks_and_create_rst(d_path, new_d_path, d_name):
        os.makedirs(new_d_path, exist_ok=True)
        list_notebooks = [f for f in os.listdir(d_path) if os.path.splitext(f)[-1] == '.ipynb']
        for notebook_f_name in list_notebooks:
            shutil.copyfile(os.path.join(d_path, notebook_f_name), os.path.join(new_d_path, notebook_f_name))

        # RST file (see for example docs/overview.rst)
        rst_file = '\n'.join(
            [f'{d_name}', '======================', '', '.. toctree::',
             '    :maxdepth: 1', '    :glob:', '', '    *', '']
        )
        with open(os.path.join(new_d_path, 'index.rst'), 'w') as f:
            f.write(rst_file)

    docs_path = pathlib.Path(__file__).parent
    tutorials_path = os.path.join(docs_path.parent, 'tutorial')
    tutorials_doc_path = os.path.join(docs_path, 'tutorials')

    # Create a directory in shapash/docs/tutorials for each directory of shapash/tutorial
    # And copy each notebook file in it
    list_dir = [d for d in os.listdir(tutorials_path) if os.path.isdir(os.path.join(tutorials_path, d))
                and not d.startswith('.')]
    for d_name in list_dir:
        d_path = os.path.join(tutorials_path, d_name)
        new_d_path = os.path.join(tutorials_doc_path, d_name)
        _copy_notebooks_and_create_rst(d_path, new_d_path, d_name)

    # Also copying all the overview tutorials (shapash/tutorial/shapash-overview-in-jupyter.ipynb for example)
    _copy_notebooks_and_create_rst(tutorials_path, tutorials_doc_path, 'overview')


setup_tutorials()
