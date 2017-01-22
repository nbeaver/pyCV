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

    python pyCV.py --input example-EZStat-data.csv --title "Mesoporous carbon"

This will produce a folder called ``example-EZStat-data_pyCV_plots/`` containing a ``png`` image, a ``jpeg`` image, and a ``csv`` file for each cycle.

-------
License
-------

This project is licensed under the terms of the `MIT license`_.

.. _MIT license: LICENSE.txt
