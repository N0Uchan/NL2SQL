from flask import Flask, request, jsonify
from schema_processor import SchemaProcessor
import google.generativeai as genai
import re
import json

app = Flask(__name__)

# Initialize Gemini API
genai.configure(api_key="AIzaSyAQ2KATdbxds1YECAg-De56dFZbWYqgmgw")
model = genai.GenerativeModel('gemini-1.5-pro')

def refine_with_gemini(text):
    """
    Refine the text input into a JSON schema using the Gemini API.
    Handles cases where Gemini returns non-JSON output.
    """
    prompt = (
        "Convert the following natural language description into a JSON schema and generate an SQL query to create the table:\n"
        f"{text}\n\n"
        "Return only the JSON schema and SQL query in the following format:\n"
        "{\n"
        '  "tables": [\n'
        '    {\n'
        '      "name": "table_name",\n'
        '      "columns": [\n'
        '        {"name": "column_name", "type": "data_type"},\n'
        '        ...\n'
        '      ],\n'
        '      "foreign_keys": [\n'
        '        {"column": "column_name", "reference_table": "table_name"},\n'
        '        ...\n'
        '      ],\n'
        '      "sql_query": "CREATE TABLE table_name (...);"\n'
        '    },\n'
        '    ...\n'
        '  ]\n'
        "}"
    )
    response = model.generate_content(prompt)
    
    # Extract JSON from Gemini's response
    try:
        # Attempt to parse the response as JSON
        schema_json = json.loads(response.text)
    except json.JSONDecodeError:
        # If parsing fails, extract JSON part from the response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            schema_json = json.loads(json_match.group(0))
        else:
            raise ValueError("Gemini did not return valid JSON.")
    
    return schema_json

def generate_sql_queries_for_schema(schema_json):
    """
    Generate SQL queries for the provided JSON schema using Gemini.
    """
    prompt = (
        "Generate SQL CREATE TABLE queries for the following JSON schema:\n"
        f"{json.dumps(schema_json, indent=2)}\n\n"
        "Return only the SQL queries in the following format:\n"
        "{\n"
        '  "tables": [\n'
        '    {\n'
        '      "name": "table_name",\n'
        '      "sql_query": "CREATE TABLE table_name (...);"\n'
        '    },\n'
        '    ...\n'
        '  ]\n'
        "}"
    )
    response = model.generate_content(prompt)
    
    # Extract JSON from Gemini's response
    try:
        # Attempt to parse the response as JSON
        sql_queries_json = json.loads(response.text)
    except json.JSONDecodeError:
        # If parsing fails, extract JSON part from the response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            sql_queries_json = json.loads(json_match.group(0))
        else:
            raise ValueError("Gemini did not return valid JSON.")
    
    return sql_queries_json

def generate_gemini_prompt(schema, query):
    """
    Generate a prompt for Gemini to select relevant tables.
    """
    schema_description = "\n".join(
        f"- Table: {table['name']}\n  Columns: {', '.join(table['columns'])}"
        for table in schema['tables']
    )
    prompt = (
        "You are a database assistant. Your task is to select the most relevant tables "
        "from the following schema based on the user's query.\n\n"
        f"Schema:\n{schema_description}\n\n"
        f"User Query: \"{query}\"\n\n"
        "Return only the names of the relevant tables as a JSON list. For example:\n"
        '["orders", "customers"]'
    )
    return prompt

