# PyBot — Rule-Based Python Chatbot

A beginner-friendly, menu-driven Python chatbot built as a first-year group project. PyBot uses predefined keyword rules to respond to messages, supports basic calculations, and saves chat history locally.

## Features

- Keyword-based responses for greetings, help, jokes, date, and time
- Basic calculator for addition, subtraction, multiplication, and division
- Inline calculations such as `5 + 3` and `add 5 and 3`
- Current-session chat history and persistent text-file history
- Option to clear saved history
- Input validation and error handling

## Requirements

- Python 3.8 or newer
- No external Python packages required

## Run locally

1. Download or clone this repository.
2. Open a terminal in the `chatbot` folder.
3. Run:

   ```bash
   python chatbot.py
   ```

   On some systems, use `python3 chatbot.py` instead.

4. Enter your name, then choose an option from the menu.

## Example interaction

```text
Enter your name: Alex

--- MAIN MENU ---
1. Start Chatting
2. Calculator (Add, Subtract, Multiply, Divide)
3. View This Session's History
4. View All Saved History (File)
5. Clear Chat History
6. Exit

Enter your choice (1-6): 1
You: add 5 and 3
PyBot: 🔢 5 + 3 = 8
```

## How it works

The `Chatbot` class stores keyword-response rules in a dictionary. Incoming messages are first checked for supported math expressions, then matched against keywords. Messages are saved in memory and appended to a local `chat_history.txt` file.

**Note:** This is a rule-based chatbot, not a machine-learning or generative-AI chatbot. It cannot answer arbitrary questions or retrieve live weather information.

## Run tests

```bash
python -m unittest discover -p "test_*.py" -v
```

## Python concepts demonstrated

Classes and objects, methods, dictionaries, lists, tuples, loops, conditional statements, regular expressions, file handling, and exception handling.

## Contributors

Developed as a first-year group project by five students. Add the actual contributors' names and specific contributions here before publishing.

## Privacy

Chat messages are written to `chat_history.txt` on the local computer. This file is excluded from Git using `.gitignore`; avoid committing private conversations.
