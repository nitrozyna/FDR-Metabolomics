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

* *2 hours* Familiarised myself with biology concepts necessary for understanding metabolomic problems mentioned by the supervisor.
* *5 hours* Read the metabolomic papers provided by the supervisor and decided to pursue the FDR problem over LC/MS peak detection problem.

## Week 1

### 29 Sep 2019

* *1 hour* Meeting with supervisor.
* *2 hours* Wrote meeting minutes and created a plan for the upcoming weeks.

### 1 Oct 2020

* *2 hour* Familirised myself with the concept of cosine similiraty score and Word2Vec approach.
* *4 hours* Read the main FDR paper and created notes with all the concepts that are new.

### 2 Oct 2020

* *3 hours* Continued on understanding the FDR metabolomic paper and looked at other student's available repo that approaches two main methods.
* *1 hour* Reorganised notes and created a GitHub repo with all the resources.

## Week 2

### 5 Oct 2020

* *1.5 hours* Updated Conda environment, installed MatchMS.

### 6 Oct 2020

* *2.5 hours* Installed Spec2Vec, Created a notebook with an example dataset, analysed the data, prepared questions for the meeting with supervisor
* *0.5 hour* Meeting with the supervisor, definining the plan for next week.

### 7 Oct 2020

* *3 hours* More reading of FDR approaches in proteonomics, preparing to reproduce results from passatuto, downloaded the codebase and reorganised the data.

### 8 Oct 2020

* *3 hours* Looked into the passatuto codebase, dived into other notebooks, prepared for parsing of passatuto data.

### 9 Oct 2020

* *4 hours* Created a parser for passatuto data, emailed Justin and supervisor and decided to refine the approach for reproducing passatuto results.

### 10 Oct 2020

* *1.5 hours* Read resources about mass spectrometry in metabolomics from Justin and Simon, talked to a mass spectrometry lecturer to clarify a few concepts.

### 11 Oct 2020

* *1 hour* Read parts of the "Proteomics, lipidomics, metabolomics: a mass spectrometry tutorial from a computer scientist's point of view" by R. Smith et al.

## Week 3

### 12 Oct 2020

* *1 hour* Went through the Github Gist tutorial on Word2Vec from Allison Parrish.

### 13 Oct 2020

* *3 hours* Organised papers in a new reference manager, made notes for "Proteomics, lipidomics, metabolomics: a mass spectrometry tutorial from a computer scientist's point of view" by R. Smith et al.

### 14 Oct 2020

* *0.5 hour* Started reading and creating a Level 2 summary of "Target-decoy search strategy for increased confidence in large-scale protein identifications by mass spectrometry" by J. E. Elias et al.

### 15 Oct 2020

* *2 hours* Created a level 2 summary for "Target-decoy search strategy for increased confidence in large-scale protein identifications by mass spectrometry" by J. E. Elias et al.

### 16 Oct 2020 
* *2 hours* Created level 1 and level 2 summary for "Assigning Significance to Peptides Identified by Tandem Mass Spectrometry Using Decoy Databases" by Kall L et al.

### 17 Oct 2020
* *2 hours* Created level 2 summary for "Spec2Vec: Improved mass spectral similarity scoring through learning of structural relationships" ny Huber F. et al.

### 18 Oct 2020
* *2 hours* Started writing introduction, added more resources to the list.
* *2 hours* First read of "Knockoffs for the Mass: New Feature Importance Statistics with False Discovery Guarantees" for general understanding bt Gimenez J R et al.

## Week 4

### 19 Oct 2020
* *5 hours* Completed the introduction/literature review.

### 20 Oct 2020
* *2 hours* Tidied up the references in the literature review, prepared for the meeting with the supervisor.
* *0.5 hour* Meeting with the supervisor.

### 21 Oct 2020
* *0.5 hour* Compiled the Latex template for the Masters Project, added some bits to the intro.

### 22 Oct 2020
* *0.5 hour* Tidied up notebooks and started the Passautto analysis notebook.

### 24 Oct 2020
* *1.5 hours* Corrected the passatuto parser and continued on the Passatuto analysis.

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
* *1.5 hours* Started recreating the q_value plots for Passatuto data.

### 31 Oct 2020
* *3 hours* Tried to calculate true q-values, realised the Passatuto parser needs to be enhanced and dived deeper into that.

### 1 Nov 2020
* *3 hours* Continued trying to recreate Passautto q values.

## Week 6

### 2 Nov 2020
* *3 hours* Continued trying to recreate Passautto q values, still no luck but seeing the main differences.

### 3 Nov 2020
* *1 hour* Prepared for the meeting wirh supervisor by making notes and reorganising the notebook to show some results.
* *0.5 hour* Meeting with supervisor.

