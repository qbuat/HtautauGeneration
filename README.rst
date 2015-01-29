.. -*- mode: rst -*-

Setup
-----

* Create output directories::

   mkdir prod; mkdir plots; mkdir log; mkdir joboptions

* Source the setup script::

   source setup_root.sh

* To see details on the running command::

  ./submit --help

Event Generation
----------------

* To generate Nevents X Nchunks events::
  
  ./submit gen --events Nevents --chunks Nchunks

Making Truth D3PDs
------------------

* To convert the EVNT record into a ROOT readable format::

  ./submit d3pd 


Making flat trees with variables of interest
--------------------------------------------

* There is two drivers for two flavor of flat trees (flat and flat2)::

  ./submit flat
  ./submit flat2


Cleaning the run directory
--------------------------
* To cleanup the prod directory from the garbage files::

  ./submit clean
