import pyrebase

firebase = pyrebase.initialize_app(os.getenv("FIREBASE_APP_KEY"))

storage = firebase.storage()

file_name = "user_track_df.parquet"

storage.child(file_name).download("dhhd.parquet")
