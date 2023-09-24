import unittest
from unittest.mock import patch
import io
import sys
import raffle_app


class TestRaffleApp(unittest.TestCase):
    def setUp(self):
        self.app = raffle_app
        self.initial_pot = self.app.pot

    def test_start_new_draw(self):
        self.app.start_new_draw()
        self.assertNotEqual(self.app.pot, self.initial_pot)
        self.assertEqual(self.app.pot, self.app.INITIAL_POT)

    @patch("builtins.input", side_effect=["TestUser,3"])
    def test_buy_tickets(self, mock_input):
        self.app.start_new_draw()
        initial_pot = self.app.pot

        self.app.buy_tickets()

        self.assertNotEqual(self.app.pot, initial_pot)
        self.assertEqual(len(self.app.participants), 1)
        self.assertEqual(len(self.app.participants[0].numbers), 5)
        self.assertEqual(self.app.participants[0].owner, "TestUser")

    @patch("builtins.input", side_effect=["TestUser,3"])
    def test_buy_tickets_insufficient_funds(self, mock_input):
        self.app.start_new_draw()
        self.app.pot = 10  # Set a low pot value

        with self.assertRaises(SystemExit) as cm:
            self.app.buy_tickets()

        self.assertEqual(cm.exception.code, 1)

    def test_run_raffle_no_participants(self):
        self.app.start_new_draw()
        self.app.pot = 1000  # Ensure there's enough in the pot
        initial_pot = self.app.pot

        with self.assertRaises(SystemExit) as cm:
            self.app.run_raffle()

        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(self.app.pot, initial_pot)  # Pot should remain the same

    @patch("random.sample", side_effect=lambda x, y: [1, 2, 3, 4, 5])  # Mock a winning ticket
    def test_run_raffle_winner(self, mock_sample):
        self.app.start_new_draw()
        self.app.pot = 1000
        self.app.buy_tickets()
        initial_pot = self.app.pot

        with patch("builtins.input", side_effect=["3"]):
            self.app.run_raffle()

        self.assertEqual(self.app.pot, 0)  # Pot should be reset
        self.assertEqual(len(self.app.participants), 0)  # Participants list should be cleared

    def tearDown(self):
        self.app.pot = self.initial_pot
        self.app.participants.clear()


if __name__ == "__main__":
    unittest.main()
