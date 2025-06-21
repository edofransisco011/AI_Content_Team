import gradio as gr
from main import ContentTeam

# Initialize our ContentTeam once when the app starts
print("Starting the AI Content Team application...")
content_team = ContentTeam()
print("Application ready.")

def generate_article(topic):
    """
    The main function that Gradio will call. 
    It takes a topic, runs the agent team, and returns the result.
    """
    if not topic:
        return "Please provide a topic."
    
    # Run the content creation process
    # This will print progress to the console and return the final markdown
    final_article_md = content_team.run(topic)
    
    return final_article_md

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
    submit_button.click(
        fn=generate_article, 
        inputs=topic_input, 
        outputs=output_markdown
    )

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
