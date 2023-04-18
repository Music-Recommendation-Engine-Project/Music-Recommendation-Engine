import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

# Load the service account key from an environment variable
load_dotenv()
cert = os.environ.get('SERVICE_ACCOUNT_KEY')
firebase_admin.initialize_app(cert)