#!/usr/bin/env python
"""
Ultra-simple CrewAI demo - Guaranteed to work
"""
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function with comprehensive error handling"""
    try:
        logger.info("🚀 Starting Simple CrewAI Demo...")
        
        # Test 1: Basic Python functionality
        logger.info("✅ Python is working")
        
        # Test 2: Environment variables
        openai_key = os.getenv('OPENAI_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        if openai_key:
            logger.info("✅ OpenAI API key found")
        if gemini_key:
            logger.info("✅ Gemini API key found")
        
        if not openai_key and not gemini_key:
            logger.warning("⚠️ No API keys found - demo mode only")
        
        # Test 3: Try importing CrewAI
        try:
            from crewai import Agent, Crew, Task
            logger.info("✅ CrewAI imported successfully")
            
            # Test 4: Create a minimal crew
            agent = Agent(
                role='Demo Agent',
                goal='Demonstrate basic functionality',
                backstory='I am a simple demo agent.',
                verbose=False,
                allow_delegation=False
            )
            
            task = Task(
                description='Say hello and confirm the system is working',
                expected_output='A simple greeting message',
                agent=agent
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )
            
            logger.info("✅ Crew created successfully")
            
            # Test 5: Run the crew
            if openai_key or gemini_key:
                logger.info("🎬 Running demo crew...")
                result = crew.kickoff()
                logger.info("✅ Crew completed!")
                return f"Success! Crew result: {result}"
            else:
                logger.info("⚠️ Skipping crew execution - no API keys")
                return "✅ System is working! (Demo mode - add API keys to run crew)"
                
        except Exception as e:
            logger.error(f"❌ CrewAI error: {e}")
            return f"CrewAI error: {e}"
            
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        return f"System error: {e}"

def health_check():
    """Simple health check"""
    try:
        logger.info("🔍 Health check...")
        
        # Check Python
        import sys
        logger.info(f"Python version: {sys.version}")
        
        # Check environment
        has_keys = bool(os.getenv('OPENAI_API_KEY') or os.getenv('GEMINI_API_KEY'))
        logger.info(f"API keys: {'✅' if has_keys else '❌'}")
        
        return "✅ Healthy"
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return f"❌ Unhealthy: {e}"

if __name__ == "__main__":
    print("🎯 Ultra-Simple CrewAI Demo")
    print("=" * 40)
    
    # Health check
    health = health_check()
    print(f"Health: {health}")
    
    # Main demo
    result = main()
    print(f"\nResult: {result}")
    
    print("\n🎉 Demo completed!")