import random
import math
import os

# Constants
MAX_TICKETS_PER_DRAW = 5
TICKET_PRICE = 5
INITIAL_POT = 100
NUMBERS_RANGE = list(range(1, 16))
GROUP_REWARDS = {
    2: 0.10,
    3: 0.15,
    4: 0.25,
    5: 0.50,
}

# Global variables
pot = INITIAL_POT
participants = []


# Utility function to generate random unique numbers for a ticket
def generate_random_ticket():
    return random.sample(NUMBERS_RANGE, 5)


# Define the Ticket class
class Ticket:
    def __init__(self, owner):
        self.owner = owner
        self.numbers = generate_random_ticket()


# Function to start a new draw
def start_new_draw():
    global pot
    pot = INITIAL_POT
    print("New draw started with a pot of $100.")
    return


# Function to buy tickets
def buy_tickets():
    global pot  # Declare pot as global before modifying it
    name, num_tickets = input("Enter your name, number of tickets to purchase (e.g., James,1): ").split(",")
    num_tickets = int(num_tickets.strip())

    if num_tickets < 1 or num_tickets > MAX_TICKETS_PER_DRAW:
        print("Invalid number of tickets. You can buy between 1 and 5 tickets.")
        return

    if pot < num_tickets * TICKET_PRICE:
        print("Not enough funds in the pot to purchase tickets.")
        return

    tickets = [Ticket(name) for _ in range(num_tickets)]
    participants.extend(tickets)

    pot -= num_tickets * TICKET_PRICE

    print(f"Tickets purchased successfully! You now have {num_tickets} ticket(s).")
    for ticket in tickets:
        print(f"Ticket numbers: {ticket.numbers}")

    input("Press any key to return to the main menu.")
    return


# Function to run the raffle
def run_raffle():
    if not participants:
        print("No participants. Buy tickets first.")
        return

    global pot  # Declare pot as global before modifying it
    winning_ticket = Ticket("Winning Ticket")
    winners = {2: [], 3: [], 4: [], 5: []}

    for participant in participants:
        matched_numbers = len(set(participant.numbers) & set(winning_ticket.numbers))
        if matched_numbers in winners:
            winners[matched_numbers].append(participant)

    total_reward = 0
    for group, winners_list in winners.items():
        if winners_list:
            reward_per_winner = (pot * GROUP_REWARDS[group]) / len(winners_list)
            for winner in winners_list:
                winner_reward = math.ceil(reward_per_winner)
                winner.owner += f" (Group {group})"
                print(f"{winner.owner} won ${winner_reward} in Group {group}!")
                total_reward += winner_reward

    pot = 0  # Reset the pot
    participants.clear()

    print(f"Total prize awarded: ${total_reward}")
    input("Press any key to return to the main menu.")
    return


# Main menu
def main_menu():
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print("Welcome to My Raffle App")
        print(f"Status: Pot size - ${pot}")
        print("[1] Start a New Draw")
        print("[2] Buy Tickets")
        print("[3] Run Raffle")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            start_new_draw()
        elif choice == "2":
            buy_tickets()
        elif choice == "3":
            run_raffle()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main_menu()
