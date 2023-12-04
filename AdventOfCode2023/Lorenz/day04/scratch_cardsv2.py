import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(relativeCreated)6d %(threadName)s %(levelname)-8s %(message)s')


class Card(object):

    def __init__(self, card_data):
        self.id = int(card_data.split(':')[0].split(' ')[-1])
        self.numbers = [int(x) for x in card_data.split('|')[-1][:-1].split(' ') if x != '']
        self.winning_numbers = [int(x) for x in card_data.split('|')[0].split(':')[-1].split(' ') if x != '']

    @property
    def value(self):
        n_winning = len([x for x in self.numbers if x in self.winning_numbers])
        if n_winning == 0:
            return 0
        else:
            return 2**(n_winning-1)

    def process(self):
        n_winning = len([x for x in self.numbers if x in self.winning_numbers])
        return range(self.id+1, self.id+n_winning+1)


class Stack(object):
    LOGGER = logger

    def __init__(self, data):
        self.cards = {}
        self.pile = []

        for line in data:
            new_card = Card(line)
            self.cards[new_card.id] = new_card
            self.add_card(new_card)

    @property
    def value(self):
        return sum([card.value for card in self.pile])

    @property
    def size(self):
        return len(self.pile)

    def card_count(self, idx):
        return len([card for card in self.pile if card.id == idx])

    def add_card(self, card):
        self.pile.append(card)

    def process_results(self):
        for idx, card in self.cards.items():

            card_count = self.card_count(idx)
            for new_idx in list(card.process())*card_count:
                self.add_card(self.cards[new_idx])
            self.LOGGER.info(f'processed cards with idx {idx}')


if __name__ == "__main__":
    # opening and reading the lines from the input
    with open('./input.txt', 'r') as f:
        lines = f.readlines()

    my_stack = Stack(lines)
    my_stack.process_results()
    my_stack.LOGGER.info(f'your stack has a size of {my_stack.size}')