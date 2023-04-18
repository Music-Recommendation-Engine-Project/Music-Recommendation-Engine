import firebase_admin
from firebase_admin import credentials
import json
import subprocess

# Specify the encoding when opening the file
with open('serviceAccountKey.json', encoding='latin1') as f: # or whatever encoding your file uses
  cert = json.load(f)
cred = credentials.Certificate(cert)
firebase_admin.initialize_app(cred)

# Run iconv command using subprocess
subprocess.run(['iconv', '-f', 'latin1', '-t', 'utf8', 'serviceAccountKey.json', '>', 'serviceAccountKey_utf8.json'])

# Run recode command using subprocess
subprocess.run(['recode', 'latin1..utf8', 'inputfile'])

# Then use the converted file as usual
cred = credentials.Certificate('serviceAccountKey_utf8.json')
firebase_admin.initialize_app(cred)