
import os
from rich import print

def set_open_ai_key():
    # Set an environment variable
    os.environ['OPENAI_API_KEY'] = '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'

    # Verify that the environment variable is set
    print(os.getenv('OPENAI_API_KEY')[-30:])

def print_input(input_data):
    print("input:")
    print(input_data)
    return input_data

def gothrough(input_data):
    return input_data


def print_current_path():
    current_directory = os.getcwd()
    print("当前目录:", current_directory)