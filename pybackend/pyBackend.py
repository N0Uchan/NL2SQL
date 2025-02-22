from flask import Flask, request, jsonify
import json
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import numpy as np
from schema_processor import SchemaProcessor

app = Flask(__name__)

@app.route('/process_schema', methods=['GET'])
def process_schema():
    # schema_json = request.get_json()
    schema_json = {
    "tables": [
        {
            "name": "sales",
            "columns": [
                {"name": "id", "type": "int"},
                {"name": "amount", "type": "decimal"}
            ]
        }
    ]
}
    if not schema_json:
        return jsonify({"error": "Schema JSON is required"}), 400
    
    schema_processor = SchemaProcessor(schema_json)
    schema_processor.save_processed_schema("processed_schema.json")
    return jsonify({"message": "Schema processed and saved successfully"})

@app.route('/load_schema', methods=['GET'])
def load_schema():
    schema_processor = SchemaProcessor.load_processed_schema("processed_schema.json")
    return jsonify({"message": "Schema loaded successfully"})

@app.route('/process_query', methods=['GET'])
def process_query():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    schema_processor = SchemaProcessor.load_processed_schema("processed_schema.json")
    selected_tables = schema_processor.select_tables(query)
    return jsonify(selected_tables)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
