import sys
import os
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent.agents import Assistant
from config import get_llm_config

class OutlineAgent:
    def __init__(self):
        """
        Initializes the OutlineAgent.
        This agent is responsible for creating a blog post outline.
        """
        # Define the persona and instructions for the agent
        system_prompt = (
            "You are a senior content strategist. Your task is to take a given topic and "
            "create a comprehensive, well-structured blog post outline. "
            "The outline should include an introduction, 3-5 main body sections with sub-points, and a conclusion. "
            "Output the result as a JSON object with a single key 'outline' which contains a list of strings."
        )

        # Get the LLM configuration from our central config file
        llm_config = get_llm_config()

        # Initialize the Assistant agent from the qwen-agent library
        self.agent = Assistant(
            llm=llm_config,
            system_message=system_prompt
        )

    def run(self, topic: str):
        """
        Runs the agent to generate an outline for the given topic.

        Args:
            topic (str): The topic for the blog post.

        Returns:
            list: A list of strings representing the blog post outline, or None if an error occurs.
        """
        print(f"OutlineAgent: Generating outline for topic: '{topic}'")
        
        # We will structure the user message to be clear and direct
        messages = [{"role": "user", "content": f"Generate a blog post outline for the topic: {topic}"}]
        
        # The agent's run method returns a generator, so we iterate through it
        response = []
        for res in self.agent.run(messages=messages):
            response.extend(res)

        # The final response from the agent should contain the outline
        if response and isinstance(response[-1], dict) and 'content' in response[-1]:
            try:
                # The LLM should return a JSON string, which we parse
                content_str = response[-1]['content']
                json_start = content_str.find('{')
                json_end = content_str.rfind('}') + 1
                json_str = content_str[json_start:json_end]
                
                outline_data = json.loads(json_str)
                print("OutlineAgent: Successfully generated and parsed the outline.")
                return outline_data.get("outline", [])
            except json.JSONDecodeError as e:
                print(f"Error: Could not decode JSON from the agent's response. Error: {e}")
                print(f"Raw response content: {response[-1]['content']}")
                return None
        
        print("Error: The agent did not return the expected outline format.")
        return None

# This block allows us to test the agent directly
if __name__ == '__main__':
    # Create an instance of our agent
    outline_creator = OutlineAgent()

    # Define a sample topic for testing
    sample_topic = "The Impact of AI on Software Development"

    # Run the agent
    generated_outline = outline_creator.run(sample_topic)

    # Print the result
    if generated_outline:
        print("\n--- Generated Outline ---")
        for item in generated_outline:
            print(f"- {item}")
        print("-------------------------\n")
    else:
        print("Failed to generate an outline.")

