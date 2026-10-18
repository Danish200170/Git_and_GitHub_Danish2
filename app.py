import os, json, uuid, hashlib
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"), serverSelectionTimeoutMS=2000)
collection = client[os.getenv("MONGODB_DATABASE", "git_github_assignment")][os.getenv("MONGODB_COLLECTION", "todo_items")]

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api")
def api():
    with open(os.path.join(app.root_path, "data.json"), encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.post("/submittodoitem")
def submit_todo_item():
    payload = request.get_json(silent=True) if request.is_json else request.form
    if payload is None:
        return jsonify({"error": "Send JSON or form data."}), 400
    name = str(payload.get("itemName", "")).strip()
    description = str(payload.get("itemDescription", "")).strip()
    if not name or not description:
        return jsonify({"error": "itemName and itemDescription are required."}), 400
    item_id = str(payload.get("itemId", "")).strip() or str(int(datetime.now().timestamp()*1000))
    item_uuid = str(payload.get("itemUuid", "")).strip() or str(uuid.uuid4())
    item_hash = str(payload.get("itemHash", "")).strip() or hashlib.sha256(
        f"{item_id}:{item_uuid}:{name}:{description}".encode()).hexdigest()
    doc = {"itemId": item_id, "itemUuid": item_uuid, "itemHash": item_hash,
           "itemName": name, "itemDescription": description,
           "createdAt": datetime.now(timezone.utc).isoformat()}
    try:
        client.admin.command("ping")
        result = collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return jsonify({"message": "To-do item saved.", "item": doc}), 201
    except PyMongoError:
        app.logger.exception("MongoDB operation failed")
        return jsonify({"error": "MongoDB unavailable; check MONGODB_URI and that MongoDB is running."}), 503

@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "ok", "mongodb": "connected"})
    except PyMongoError:
        return jsonify({"status": "degraded", "mongodb": "unavailable"}), 503

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
