from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import Weaviate
from langchain_core.documents import Document
from langchain_mcp_adapters import MCPAdapter
from app.core.config import settings
from app.services.curriculum_service import CurriculumService
from app.services.vector_service import VectorService
from app.schemas.curriculum import CurriculumCreate
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
import weaviate

class AgentService:
    def __init__(self):
        # Initialize AI provider based on configuration
        if settings.AI_PROVIDER.lower() == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.7,
                google_api_key=settings.GEMINI_API_KEY
            )
        else:
            # Default to OpenAI
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        
        self.search_tool = DuckDuckGoSearchRun()
        self.vector_service = VectorService()
        self.mcp_adapter = MCPAdapter()
        
        # Initialize tools
        self.tools = [
            self.search_tool,
            self.vector_service.search_tool,
            self.mcp_adapter.get_tool("send_email"),
            self.mcp_adapter.get_tool("send_push_notification")
        ]
    
    async def generate_curriculum(self, user_id: int, curriculum_data: CurriculumCreate, db: Session) -> Dict[str, Any]:
        """Generate a personalized curriculum using AI agent"""
        
        # Get user profile
        from app.models.user import UserProfile
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        # Create curriculum generation prompt
        prompt = ChatPromptTemplate.from_template("""
        You are an AI curriculum architect. Generate a personalized learning curriculum based on the user's profile and goals.
        
        User Profile:
        - Learning Style: {learning_style}
        - Pace: {pace}
        - Interests: {interests}
        - Goals: {goals}
        
        Curriculum Request:
        - Title: {title}
        - Description: {description}
        
        Generate a structured curriculum with:
        1. 3-5 modules with clear learning objectives
        2. 5-8 learning resources per module (mix of videos, articles, interactive content)
        3. Resources should be diverse and high-quality
        4. Consider the user's learning style and pace
        
        Return the curriculum as a JSON structure with modules and resources.
        """)
        
        # Prepare context
        context = {
            "learning_style": profile.learning_style if profile else "visual",
            "pace": profile.pace if profile else "moderate",
            "interests": profile.interests if profile else [],
            "goals": profile.goals if profile else [],
            "title": curriculum_data.title,
            "description": curriculum_data.description
        }
        
        # Generate curriculum structure
        chain = prompt | self.llm | JsonOutputParser()
        curriculum_structure = await chain.ainvoke(context)
        
        # Create curriculum in database
        curriculum_service = CurriculumService(db)
        curriculum = curriculum_service.create_curriculum(user_id, curriculum_data)
        
        # Create modules and resources
        for i, module_data in enumerate(curriculum_structure.get("modules", [])):
            module = curriculum_service.create_module(
                curriculum_id=curriculum.id,
                title=module_data["title"],
                description=module_data.get("description", ""),
                order=i
            )
            
            # Create resources for this module
            for j, resource_data in enumerate(module_data.get("resources", [])):
                curriculum_service.create_resource(
                    module_id=module.id,
                    title=resource_data["title"],
                    url=resource_data["url"],
                    resource_type=resource_data["type"],
                    description=resource_data.get("description", ""),
                    order=j
                )
        
        return curriculum
    
    async def chat(self, user_id: int, message: str, curriculum_id: int = None, db: Session = None) -> str:
        """Chat with the AI agent"""
        
        # Create chat prompt
        prompt = ChatPromptTemplate.from_template("""
        You are an AI learning companion. Help the user with their learning journey.
        
        User Message: {message}
        
        If the user is asking about their curriculum or progress, provide helpful guidance.
        If they need additional resources, suggest relevant materials.
        If they have questions about their learning path, provide personalized advice.
        
        Be encouraging, helpful, and personalized in your response.
        """)
        
        # Get user context if database is available
        context = {"message": message}
        if db:
            from app.models.user import UserProfile
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if profile:
                context["learning_style"] = profile.learning_style
                context["pace"] = profile.pace
                context["interests"] = profile.interests
                context["goals"] = profile.goals
        
        # Generate response
        chain = prompt | self.llm
        response = await chain.ainvoke(context)
        
        return response.content
    
    async def search_resources(self, query: str) -> List[Dict[str, Any]]:
        """Search for learning resources using web search and vector search"""
        
        # Web search
        web_results = self.search_tool.run(query)
        
        # Vector search
        vector_results = await self.vector_service.search(query)
        
        # Combine and format results
        results = []
        
        # Add web search results
        if web_results:
            results.append({
                "source": "web_search",
                "content": web_results[:500],  # Limit length
                "relevance": 0.8
            })
        
        # Add vector search results
        for doc in vector_results:
            results.append({
                "source": "vector_search",
                "content": doc.page_content,
                "relevance": doc.metadata.get("score", 0.7)
            })
        
        return results
    
    async def send_progress_email(self, user_id: int, user_email: str) -> bool:
        """Send weekly progress digest email"""
        try:
            # Get progress summary
            if db:
                progress_service = ProgressService(db)
                summary = progress_service.get_progress_summary(user_id)
                
                # Generate email content
                email_content = f"""
                Weekly Learning Progress Digest
                
                Hello! Here's your learning progress summary:
                
                - Total Resources: {summary['total_resources']}
                - Completed: {summary['completed_resources']}
                - In Progress: {summary['in_progress_resources']}
                - Completion Rate: {summary['completion_percentage']}%
                
                Keep up the great work! Continue with your learning journey.
                """
                
                # Send email using MCP adapter
                await self.mcp_adapter.send_email(
                    to_email=user_email,
                    subject="Weekly Learning Progress",
                    content=email_content
                )
                
                return True
        except Exception as e:
            print(f"Failed to send progress email: {e}")
            return False
    
    async def send_daily_notification(self, user_id: int) -> bool:
        """Send daily learning prompt notification"""
        try:
            # Generate daily learning prompt
            prompt = ChatPromptTemplate.from_template("""
            Generate a daily learning prompt or vocabulary word that would be relevant for a learner.
            Make it encouraging and educational. Keep it short and engaging.
            """)
            
            chain = prompt | self.llm
            response = await chain.ainvoke({})
            
            # Send push notification using MCP adapter
            await self.mcp_adapter.send_push_notification(
                user_id=user_id,
                title="Daily Learning Prompt",
                message=response.content
            )
            
            return True
        except Exception as e:
            print(f"Failed to send daily notification: {e}")
            return False 