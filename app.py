import gradio as gr
from main import ContentTeam
import time

# Initialize our ContentTeam once when the app starts
print("Starting the AI Content Team application...")
content_team = ContentTeam()
print("Application ready.")

def generate_article(topic):
    """
    The main function that Gradio will call. 
    It takes a topic, runs the agent team, and returns the result.
    This is a generator function to provide real-time UI updates.
    """
    if not topic:
        yield "Please provide a topic."
        return

    # Immediately yield a status update to the user.
    yield "🤖 Agents are assembling... Generating outline."
    
    # Run the content creation process
    # This will print detailed progress to the console
    final_article_md = content_team.run(topic)
    
    # Yield the final result to the UI
    yield final_article_md

# Define the Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 AI-Powered Content Creation Team")
    gr.Markdown("Enter a topic below and the multi-agent team will write a complete blog post with a cover image.")
    
    with gr.Row():
        topic_input = gr.Textbox(
            label="Blog Post Topic", 
            placeholder="e.g., The Future of Renewable Energy"
        )
    
    submit_button = gr.Button("Generate Article", variant="primary")
    
    output_markdown = gr.Markdown(label="Generated Article")

    # Define the button's click behavior
    # Gradio automatically handles generator functions for streaming output.
    submit_button.click(
        fn=generate_article, 
        inputs=topic_input, 
        outputs=output_markdown
    )

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
