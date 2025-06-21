import os
from dotenv import load_dotenv

def configure_environment():
    """
    Loads environment variables from a .env file and sets them
    in the environment. This is a best practice for managing secrets
    like API keys.
    """
    # Load environment variables from .env file
    load_dotenv()

    # You can add other configurations here later if needed
    # For example, setting up model names or other constants.
    
    print("Environment configured.")

def get_llm_config():
    """
    Prepares the LLM configuration dictionary for the Qwen-Agent.
    It fetches the API key from the environment variables.
    """
    # Ensure the environment is configured before accessing keys
    configure_environment()
    
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY not found in environment variables. "
                         "Please check your .env file.")

    # This is the standard configuration format for using the Dashscope Qwen model
    # with the qwen-agent framework. We are selecting qwen-long because content
    # creation can benefit from a larger context window.
    return {
        'model': 'qwen-plus-2025-01-25',
        'model_server': 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1',
        'api_key': api_key,
    }

if __name__ == '__main__':
    # This block allows you to test the configuration directly
    try:
        llm_config = get_llm_config()
        print("LLM Configuration loaded successfully:")
        # We print the model and server but hide the key for security
        print(f"  Model: {llm_config['model']}")
        print(f"  Model Server: {llm_config['model_server']}")
        print(f"  API Key: {'*' * 10}")
    except ValueError as e:
        print(f"Error: {e}")

