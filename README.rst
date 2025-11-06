Markdown blockdiag
==================

.. image:: https://travis-ci.org/gisce/markdown-blockdiag.svg?branch=master
    :target: https://travis-ci.org/gisce/markdown-blockdiag


This is the `blockdiag <http://blockdiag.com/en/blockdiag/index.html>`_
extension for `Python Markdown <http://pythonhosted.org/Markdown/>`_

Install
-------

.. code-block::

  $ pip install markdown-blockdiag

Use
---

In your markdown text you can define the block

.. code-block::

  blockdiag {
      A -> B -> C -> D;
      A -> E -> F -> G;
  }


Background Images and Icons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Blockdiag supports background images and icons on nodes. You can use local file paths or URLs:

.. code-block::

  blockdiag {
      A [label = "Node A"];
      B [label = "", background = "/path/to/image.png"];
      C [icon = "/path/to/icon.png"];
      D [label = "", background = "http://example.com/image.gif"];
      
      A -> B -> C -> D;
  }

**Important:** When using URLs for background images or icons, network access is required at diagram 
rendering time. If your environment restricts network access (e.g., CI/CD pipelines, containers, 
or offline builds), the images will not be displayed. In such cases, use local file paths instead.

For more examples, see the `blockdiag documentation <http://blockdiag.com/en/blockdiag/examples.html>`_.


Testing
-------


.. code-block::

  $ pip install coverage
  $ python setup.py test


MkDocs Integration
------------------

In your mkdocs.yml add this to markdown_extensions.

.. code-block::

  markdown_extensions:
    - markdown_blockdiag:
        format: svg
        fetch_remote_images: true  # Enable prefetching of remote images (default: true)

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

The extension supports the following configuration options:

- ``format``: Output format, either ``png`` (default) or ``svg``
- ``fontpath``: Path to a font file to use for text rendering
- ``fontantialias``: Enable/disable font antialiasing (default: ``true``)
- ``fetch_remote_images``: Pre-fetch remote images before rendering (default: ``true``). 
  When enabled, the extension will download remote images referenced in ``background`` and 
  ``icon`` attributes and cache them locally, allowing diagrams to render even in environments 
  with restricted network access. If disabled, blockdiag will attempt to fetch images directly,
  which may fail in restricted environments.
