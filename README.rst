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

Configure `dir` parameter extension with the path to save the diagrams.

In your markdown text you can define the block

.. code-block::

  blockdiag {
      A -> B -> C -> D;
      A -> E -> F -> G;
  }
