import os
import shelve
from string import printable


class CharacterFrequencyDatabase:

    def __init__(self, db_path):
        self.db_path = db_path
        self.char_counts = None
        self.n_chars = None
        self.char_frequencies = None
        if os.path.isfile(self.db_path):
            self.load()
        else:
            self.init_db()

    def init_db(self):
        self.char_counts, self.char_frequencies = ({char: 0 for char in printable} for _ in range(2))
        self.n_chars = 0

    def load(self):
        with shelve.open(self.db_path) as db:
            self.char_counts = db['character_counts']
            self.n_chars = db['n_characters']
            self.char_frequencies = db['character_frequencies']

    def save(self):
        with shelve.open(self.db_path) as db:
            db['character_counts'] = self.char_counts
            db['n_characters'] = self.n_chars
            db['character_frequencies'] = self.char_frequencies

    @staticmethod
    def get_char_counts(text):
        return {char: text.count(char) for char in printable}

    @staticmethod
    def get_n_chars(character_counts):
        return sum(character_counts.values())

    def score_text(self, text):
        char_counts = self.get_char_counts(text)
        n_chars = self.get_n_chars(char_counts)
        chi_squared = 0
        for char, observed_count in char_counts.items():
            frequency = self.char_frequencies[char]
            # Use a very small frequency instead of 0 to avoid division by 0.
            if frequency == 0:
                frequency = 1e-4
            expected_count = frequency * n_chars
            chi_squared += (observed_count - expected_count) ** 2 / expected_count
        return chi_squared

    def update_char_frequencies(self):
        for char, count in self.char_counts.items():
            self.char_frequencies[char] = count / self.n_chars

    def add_text(self, text):
        char_counts = self.get_char_counts(text)
        n_char = self.get_n_chars(char_counts)
        for char, count in char_counts.items():
            self.char_counts[char] += count
        self.n_chars += n_char
        self.update_char_frequencies()

    def __iter__(self):
        for char in self.char_frequencies:
            yield char

    def __repr__(self):
        sorted_chars = sorted(self.char_frequencies, key=self.char_frequencies.get, reverse=True)
        sorted_char_frequencies = [(char, self.char_frequencies[char]) for char in sorted_chars]
        output = f'Character frequency database.\n{self.n_chars:,} characters total.\nCharacter frequencies (sorted):\n'
        for i, (char, frequency) in enumerate(sorted_char_frequencies):
            output += repr(f'{char}: {frequency:.5f}')
            if (i + 1) % 5 == 0:
                output += '\n'
            else:
                output += ' '
        return output


def text_files(path):
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if os.path.splitext(file_name)[-1] == '.txt':
                yield os.path.join(dir_path, file_name)


def oanc_texts(path):
    for text_file in text_files(path):
        print('Opening:' + text_file)
        with open(text_file, 'r') as f:
            yield f.read().strip()


def main():
    character_frequencies = CharacterFrequencyDatabase('character_data')
    for text in oanc_texts('OANC-GrAF'):
        character_frequencies.add_text(text)
    character_frequencies.save()
    print(character_frequencies)


if __name__ == '__main__':
    main()
