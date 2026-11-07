# ============================================================
# PROJECT: Rule-Based Chatbot with Chat History
# GROUP: 1st Year Students (5 Members)
# DESCRIPTION: A simple chatbot that responds to user input
#              using rules, stores chat history in a file,
#              and has a menu-driven interface.
# ============================================================

import datetime   # To get current date and time
import re         # To detect math expressions in user input

# ============================================================
# OOP: Define a Class called Chatbot
# ============================================================

class Chatbot:
    """A simple rule-based chatbot with chat history."""

    # Constructor: runs when we create a Chatbot object
    def __init__(self, bot_name, user_name):
        self.bot_name = bot_name        # Bot's name (string)
        self.user_name = user_name      # User's name (string)
        self.chat_history = []          # List to store messages (List)
        self.history_file = "chat_history.txt"   # File to save chats

        # Dictionary: stores rules (keyword -> response)
        self.rules = {
            "hello": f"Hello, {self.user_name}! How can I help you today?",
            "hi": f"Hi there, {self.user_name}! Hope you're doing well!",
            "how are you": "I'm just a bot, but I'm doing great! Thanks for asking.",
            "name": f"My name is {self.bot_name}. Nice to meet you!",
            "help": "You can ask me: hello, how are you, my name, joke, time, date, bye.\n  🔢 MATH: Type 'calc' for the calculator, or just ask: 'add 5 and 3', '10 / 2.5', '7 * 3'",
            "joke": "Why don't scientists trust atoms? Because they make up everything! 😄",
            "time": self.get_time,        # Calls a method to get current time
            "date": self.get_date,        # Calls a method to get current date
            "bye": f"Goodbye, {self.user_name}! Have a wonderful day! 👋",
            "thanks": "You're welcome! Anytime! 😊",
            "age": "I was created recently, so I'm pretty young!",
            "weather": "I can't check real weather, but I hope it's sunny where you are! ☀️",
        }

    # ============================================================
    # METHOD: Get current time
    # ============================================================
    def get_time(self):
        """Returns the current time as a string."""
        now = datetime.datetime.now()
        return f"The current time is: {now.strftime('%I:%M %p')}"

    # ============================================================
    # METHOD: Get current date
    # ============================================================
    def get_date(self):
        """Returns the current date as a string."""
        today = datetime.date.today()
        return f"Today's date is: {today.strftime('%B %d, %Y')}"

    # ============================================================
    # METHOD: Convert a string to int or float smartly
    # ============================================================
    def parse_number(self, text):
        """
        Tries to convert a string to a number.
        Returns int if it's a whole number, float if it has a decimal.
        Raises ValueError if it's not a valid number.
        """
        text = text.strip()
        if '.' in text:
            return float(text)   # e.g. "3.5" → 3.5 (float)
        else:
            return int(text)     # e.g. "7"   → 7   (int)

    # ============================================================
    # METHOD: Format answer — show int if whole, else float
    # ============================================================
    def format_answer(self, result):
        """
        If the result is a whole number (e.g. 6.0), show it as 6.
        Otherwise show up to 6 decimal places, stripping trailing zeros.
        """
        if isinstance(result, float) and result.is_integer():
            return int(result)                  # 6.0 → 6
        elif isinstance(result, float):
            return f"{result:.6f}".rstrip('0')  # 3.333333... → 3.333333
        else:
            return result

    # ============================================================
    # METHOD: Perform basic math (add, subtract, multiply, divide)
    # ============================================================
    def calculate(self, num1, operator, num2):
        """
        Takes two numbers and an operator (+, -, *, /).
        Accepts both int and float.
        Returns a formatted result string.
        """
        # Convert inputs to numbers (int or float)
        try:
            a = self.parse_number(str(num1))
            b = self.parse_number(str(num2))
        except ValueError:
            return "❌ Invalid numbers. Please enter valid integers or decimals."

        # Perform the correct operation based on operator
        if operator in ('+', 'add', 'plus', 'addition', 'sum'):
            result = a + b
            symbol = '+'

        elif operator in ('-', 'sub', 'subtract', 'minus', 'difference'):
            result = a - b
            symbol = '-'

        elif operator in ('*', 'x', 'mul', 'multiply', 'times', 'product'):
            result = a * b
            symbol = '×'

        elif operator in ('/', 'div', 'divide', 'divided', 'quotient'):
            if b == 0:
                return "❌ Cannot divide by zero! Please enter a valid divisor."
            result = a / b
            symbol = '÷'

        else:
            return "❌ Unknown operator. Use +, -, *, / or words like add, subtract, multiply, divide."

        answer = self.format_answer(result)
        return f"🔢 {a} {symbol} {b} = {answer}"

    # ============================================================
    # METHOD: Detect inline math from natural chat (e.g. "add 5 and 3")
    # ============================================================
    def detect_inline_math(self, user_input):
        """
        Scans user's chat message for a math expression.
        Supports patterns like:
          - "add 5 and 3"
          - "what is 10 divided by 2.5"
          - "5 + 3", "7 * 2.0", "10 / 4"
        Returns the result string, or None if no math found.
        """
        text = user_input.lower().strip()

        # Pattern 1: word-based — "add 5 and 3", "multiply 4.5 and 2"
        word_pattern = re.search(
            r'(add|plus|sum|subtract|minus|difference|multiply|times|product|divide|divided|quotient)'
            r'\s+([\d.]+)\s+(?:and|by|with)?\s*([\d.]+)',
            text
        )
        if word_pattern:
            operator = word_pattern.group(1)
            num1     = word_pattern.group(2)
            num2     = word_pattern.group(3)
            return self.calculate(num1, operator, num2)

        # Pattern 2: symbol-based — "5 + 3", "10.5 / 2", "7*3"
        symbol_pattern = re.search(
            r'([\d.]+)\s*([+\-*/x])\s*([\d.]+)',
            text
        )
        if symbol_pattern:
            num1     = symbol_pattern.group(1)
            operator = symbol_pattern.group(2)
            num2     = symbol_pattern.group(3)
            return self.calculate(num1, operator, num2)

        return None   # No math expression found

    # ============================================================
    # METHOD: Get a response from the chatbot
    # ============================================================
    def get_response(self, user_input):
        """Checks the user's message against rules and returns a reply."""
        user_input_lower = user_input.lower()   # Convert to lowercase for easy matching

        # STEP 1: Check for inline math expressions FIRST (e.g. "5 + 3", "add 4 and 2")
        math_result = self.detect_inline_math(user_input)
        if math_result:
            return math_result

        # STEP 2: Loop through each keyword in the rules dictionary
        for keyword, response in self.rules.items():
            if keyword in user_input_lower:       # If keyword found in user message
                # Check if the response is a method (callable) or a string
                if callable(response):
                    return response()             # Call the method to get the reply
                else:
                    return response               # Return the string reply

        # If no rule matched, return a default reply
        return "Hmm, I didn't understand that. Type 'help' to see what I can do!"

    # ============================================================
    # METHOD: Save a message to chat_history (List) and to File
    # ============================================================
    def save_message(self, sender, message):
        """Saves a message to the history list and the file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {sender}: {message}"   # Create a formatted entry

        self.chat_history.append(entry)    # Add to list (Data Structure: List)

        # File Handling: Write to file using try-except (Exception Handling)
        try:
            with open(self.history_file, "a") as file:   # Open in append mode
                file.write(entry + "\n")                  # Write the entry + newline
        except Exception as e:
            print(f"Warning: Could not save to file. Error: {e}")

    # ============================================================
    # METHOD: Display all chat history from the list
    # ============================================================
    def display_history(self):
        """Shows all messages saved during the session."""
        if len(self.chat_history) == 0:      # Check if list is empty
            print("\n  No chat history yet.\n")
        else:
            print("\n" + "=" * 50)
            print("         CHAT HISTORY (This Session)")
            print("=" * 50)
            for entry in self.chat_history:   # Loop through List
                print(" ", entry)
            print("=" * 50 + "\n")

    # ============================================================
    # METHOD: Read and display saved history from the File
    # ============================================================
    def read_history_from_file(self):
        """Reads and shows all previous chat history from the file."""
        print("\n" + "=" * 50)
        print("       ALL SAVED CHAT HISTORY (From File)")
        print("=" * 50)

        # Exception Handling: try-except in case file doesn't exist
        try:
            with open(self.history_file, "r") as file:   # Open in read mode
                lines = file.readlines()                  # Read all lines
                if len(lines) == 0:
                    print("  No history found in file.")
                else:
                    for line in lines:
                        print(" ", line.strip())          # Print each line
        except FileNotFoundError:
            print("  No history file found. Start chatting first!")
        except Exception as e:
            print(f"  Error reading file: {e}")

        print("=" * 50 + "\n")

    # ============================================================
    # METHOD: Delete / Clear the chat history file
    # ============================================================
    def clear_history(self):
        """Deletes all saved chat history from the file."""
        try:
            with open(self.history_file, "w") as file:   # Open in write mode (clears file)
                file.write("")                            # Write nothing (empty)
            self.chat_history = []                        # Also clear the session list
            print("\n  ✅ Chat history cleared successfully!\n")
        except Exception as e:
            print(f"\n  Error clearing history: {e}\n")


# ============================================================
# FUNCTION: Standalone Calculator Menu
# ============================================================
def run_calculator(bot):
    """
    A dedicated calculator mode.
    Asks the user to pick an operation, enter two numbers,
    and shows the accurate result. Supports int and float.
    """
    print("\n" + "=" * 50)
    print("        🔢 CALCULATOR MODE")
    print("   Supports int and float numbers")
    print("=" * 50)
    print("  Operations:")
    print("  1. Addition       (+)")
    print("  2. Subtraction    (-)")
    print("  3. Multiplication (*)")
    print("  4. Division       (/)")
    print("  5. Back to Menu")
    print("=" * 50)

    # Operator map: user's choice → operator keyword
    op_map = {
        "1": "+",
        "2": "-",
        "3": "*",
        "4": "/",
    }
    op_name = {
        "1": "Addition",
        "2": "Subtraction",
        "3": "Multiplication",
        "4": "Division",
    }

    while True:
        op_choice = input("\n  Choose operation (1-5): ").strip()

        if op_choice == "5":
            print("  Returning to main menu...\n")
            break

        if op_choice not in op_map:
            print("  ❌ Invalid choice. Enter 1 to 5.")
            continue

        print(f"\n  ✅ Selected: {op_name[op_choice]}")

        # Get first number with validation
        while True:
            try:
                num1_input = input("  Enter first number  : ").strip()
                num1 = bot.parse_number(num1_input)   # Accepts int or float
                break
            except ValueError:
                print("  ❌ Not a valid number. Please enter digits like 5 or 3.14")

        # Get second number with validation
        while True:
            try:
                num2_input = input("  Enter second number : ").strip()
                num2 = bot.parse_number(num2_input)   # Accepts int or float

                # Extra check for division by zero before calculating
                if op_choice == "4" and num2 == 0:
                    print("  ❌ Second number cannot be 0 for division. Try again.")
                    continue
                break
            except ValueError:
                print("  ❌ Not a valid number. Please enter digits like 5 or 3.14")

        # Calculate and show the result
        operator = op_map[op_choice]
        result_str = bot.calculate(str(num1), operator, str(num2))

        print(f"\n  {result_str}")

        # Also save this calculation to chat history
        bot.save_message("Calculator", result_str)

        again = input("\n  Do another calculation? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("  Returning to main menu...\n")
            break


# ============================================================
# FUNCTION: Display the welcome banner
# ============================================================
def show_banner():
    """Prints a welcome banner when the program starts."""
    print("=" * 50)
    print("     🤖 WELCOME TO SIMPLE CHATBOT 🤖")
    print("     Made by: Group of 5 | 1st Year")
    print("=" * 50)


# ============================================================
# FUNCTION: Display the main menu
# ============================================================
def show_menu():
    """Prints the menu options for the user."""
    print("\n--- MAIN MENU ---")
    print("1. Start Chatting")
    print("2. Calculator (Add, Subtract, Multiply, Divide)")
    print("3. View This Session's History")
    print("4. View All Saved History (File)")
    print("5. Clear Chat History")
    print("6. Exit")
    print("-" * 20)


# ============================================================
# FUNCTION: Start a chat session
# ============================================================
def start_chat(bot):
    """Runs the chat loop where user talks to the bot."""
    print(f"\n  🤖 {bot.bot_name}: Hello, {bot.user_name}! I'm ready to chat.")
    print("  (Type 'menu' anytime to go back to the main menu)\n")

    while True:    # Keep chatting until user says 'menu' or 'bye'
        user_input = input(f"  You: ").strip()   # Get user input

        if user_input == "":          # If user typed nothing
            print("  Please type something!\n")
            continue

        bot.save_message(bot.user_name, user_input)   # Save user message

        if user_input.lower() == "menu":    # User wants to go back to menu
            print("  Returning to main menu...\n")
            break

        response = bot.get_response(user_input)       # Get bot's reply
        bot.save_message(bot.bot_name, response)      # Save bot's reply

        print(f"  🤖 {bot.bot_name}: {response}\n")

        if "goodbye" in response.lower() or "bye" in response.lower():
            break    # End chat if bot said goodbye


# ============================================================
# FUNCTION: Get the user's name (with validation)
# ============================================================
def get_user_name():
    """Asks the user for their name and validates it."""
    while True:
        name = input("  Enter your name: ").strip()
        if name == "":
            print("  Name cannot be empty. Please try again.")
        else:
            return name     # Return the valid name


# ============================================================
# MAIN FUNCTION: Entry point of the program
# ============================================================
def main():
    """Main function that controls the flow of the program."""

    # Tuple: fixed chatbot settings (cannot be changed)
    bot_settings = ("PyBot", "1.0", "Rule-Based")
    bot_name = bot_settings[0]       # Access Tuple by index
    bot_version = bot_settings[1]

    show_banner()
    print(f"  Bot Name: {bot_name}  |  Version: {bot_version}\n")

    user_name = get_user_name()      # Ask for user's name

    # Create a Chatbot object (OOP)
    bot = Chatbot(bot_name, user_name)

    print(f"\n  Welcome, {user_name}! Your chatbot is ready. 🎉\n")

    # Menu-Driven Loop
    while True:
        show_menu()

        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "1":
            start_chat(bot)               # Option 1: Chat

        elif choice == "2":
            run_calculator(bot)           # Option 2: Calculator

        elif choice == "3":
            bot.display_history()         # Option 3: Session history

        elif choice == "4":
            bot.read_history_from_file()  # Option 4: File history

        elif choice == "5":
            bot.clear_history()           # Option 5: Clear history

        elif choice == "6":
            print(f"\n  👋 Thanks for using {bot_name}. Goodbye, {user_name}!\n")
            break                         # Exit the program

        else:
            print("\n  ❌ Invalid choice. Please enter a number between 1 and 6.\n")


# ============================================================
# Run the program
# ============================================================
if __name__ == "__main__":
    main()