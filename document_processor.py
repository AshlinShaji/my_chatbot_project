"""
Process documents and create vector embeddings.
This converts documents into a searchable database.
"""

from pathlib import Path
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from config import VECTOR_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

class DocumentProcessor:
    """
    Processes documents and creates vector embeddings.
    
    Process:
    1. Load PDF/TXT files
    2. Split into chunks
    3. Convert to embeddings (numbers)
    4. Store in FAISS (super-fast search)
    """
    
    def __init__(self):
        """Initialize the processor"""
        # OllamaEmbeddings converts text to numbers
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        
        # FAISS will store our vector database
        self.vector_store = None
        
        # TextSplitter cuts documents into manageable chunks
        self.text_splitter = CharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
        print("✅ DocumentProcessor initialized")
    
    def load_documents(self, folder_path="./data"):
        """
        Load all PDF and TXT files from a folder.
        
        Args:
            folder_path: Path to folder containing documents
            
        Returns:
            List of documents
        """
        documents = []
        
        # Create folder if doesn't exist
        Path(folder_path).mkdir(exist_ok=True)
        
        # Load all PDF files
        for pdf_file in Path(folder_path).glob("*.pdf"):
            print(f"📄 Loading PDF: {pdf_file.name}...")
            loader = PyPDFLoader(str(pdf_file))
            try:
                documents.extend(loader.load())
                print(f"   ✅ Loaded {pdf_file.name}")
            except Exception as e:
                print(f"   ❌ Error loading {pdf_file.name}: {e}")
        
        # Load all TXT files
        for txt_file in Path(folder_path).glob("*.txt"):
            print(f"📄 Loading TXT: {txt_file.name}...")
            loader = TextLoader(str(txt_file))
            try:
                documents.extend(loader.load())
                print(f"   ✅ Loaded {txt_file.name}")
            except Exception as e:
                print(f"   ❌ Error loading {txt_file.name}: {e}")
        
        print(f"\n✅ Total documents loaded: {len(documents)}\n")
        return documents
    
    def create_vector_store(self, documents):
        """
        Convert documents to embeddings and create FAISS vector store.
        
        This is where the "magic" happens:
        1. Split documents into chunks
        2. Convert chunks to embeddings (numbers)
        3. Store in FAISS for fast search
        """
        if not documents:
            print("⚠️ No documents to process!")
            return
        
        # Step 1: Split documents into chunks
        print(f"✂️ Splitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"   ✅ Created {len(chunks)} chunks")
        
        # Step 2: Show example chunk
        if chunks:
            print(f"\n📍 Example chunk:")
            print(f"   {chunks[0].page_content[:200]}...\n")
        
        # Step 3: Convert to embeddings
        print(f"🧠 Converting to embeddings...")
        print(f"   (This may take 1-2 minutes...)")
        
        try:
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            print(f"   ✅ Embeddings created!")
            
            # Step 4: Save to disk
            print(f"\n💾 Saving vector store...")
            Path(VECTOR_DB_PATH).mkdir(exist_ok=True)
            self.vector_store.save_local(VECTOR_DB_PATH)
            print(f"   ✅ Saved to {VECTOR_DB_PATH}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def load_vector_store(self):
        """
        Load existing vector store from disk.
        
        Use this after you've already processed documents once.
        """
        try:
            self.vector_store = FAISS.load_local(VECTOR_DB_PATH, self.embeddings, allow_dangerous_deserialization=True)
            print(f"✅ Vector store loaded from {VECTOR_DB_PATH}")
            return True
        except Exception as e:
            print(f"⚠️ No vector store found: {e}")
            print(f"   Please run create_vector_store() first")
            return False
    
    def search_documents(self, query, k=3):
        """
        Search for documents similar to the query.
        
        Args:
            query: Your question
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if not self.vector_store:
            if not self.load_vector_store():
                return []
        
        print(f"\n🔍 Searching for: '{query}'")
        results = self.vector_store.similarity_search(query, k=k)
        
        print(f"   Found {len(results)} similar documents\n")
        for i, result in enumerate(results, 1):
            print(f"   Result {i}:")
            print(f"   {result.page_content[:150]}...\n")
        
        return results
    
    def get_retriever(self):
        """
        Get a retriever object for LangChain.
        Used by the chatbot to find relevant documents.
        """
        if not self.vector_store:
            self.load_vector_store()
        
        return self.vector_store.as_retriever(search_kwargs={"k": 3})

# USAGE EXAMPLE
if __name__ == "__main__":
    print("Document Processor Test\n")
    
    processor = DocumentProcessor()
    
    # Step 1: Load documents
    docs = processor.load_documents("./data")
    
    # Step 2: Create vector store (one time only!)
    if docs:
        processor.create_vector_store(docs)
    
    # Step 3: Test search
    processor.load_vector_store()
    processor.search_documents("What pizzas do you have?")