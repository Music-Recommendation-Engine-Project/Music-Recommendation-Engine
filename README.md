# Music-Recommendation-Engine

A recommendation system for music and song recommendations is a project that uses machine learning algorithms to analyse data on user's listening habits and recommend new songs that they may be interested in. 
Recommendation systems are widely used in the music industry. One of the reasons they have become so ubiquitous is due to the fact that online listener behaviour is characterised by cognitive biases - users prefer to take mental shortcuts rather than evaluate a large range of music choices on a daily basis. RS provides these mental shortcuts by offering personalised recommendations based on the user’s preferences.

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

1M Song Dataset Challenge: https://www.ee.columbia.edu/~dpwe/pubs/McFeeBEL12-MSDC.pdf (original paper)
The Problems:
Dataset is quite old 
Some useful links expired —> lack of updated resources
Dataset conversion to ready-to-use form will take some time


1,000,000 songs / files
273 GB of data
44,745 unique artists
7,643 unique terms (The Echo Nest tags)
2,321 unique musicbrainz tags
43,943 artists with at least one term
2,201,916 asymmetric similarity relationships
515,576 dated tracks starting from 1922
18,196 cover songs identified

On Top of That:
1. Lyrics — musiXmatch dataset, matching exactly 237,662 tracks (but the full dataset of lyrics is 779k songs. The difference comes from the fact that from 779k, instrumental songs were removed, as well as duplicates, and copyright-violation songs. 
  - The lyrics come in bag-of-words format: each track is described as the word-counts for a dictionary of the top 5,000 words ( 210,519 training bag-of-words, 27,143 testing ones) across the set. Although copyright issues prevent us from distributing the full, original lyrics, we hope and believe that this format is for many purposes just as useful, and may be easier to use.
  - Matches provided by musiXmatch based on artist names and song titles from the Million Song Dataset.
  - Why use bag-of-words and not the original lyrics? → The actual lyrics are protected by copyright and we do not have permissions to redistribute them. 
Stemming Applied

2. Tags (such as rock, jazz) – Last.fm
943,347 matched tracks MSD

3. User Data (user, song, play count)  — Echo.nest
1,019,318 unique users
384,546 unique MSD songs
48,373,586 user - song - play count triplets

https://archive.org/details/thisismyjam-datadump which provides spotify_uri+ followers+ likes

4. Genre Tags 1
5. More features
6. Taste Profiles

Other datasets (): 
https://developer.spotify.com/discover/
https://www.youtube.com/watch?v=goUzHd7cTuA&ab_channel=MarkKoh
Ready Datasets: https://research.atspotify.com/datasets/ , https://www.kaggle.com/datasets/lehaknarnauli/spotify-datasets?select=artists.csv 
OR scrape our own dataset 
OR (x2): https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db (!)
Shape: (232 725, 18)

Columns:

 0. genre             232725 non-null  object 
 1. artist_name       232725 non-null  object 
 2. track_name        232725 non-null  object 
 3. track_id          232725 non-null  object
 4. popularity        232725 non-null  int64 
 5. acousticness      232725 non-null  float64
 6. danceability      232725 non-null  float64
 7. duration_ms       232725 non-null  int64  
 8. energy            232725 non-null  float64
 9. instrumentalness  232725 non-null  float64
 10. key               232725 non-null  object 
 11. liveness          232725 non-null  float64
 12. loudness          232725 non-null  float64
 13. mode              232725 non-null  object 
 14. speechiness       232725 non-null  float64
 15. tempo             232725 non-null  float64
 16. time_signature    232725 non-null  object 
 17. valence           232725 non-null  float64
 
 # Models used
 
