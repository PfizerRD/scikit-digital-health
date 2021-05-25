"""
Binary File Reading (:mod:`skdh.read`)
=======================================

.. currentmodule:: skdh.read

Binary File Readers
-------------------

.. autosummary::
    :toctree: generated/

    ReadCWA
    ReadBin
    ReadGT3X
"""
from skdh.read.axivity import ReadCWA
from skdh.read import axivity
from skdh.read.geneactiv import ReadBin
from skdh.read import geneactiv
from skdh.read.actigraph import ReadGT3X
from skdh.read import actigraph

__all__ = ("ReadCWA", "ReadBin", "ReadGT3X", "axivity", "geneactiv", "actigraph")