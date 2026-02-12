from document_processor import DocumentProcessor

print("Testing document search...\n")

processor = DocumentProcessor()

# Load existing vector store
processor.load_vector_store()

# Test different searches
test_queries = [
    "What pizzas do you have?",
    "Tell me about salads",
    "What are your policies?",
    "Do you have vegetarian options?",
    "How much does pepperoni cost?"
]

for query in test_queries:
    print(f"\n{'='*60}")
    processor.search_documents(query, k=2)
    print(f"{'='*60}")