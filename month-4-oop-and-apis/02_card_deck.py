"""
PROJECT 02: CARD DECK & BLACKJACK
====================================
Build a deck of cards and play Blackjack!

WHAT YOU'LL LEARN:
- Multiple classes working together
- Class relationships (a Deck has Cards, a Hand has Cards)
- More OOP practice
"""

import random

# ============================================================
# THE PROJECT: Card, Deck, and Blackjack
# ============================================================

class Card:
    """Represents a single playing card."""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        """Get the Blackjack value of this card."""
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        elif self.rank == "Ace":
            return 11  # Will handle soft aces in Hand class
        else:
            return int(self.rank)

    def __str__(self):
        suits = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
        symbol = suits.get(self.suit, self.suit)
        return f"{self.rank}{symbol}"


class Deck:
    """Represents a deck of 52 playing cards."""

    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "Jack", "Queen", "King", "Ace"]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        """Deal one card from the top of the deck."""
        if self.cards:
            return self.cards.pop()
        return None

    def __len__(self):
        return len(self.cards)


class Hand:
    """Represents a hand of cards (for Blackjack)."""

    def __init__(self, name="Player"):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        """Calculate Blackjack hand value, handling Aces smartly."""
        total = 0
        aces = 0

        for card in self.cards:
            total += card.value()
            if card.rank == "Ace":
                aces += 1

        # If we're over 21, count Aces as 1 instead of 11
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self):
        return self.value() > 21

    def show(self, hide_first=False):
        """Display the hand. If hide_first, hide the dealer's first card."""
        if hide_first:
            print(f"  {self.name}'s hand: [??] {self.cards[1]}")
        else:
            cards_str = " ".join(str(c) for c in self.cards)
            print(f"  {self.name}'s hand: {cards_str} (value: {self.value()})")


def play_blackjack():
    """Play one round of Blackjack."""
    print("\n  === BLACKJACK ===\n")

    # Create and shuffle deck
    deck = Deck()
    deck.shuffle()

    # Deal initial hands
    player = Hand("Player")
    dealer = Hand("Dealer")

    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())

    # Show hands (hide dealer's first card)
    dealer.show(hide_first=True)
    player.show()

    # Check for blackjack
    if player.is_blackjack():
        print("\n  BLACKJACK! You win!")
        return "win"

    # Player's turn
    while True:
        choice = input("\n  (H)it or (S)tand? ").upper().strip()

        if choice == "H":
            player.add_card(deck.deal())
            player.show()

            if player.is_bust():
                print("\n  BUST! You went over 21. Dealer wins.")
                return "loss"
        elif choice == "S":
            break

    # Dealer's turn
    print(f"\n  Dealer reveals...")
    dealer.show()

    while dealer.value() < 17:
        print("  Dealer hits...")
        dealer.add_card(deck.deal())
        dealer.show()

    # Determine winner
    print()
    if dealer.is_bust():
        print("  Dealer BUSTS! You win!")
        return "win"
    elif player.value() > dealer.value():
        print(f"  You win! {player.value()} beats {dealer.value()}")
        return "win"
    elif dealer.value() > player.value():
        print(f"  Dealer wins! {dealer.value()} beats {player.value()}")
        return "loss"
    else:
        print(f"  Push! Both have {player.value()}")
        return "tie"


# --- Main game loop ---
print("=" * 30)
print("  BLACKJACK")
print("=" * 30)

chips = 100
print(f"\n  Starting chips: {chips}")

while chips > 0:
    print(f"\n  Your chips: {chips}")
    try:
        bet = int(input("  Place your bet (0 to quit): "))
    except ValueError:
        print("  Invalid bet!")
        continue

    if bet == 0:
        break
    if bet > chips:
        print("  You don't have enough chips!")
        continue

    result = play_blackjack()

    if result == "win":
        chips += bet
    elif result == "loss":
        chips -= bet

if chips <= 0:
    print("\n  You're out of chips! The house always wins...")
else:
    print(f"\n  You're walking away with {chips} chips. Nice!")

# ============================================================
# CHALLENGES
# ============================================================

# CHALLENGE 1: Add "double down" — double your bet but only get one more card.

# CHALLENGE 2: Add "split" — if you have two cards of the same rank,
# split into two hands.

# CHALLENGE 3: Create a DIFFERENT card game using the same Card/Deck classes
# (e.g., War, Go Fish, or Poker hand evaluator).
