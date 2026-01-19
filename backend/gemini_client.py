import os
import json
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv
import glob
from pathlib import Path

# Path to the docs directory containing schema markdown files
DOCS_DIR = Path(__file__).parent.parent / "docs"

def load_schemas() -> str:
    """
    Loads all schema markdown files from the docs directory and concatenates them
    into a single string to be used as context for the LLM.
    """
    schema_context = "Here are the database schemas for the MongoDB collections:\n\n"
    schema_files = glob.glob(str(DOCS_DIR / "*SCHEMA*.md"))
    
    if not schema_files:
        print(f"Warning: No schema files found in {DOCS_DIR}")
        return ""
        
    for file_path in schema_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                schema_context += f"--- START OF {os.path.basename(file_path)} ---\n"
                schema_context += f.read()
                schema_context += f"\n--- END OF {os.path.basename(file_path)} ---\n\n"
        except Exception as e:
            print(f"Error reading schema file {file_path}: {e}")
            
    return schema_context

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize Client
client = genai.Client(api_key=API_KEY)

# Model Name
MODEL_NAME = "gemini-2.5-flash-lite" 

SYSTEM_INSTRUCTION_QUERY = """
You are an expert MongoDB developer. Your task is to convert natural language queries into executable MongoDB queries based on the provided database schema.

Output STRICT JSON only. Do not include markdown formatting (like ```json).
The JSON must follow this structure:
{
  "collection": "users" | "surveys" | "questions" | "answers" | "surveyhistories",
  "action": "find" | "aggregate" | "count_documents",
  "filter": { ... },     // for 'find' or 'count_documents'
  "pipeline": [ ... ],   // for 'aggregate'
  "limit": number        // optional, default 20
}

Date Handling:
- For relative dates like "last month", "yesterday", or "last 10 days", you MUST calculate the PAST date range relative to the current date (2026-01-17).
- For example, if today is 2026-01-17, "last month" should be approximately 2025-12-17 to 2026-01-17.
- Always output dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).

Performance & Joins:
- IMPORTANT: When searching for a user's surveys/answers by phone number, you MUST join the 'users' collection with other collections.
- Relationship: 'users._id' matches 'surveyhistories.userId' and 'answers.userId'.
- Phone Number: Always use 'user.number' for phone numbers, not 'user.phone' or 'surveyhistories.phone'.
- Efficient Joins: Always `$match` the user by phone number in the 'users' collection BEFORE performing a `$lookup` if possible, or ensure the `$match` filters the joined dataset as early as possible.
- If a simpler 'find' can answer the question (e.g., "count users"), prefer it over 'aggregate'.

Schema Context:
{SCHEMA_CONTEXT}
"""

SYSTEM_INSTRUCTION_RESPONSE = """
You are a helpful data analyst assistant. You have successfully retrieved data from a MongoDB database based on a user's query.
Your task is to present these results in a natural, easy-to-read textual format. 
Cite specific numbers and key insights from the data.
Do not simply output the raw JSON. Summarize it effectively.
"""

def generate_mongo_query(user_query: str) -> dict:
    """
    Step 1: Convert natural language to MongoDB query JSON.
    """
    try:
        schema_context = load_schemas()
        system_prompt = SYSTEM_INSTRUCTION_QUERY.replace("{SCHEMA_CONTEXT}", schema_context)
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"User Query: {user_query}\n\nGenerate the MongoDB query JSON:",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        )
        
        result_text = response.text
        # Clean up potential markdown if not handled by mime_type
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(result_text)
        
    except Exception as e:
        error_msg = f"CRITICAL ERROR generating Mongo query: {str(e)}"
        print(error_msg)
        logging.error(f"{error_msg}\nTraceback:", exc_info=True)
        return {"error": "Failed to generate query", "details": str(e)}

def convert_results_to_natural_language(user_query: str, results: list) -> str:
    """
    Step 2: Convert MongoDB results to natural language response.
    """
    try:
        results_json = json.dumps(results, default=str) # Handle ObjectId/Date
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"User Query: {user_query}\n\nQuery Results: {results_json}\n\nPlease provide a natural language answer based on these results.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION_RESPONSE
            )
        )
        return response.text
        
    except Exception as e:
        print(f"Error generating natural language response: {e}")
        logging.error("Error generating NL response:", exc_info=True)
        return "Sorry, I successfully retrieved the data but encountered an error generating the text response."
