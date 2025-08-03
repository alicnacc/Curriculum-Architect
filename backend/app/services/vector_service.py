import weaviate
from langchain_community.vectorstores import Weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.tools import tool
from app.core.config import settings
from typing import List, Dict, Any
import json

class VectorService:
    def __init__(self):
        self.client = weaviate.Client(settings.WEAVIATE_URL)
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self.vectorstore = Weaviate(
            client=self.client,
            index_name="LearningResource",
            text_key="content",
            embedding=self.embeddings
        )
        
        # Initialize the schema if it doesn't exist
        self._init_schema()
    
    def _init_schema(self):
        """Initialize Weaviate schema for learning resources"""
        schema = {
            "class": "LearningResource",
            "properties": [
                {
                    "name": "title",
                    "dataType": ["text"],
                    "description": "Title of the learning resource"
                },
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "Content or description of the learning resource"
                },
                {
                    "name": "url",
                    "dataType": ["text"],
                    "description": "URL of the learning resource"
                },
                {
                    "name": "resource_type",
                    "dataType": ["text"],
                    "description": "Type of resource (video, article, interactive, etc.)"
                },
                {
                    "name": "tags",
                    "dataType": ["text[]"],
                    "description": "Tags for categorizing the resource"
                },
                {
                    "name": "difficulty",
                    "dataType": ["text"],
                    "description": "Difficulty level (beginner, intermediate, advanced)"
                }
            ],
            "vectorizer": "text2vec-openai"
        }
        
        try:
            self.client.schema.create_class(schema)
        except Exception:
            # Schema might already exist
            pass
    
    async def add_resource(self, title: str, content: str, url: str, resource_type: str, tags: List[str] = None, difficulty: str = "intermediate") -> bool:
        """Add a learning resource to the vector database"""
        try:
            doc = Document(
                page_content=content,
                metadata={
                    "title": title,
                    "url": url,
                    "resource_type": resource_type,
                    "tags": tags or [],
                    "difficulty": difficulty
                }
            )
            
            self.vectorstore.add_documents([doc])
            return True
        except Exception as e:
            print(f"Failed to add resource to vector database: {e}")
            return False
    
    async def search(self, query: str, limit: int = 5) -> List[Document]:
        """Search for learning resources using semantic search"""
        try:
            results = self.vectorstore.similarity_search(query, k=limit)
            return results
        except Exception as e:
            print(f"Failed to search vector database: {e}")
            return []
    
    @tool
    def search_learning_resources(self, query: str) -> str:
        """Search for learning resources using semantic search"""
        results = self.vectorstore.similarity_search(query, k=3)
        
        if not results:
            return "No relevant learning resources found."
        
        formatted_results = []
        for i, doc in enumerate(results, 1):
            formatted_results.append(f"{i}. {doc.metadata.get('title', 'Untitled')}")
            formatted_results.append(f"   Type: {doc.metadata.get('resource_type', 'Unknown')}")
            formatted_results.append(f"   URL: {doc.metadata.get('url', 'No URL')}")
            formatted_results.append(f"   Content: {doc.page_content[:200]}...")
            formatted_results.append("")
        
        return "\n".join(formatted_results)
    
    async def get_recommendations(self, user_interests: List[str], learning_style: str = "visual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get personalized learning resource recommendations"""
        try:
            # Create a query based on user interests and learning style
            query = f"learning resources about {' '.join(user_interests)} for {learning_style} learners"
            
            results = await self.search(query, limit)
            
            recommendations = []
            for doc in results:
                recommendations.append({
                    "title": doc.metadata.get("title", "Untitled"),
                    "url": doc.metadata.get("url", ""),
                    "resource_type": doc.metadata.get("resource_type", "unknown"),
                    "content": doc.page_content[:300],
                    "tags": doc.metadata.get("tags", []),
                    "difficulty": doc.metadata.get("difficulty", "intermediate")
                })
            
            return recommendations
        except Exception as e:
            print(f"Failed to get recommendations: {e}")
            return []
    
    async def index_existing_resources(self, resources: List[Dict[str, Any]]) -> bool:
        """Index existing learning resources from the database"""
        try:
            documents = []
            for resource in resources:
                doc = Document(
                    page_content=resource.get("description", "") or resource.get("title", ""),
                    metadata={
                        "title": resource.get("title", ""),
                        "url": resource.get("url", ""),
                        "resource_type": resource.get("resource_type", ""),
                        "tags": resource.get("tags", []),
                        "difficulty": resource.get("difficulty", "intermediate")
                    }
                )
                documents.append(doc)
            
            if documents:
                self.vectorstore.add_documents(documents)
            
            return True
        except Exception as e:
            print(f"Failed to index existing resources: {e}")
            return False 