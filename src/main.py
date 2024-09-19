from flask import Flask, request, jsonify
from pydantic import BaseModel
from pydantic import ValidationError

from utils import bulk_rolls, search_bulk_worksheet

app = Flask(__name__)

class BulkRequest(BaseModel):
    roll_f: str
    roll_l: str
    sem: int
    sub: str
    week: int

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "Working"})

@app.route("/bulk", methods=["POST"])
def bulk():
    try:
        data = request.get_json()
        bulk_request = BulkRequest(**data)
        result = search_bulk_worksheet(bulk_rolls(bulk_request.roll_f, bulk_request.roll_l),
                                       bulk_request.sem, bulk_request.sub, bulk_request.week)
        return jsonify(result)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
