
import os


def set_open_ai_key():
    # Set an environment variable
    os.environ['OPENAI_API_KEY'] = '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'

    # Verify that the environment variable is set
    print(os.getenv('OPENAI_API_KEY')[-10:])
