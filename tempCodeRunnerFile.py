# Test that all imports work
try:
    import langchain
    print("✅ langchain imported")
    
    import ollama
    print("✅ ollama imported")
    
    import faiss
    print("✅ faiss imported")
    
    import streamlit as st
    print("✅ streamlit imported")
    
    import mysql.connector
    print("✅ mysql.connector imported")
    
    print("\n✅ ALL IMPORTS SUCCESSFUL!")
    
except ImportError as e:
    print(f"❌ Error: {e}")