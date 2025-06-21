import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qwen_agent.agents import Assistant
from config import get_llm_config

class ReviewerAgent:
    def __init__(self):
        """
        Initializes the ReviewerAgent.
        This agent is responsible for reviewing and polishing a draft.
        """
        # Define the persona and instructions for the agent
        system_prompt = (
            "You are a meticulous and professional editor. You will receive a draft of a blog post. "
            "Your job is to review it for clarity, grammar, tone, and flow. "
            "If you find awkward phrasing or areas for improvement, you must rewrite them to be more professional, engaging, and clear. "
            "Do not add any new information. Your only focus is improving the quality of the existing text. "
            "Provide only the final, polished version of the full text as your response."
        )

        # Get the LLM configuration
        llm_config = get_llm_config()

        # Initialize the Assistant agent. This agent does not need any tools.
        self.agent = Assistant(
            llm=llm_config,
            system_message=system_prompt
        )

    def run(self, draft_content: str):
        """
        Runs the agent to review and polish the given draft content.

        Args:
            draft_content (str): The draft text of the blog post.

        Returns:
            str: The polished, final version of the text.
        """
        print("\nReviewerAgent: Polishing the draft...")
        
        messages = [{"role": "user", "content": draft_content}]
        
        response = []
        for res in self.agent.run(messages=messages):
            response.extend(res)

        # The final text is in the 'content' of the last message
        if response and isinstance(response[-1], dict) and 'content' in response[-1]:
            polished_content = response[-1]['content']
            print("ReviewerAgent: Draft has been successfully polished.")
            return polished_content
        
        print("Error: The ReviewerAgent did not return the expected text format.")
        return "Error: Could not review the content."

# This block allows us to test the agent directly
if __name__ == '__main__':
    # Create an instance of our agent
    reviewer = ReviewerAgent()

    # Create a sample draft with some deliberate awkwardness for testing
    sample_draft = (
        "Enhancing code quality debugging is super important for apps. "
        "Devs use tools for this. Tools like Refact.ai have AI code reviews [1]. "
        "These things find problems. Also static code analysis like Klocwork is good for security [3]. "
        "Using AI dev tools means better code quality. It automates stuff so people make less mistakes [2]."
    )

    # Run the agent
    polished_text = reviewer.run(sample_draft)

    # Print the results
    print("\n--- Original Draft ---")
    print(sample_draft)
    print("\n--- Polished Text ---")
    print(polished_text)
    print("---------------------\n")
