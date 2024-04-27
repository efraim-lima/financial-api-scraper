from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

# Configure Flask-Caching
app.config.from_mapping(
    CACHE_TYPE="SimpleCache",
    CACHE_DEFAULT_TIMEOUT=300  # 5 minutes
)
cache = Cache(app)

@app.route("/api/<item_id>", methods=["GET"])
@cache.memoize()
def get_item(item_id):
    # Fetch the item from a database or external API
    item = fetch_item(item_id)
    return jsonify(item)

def fetch_item(item_id):
    # Implement the logic to fetch the item
    # This function will be cached based on the item_id
    return {"id": item_id, "name": f"Item {item_id}"}
