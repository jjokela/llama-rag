import os


def save_prompt_and_response(prompt, response, folder='results'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    valid_filename = "".join(char for char in prompt if char.isalnum() or char in [" ", "_"]).rstrip()
    filename = f"{valid_filename}.txt"

    with open(os.path.join(folder, filename), 'w') as file:
        file.write(f"Prompt: {prompt}\n\nAnswer: {response}")
