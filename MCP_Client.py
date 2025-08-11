#!/usr/bin/env python3
"""
Simple RAG Test Client
Directly tests the RAG functionality without MCP complexity
"""

import sys
import os
from utils.rag import EmbRag


def test_rag_directly():
    """Test RAG functionality directly"""
    print("🧪 Testing RAG functionality directly...")
    
    try:
        # Check if required directories exist
        docs_path = "/home/chandrahaas/codes/Bot/DOCS"
        faiss_path = "/home/chandrahaas/codes/Bot/Faiss"
        
        if not os.path.exists(docs_path):
            print(f"❌ DOCS directory not found: {docs_path}")
            return False
            
        if not os.path.exists(faiss_path):
            print(f"❌ FAISS directory not found: {faiss_path}")
            return False
        
        print(f"✅ DOCS directory: {docs_path}")
        print(f"✅ FAISS directory: {faiss_path}")
        
        # Initialize RAG
        print("\n🚀 Initializing RAG system...")
        rag = EmbRag(docs_path=docs_path, faiss_path=faiss_path)
        print("✅ RAG system initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG initialization failed: {str(e)}")
        return False


def run_search_queries():
    """Run example search queries"""
    print("\n🔍 Running example search queries...")
    
    docs_path = "/home/chandrahaas/codes/Bot/DOCS"
    faiss_path = "/home/chandrahaas/codes/Bot/Faiss"
    
    # Initialize RAG
    rag = EmbRag(docs_path=docs_path, faiss_path=faiss_path)
    
    # Example queries
    example_queries = [
        "Who is the POC for insurance?",
        "How to mark attendance?",
        "What is the payroll cut-off date?",
        "How to apply for leave?",
        "What is the mCAS system?"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n--- Query {i}/{len(example_queries)} ---")
        print(f"🔍 Question: {query}")
        
        try:
            answer = rag.queryDB(query)
            print("✅ Answer received:")
            print(f"📄 {answer}")
        except Exception as e:
            print(f"❌ Query failed: {str(e)}")


def test_mcp_server_file():
    """Test if the MCP server file can be imported"""
    print("\n🧪 Testing MCP server file...")
    
    try:
        # Check if RAG_MCP.py exists
        if not os.path.exists("RAG_MCP.py"):
            print("❌ RAG_MCP.py not found")
            return False
        
        # Try to import it
        import importlib.util
        spec = importlib.util.spec_from_file_location("rag_mcp", "RAG_MCP.py")
        rag_mcp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rag_mcp)
        
        print("✅ RAG_MCP.py can be imported successfully")
        print(f"📋 Server name: {rag_mcp.mcp.name}")
        
        # Check if the tool exists
        if hasattr(rag_mcp, 'search_docs'):
            print("✅ search_docs tool found")
        else:
            print("⚠️  search_docs tool not found")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server file test failed: {str(e)}")
        return False


def main():
    """Main function to test RAG functionality"""
    print("🚀 Starting RAG Test Client")
    print("=" * 50)
    
    # Test RAG directly
    if not test_rag_directly():
        print("❌ RAG test failed, exiting")
        sys.exit(1)
    
    # Test MCP server file
    test_mcp_server_file()
    
    # Run search queries
    try:
        run_search_queries()
    except Exception as e:
        print(f"❌ Search queries failed: {str(e)}")
        print("💡 This might be due to missing dependencies or configuration issues")
    
    print("\n👋 RAG Test Client finished")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Client stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("💡 Check your environment and dependencies")