@app.route('/process_schema', methods=['POST'])
def process_schema():
    # Get input data from the request
    data = request.get_json()
    if not data or "input" not in data:
        return jsonify({"error": "Input is required"}), 400
    
    input_data = data["input"]
    
    try:
        # Determine if the input is JSON or text
        if isinstance(input_data, dict):  # JSON input
            schema_json = input_data
            # Generate SQL queries for the provided JSON schema
            sql_queries_json = generate_sql_queries_for_schema(schema_json)
            # Merge SQL queries into the schema JSON
            for table in schema_json["tables"]:
                for sql_table in sql_queries_json["tables"]:
                    if table["name"] == sql_table["name"]:
                        table["sql_query"] = sql_table["sql_query"]
                        break
        else:  # Text input
            # Convert text to JSON using Gemini
            schema_json = refine_with_gemini(input_data)
        
        # Process the schema
        schema_processor = SchemaProcessor(schema_json)
        schema_processor.save_processed_schema("processed_schema.json")
        
        # Return the processed schema as JSON
        return jsonify({
            "message": "Schema processed successfully",
            "schema": schema_json
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process_query', methods=['GET'])
def process_query():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    try:
        # Load the processed schema
        with open("processed_schema.json") as f:
            schema = json.load(f)
        
        # Generate a prompt for Gemini
        prompt = generate_gemini_prompt(schema, query)
        
        # Send the prompt to Gemini
        response = model.generate_content(prompt)
        
        # Debugging: Print the response from Gemini
        print("Gemini Response:", response.text)
        
        # Extract JSON from Gemini's response
        try:
            # Attempt to parse the response as JSON
            selected_tables = json.loads(response.text)
        except json.JSONDecodeError:
            # If parsing fails, extract JSON part from the response
            json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if json_match:
                selected_tables = json.loads(json_match.group(0))
            else:
                raise ValueError("Gemini did not return valid JSON.")
        
        # Filter the schema to return only the selected tables
        selected_schema = {
            "tables": [
                table for table in schema['tables']
                if table['name'] in selected_tables
            ]
        }
        
        return jsonify({
            "message": "Query processed successfully",
            "selected_tables": selected_schema
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# from flask import Flask, request, jsonify
# from schema_processor import SchemaProcessor
# import google.generativeai as genai
# import re
# import json

# app = Flask(__name__)

# # Initialize Gemini API
# genai.configure(api_key="AIzaSyAQ2KATdbxds1YECAg-De56dFZbWYqgmgw")
# model = genai.GenerativeModel('gemini-1.5')

# def refine_with_gemini(text):
#     """
#     Refine the text input into a JSON schema using the Gemini API.
#     Handles cases where Gemini returns non-JSON output.
#     """
#     prompt = (
#         "Convert the following natural language description into a JSON schema and generate an SQL query to create the table:\n"
#         f"{text}\n\n"
#         "Return only the JSON schema and SQL query in the following format:\n"
#         "{\n"
#         '  "tables": [\n'
#         '    {\n'
#         '      "name": "table_name",\n'
#         '      "columns": [\n'
#         '        {"name": "column_name", "type": "data_type"},\n'
#         '        ...\n'
#         '      ],\n'
#         '      "foreign_keys": [\n'
#         '        {"column": "column_name", "reference_table": "table_name"},\n'
#         '        ...\n'
#         '      ],\n'
#         '      "sql_query": "CREATE TABLE table_name (...);"\n'
#         '    },\n'
#         '    ...\n'
#         '  ]\n'
#         "}"
#     )
#     response = model.generate_content(prompt)
    
#     # Extract JSON from Gemini's response
#     try:
#         # Attempt to parse the response as JSON
#         schema_json = json.loads(response.text)
#     except json.JSONDecodeError:
#         # If parsing fails, extract JSON part from the response
#         json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
#         if json_match:
#             schema_json = json.loads(json_match.group(0))
#         else:
#             raise ValueError("Gemini did not return valid JSON.")
    
#     return schema_json

# @app.route('/process_schema', methods=['POST'])
# def process_schema():
#     # Get input data from the request
#     data = request.get_json()
#     if not data or "input" not in data:
#         return jsonify({"error": "Input is required"}), 400
    
#     input_data = data["input"]
    
#     try:
#         # Determine if the input is JSON or text
#         if isinstance(input_data, dict):  # JSON input
#             schema_json = input_data
#         else:  # Text input
#             # Convert text to JSON using Gemini
#             schema_json = refine_with_gemini(input_data)
        
#         # Process the schema
#         schema_processor = SchemaProcessor(schema_json)
#         schema_processor.save_processed_schema("processed_schema.json")
        
#         # Return the processed schema as JSON
#         return jsonify({
#             "message": "Schema processed successfully",
#             "schema": schema_json
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/load_schema', methods=['GET'])
# def load_schema():
#     try:
#         schema_processor = SchemaProcessor.load_processed_schema("processed_schema.json")
#         return jsonify({
#             "message": "Schema loaded successfully",
#             "processed_schema": {
#                 "tables": schema_processor.tables,
#                 "table_embeddings": schema_processor.table_embeddings.tolist()
#             }
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/process_query', methods=['GET'])
# def process_query():
#     query = request.args.get('query', '')
#     if not query:
#         return jsonify({"error": "Query parameter is required"}), 400
    
#     try:
#         # Load the processed schema
#         with open("processed_schema.json") as f:
#             schema = json.load(f)
        
#         # Generate a prompt for Gemini
#         prompt = generate_gemini_prompt(schema, query)
        
#         # Send the prompt to Gemini
#         response = model.generate_content(prompt)
        
#         # Parse the response (expected format: ["table1", "table2"])
#         selected_tables = json.loads(response.text)
        
#         # Filter the schema to return only the selected tables
#         selected_schema = {
#             "tables": [
#                 table for table in schema['tables']
#                 if table['name'] in selected_tables
#             ]
#         }
        
#         return jsonify({
#             "message": "Query processed successfully",
#             "selected_tables": selected_schema
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
