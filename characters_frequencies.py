import os
import shelve
from string import printable

class CharacterFrequencies:

    def __init__(self, db_path):
        self.db_path = db_path
        self.character_counts = None
        self.n_characters = None
        self.character_frequencies = None
        if os.path.isfile(self.db_path):
            self.load()
        else:
            self.init_db()

    def init_db(self):
        self.character_counts = {character: 0 for character in printable}
        self.n_characters = 0
        self.character_frequencies = {character: 0 for character in printable}

    def load(self):
        with shelve.open(self.db_path) as db:
            self.character_counts = db['character_counts']
            self.n_characters = db['n_characters']
            self.character_frequencies = db['character_frequencies']

    def save(self):
        with shelve.open(self.db_path) as db:
            db['character_counts'] = self.character_counts
            db['n_characters'] = self.n_characters
            db['character_frequencies'] = self.character_frequencies

    @staticmethod
    def get_character_counts(text):
        return {character: text.count(character) for character in printable}

    @staticmethod
    def get_n_characters(character_counts):
        return sum(character_counts.values())

    def score(self, text):
        character_counts = self.get_character_counts(text)
        n_characters = self.get_n_characters(character_counts)
        chi_squared = 0
        for character, observed_count in character_counts.items():
            expected_count = self.character_frequencies.get(character, 0.0001) * n_characters
            chi_squared += (observed_count - expected_count) ** 2 / expected_count
        return chi_squared

    def update_character_frequencies(self):
        for character, count in self.character_counts.items():
            self.character_frequencies[character] = count / self.n_characters

    def add_text(self, text):
        character_counts = self.get_character_counts(text)
        n_characters = self.get_n_characters(character_counts)
        for character, count in character_counts.items():
            self.character_counts[character] += count
        self.n_characters += n_characters
        self.update_character_frequencies()


def main():
    character_frequencies = CharacterFrequencies('kappa')
    for item in character_frequencies.character_frequencies.items():
        print(item)


if __name__ == '__main__':
    main()