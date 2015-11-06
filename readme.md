Insight Data Engineering - Coding Challenge
===========================================================

## Challenge Summary

This repository is my implementation of the two features of the challange requirements.

Feature 1: Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.

Feature 2: Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

## Details of Implementation

I have implemented both features as stand-alone programs in case the end-user would like to utilize only one.
Both programs take 2 arguments (input file, output file).

e.g. python ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt

It is assumed that the input file is a text document with each line containing JSON of tweet from the Twitter API.

Expected tweets.txt example:

	{JSON of first tweet}  
	{JSON of second tweet}  
	{JSON of third tweet}  
	.
	.
	.
	{JSON of last tweet}  

## First Feature

The point of the first feature is to extract and clean the relevant data for the Twitter JSON messages.  For example, a typical tweet might come in the following JSON message (which we have expanded on to multiple lines to make it easier to read):

<pre>
{
 "created_at":"<b>Thu Oct 29 17:51:01 +0000 2015</b>","id":659789759787589632,
 "id_str":"659789759787589632","text":"<b>Spark Summit East this week! #Spark #Apache</b>",
 "source":"\u003ca href=\"http:\/\/twitter.com\" rel=\"nofollow\"\u003eTwitter Web Client\u003c\/a\u003e",
 "truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,
 "in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,
 "user":{"id":40077534,"id_str":"40077534","name":"scott bordow","screen_name":"sbordow",
 "location":null,"url":null,"description":"azcentral sports high school sports columnist. If you send me a tweet, you consent to letting azcentral sports use and showcase it in any media.",
 "protected":false,"verified":true,"followers_count":4704,"friends_count":2249,"listed_count":94,
 "favourites_count":51,"statuses_count":15878,"created_at":"Thu May 14 20:36:46 +0000 2009",
 "utc_offset":-25200,"time_zone":"Pacific Time (US & Canada)","geo_enabled":true,"lang":"en",
 "contributors_enabled":false,"is_translator":false,"profile_background_color":"C0DEED",
 "profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png",
 "profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png",
 "profile_background_tile":false,"profile_link_color":"0084B4","profile_sidebar_border_color":"C0DEED",
 "profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,
 "profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/576178462496423936\/YnOZ-StV_normal.jpeg",
 "profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/576178462496423936\/YnOZ-StV_normal.jpeg",
 "default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},
 "geo":null,"coordinates":null,"place":{"id":"a612c69b44b2e5da","url":"https:\/\/api.twitter.com\/1.1\/geo\/id\/a612c69b44b2e5da.json","place_type":"admin","name":"Arizona","full_name":"Arizona, USA","country_code":"US",
 "country":"United States","bounding_box":{"type":"Polygon","coordinates":[[[-114.818269,31.332246],[-114.818269,37.004261],[-109.045152,37.004261],[-109.045152,31.332246]]]},
 "attributes":{}},"contributors":null,"is_quote_status":false,"retweet_count":0,"favorite_count":0,
 "entities":{"hashtags":[{"text":"Spark","indices":[29,35]},{"text":"Apache","indices":[36,43]}],"urls":[],"user_mentions":[],"symbols":[]},
 "favorited":false,"retweeted":false,"filter_level":"low","lang":"en","timestamp_ms":"1446141111691"
}  
</pre>

where the relevant text that we want to extract has been bolded.  After extracting this information, this tweet should be outputted as

	Spark Summit East this week! #Spark #Apache (timestamp: Thu Oct 29 17:51:01 +0000 2015)

with the format of 

	<contents of "text" field> (timestamp: <contents of "created_at" field>)

In this case, the tweet's text was already clean, but another example tweet might be:



## Second Feature
The second feature will continually update the Twitter hashtag graph and hence, the average degree of the graph. The graph should just be built using tweets that arrived in the last 60 seconds as compared to the timestamp of the latest tweet. As new tweets come in, edges formed with tweets older than 60 seconds from the timstamp of the latest tweet should be evicted. For each incoming tweet, only extract the following fields in the JSON response
* "hashtags" - hashtags found in the tweet
* "created_at" - timestamp of the tweet

### Building the Twitter Hashtag Graph

```

The full list of tweets now is 
```
Spark Summit East this week! #Spark #Apache (timestamp: Thu Oct 29 17:51:01 +0000 2015)
Just saw a great post on Insight Data Engineering #Apache #Hadoop #Storm (timestamp: Thu Oct 29 17:51:30 +0000 2015)
Doing great work #Apache (timestamp: Thu Oct 29 17:51:55 +0000 2015)
Excellent post on #Flink and #Spark (timestamp: Thu Oct 29 17:51:56 +0000 2015)
New and improved #HBase connector for #Spark (timestamp: Thu Oct 29 17:51:59 +0000 2015)
New 2.7.1 version update for #Hadoop #Apache (timestamp: Thu Oct 29 17:52:05 +0000 2015)
```

We can see that the very first tweet has a timestamp that is more than 60 seconds behind this new tweet. This means that we do not want to include our first tweet in our average degree calculation.

The new hashtags to be used are as follows
```
#Apache, #Hadoop, #Storm (timestamp: Thu Oct 29 17:51:30 +0000 2015)
#Apache (timestamp: Thu Oct 29 17:51:55 +0000 2015)
#Flink, #Spark (timestamp: Thu Oct 29 17:51:56 +0000 2015)
#HBase, #Spark (timestamp: Thu Oct 29 17:51:59 +0000 2015)
#Hadoop #Apache (timestamp: Thu Oct 29 17:52:05 +0000 2015)
```

The new edge list only has the `#Spark` <-> `#Apache` edge removed since `#Hadoop` <-> `#Apache` from the new tweet already exists in the edge list.
```
#Apache <-> #Hadoop
#Hadoop <-> #Storm
#Storm <-> #Apache

#Flink <-> #Spark

#HBase <-> $Spark
```



The output of the second feature should be a file in the `tweet_output` directory named `ft2.txt` that contains the rolling average for each tweet in the file (e.g. if there are three input tweets, then there should be 3 averages), following the format above.  The precision of the average should be two digits after the decimal place (i.e. rounded to the nearest hundredths place).

## Collecting tweets from the Twitter API

## Additional Features

## Repo directory structure
	├── README.md  
	├── run.sh  
	├── src  
	│   ├── average_degree.py  
	│   └── tweets_cleaned.py  
	├── tweet_input  
	│   └── tweets.txt  
	└── tweet_output  
	    ├── ft1.txt  
	    └── ft2.txt  