### 4 Nov 2020
* *2 hours* Changed inchi comparison method a few times, q values still differ from the Passatuto results.

### 5 Nov 2020
* *1 hour* Reorganised the Passatuto notebook included additional information so that it's easier to recreate.

## Week 7

### 11 Nov 2020
* *1 hour* Prepared for the meeting wirh supervisor by creating some questions.
* *0.5 hour* Meeting with supervisor.
* *1.5 hours* Worked on creation of the general pipelines we talked about on the meeting.

### 14 Nov 2020
* *6 hours* Created parts of the pipeline, encountered a few problems, still have some bugs.

### 15 Nov 2020
* *4 hours* Finished the pipeline with cosine similarity, moved parts of the notebook to the python pipeline.

## Week 8

### 16 Nov 2020
* *2 hours* Updated some meeting notes with progress of compound comparisons, extracted two of the relevant compounds, started the notebook with cosine comparisons and grid search.

### 17 Nov 2020
* *1.5 hours* Prepared for the meeting with supervisor, introduced grid search to the basic pipeline notebook.
* *0.5 hour* Meeting with supervisor.
* *2 hours* Updated notebooks and cosine similarity functions.

### 18 Nov 2020
* *1 hour* Reread the Kall et al. paper to be able to approach decoy FDR calculation.

### 21 Nov 2020
* *2 hours* Planned exactly each step of the pipeline: creating decoy database, p-value calc, FDR, q-value calc and plots.

## Week 9

### 23 Nov 2020
* *6 hours* Finished the estimated and true q-value calculation for Passatuto data.

### 24 Nov 2020
* *0.5 hour* Prepared for meeting with supervisor.
* *0.5 hour* Meeting with supervisor.

### 26 Nov 2020
* *5 hours* Read a paper from Wang et al. "Target-decoy Based False Discovery Rate Estimation for Large scale Metabolite Identification" and created a Level 3 Summary.

## Week 10

### 30 Nov 2020
* *2 hours* Played with Spec2Vec, read documentation and preprint to prepare for coding up the Spec2Vec model.
* *6 hours* Coded up the Spec2Vec model with a pretrained dataset.

### 01 Dec 2020
* *0.5 hours* Meeting with the supervisor.
* *0.5 hours* Organised notes after the meeting.

## Week 11

### 07 Dec 2020
* *4 hours* Read "Knockoffs for the Mass: New Feature Importance Statistics with False Discovery Guarantees" by Gimenez et al.

### 08 Dec 2020
* *1 hour* Read "Knockoffs for the Mass: New Feature Importance Statistics with False Discovery Guarantees" by Gimenez et al. 
* *0.5 hours* Made a plan for writing up knockoffs.
* *2 hours* Played with training a model for Spec2Vec.
* *2 hours* Played with dimentionality.
* *1 hour* Started on the status report.

### 09 Dec 2020
* *3 hours* Continued writing the status report.
* *4 hour* Trying to understand the knockoff procedure further by reading statistics resources and other students code.

### 10 Dec 2020
* *3 hours* Continued writing the status report.
* *2 hour* Trying to understand the knockoff procedure further by reading statistics resources.
* *0.5 hour* Prepared for the meeting with supervisor.

### 11 Dec 2020
* *0.5 hours* Meeting with supervisor.
* *0.5 hour* Organised meeting notes and defined the plan of work.
* *4 hours* Finished writing the status report.
* *1 hour* Moved the status report to latex, organised references and formatting

## Week 12

### 15 Dec 2020
* *1 hour* Extended status report by adding statistical methods for measuring success in this project.

### 16 Dec 2020
* *3 hours* Added background knowledge to the status report, extended the aim section.
* *2 hours* Read the "Deep Knockoffs" by Romano Y. et al.
* *1 hours* Clarified some statistical concepts.
* *2 hours* Prepared a mathematical model and listed necessary libraries to be able to implement knockoffs appropriately.

### 17 Dec 2020
* *5 hours* Programmed knockoffs with an unsuccessful result.
* *2 hours* Tried to change various parameters like the number of components or dimensions, no luck.

### 18 Dec 2020
* *1 hour* Prepared for meeting with supervisor.
* *0.5 hour* Meeting with supervisor.

## Christmas break
* *2 hour* Played with the knockoff technique sent by supervisor.
* *1.5 hour* Started the notebook with creating knockoffs from spectra.

## Week 13

### 11 Jan 2021
* *3 hours* Moved the 2D knockoff model to embedded spectra.

### 13 Jan 2021
* *2 hours* Tweaked the knockoff model a little bit and adjusted it to more dimensions.

