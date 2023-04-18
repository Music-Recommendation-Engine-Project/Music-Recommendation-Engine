import firebase_admin
from firebase_admin import credentials
import json

cred = credentials.Certificate(json.loads("${{ secrets.SAK }}"))
firebase_admin.initialize_app(cred)