# seed_data.py
from firebase_admin import credentials, firestore, initialize_app
import os

cred = credentials.Certificate('path/to/firebase-key.json')
initialize_app(cred)
db = firestore.client()

# Add sample writing
db.collection('writings').add({
    'title': 'First Post',
    'content': '# Hello\n\nThis is a test post.',
    'date': '2024-01-01',
    'tags': ['test'],
    'series': None,
    'slug': 'first-post'
})

print("Sample data added")