### 15 Jan 2021
* *0.5 hours* Meeting with supervisor.
* *0.5 hours* Organised the meeting notes and revised the plan for next week.
* *1 hour* Experimented with fitting a GMM to the spectral vectors.

### 17 Jan 2021
* *2 hours* Fitted a GMM for each spectrum vector and created a process for multiple knockoff creation given multiple spectra.

## Week 14

### 18 Jan 2021
* *3 hours* Partially replaced Passatutto approach with ready knockoffs in the basic pipeline.

### 19 Jan 2021
* *1 hour* Restrospective on progress, planning the next few weeks.

### 20 Jan 2021
* *4 hours* Finished the knockoff technique, plotted the q-value plots with comparison to library data (from the Boecker lab).
* *1 hour* Manually experimented with D, number of dimensions, intensity_weighting_power, allowed_missing_percentage to see relations and define optimal parameters.

### 21 Jan 2021
* *3 hours* Updated the knockoff technique for LC/MS data, plotted the q-value plots.
* *2 hours* Created graphs with True/False hits and cosine score representations for he LC/MS dataset.
* *1 hour* Played with dimension and effect on the True/False hits.

### 22 Jan 2021
* *3 hours* Created a notebook which accepts varying D, dimensions etc. and generates q-value plots for knockoffs.
* *2 hours* Played with the true/false positive rate graphs and generated plots with varying dimensions (without cosine comparison yet)
* *0.5 hour* Meeting with supervisor.
* *0.5 hour* Meeting notes and defined a plan for the next couple of days working on the project.

### 23 Jan 2021
* *2 hours* Read a few thesis papers from previous UofG students.
* *2 hours* Started writing background and parts of introduction of the thesis.

## Week 15

### 28 Jan 2021
* *4 hours* Experimenting with dimensions. Problems to achieve the same performance with Spec2Vec as Cosine.

### 29 Jan 2021
* *5 hours* Experimenting with dimensions. Problems to achieve the same performance with Spec2Vec as Cosine.
* *0.5 hour* Meeting with supervisor.

### 30 Jan 2021
* *1 hours* Set up model training on another machine with different dimensions and let it run for a couple of days.

## Week 16

### 02 Feb 2021
* *2 hours* Obtained models with different dimensions and set up experiments with varying library and query spectra to check the performance in comparison to Cosine Similarity.
* *1 hour* Interpreted the results for above experiments and noted down the plan for future experiments.
* *0.5 hour* Set up another experimental model training on another machine with different dimensions and let it run for a couple of days.

### 03 Feb 2021
* *2 hours* Collected and evaluated results from the last experiment.
* *2 hours* Set up another experiment to recreate exact true/false positive rate plots from Huber et al (page 8). 

### 04 Feb 2021
* *2 hours* Debugging as I can't obtain the results mentioned above.

### 05 Feb 2021
* *2 hours* Debugging
* *2 hours* Changed the cosine to min_max = 6, interpreted the results. 
* *0.5 hour* Meeting with supervisor

## Week 17

### 11 Feb 2021
* *4 hours* Collected all the pieces together (drew the plan for the pipeline), refactored previous code and created half of the knockoff pipeline.

### 12 Feb 2021
* *4 hours* Finished the knockoff pipeline and started debugging as the q-value plot doesn't look great.
* *0.5 hour* Meeting with supervisor.
* *0.5 hour* Meeting notes and revised plan.

## Week 18

### 20 Feb 2021
* *7 hours* Debugging knockoffs, tuning all the parameters.

### 21 Feb 2021
* *7 hours* Finished debugging knockoffs, figured out D is the most sensitive, changed to covariance type = diag, number of components is the same as number of dimensions.
 
## Week 19

### 23 Feb 2021
* *3 hours* Progressed on writing the thesis: knockoffs, Spec2Vec, some basic explanations of biological concepts.

### 24 Feb 2021
* *1 hour* Progressed on writing the thesis: Spec2Vec

### 25 Feb 2021
* *1.5 hours* Wrote parts on thesis about cosine similarity and modified cosine.

### 26 Feb 2021
* *0.5 hour* Meeting with supervisor
* *0.5 hour* Meeting notes, organising plan for GC/MS analysis.

### 27 Feb 2021
* *4 hours* Progressed on writing thesis and the methods described by Scheubert et al.

### 28 Feb 2021
* *0.5 hour* Exchanged several emails with other parties interested in the project.

## Week 20

### 1 March 2021
* *2 hours* Progressed on writing thesis and the methods described by Scheubert et al.

### 2 March 2021
* *1 hour* More writing of the thesis.
* *2 hours* Discovered the new multiknockoff paper that would help in variability and instability of the single knockoff technique. Made notes and contacted the supersior about it.

### 3 March 2021
* *3 hours* Created a comparison of knockoffs to Passautto decoys.

