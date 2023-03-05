# Music-Recommendation-Engine

A recommendation system for music and song recommendations is a project that uses machine learning algorithms to analyse data on user's listening habits and recommend new songs that they may be interested in. 
Recommendation systems are widely used in the music industry. One of the reasons they have become so ubiquitous is due to the fact that online listener behaviour is characterised by cognitive biases - users prefer to take mental shortcuts rather than evaluate a large range of music choices on a daily basis. RS provides these mental shortcuts by offering personalised recommendations based on the user’s preferences.

Frontend Preview: https://www.figma.com/proto/d80N8dn5vyP8Eww70624hW/Final-PC?node-id=2%3A2&scaling=scale-down&page-id=0%3A1&starting-point-node-id=2%3A2

# Valuable Variables

- Song Lyrics and Sentiment Analysis of the song
- Binary Encoded songs
- Waveform of the songs
- Classical variables employed by the state-of-the-art solutions: history of listening, genre, year of the release of the song 
- Metadata of the song - learned from audio signals in a song recommendation scenario
- Location of the user
- Audio-specific:  tempo, key, mode
- Time of day for listening the song
- Artist embeddings from biographies by combining semantics, text features, and aggregates usage data
- Feedback from the user - like/dislike of the song


# Dataset 

The first step was preparing the data related to users and songs from various sources, which become the main dataset for the modelling. This way every fundamental feature is included. The data related to common IDs between the Echo Nest and Spotify APIs was also extracted and combined into a single data frame. This part of the project aimed to ensure the data was clean, accurate, and ready for further analysis and integration into other applications.

Data Sources: 
Triplets dataset contained information about users' interactions with songs, including user IDs, song IDs, and play counts. 
 # fd50c4007b68a3737fe052d5a4f78ce8aa117f3d    SOBONKR12A58A7A7E0    1
Songid_name dataset: This dataset contained song information, including song IDs, song names, and artist names.
# TRYYXOR128F92D7391<SEP>SOYIIVT12AAF3B3F1F<SEP>Blue Highway<SEP>Only
Tracks dataset from Spotify API: This dataset contains song information, including song IDs, artist names, and track URIs.
['track_uri', 'track_name', 'popularity', 'duration_ms', 'explicit', 'artists', 'id_artists', 'release_date', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', ‘'tempo', 'time_signature']

ETL Process:
Extract: The data extracted is related to users and songs from the Triplets and Songid_name datasets. Song-related data was also extracted from the Tracks dataset from the Spotify API.
Transform: Then the data was transformed to ensure it was in a suitable format for merging and analysis. For example, columns were renamed, duplicates filtered, and relevant information was selected. The first artist and ID were selected from several sources for each artist to ensure consistency in the data.
Load: Next, the transformed data is loaded into a single data frame called df_users_songMD, which contains all the relevant information related to users' songs.
Extract and Transform: Then data that is related to standard IDs between the Echo Nest and Spotify APIs is extracted. All the songs' IDs and track URI are selected and combined into a single data frame using the song_id and track_uri columns. Then the data is transformedto remove duplicates and group by song_id to create a unique list of track_uris associated with each song_id.
Data Quality: Throughout the ETL process, it was ensured that the data was clean, accurate, and consistent. It was also verified that all data fields were correctly formatted and no null or missing values existed.

It successfully completed the ETL process for users and songs data and common IDs between the Echo Nest and Spotify APIs. It was ensured the data was clean, accurate, and consistent throughout the process. The final data frame, df_users_songMD, contains all the relevant information about users' songs. The combined data frame with the common IDs allows for further analysis and integration with other applications.

 
 # Models used
  
  The Modelling process consisted of building four different models and observing their performance. 
The models built were the following:
 
·       Popularity-based Recommendation System
The popularity-based system is based on the count of user ids for each unique song. It has the following principal steps:
1)     Get a count of user ids for each unique song as a recommendation score
2)     Sort the songs based on the scores 
3)     Generate a recommendation rank based on the score
4)     Generate top ten recommendations according to the rank
 
It is tested using precision and recall. 

 
·       Item Similarity-based Collaborative Filtering Model
The system works by calculating the similarity between user songs and all unique songs in the training data. It has the following principal steps:
1)     Get unique songs of a given user
2)     Get unique users for a given song
3)     Get unique songs in the training data
4)     Construct a cooccurrence matrix by calculating the similarities between the songs associated with a user and all unique songs
5)     Generate top ten recommendations based on the cooccurrence matrix
 
It is tested using precision and recall.
It can be observed that the Item-Similarity based Collaborative Filtering Model outperforms the Popularity-based Recommendation System.

 
·       K-Means Clustering
The recommendation system clusters songs by implementing K-Means using sklearn library and generates recommendations according to the clusters. It has the following principal steps:
1)     Find optimal number of clusters using the Elbow method
2)     Fit the K-means model
3)     Add a column with the corresponding clusters
4)     Find out the maximum occurring cluster number according to user’s favorite track types
5)     Sort the cluster numbers and find out the number which occurs the most
6)     Get the tracks of that cluster and print the first five rows of the dataframe having that cluster number as their type
 
It is tested using the silhouette score – 0.52 on a scale from -1 to 1.
 
·       Matrix Factorization using SVD
The Matrix Factorization system aims to generate recommendations using SVD. In addition, it uses cosine similarity to find similar songs. It has the following principal steps:
1)    Add ratings column to the dataset based on the listen count of each user
2)    Keep only popular songs and active users
3)    Transform the database into a matrix (user id as index, track id as columns, ratings as values)
4)    Apply SVD
5)    Use cosine similarity to find similarities between the songs

