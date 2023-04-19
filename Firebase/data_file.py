import pyrebase

config = {
  "apiKey": "${{ secrets.FIREBASE_API_KEY }}",
  "authDomain": "${{ secrets.FIREBASE_AUTH_DOM }}",
  "databaseURL": "${{ secrets.FIREBASE_DATA_URL }}",
  "storageBucket": "${{ secrets.FIREBASE_STG_BKT }}"
}

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

storage.child("user_track_df.parquet").download("./Firebase/user_track_df.parquet")