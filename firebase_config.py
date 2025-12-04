import firebase_admin
from firebase_admin import credentials, auth, firestore

# Nome do arquivo JSON que você baixou do Firebase
cred = credentials.Certificate("integra-tech-firebase-adminsdk-fbsvc-40bf2a0ad0.json")

firebase_admin.initialize_app(cred)

db = firestore.client()