### 4 March 2021
* *2 hour* Did a grid search on best D for knockoffs. Created graphs to represent variability and instability of sing knockoffs.

### 5 March 2021
* *0.5 hour* Meeting with supervisor.
* *4 hours* Wrote parts of the thesis about knockoffs.

## Week 21

### 9 March 2021
* *3 hours* Wrote parts of the thesis: FDR, q-value calculation with references to mass spectra matches and decoys.
* *4 hours* Progressed GC-MS Spec2Vec and knockoff analysis.

### 10 March 2021
* *1 hour* Grid search for the right D in the GC-MS dataset.
* *2 hours* Wrote parts of the thesis: p-values and q-value correction.

### 11 March 2021
* *2 hours* Debugging GC-MS.

### 12 March 2021
* *2 hours* Changed knockoffs to see if they can be less variable.
* *1 hour* Meeting with supervisor

### 13 March 2021
* *6 hours* Thesis writing: knockoffs.

### 14 March 2021
* *8 hours* Fixed knockoffs for LC-MS, still struggling with GC-MS.

## Week 22

### 15 March 2021
* *5 hours* More thesis writing: knockoffs.

### 17 March 2021
* *2 hours* More thesis writing: knockoffs.

### 18 March 2021
* *2 hours* More thesis writing: knockoffs.

### 19 March 2021
* *1 hour* Focused on analysis of the unfiltered Passatutto data.
* *1 hour* Meeting with supervisor and updated meeting notes.

## Week 23

### 23 March 2021
* *6 hours* Wrote parts of thesis: organised knockoff text and started experimentation.

### 24 March 2021
* *8 hours* Wrote parts of thesis: finished LC-MS experimentation.

### 25 March 2021
* *8 hours* Wrote parts of thesis: Passatutto experimentation section.

### 26 March 2021
* *1 hour* Meeting with supervisor, meetings notes.
* *7 hours* Wrote parts of thesis: Passatutto experimentation section, dimensionality epxeriment, trianed models section.

### 28 March 2021
* *6 hours* Rerunned all notebooks, restructured the directory to produce graphs for the paper
* *3 hours* Tried to run the LC-MS pipeline with new knockoffs.
* *2 hours* Repeated the dimensionality experiment with 1 n_decimals.

## Week 24

### 29 March 2021
* *4 hours* Optimised embeddings by creating a new spec2vec_hit method to avoid repetitive embedding computation.
* *2 hours* Tried to run the LC-MS pipeline with new knockoffs - the data turns out to be messy and additional preprocessing would be necessary.
* *2 hours* Ran more dimensionality experiments, with differing min_match peaks.
* *3 hours* Finalized the basic passatutto pipeline (in writing and notebooks)
* *2 hours* Finalized the spec2vec passatutto pipeline, added knockoffs in writing.

### 30 March 2021
* *3 hours* Finalised the Section describing Spec2Vec and cosine-based similarity scoring.
* *2 hours* Finalised the Background/Introduction Section.
* *1 hour* Training the models to see final dimensions I want to use.
* *3 hours* Tweaking the LC-MS data, it's really messy and that's why knockoffs don't perform well.
* *3 hours* More writing: Finalised abstract and described a few more details in methods based on tweaking the dataset.

### 31 March 2021
* *3 hours* More writing: Finished up writing the LC-MS Experiment.
* *3 hours* More writing: Page about dimension optimization without the descirption of the graph.
* *4 hours* Reread the entire thesis up to methods, applied corrections.
* *3 hours* Tried to rerun all the experiments to do a more detailed grid-search to see if I the knockoff FDR can be improved.

### 1 April 2021
* *4 hours* More writing: Descibed results for LC-MS datasets.
* *2 hours* More writing: Described results for the GC-MS dataset.
* *6 hours* Placed thesis in latex (created formulas and references)
* *2 hours* Wrote Conclusions.

### 2 April 2021
* *1 hour* Meeting with supervisor, meeting notes.

### 3 April 2021
* *2 hours* Applied a couple of corrections in the paper suggested by the supervisor.

### 4 April 2021
* *8 hours* Applied more corrections in the paper suggested by the supervisor: explained mass spectrum, target, query, provided a couple of figures.

### 5 April 2021
* *8 hours* Provided more information in the introduction given supervisor's comments. Included two additional spectrum figures and a Gaussian distribution figure.
* *4 hours* Applied corrections to the other parts of the paper including figure captions and details highlighted by the supervisor. 

### 6 April 2021
* *2 hours* Created a new figure representing the Gaussian density function.
* *3 hours* Reread the report and applied last corrections. Added the FDR threshold calculation.

### 7 April 2021
* *3 hours* Reread the report again and applied more corrections.

