# Timelog

* PROJECT TITLE: Knockoff target-decoy approach to compute similarities of real metabolomic spectra and decoys using Spec2Vec embeddings.
* NAME: Malgorzata Kurkiewicz
* STUDENT_ID: 2145411k
* SUPERVISOR NAME: Simon Rogers

## Guidance

* This file contains the time log for your project. It will be submitted along with your final dissertation.
* **YOU MUST KEEP THIS UP TO DATE AND UNDER VERSION CONTROL.**
* This timelog should be filled out honestly, regularly (daily) and accurately. It is for *your* benefit.
* Follow the structure provided, grouping time by weeks.  Quantise time to the half hour.

## Week 0

### 22 Sep 2020

* *2 hours* Familiarised myself with biology concepts necessary for understanding metabolomic problems mentioned by the supervisor
* *5 hours* Read the metabolomic papers provided by the supervisor and decided to pursue the FDR problem over LC/MS peak detection problem

## Week 1

### 29 Sep 2019

* *1 hour* Meeting with supervisor
* *2 hours* Wrote meeting minutes and created a plan for the upcoming weeks

### 1 Oct 2020

* *2 hour* Familirised myself with the concept of cosine similiraty score and Word2Vec approach
* *4 hours* Read the main FDR paper and created notes with all the concepts that are new 

### 2 Oct 2020

* *3 hours* Continued on understanding the FDR metabolomic paper and looked at other student's available repo that approaches two main methods
* *1 hour* Reorganised notes and created a GitHub repo with all the resources

## Week 2

### 5 Oct 2020

* *1.5 hours* Updated Conda environment, installed MatchMS

### 6 Oct 2020

* *2.5 hours* Installed Spec2Vec, Created a notebook with an example dataset, analysed the data, prepared questions for the meeting with supervisor
* *0.5 hour* Meeting with the supervisor, definining the plan for next week

### 7 Oct 2020

* *3 hours* More reading of FDR approaches in proteonomics, preparing to reproduce results from passatuto, downloaded the codebase and reorganised the data

### 8 Oct 2020

* *3 hours* Looked into the passatuto codebase, dived into other notebooks, prepared for parsing of passatuto data

### 9 Oct 2020

* *4 hours* Created a parser for passatuto data, emailed Justin and supervisor and decided to refine the approach for reproducing passatuto results

### 10 Oct 2020

* *1.5 hours* Read resources about mass spectrometry in metabolomics from Justin and Simon, talked to a mass spectrometry lecturer to clarify a few concepts

### 11 Oct 2020

* *1 hour* Read parts of the "Proteomics, lipidomics, metabolomics: a mass spectrometry tutorial from a computer scientist's point of view" by R. Smith et al

## Week 3

### 12 Oct 2020

* *1 hour* Went through the Github Gist tutorial on Word2Vec from Allison Parrish

### 13 Oct 2020

* *3 hours* Organised papers in a new reference manager, made notes for "Proteomics, lipidomics, metabolomics: a mass spectrometry tutorial from a computer scientist's point of view" by R. Smith et al

### 14 Oct 2020

* *0.5 hour* Started reading and creating a Level 2 summary of "Target-decoy search strategy for increased confidence in large-scale protein identifications by mass spectrometry" by J. E. Elias et al

### 15 Oct 2020

* *2 hours* Created a level 2 summary for "Target-decoy search strategy for increased confidence in large-scale protein identifications by mass spectrometry" by J. E. Elias et al

### 16 Oct 2020 
* *2 hours* Created level 1 and level 2 summary for "Assigning Significance to Peptides Identified by Tandem Mass Spectrometry Using Decoy Databases" by Kall L et al

### 17 Oct 2020
* *2 hours* Created level 2 summary for "Spec2Vec: Improved mass spectral similarity scoring through learning of structural relationships" ny Huber F. et al

### 18 Oct 2020
* *2 hours* Started writing introduction, added more resources to the list.
* *2 hours* First read of "Knockoffs for the Mass: New Feature Importance Statistics with False Discovery Guarantees" for general understanding bt Gimenez J R et al

## Week 4

### 19 Oct 2020
* *5 hours* Completed the introduction/literature review

### 20 Oct 2020
* *2 hours* Tidied up the references in the literature review, prepared for the meeting with the supervisor
* *0.5 hour* Meeting with the supervisor

### 21 Oct 2020
* *0.5 hour* Compiled the Latex template for the Masters Project, added some bits to the intro.

### 22 Oct 2020
* *0.5 hour* Tidied up notebooks and started the Passautto analysis notebook.

### 24 Oct 2020
* *1.5 hours* Corrected the passatutto parser and continued on the Passatutto analysis.

### 25 Oct 2020
* *2 hours* Created the Passautto q-value analysis.
* *3 hours* Started moving code outside of the notebook for better readability and reproducability.

## Week 5

### 26 Oct 2020
* *1 hour* Created some questions for the meeting with supervisor and redesigned the data analysis pipeline, prepared to present it to supervisor.

### 27 Oct 2020
* *0.5 hour* Meeting with supervisor.
* *0.5 hour* Defining the plan for next week.

### 30 Oct 2020
* *1.5 hours* Started recreating the q_value plots for Passatutto data.

### 31 Oct 2020
* *3 hours* Tried to calculate true q-values, realised the Passatutto parser needs to be enhanced and dived deeper into that.

### 1 Nov 2020
* *3 hours* Continued trying to recreate Passautto q values.

## Week 6

### 2 Nov 2020
* *3 hours* Continued trying to recreate Passautto q values, still no luck but seeing the main differences.

### 3 Nov 2020
* *1 hour* Prepared for the meeting wirh supervisor by making notes and reorganising the notebook to show some results.
* *0.5 hour* Meeting with supervisor.

### 4 Nov 2020
* *2 hours* Changed inchi comparison method a few times, q values still differ from the Passatutto results.
