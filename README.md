# TED-KIS: A Known Item Search Benchmark for Speech Videos
The attachment files of SIGIR 2018 submission 705.  


### Table of Contents
- <a href='#ted_talk_collection'>TED Talk Collection</a>
- <a href='#topic_collection'>Topic Collection</a>
- <a href='#evaluation'>Evaluation</a>
- <a href='#citation'>Citation</a>

## TED Talk Collection
- Unzip the ted_talk_collection.zip.* files;
- Each separated XML file is a speech extracted from TED.com;
- XML tags:   <id>: a unique id for each video document
              <url>: corresponding link on youtube.com for original video
              <title>: speech video title
              <speaker>: person who gived the speech
              <view_count>: how many users have watched this video
              <publish_date>: the time when the video was uploaded
              <ted_event>: the channels on youtube.com
              <category>: the categories of content on TED.com
              <description>: the original introduction of video privided when uploaded
              <transcript>: the automatic subtitles.

## Topic Collection
- Open requested_topics.xml;
- XML tags:   <url>: the original link to fetch the request, null stands for manually labeled topics;
              <type>: direct (video title directly provided), definite (time/speaker or other definite clues provided, short), detailed (several detailed content provided, long descriptions), list (requiring videos which have certain characteristics)
              <title>: requested topic title
              <topic_creator>：the user name, or "volunteer"
              <publish_date>: the time of posting request
              <description>: detailed descriptions of request
              <answer>: the link to ground truth video.

## Evaluation
- Download TREC evalution tool from http://trec.nist.gov/trec_eval/trec_eval_latest.tar.gz;
- Generate standard TREC search result file
    Format:   #query_id  Q0 #document_id rank predicted_relevance_score system_name;
- Use the ground truth file
    Format:   #query_id 0 #ground_truth_answer relevance_score;
- Compile the tool through command
···
  make
···

- Run the evaluation:
    
