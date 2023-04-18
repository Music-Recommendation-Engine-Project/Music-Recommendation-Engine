import os
import base64
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

# Load the service account key from an environment variable
load_dotenv()
cert = os.environ.get('SERVICE_ACCOUNT_KEY')

# Decode and write the service account key to a json file
with open('serviceAccountKey.json', 'wb') as f:
  f.write(base64.b64decode(cert))

# Initialize from the json file
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
