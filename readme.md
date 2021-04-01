# Knockoff-based target-decoy approach to computesimilarities of metabolomic spectra and decoys usingSpec2Vec embeddings

Accurate  metabolite  identification  from  liquid  chromatogra-phy  tandem  mass  spectrometry  (LC–MS/MS)  is  a  difficultproblem that has been addressed by a few studies.  The mostcommon technique consists of matching fragment spectra toreference library spectra.  To be able to assess the quality ofthese  matches,  the  contemporary  methods  use  target-decoyapproaches  that  are  compatible  with  the  commonly  used  co-sine similarity scores while keeping the False Discovery Rate(FDR) under control.  Recently, there has been an advance-ment  in  definition  of  spectral  similarity  which  introducedan unsupervised machine learning technique, Spec2Vec, thathas  proven  more  successful  in  identification  of  metabolites.This  paper  improves  the  existing  target-decoy  methods  andintroduces  a  new  Gaussian  knockoff-based  method  native  toSpec2Vec embeddings




This is a suggested template for a project. You can modify it as you please, but
but remember to keep:

* a timelog, updated regularly in the `timelog.md` format;
* all source under version control;
* data well organised and with appropriate ethical approval (for human subject data);

Here's an overview of the structure as it stands:

* `timelog.md` The time log for your project.
* `plan.md` A skeleton week-by-week plan for the project. 
* `data/` data you acquire during the project
* `src/` source code for your project
* `status_report/` the status report submitted in December
* `meetings/` Records of the meetings you have during the project.
* `dissertation/` source and for your project dissertation
* `presentation/` your presentation

* Make sure you add a `.gitignore` or similar for your VCS for the tools you are using!
* Add any appropriate continuous integration (e.g. Travis CI) in this directory.

* Remove this `readme.md` file from any repository and replace it with something more appropriate!

## Important
* It should be easy to rebuild and run your project and your dissertation
        * Include clear instructions in the relevant directories to make this possible
