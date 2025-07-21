# utils.py
from bson import ObjectId
from typing import List, Dict, Any

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

def serialize_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert list of MongoDB documents to JSON serializable format"""
    return [serialize_doc(doc.copy()) for doc in docs]

def validate_object_id(obj_id: str) -> bool:
    """Validate if string is a valid ObjectId"""
    return ObjectId.is_valid(obj_id)