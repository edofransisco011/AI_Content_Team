import sys
import os
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent.agents import Assistant
# Import our new custom tool instead of the old one
from tools.tavily_search import TavilySearchTool
from config import get_llm_config, configure_environment

class WriterAgent:
    def __init__(self):
        """
        Initializes the WriterAgent with our custom Tavily search tool.
        """
        # Load environment variables from .env file.
        configure_environment()

        # Define the persona and instructions for the agent
        system_prompt = (
            "You are an expert blog writer. You will be given a specific topic for a section of a blog post. "
            "Your task is to use your 'tavily_search' tool to gather relevant, up-to-date information. "
            "Then, write a detailed, engaging, and informative paragraph of 150-200 words for that section. "
            "Cite your sources by including a markdown link to the URL you used. "
            "Directly output the final written text without any introductory phrases like 'Here is the paragraph'."
        )

        # Get LLM config and initialize our new tool.
        llm_config = get_llm_config()
        tools = [TavilySearchTool()]

        # Initialize the Assistant agent with our custom tool
        self.agent = Assistant(
            llm=llm_config,
            system_message=system_prompt,
            function_list=tools
        )

    def run(self, section_topic: str):
        """
        Runs the agent to write content for the given section topic.
        """
        print(f"\nWriterAgent: Writing content for section: '{section_topic}'")
        
        messages = [{
            "role": "user", 
            "content": f"Please use your search tool to write the content for the blog post section: '{section_topic}'"
        }]
        
        response = []
        for res in self.agent.run(messages=messages):
            response.extend(res)

        if response and isinstance(response[-1], dict) and 'content' in response[-1]:
            content = response[-1]['content']
            print(f"WriterAgent: Successfully generated content for section.")
            return content
        
        print("Error: The WriterAgent did not return the expected text format.")
        return "Error: Could not generate content for this section."

# This block allows us to test the agent directly
if __name__ == '__main__':
    content_writer = WriterAgent()
    sample_section = "Section 2: Enhanced Code Quality and Debugging"
    generated_content = content_writer.run(sample_section)

    print("\n--- Generated Content ---")
    print(generated_content)
    print("-------------------------\n")
