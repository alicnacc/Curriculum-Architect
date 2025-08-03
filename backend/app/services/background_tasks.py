import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.agent_service import AgentService
from app.models.user import User
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class BackgroundTaskService:
    def __init__(self):
        self.agent_service = AgentService()
        self.running = False
    
    async def start_background_tasks(self):
        """Start background tasks for email and push notifications"""
        if not settings.ENABLE_BACKGROUND_TASKS:
            logger.info("Background tasks disabled")
            return
        
        self.running = True
        
        # Start tasks in separate coroutines
        asyncio.create_task(self._weekly_email_task())
        asyncio.create_task(self._daily_notification_task())
        
        logger.info("Background tasks started")
    
    async def stop_background_tasks(self):
        """Stop background tasks"""
        self.running = False
        logger.info("Background tasks stopped")
    
    async def _weekly_email_task(self):
        """Send weekly progress digest emails"""
        while self.running:
            try:
                # Check if it's time to send weekly emails (every Sunday at 9 AM)
                now = datetime.now()
                if now.weekday() == 6 and now.hour == 9:  # Sunday at 9 AM
                    await self._send_weekly_emails()
                
                # Wait for 1 hour before checking again
                await asyncio.sleep(3600)
            except Exception as e:
                logger.error(f"Error in weekly email task: {e}")
                await asyncio.sleep(3600)
    
    async def _daily_notification_task(self):
        """Send daily learning prompt notifications"""
        while self.running:
            try:
                # Check if it's time to send daily notifications (every day at 8 AM)
                now = datetime.now()
                if now.hour == 8 and now.minute == 0:
                    await self._send_daily_notifications()
                
                # Wait for 1 minute before checking again
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Error in daily notification task: {e}")
                await asyncio.sleep(60)
    
    async def _send_weekly_emails(self):
        """Send weekly progress digest emails to all users"""
        db = SessionLocal()
        try:
            users = db.query(User).all()
            
            for user in users:
                try:
                    success = await self.agent_service.send_progress_email(
                        user_id=user.id,
                        user_email=user.email
                    )
                    
                    if success:
                        logger.info(f"Sent weekly email to {user.email}")
                    else:
                        logger.warning(f"Failed to send weekly email to {user.email}")
                        
                except Exception as e:
                    logger.error(f"Error sending weekly email to {user.email}: {e}")
                    
        except Exception as e:
            logger.error(f"Error in weekly email batch: {e}")
        finally:
            db.close()
    
    async def _send_daily_notifications(self):
        """Send daily learning prompt notifications to all users"""
        db = SessionLocal()
        try:
            users = db.query(User).all()
            
            for user in users:
                try:
                    success = await self.agent_service.send_daily_notification(
                        user_id=user.id
                    )
                    
                    if success:
                        logger.info(f"Sent daily notification to user {user.id}")
                    else:
                        logger.warning(f"Failed to send daily notification to user {user.id}")
                        
                except Exception as e:
                    logger.error(f"Error sending daily notification to user {user.id}: {e}")
                    
        except Exception as e:
            logger.error(f"Error in daily notification batch: {e}")
        finally:
            db.close()

# Global background task service instance
background_task_service = BackgroundTaskService()

async def start_background_tasks():
    """Start background tasks"""
    await background_task_service.start_background_tasks()

async def stop_background_tasks():
    """Stop background tasks"""
    await background_task_service.stop_background_tasks() 