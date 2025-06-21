import os
import argparse
from datetime import datetime

# Import our agent classes
from agents.outline_agent import OutlineAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent
from agents.image_agent import ImageAgent

class ContentTeam:
    def __init__(self):
        """
        Initializes the multi-agent content creation team.
        """
        print("Initializing the AI Content Team...")
        self.outline_agent = OutlineAgent()
        self.writer_agent = WriterAgent()
        self.reviewer_agent = ReviewerAgent()
        self.image_agent = ImageAgent()
        print("All agents have been initialized.")

    def run(self, topic: str):
        """
        Executes the full content creation workflow.
        
        Args:
            topic (str): The main topic for the blog post.
        
        Returns:
            str: The full content of the final markdown article.
        """
        # Step 1: Generate the outline
        outline = self.outline_agent.run(topic)
        if not outline:
            message = "Halting process: Could not generate an outline."
            print(message)
            return message

        print("\n--- Step 1: Outline Generated ---")
        for item in outline:
            print(f"- {item}")
        print("---------------------------------\n")

        # Step 2: Write content for each section in the outline
        draft_sections = []
        for section_topic in outline:
            section_content = self.writer_agent.run(section_topic)
            draft_sections.append(section_content)
        
        full_draft = "\n\n".join(draft_sections)
        print("\n--- Step 2: Full Draft Written ---")
        print(full_draft[:500] + "...") # Print a preview
        print("----------------------------------\n")

        # Step 3: Review and polish the full draft
        polished_text = self.reviewer_agent.run(full_draft)
        print("\n--- Step 3: Draft Polished ---")
        print(polished_text[:500] + "...") # Print a preview
        print("------------------------------\n")
        
        # Step 4: Generate a cover image
        image_topic = f"{topic}, digital art style"
        image_url = self.image_agent.run(image_topic)
        print("\n--- Step 4: Cover Image Generated ---")
        print(f"Image URL: {image_url}")
        print("-------------------------------------\n")

        # Step 5: Combine everything and save the final article
        final_article = self.save_article(topic, polished_text, image_url)
        
        return final_article

    def save_article(self, topic: str, content: str, image_url: str):
        """
        Saves the final article as a markdown file and returns its content.
        """
        safe_topic = "".join(x for x in topic if x.isalnum() or x in " -").rstrip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/{safe_topic.replace(' ', '_')}_{timestamp}.md"

        os.makedirs("outputs", exist_ok=True)
        
        final_content = f"# {topic.title()}\n\n"
        if image_url:
            final_content += f"![{topic}]({image_url})\n\n"
        final_content += content

        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        print(f"✅ Success! Your article has been saved to: {filename}")
        return final_content

# The main block now only runs for direct CLI execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the AI Content Creation Team CLI.")
    parser.add_argument("--topic", type=str, required=True, help="The topic for the blog post.")
    args = parser.parse_args()

    team = ContentTeam()
    team.run(args.topic)
