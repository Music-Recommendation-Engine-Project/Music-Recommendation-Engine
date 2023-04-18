import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("${{ secrets.SERVICE_ACCOUNT_KEY }}")
firebase_admin.initialize_app(cred)