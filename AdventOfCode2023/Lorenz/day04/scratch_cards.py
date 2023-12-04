import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(relativeCreated)6d %(threadName)s %(levelname)-8s %(message)s')

# logger.basicConf('%(asctime)s %(qThreadName)-12s %(levelname)-8s %(message)s')
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


class Stack(object):

    def __init__(self, data):
        self.cards = []

        for line in data:
            self.cards.append(Card(line))

    @property
    def value(self):
        return sum([card.value for card in self.cards])


if __name__ == "__main__":
    # opening and reading the lines from the input
    with open('./input.txt', 'r') as f:
        lines = f.readlines()

    my_stack = Stack(lines)
    logger.info(f'your stack has a value of {my_stack.value}')