"""
The main chatbot agent.
This combines documents, database, and AI to answer questions.
"""

from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.agents import Tool, initialize_agent, AgentType

from document_processor import DocumentProcessor
from database import DatabaseConnector
from config import LLM_MODEL

class ChatbotAgent:
    """
    The main chatbot.
    
    It can:
    - Answer questions from documents (RAG)
    - Query the database for real-time data
    - Combine both to give smart answers
    """
    
    def __init__(self):
        """Initialize the agent"""
        print("🚀 Initializing ChatBot...\n")
        
        # Initialize AI model
        print("Loading AI model (Ollama)...")
        self.llm = Ollama(model=LLM_MODEL, temperature=0.7)
        print(f"   ✅ Loaded {LLM_MODEL}\n")
        
        # Initialize document processor
        print("Loading document processor...")
        self.doc_processor = DocumentProcessor()
        print()
        
        # Initialize database
        print("Connecting to database...")
        self.db = DatabaseConnector()
        print()
        
        # Load vector store
        if not self.doc_processor.load_vector_store():
            print("⚠️ Warning: Vector store not found")
            print("   Run: python document_processor.py")
            print("   to process documents first\n")
        
        # Create the QA chain
        print("Creating QA chain...")
        self.qa_chain = self._create_qa_chain()
        print("   ✅ QA chain ready\n")
        
        # Create tools
        print("Creating agent tools...")
        self.tools = self._create_tools()
        print(f"   ✅ Created {len(self.tools)} tools\n")
        
        # Create the agent
        print("Initializing agent...")
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=5
        )
        print("✅ ChatBot Ready!\n")
    
    def _create_qa_chain(self):
        """
        Create a retrieval-based QA chain.
        
        This chain:
        1. Takes your question
        2. Finds relevant documents
        3. Sends to AI with documents as context
        """
        template = """You are a helpful restaurant assistant.
Use the following context to answer questions accurately.
If you don't know, say so honestly.

Context from documents:
{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.doc_processor.get_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa_chain
    
    def _create_tools(self):
        """
        Create tools that the agent can use.
        
        Tools are like "super powers" the agent can use to answer questions.
        """
        
        # Tool 1: Search Documents
        def search_documents(query):
            """Search through documents"""
            try:
                return self.qa_chain.run(query)
            except Exception as e:
                return f"Error: {e}"
        
        doc_tool = Tool(
            name="DocumentSearch",
            func=search_documents,
            description="Search through restaurant documents (menu, policies). Use for questions about offerings, policies, hours."
        )
        
        # Tool 2: Query Database
        def query_database(question):
            """Use natural language to query database"""
            
            # Simple logic to convert questions to SQL queries
            question_lower = question.lower()
            
            if "available" in question_lower or "stock" in question_lower:
                results = self.db.query(
                    "SELECT name, quantity FROM menu_items WHERE quantity > 0"
                )
                return self._format_results(results)
            
            elif "price" in question_lower:
                results = self.db.query(
                    "SELECT name, price FROM menu_items"
                )
                return self._format_results(results)
            
            elif "order" in question_lower:
                results = self.db.query(
                    "SELECT customer_name, items, total_price FROM orders ORDER BY created_at DESC LIMIT 5"
                )
                return self._format_results(results)
            
            else:
                return "Database query: Ask about available items, prices, or recent orders."
        
        db_tool = Tool(
            name="DatabaseQuery",
            func=query_database,
            description="Query live inventory, prices, and orders. Use for current stock, pricing, or order status."
        )
        
        return [doc_tool, db_tool]
    
    def _format_results(self, results):
        """Format database results nicely"""
        if not results:
            return "No results found."
        
        formatted = "Results:\n"
        for row in results:
            formatted += f"  • {row}\n"
        
        return formatted
    
    def chat(self, user_question):
        """
        Process a user question and return answer.
        
        Args:
            user_question: What the user asks
            
        Returns:
            The AI's answer
        """
        try:
            response = self.agent.run(user_question)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def close(self):
        """Clean up connections"""
        self.db.close()

# TEST IT!
if __name__ == "__main__":
    agent = ChatbotAgent()
    
    # Test questions
    test_questions = [
        "What pizzas do you have?",
        "How many pepperoni pizzas are available?",
        "What's the price of margherita?",
    ]
    
    print("\n" + "="*60)
    print("TESTING AGENT WITH SAMPLE QUESTIONS")
    print("="*60 + "\n")
    
    for question in test_questions:
        print(f"\n📝 User: {question}")
        answer = agent.chat(question)
        print(f"\n🤖 Assistant: {answer}\n")
        print("-" * 60)
    
    agent.close()