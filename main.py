import argparse
import os

from dotenv import load_dotenv

from query import set_debug, get_reranked_results
from results import save_prompt_and_response
from storage import get_index

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')


def get_cli_arguments():
    parser = argparse.ArgumentParser(description="Process command-line arguments.")
    parser.add_argument("prompt", nargs='?', default="What is this document about?", type=str,
                        help="Mandatory prompt argument")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_cli_arguments()

    if args.debug:
        set_debug()

    prompt = args.prompt

    index = get_index()
    result = get_reranked_results(index, prompt)

    response = result.response

    save_prompt_and_response(prompt, response)

    print(response)
