# TED-KISS: a Known-Item Speech video Search benchmark
The attachment files of CIKM 2018 submission 1380.


### Table of Contents
- <a href='#ted_talk_collection'>TED Talk Collection</a>
- <a href='#topic_collection'>Topic Collection</a>
- <a href='#evaluation'>Evaluation</a>
- <a href='#citation'>Citation</a>
- <a href='#neural-ir_models'>Neural-IR Models</a>


## TED Talk Collection
- Unzip the ```ted_talk_collection.zip.*``` files;
- Each separated XML file is a speech extracted from TED.com;
- XML tags:
	- \<id\>: a unique id for each video document
	- \<url\>: corresponding link on youtube.com for original video
	- \<title\>: speech video title
	- \<speaker\>: person who gived the speech
	- \<view_count\>: how many users have watched this video
	- \<publish_date\>: the time when the video was uploaded
	- \<ted_event\>: the channels on youtube.com
	- \<category\>: the categories of content on TED.com
	- \<description\>: the original introduction of video privided when uploaded
	- \<transcript\>: the automatic subtitles.

## Topic Collection
- Open ```requested_topics.xml```;
- XML tags:   
	- \<url\>: the original link to fetch the request, null stands for manually labeled topics
	- \<type\>: direct (video title directly provided), definite (time/speaker or other definite clues provided, short), detailed (several detailed content provided, long descriptions), list (requiring videos which have certain characteristics)
	- \<title\>: requested topic title
	- \<topic_creator\>：the user name, or "volunteer"
	- \<publish_date\>: the time of posting request
	- \<description\>: detailed descriptions of request
	- \<answer\>: the link to ground truth video.

## Neural-IR Models
The two Neu-IR models are from https://github.com/white127/insuranceQA-cnn-lstm
- Files 
	- 4SeaResCombine.txt: an example of a standard TREC search result file (the index built with no_description_speaker; the IR model used is the query likelihood (QL))
	- 100_no_answer_queryids.txt: a query_id set (the first 100 answers to these queries in a standard TREC search result file do not contain the ground truth answer; 
	- TED Talk Collection: unzip the ted_talk_collection.zip.* files to get total 77,933 xml files (stored in 1xml/)
- Pre-processing
	- Use ```requested_topics.xml```
	- Use ```eval_file_trec_format.txt```
	- Use ```code/Neu-IR_input/4SeaResCombine.txt```
	- Use ```code/Neu-IR_input/100_no_answer_queryids.txt```
	- reformat the input files
	- change filepath to your input files
	- Run Script:
		- Format:   
	  	```
	 	python input_NN.py;
	    	```
- Run CNN/CNN+LSTM models
	
## Evaluation
- Download TREC evalution tool from http://trec.nist.gov/trec_eval/trec_eval_latest.tar.gz;
- Run your IR models and generate standard TREC search result file
	- Format:   
	  ```
	  #query_id  Q0 #document_id rank predicted_relevance_score system_name;
	    ```
- Use the ground truth file ```eval_file_trec_format.txt```
	- Format: ? 
	  ```
	  #query_id 0 #ground_truth_document_id relevance_score;
	  ```
- Compile the tool through command ```make```;
- Run the evaluation:
  ```
  trec_eval -q -c -M1000 -m all_trec eval_file_trec_format.txt path_to_result_file
## Citation
If you use our benchmark, please cite the following paper:

	@inproceedings{cikm_1380,
	  title={TED-KISS: a Known-Item Speech video Search benchmark},
	  author={Anonymous Author(s)}
	  booktitle={submitted to CIKM},
	  year={2018}
	}
 ? ?
