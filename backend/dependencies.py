from firebase_utils import get_firestore_client
from typing import Generator

def get_db() -> Generator[any, None, None]:
    """Dependency injection for Firestore client."""
    yield get_firestore_client()
