import requests

def create_new_deck():
    response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
    deck_data = response.json()
    deck_id = deck_data['deck_id']
    return deck_id

def draw_card(deck_id, count=1):
    response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}")
    cards_data = response.json()
    cards = cards_data['cards']
    return cards

def calculate_score(cards):
    score = 0
    num_aces = 0
    for card in cards:
        value = card['value']
        if value.isdigit():
            score += int(value)
        elif value in ['JACK', 'QUEEN', 'KING']:
            score += 10
        elif value == 'ACE':
            num_aces += 1
            score += 11
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

def main():
    print("Welcome to Blackjack!")
    deck_id = create_new_deck()

    player_cards = draw_card(deck_id, count=2)
    computer_cards = draw_card(deck_id, count=2)

    print("Your cards:", ", ".join([card['value'] for card in player_cards]))
    print("Computer's cards:", computer_cards[0]['value'], ", Hidden")

    while True:
        player_score = calculate_score(player_cards)
        if player_score == 21:
            print("Congratulations! You got Blackjack!")
            break
        elif player_score > 21:
            print("Busted! You went over 21. You lose.")
            break

        action = input("Do you want to (H)it or (S)tand? ").strip().upper()

        if action == 'H':
            new_card = draw_card(deck_id)[0]
            player_cards.append(new_card)
            print("You drew:", new_card['value'])
            print("Your cards:", ", ".join([card['value'] for card in player_cards]))
        elif action == 'S':
            computer_score = calculate_score(computer_cards)
            while computer_score < 17:
                new_computer_card = draw_card(deck_id)[0]
                computer_cards.append(new_computer_card)
                computer_score = calculate_score(computer_cards)

            print("Computer's cards:", ", ".join([card['value'] for card in computer_cards]))
            if computer_score > 21 or computer_score < player_score:
                print("Congratulations! You win!")
            elif computer_score == player_score:
                print("It's a tie!")
            else:
                print("Sorry, you lose!")
            break
        else:
            print("Invalid input. Please enter H or S.")

if __name__ == "__main__":
    main()
