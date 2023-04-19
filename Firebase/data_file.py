import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("./Firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "${{ secrets.FIREBASE_STG_BKT }}"
})

from google.cloud import storage

# Get a reference to the bucket
bucket = storage.bucket()

# Get a reference to the file object
blob = bucket.blob("user_track_df.parquet")

# Download the file to a local path
blob.download_to_filename("./Firebase/user_track_df.parquet")