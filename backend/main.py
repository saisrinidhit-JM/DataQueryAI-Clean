from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from gemini_client import generate_mongo_query, convert_results_to_natural_language
from mongo_client import MongoDBClient

app = FastAPI(title="Data QueryAI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
mongo_client = MongoDBClient()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    natural_language_response: str
    raw_data: list | dict
    query_used: dict

@app.get("/")
async def root():
    return {"status": "online", "message": "Data QueryAI Backend is running"}

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    print(f"\n--- Processing Query: {request.query} ---")
    
    # Step 1: Generate MongoDB Query
    print("Step 1/3: AI generating MongoDB query...")
    mongo_query = generate_mongo_query(request.query)
    print(f"Generated Query: {mongo_query}")
    
    if "error" in mongo_query:
        print(f"ERROR in Step 1: {mongo_query['error']}")
        raise HTTPException(status_code=400, detail=f"Failed to generate query: {mongo_query['error']}")

    # Step 2: Execute Query
    print("Step 2/3: Executing in MongoDB...")
    results = mongo_client.execute_query(mongo_query)
    
    if isinstance(results, dict) and "error" in results:
         print(f"ERROR in Step 2: {results['error']}")
         raise HTTPException(status_code=500, detail=f"Database error: {results['error']}")

    print(f"Found {len(results) if isinstance(results, list) else 1} results.")

    # Step 3: Generate Natural Language Response
    print("Step 3/3: AI summarizing results...")
    nl_response = convert_results_to_natural_language(request.query, results)
    print("AI Response generated.")
    
    return {
        "natural_language_response": nl_response,
        "raw_data": results,
        "query_used": mongo_query
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
