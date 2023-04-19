import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyCRK2mklm8HyvUTI-zfVcaHaRTTXy3t1mE",

  'authDomain': "music-reco-c4de1.firebaseapp.com",

  'databaseURL': "https://music-reco-c4de1-default-rtdb.firebaseio.com",

  'projectId': "music-reco-c4de1",

  'storageBucket': "music-reco-c4de1.appspot.com",

  'messagingSenderId': "1008354595590",

  'appId': "1:1008354595590:web:bfd443a817501051604487",

  'measurementId': "G-VJS6DZJGBK"
}

firebase = pyrebase.initialize_app(firebaseConfig)

storage = firebase.storage()

file_name = "user_track_df.parquet"

storage.child(file_name).download("dhhd.parquet")