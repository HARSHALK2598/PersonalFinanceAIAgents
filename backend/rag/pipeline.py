from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import os
from .knowledge_base import FinancialKnowledgeBase

class RAGPipeline:
    def __init__(self):
        # Initialize the embedding model (using a smaller open-source model)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory="./data/chroma",
            anonymized_telemetry=False
        ))
        
        # Initialize the LLM (using a smaller open-source model)
        self.llm = HuggingFaceHub(
            repo_id="google/flan-t5-small",
            model_kwargs={"temperature": 0.7, "max_length": 512}
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="financial_advice",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""Based on the following financial advice context:
            {context}
            
            Please provide a detailed financial plan for this goal: {question}
            
            Structure your response as follows:
            1. Main goal
            2. Specific steps to achieve this goal
            3. Timeline
            4. Estimated costs
            5. Potential risks
            6. Recommendations
            
            Response:"""
        )
        
        # Initialize with comprehensive financial advice
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with comprehensive financial advice."""
        initial_advice = FinancialKnowledgeBase.get_initial_advice()
        
        # Add initial advice to the collection
        self.collection.add(
            documents=[item["text"] for item in initial_advice],
            metadatas=[item["metadata"] for item in initial_advice],
            ids=[f"doc_{i}" for i in range(len(initial_advice))]
        )
    
    def add_advice(self, text: str, topic: str, category: str) -> bool:
        """Add new financial advice to the knowledge base."""
        try:
            # Get the current number of documents
            count = self.collection.count()
            
            # Add the new advice
            self.collection.add(
                documents=[text],
                metadatas=[{"topic": topic, "category": category}],
                ids=[f"doc_{count}"]
            )
            return True
        except Exception as e:
            print(f"Error adding advice: {str(e)}")
            return False
    
    def get_advice_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retrieve advice by category."""
        try:
            results = self.collection.query(
                query_texts=[""],
                where={"category": category},
                n_results=10
            )
            return [
                {"text": doc, "metadata": meta}
                for doc, meta in zip(results['documents'][0], results['metadatas'][0])
            ]
        except Exception as e:
            print(f"Error retrieving advice by category: {str(e)}")
            return []
    
    def get_advice_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Retrieve advice by topic."""
        try:
            results = self.collection.query(
                query_texts=[""],
                where={"topic": topic},
                n_results=10
            )
            return [
                {"text": doc, "metadata": meta}
                for doc, meta in zip(results['documents'][0], results['metadatas'][0])
            ]
        except Exception as e:
            print(f"Error retrieving advice by topic: {str(e)}")
            return []
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        try:
            # Get relevant context from the knowledge base
            results = self.collection.query(
                query_texts=[query],
                n_results=3
            )
            
            # Combine relevant context
            context = "\n".join(results['documents'][0])
            
            # Generate the prompt
            prompt = self.prompt_template.format(
                context=context,
                question=query
            )
            
            # Generate response using the LLM
            response = self.llm(prompt)
            
            # Parse the response into structured data
            sections = response.split("\n")
            plan = {
                "goal": sections[0] if len(sections) > 0 else "",
                "steps": [s.strip() for s in sections[1].split(".") if s.strip()] if len(sections) > 1 else [],
                "timeline": sections[2] if len(sections) > 2 else "",
                "estimated_cost": sections[3] if len(sections) > 3 else "",
                "risks": [s.strip() for s in sections[4].split(".") if s.strip()] if len(sections) > 4 else [],
                "recommendations": [s.strip() for s in sections[5].split(".") if s.strip()] if len(sections) > 5 else []
            }
            
            # Add metadata about the advice used
            plan["metadata"] = {
                "topics_used": [meta["topic"] for meta in results['metadatas'][0]],
                "categories_used": [meta["category"] for meta in results['metadatas'][0]]
            }
            
            return {
                "success": True,
                "message": "Financial plan generated successfully",
                "data": plan
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to generate financial plan",
                "error": str(e)
            } 