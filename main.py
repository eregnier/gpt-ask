import os
import json
import readline
import argparse
import openai


readline.parse_and_bind('"\e[D": backward-char')
readline.parse_and_bind('"\e[C": forward-char')


with open(os.path.expanduser("~/.gkey")) as f:
    openai.api_key = f.read().strip()

messages = []


def multi_line_input(prompt: str):
    lines = []
    while True:
        line = input(prompt).strip()
        lines.append(line)

        if not line:
            break
        else:
            prompt = " "
    return "\n".join(lines).strip()


def ask(model: str = "gpt-3.5-turbo"):
    while True:
        q = multi_line_input("\n[?]\n> ").strip()
        if q:
            print("-" * 28)
            print("|   wait for response...   |")
            print("-" * 28)
            messages.append({"role": "user", "content": q})
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            response = response["choices"][0]["message"]["content"]
            print("\n" + response)
            messages.append({"role": "system", "content": response})
        else:
            print("invalid input. retrying...")


def command_line_input(
    q: str,
    model: str = "gpt-3.5-turbo",
):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages + [{"role": "user", "content": q}],
    )
    print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GPT cli single shot or interactive mode by default"
    )
    parser.add_argument(
        "-c",
        "--command",
        type=str,
        help="Single shot mode prompt with direct stdout output : -c 'what is the color of the sky?'",
    )
    parser.add_argument(
        "-ctx",
        "--context",
        type=str,
        help=(
            "Path to context file to load before query are sent.\n"
            "it have to be a json file with a list that looks like :\n"
            '[{"role":"system", "content": "you are a lovely computing science assistant"},'
            '{"role":"user", "content": "Can you explain me things like I am 12 ?"}]'
        ),
    )
    args = parser.parse_args()
    if args.context:
        with open(args.context) as f:
            messages = json.load(f)
    if args.command:
        command_line_input(q=args.command)
    else:
        try:
            print("\n Hello there! Ask me anything :)")
            ask()
        except KeyboardInterrupt:
            print("bye!")
