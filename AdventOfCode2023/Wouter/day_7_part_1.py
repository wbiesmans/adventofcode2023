with open("Wouter/day_7_input_final.txt") as f:
    input_lines = f.readlines()

order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
num_card_types = len(order)


def secondary_hand_value(hand):
    reverse_order = order[::-1]
    return num_card_types**4 * reverse_order.index(hand[0]) + \
        num_card_types**3 * reverse_order.index(hand[1]) + \
        num_card_types**2 * reverse_order.index(hand[2]) + \
        num_card_types * reverse_order.index(hand[3]) + \
        reverse_order.index(hand[4])


def get_hand_value(hand):
    # Assign value to each hand
    card_counts = []
    for index, card in enumerate(order):
        # Count the number of cards in the hand
        card_counts.append(hand.count(card))

    num_of_a_kind = max(card_counts)

    is_full_house = num_of_a_kind == 3 and 2 in card_counts
    is_two_pair = card_counts.count(2) == 2

    if num_of_a_kind == 1:
        primary_hand_value = 0
    elif num_of_a_kind == 2 and not is_two_pair:
        primary_hand_value = 1
    elif is_two_pair:
        primary_hand_value = 2
    elif num_of_a_kind == 3 and not is_full_house:
        primary_hand_value = 3
    elif is_full_house:
        primary_hand_value = 4
    elif num_of_a_kind == 4:
        primary_hand_value = 5
    elif num_of_a_kind == 5:
        primary_hand_value = 6
    else:
        raise ValueError("Something went wrong")

    hand_value = primary_hand_value * num_card_types**5 \
        + secondary_hand_value(hand)

    return hand_value


if __name__ == "__main__":

    values = []
    bids = []
    hands = []
    for hand, bid in [line.split() for line in input_lines]:
        bid_int = int(bid)
        bids.append(bid_int)
        hands.append(hand)

        hand_value = get_hand_value(hand)
        values.append(hand_value)

    # Order the hands and their from low to high
    ordered_hands = [hand for _, hand in sorted(zip(values, hands))]
    print(ordered_hands)
    ordered_bids = [bid for _, bid in sorted(zip(values, bids))]

    # Calculate the score by multiplying the bid with the rank
    rank = range(1, len(ordered_hands)+1)
    score = 0
    for rank, bid in zip(rank, ordered_bids):
        score += rank*bid
    print(score)




