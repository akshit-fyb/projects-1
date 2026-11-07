"""Basic tests for the rule-based chatbot."""
import unittest
from chatbot import Chatbot


class ChatbotTests(unittest.TestCase):
    def setUp(self):
        self.bot = Chatbot("PyBot", "Tester")

    def test_greeting(self):
        self.assertIn("Tester", self.bot.get_response("hello"))

    def test_inline_addition(self):
        self.assertIn("= 8", self.bot.get_response("add 5 and 3"))

    def test_symbol_multiplication(self):
        self.assertIn("= 21", self.bot.get_response("7 * 3"))

    def test_division_by_zero(self):
        self.assertIn("Cannot divide by zero", self.bot.calculate(10, "/", 0))

    def test_unknown_input(self):
        self.assertIn("didn't understand", self.bot.get_response("quantum banana"))


if __name__ == "__main__":
    unittest.main()
