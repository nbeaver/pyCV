====
pyCV
====

This is a data analysis script for `cyclic voltammetry`_.
Currently it only works for data produced by the EZStat-Pro potentiostat,
but it could be adapted to other data formats.

-----
Usage
-----

Generated the cyclic voltammetry plots with the provided example data this way::

    python matplotlib-CV.py example-EZStat-data.csv

This will produce five ``png`` and five ``jpeg`` images, one plot for each cycle.
