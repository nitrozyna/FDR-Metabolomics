# Knockoff-based target-decoy approach to compute similarities of metabolomic spectra and decoys usingSpec2Vec embeddings

Accurate metabolite identification from liquid chromatography tandem mass spectrometry (LC–MS/MS) is a difficult problem that has been addressed by a few studies. The most common technique consists of matching fragment spectra to reference library spectra. To be able to assess the quality of these matches, the contemporary methods use target-decoy approaches that are compatible with the commonly used cosine similarity scores while keeping the False Discovery Rate (FDR) under control. Recently, there has been an advancement in definition of spectral similarity which introduced an unsupervised machine learning technique, Spec2Vec, that has proven more successful in identification of metabolites. This work evaluates some of the existing target-decoy methods using Spec2Vec and introduces a new Gaussian knockoff-based target-decoy method native to Spec2Vec embeddings.  


## Installation 
Prerequisites:
[Anaconda](https://docs.anaconda.com/anaconda/install/)

Note that Anaconda is a requirement because when using Spec2Vec, only Anaconda install will make sure that a [RDKit package](https://rdkit.org/) is installed properly. The ```pip``` version of installing Spec2Vec does not guarantee this package will work properly.

### Create the Anaconda environment
```conda create -n fdr-metabolomics python=3.8```

### Activate the Anaconda environment
```conda activate fdr-metabolomics```

### Clone the project
```git clone https://github.com/nitrozyna/FDR-Metabolomics.git```

and change the directory 
```cd FDR-Metabolomics```

### Install the dependencies
```conda install -c nlesc spec2vec```

## An overview of the repository structure

* `timelog.md` The time log for the project.
* `plan.md` Week-by-week plan for the project. 
* `data/` Data acquired when running the experiments.
* `src/` Source code for the project.
* `notebooks/` Source code for the project.
* `status_report/` The status report submitted in December.
* `meetings/` Records of the meetings during the project.
* `dissertation/` Project dissertation.
* `presentation/` Presentation.
