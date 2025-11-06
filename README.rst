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

Configuration Options
---------------------

The extension supports the following configuration options:

* **format** (default: ``png``): Output format for diagrams. Can be ``png`` or ``svg``.
* **fontpath** (default: ``''``): Path to font file to use for text rendering.
* **fontantialias** (default: ``True``): Enable or disable font antialiasing.
* **edge_label_box** (default: ``True``): Show or hide the box around edge labels. Set to ``False`` for cleaner diagrams without label boxes.

Example with edge labels without boxes:

.. code-block::

  markdown_extensions:
    - markdown_blockdiag:
        format: svg
        edge_label_box: False
