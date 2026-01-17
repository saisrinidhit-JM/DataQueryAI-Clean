import time
from gemini_client import generate_mongo_query, convert_results_to_natural_language
from mongo_client import MongoDBClient

def test_slow_query():
    client = MongoDBClient()
    user_query = "how many users onboarded to superj in the last month"
    
    print(f"--- Starting Test for: {user_query} ---")
    
    start_time = time.time()
    print("Step 1: Generating Mongo Query via Gemini...")
    mongo_query = generate_mongo_query(user_query)
    gen_time = time.time() - start_time
    print(f"Generated Mongo Query (took {gen_time:.2f}s):")
    print(mongo_query)
    
    if "error" in mongo_query:
        print(f"Error in generation: {mongo_query['error']}")
        return

    print("\nStep 2: Executing Query in MongoDB...")
    query_start = time.time()
    results = client.execute_query(mongo_query)
    exec_time = time.time() - query_start
    print(f"Query Execution (took {exec_time:.2f}s). Results count: {len(results) if isinstance(results, list) else 1}")

    print("\nStep 3: Generating Natural Language Response...")
    nl_start = time.time()
    nl_response = convert_results_to_natural_language(user_query, results)
    nl_time = time.time() - nl_start
    print(f"NL Response (took {nl_time:.2f}s):")
    print(nl_response)
    
    total_time = time.time() - start_time
    print(f"\n--- Total Time: {total_time:.2f}s ---")

if __name__ == "__main__":
    test_slow_query()
