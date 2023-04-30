# Music-Recommendation-Engine

A recommendation system for music and song recommendations is a project that uses machine learning algorithms to analyse data on user's listening habits and recommend new songs that they may be interested in. 
Recommendation systems are widely used in the music industry. One of the reasons they have become so ubiquitous is due to the fact that online listener behaviour is characterised by cognitive biases - users prefer to take mental shortcuts rather than evaluate a large range of music choices on a daily basis. RS provides these mental shortcuts by offering personalised recommendations based on the user’s preferences.

Frontend Preview: https://www.figma.com/proto/d80N8dn5vyP8Eww70624hW/Final-PC?node-id=2%3A2&scaling=scale-down&page-id=0%3A1&starting-point-node-id=2%3A2

## Valuable Variables

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

### Data Sources: 
First, the Triplets dataset provided information about users' interactions with songs, including user IDs, song IDs, and play counts. This dataset was used to extract user and song information, which was later used to create a list of unique users and their associated songs. Next, the Songid_name dataset contained song information, including song IDs, song names, and artist names. This dataset was used to extract song names and artist names to enhance our information about the songs. Lastly, the Tracks dataset from the Spotify API was used, which contained song information such as song IDs, artist names, and track URIs. This dataset was used to extract track URIs for each song, which were later used to combine the data from the Echo Nest and Spotify APIs.
During the Extract phase, PySpark was used to read and extract the relevant data from the datasets. To handle the large datasets, techniques such as partitioning and caching were used to optimize the performance of the code. Additionally, some datasets had missing or incorrect data, which were handled carefully to ensure that the ETL process would be unaffected.

### Transform Phase:
In the Transform phase, PySpark was used to transform the extracted data into a suitable format for merging and analysis. In addition, the data was cleaned and standardized to remove duplicates and inconsistencies. The data was also transformed to include additional columns such as song names, artist names, and track URIs to create a comprehensive list of information about users' songs.

### Load Phase:
In the Load phase, the transformed data was loaded into a single data frame called df_users_songMD. This data frame contains all the relevant information about users' songs, including user IDs, song IDs, play counts, song names, artist names, and track URIs. In addition, a unique list of track URIs associated with each song ID was also created by grouping the data by song ID and removing duplicates.
An improvement that was attempted was the vectorization of playlists for each song. The data was extracted from one of Spotify's APIs, providing one million playlists containing an average of sixty songs. However, the dataset could have been more manageable regarding size and quality. The unique song IDs were common and had different names and artists, resulting in several problems. 

A decision was made only to select the first artist, which reduced nearly half the dataset when filtering. The investigation and testing of the vectorisation revealed that the number of unique playlists and their assigned IDs was chaotic, which was resolved after fixing a coding error. However, it did not work either, resulting in more issues related to character encoding and duplicate names. After combining the playlist-transformed data with the metadata, only thirty thousand songs in common were found out of a balanced one million to two hundred thousand songs. Therefore, the decision was made not to use the playlist data.
 
 ## Models used
  
  The Modelling process consisted of building four different models and observing their performance. 
The models built were the following:
 
### Popularity-based Recommendation System
The popularity-based system is based on the count of user ids for each unique song. It has the following principal steps:
1)     Get a count of user ids for each unique song as a recommendation score
2)     Sort the songs based on the scores 
3)     Generate a recommendation rank based on the score
4)     Generate top ten recommendations according to the rank
 
It is tested using precision and recall. 

 
### Item Similarity-based Collaborative Filtering Model
The system works by calculating the similarity between user songs and all unique songs in the training data. It has the following principal steps:
1)     Get unique songs of a given user
2)     Get unique users for a given song
3)     Get unique songs in the training data
4)     Construct a cooccurrence matrix by calculating the similarities between the songs associated with a user and all unique songs
5)     Generate top ten recommendations based on the cooccurrence matrix
 
It is tested using precision and recall.
It can be observed that the Item-Similarity based Collaborative Filtering Model outperforms the Popularity-based Recommendation System.

 
### K-Means Clustering
The recommendation system clusters songs by implementing K-Means using sklearn library and generates recommendations according to the clusters. It has the following principal steps:
1)     Find optimal number of clusters using the Elbow method
2)     Fit the K-means model
3)     Add a column with the corresponding clusters
4)     Find out the maximum occurring cluster number according to user’s favorite track types
5)     Sort the cluster numbers and find out the number which occurs the most
6)     Get the tracks of that cluster and print the first five rows of the dataframe having that cluster number as their type
 
It is tested using the silhouette score – 0.52 on a scale from -1 to 1.
 
### Matrix Factorization using SVD
The Matrix Factorization system aims to generate recommendations using SVD. In addition, it uses cosine similarity to find similar songs. It has the following principal steps:
1)    Add ratings column to the dataset based on the listen count of each user
2)    Keep only popular songs and active users
3)    Transform the database into a matrix (user id as index, track id as columns, ratings as values)
4)    Apply SVD
5)    Use cosine similarity to find similarities between the songs


## Web Application Deployment

First part of productionalization of the solution is a web application hosted on Heroku and deployed with Docker and Github Actions. The application allows to:
1. Log In to Spotify
2. Search the artist.
3. Get set of recommended artists using Bayesian Personalized Ranking (BPR) model deployed. 
   * If artist was not found in the database, recommendation using Spotify recommender is retrived. 
5. For each recommended artists, the most popular songs are provided.
6. User can list to those songs directly inside the web application. 

Application is deployed using Dockerfile and heroku.yml files. 

The application can be accessed: https://song-recommender2023.herokuapp.com/ 
