
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