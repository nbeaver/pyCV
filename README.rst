====
pyCV
====

This is a data analysis script for `cyclic voltammetry`_.
Currently it only works for data produced by the `EZStat-Pro` potentiostat,
but it could be adapted to other data formats.

.. _cyclic voltammetry : http://en.wikipedia.org/wiki/Cyclic_voltammetry

.. _EZStat-Pro : http://nuvant.com/products/potentiostat_galvanostat/ezstats-series/

-----
Usage
-----

Generated the cyclic voltammetry plots with the provided example data this way::

    python pyCV.py example-EZStat-data.csv

This will produce five ``png`` and five ``jpeg`` images, one plot for each cycle.
