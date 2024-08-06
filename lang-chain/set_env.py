
import os


def set_open_ai_key():
    # Set an environment variable
    os.environ['OPENAI_API_KEY'] = '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'

    # Verify that the environment variable is set
    print(os.getenv('OPENAI_API_KEY'))
