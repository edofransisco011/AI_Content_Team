import sys
import os
import re

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent.agents import Assistant
from qwen_agent.tools import ImageGen
from config import get_llm_config, configure_environment

class ImageAgent:
    def __init__(self):
        """
        Initializes the ImageAgent.
        This agent is responsible for creating a cover image for the blog post.
        """
        # Load environment variables from .env file
        configure_environment()

        # Define the persona and instructions for the agent
        system_prompt = (
            "You are a creative visual designer. Your sole task is to use your 'image_gen' "
            "tool to create a visually appealing and relevant blog post cover image based on the user's topic. "
            "The style should be photorealistic and professional. "
            "Directly output the markdown string for the generated image."
        )

        # Get the LLM configuration
        llm_config = get_llm_config()

        # THE FIX: Initialize ImageGen without arguments. It automatically finds the
        # DASHSCOPE_API_KEY from the environment, which we loaded above.
        tools = [ImageGen()]

        # Initialize the Assistant agent
        self.agent = Assistant(
            llm=llm_config,
            system_message=system_prompt,
            function_list=tools
        )

    def run(self, topic: str):
        """
        Runs the agent to generate an image for the given topic.

        Args:
            topic (str): The topic for the blog post.

        Returns:
            str: The URL of the generated image, or None if an error occurs.
        """
        print(f"\nImageAgent: Generating image for topic: '{topic}'")
        
        # We explicitly ask the agent to generate the image
        messages = [{"role": "user", "content": f"Generate a blog post cover image about: {topic}"}]
        
        response = []
        for res in self.agent.run(messages=messages):
            response.extend(res)

        # The tool returns the image as a markdown string.
        if response and isinstance(response[-1], dict) and 'content' in response[-1]:
            markdown_image = response[-1]['content']
            print("ImageAgent: Successfully received response from agent.")
            
            # We will parse the URL from the markdown for cleaner use later
            match = re.search(r'\((.*?)\)', markdown_image)
            if match:
                image_url = match.group(1)
                print("ImageAgent: Parsed image URL successfully.")
                return image_url
            
            # Fallback in case the output format changes
            return markdown_image
        
        print("Error: The ImageAgent did not return the expected image format.")
        return None

# This block allows us to test the agent directly
if __name__ == '__main__':
    # Create an instance of our agent
    image_creator = ImageAgent()

    # Define a sample topic, adding a style hint helps
    sample_topic = "The impact of AI on software development, digital art style"

    # Run the agent
    generated_image_url = image_creator.run(sample_topic)

    # Print the result
    if generated_image_url:
        print("\n--- Generated Image URL ---")
        print(generated_image_url)
        print("---------------------------\n")
    else:
        print("Failed to generate an image.")
