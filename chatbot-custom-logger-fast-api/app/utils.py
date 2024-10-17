from bson import ObjectId

def to_json_serializable(doc):
    if isinstance(doc, ObjectId):
        return str(doc)
    if isinstance(doc, dict):
        return {key: to_json_serializable(value) for key, value in doc.items()}
    if isinstance(doc, list):
        return [to_json_serializable(item) for item in doc]
    return doc