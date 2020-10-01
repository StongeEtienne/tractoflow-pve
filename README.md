# tractoflow-pve
A variation of Tractoflow using PVE maps

Based on TractoFlow pipeline
===================

The TractoFlow pipeline is a fully automated and reproducible dMRI processing pipeline.
TractoFlow takes raw DWI, b-values, b-vectors, T1 weighted image (and a reversed
phase encoded b=0 if available) to process DTI, fODF metrics and a whole brain tractogram.


Usage
-----

See *USAGE* or run `nextflow run main.nf --help`


Documentation:
--------------

TractoFlow documentation is available here:

[https://tractoflow-documentation.readthedocs.io](https://tractoflow-documentation.readthedocs.io)

This documentation presents how to install and launch TractoFlow on a local computer and a High Performance Computer.

If you are a user and NOT A DEVELOPER, we HIGHLY RECOMMEND following the instructions on the documentation website.


Singularity
-----------
If you are on Linux, we recommend using the Singularity container to run TractoFlow

Prebuild Singularity images are available here:

[http://scil.usherbrooke.ca/en/containers_list/](http://scil.usherbrooke.ca/en/containers_list/)

FOR DEVELOPERS: The Singularity repository is available here:
[singularity-TractoFlow](https://github.com/scilus/singularity-tractoflow)



