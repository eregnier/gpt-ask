import os
import re
import json
import readline
import argparse
import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import guess_lexer
from pygments.formatters import Terminal256Formatter

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
            print("\n" + colorize_snippets(response))
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


def colorize(code):
    code_only = "\n".join(code.split("\n")[1:-1])
    lexer = guess_lexer(code_only)
    return highlight(code, lexer, Terminal256Formatter(style="monokai"))


def colorize_snippets(data):
    pattern = re.compile(r"```[a-z]*\n([\s\S]*?)\n```")
    code_match = re.search(pattern, data)
    if code_match:
        for code in re.finditer(pattern, data):
            colorized_code = colorize(code.group(0))
            data = data.replace(code.group(0), colorized_code)
    return data


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
