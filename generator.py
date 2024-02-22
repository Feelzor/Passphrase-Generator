import json
import random
import math

file_path = 'words.json'

with open(file_path, 'r') as file:
    words_file: dict[str, int] = json.load(file)

wordslist = list(words_file.keys())

AVAILABLE_SPECIAL_CHARS = ['&', '#', '"', '{', '}', '{}', "'", '()', '(', ')', '[', ']', '[]', '_', '^', '@', '=', '$', '£', '%', '*', '?', '.', ';', ',', ':', '/', '\\', '!', '§', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
AVAILABLE_PERMUTATIONS = {
    'a': ['4', '@'],
    'b': ['8'],
    'e': ['3'],
    'g': ['6'],
    'i': ['1', '!', '|'],
    'l': ['1', '!', '|'],
    'o': ['0'],
    's': ['5', '$'],
    't': ['7'],
    'z': ['2']
}
SEPARATOR = '-'
NUMBER_OF_WORDS = 5
MAX_PERMUTATIONS = 2


def prepend_with_all(word: str, nb_changes: int) -> dict[str, int]:
    list_words = {word: nb_changes}

    if nb_changes >= MAX_PERMUTATIONS:
        return list_words

    for char in AVAILABLE_SPECIAL_CHARS:
        list_words[f'{char}{word}'] = nb_changes + 1

    return list_words


def prepend_list(words: dict[str, int]) -> dict[str, int]:
    resulting_dict = {}
    for word, nb_changes in words.items():
        resulting_dict |= prepend_with_all(word, nb_changes)

    return resulting_dict


def append_with_all(word: str, nb_changes: int) -> dict[str, int]:
    list_words = {word: nb_changes}
    
    if nb_changes >= MAX_PERMUTATIONS:
        return list_words

    for char in AVAILABLE_SPECIAL_CHARS:
        list_words[f'{word}{char}'] = nb_changes + 1

    return list_words


def append_list(words: dict[str, int]) -> dict[str, int]:
    resulting_dict = {}
    for word, nb_changes in words.items():
        resulting_dict |= append_with_all(word, nb_changes)

    return resulting_dict


def middlepend_with_all(word: str, nb_changes: int) -> dict[str, int]:
    list_words = {word: nb_changes}
    
    if nb_changes >= MAX_PERMUTATIONS:
        return list_words

    middle_pos = len(word) // 2
    for char in AVAILABLE_SPECIAL_CHARS:
        list_words[f'{word[:middle_pos]}{char}{word[middle_pos:]}'] = nb_changes + 1

    return list_words


def middlepend_list(words: dict[str, int]) -> dict[str, int]:
    resulting_dict = {}
    for word, nb_changes in words.items():
        resulting_dict |= middlepend_with_all(word, nb_changes)

    return resulting_dict


def allpend(word: str, nb_changes: int) -> dict[str, int]:
    available_words = {word: nb_changes}
    available_words |= prepend_list(available_words)
    available_words |= append_list(available_words)
    available_words |= middlepend_list(available_words)

    return available_words


def permutate_at(word: str, index: int):
    return f'{word[:index]}{random.choice(AVAILABLE_PERMUTATIONS[word[index]])}{word[index+1:]}'


def can_permutate(char: str):
    return char in AVAILABLE_PERMUTATIONS.keys()


def all_permutations_for_word(words: dict[str, int], index: int) -> dict[str, int]:
    if index >= len(list(words.keys())[0]):
        return words

    permuted_words = dict(words)
    for word, nb_changes in words.items():
        if nb_changes >= MAX_PERMUTATIONS:
            continue

        if not can_permutate(word[index]):
            continue

        permuted_words[permutate_at(word, index)] = words[word] + 1

    return all_permutations_for_word(permuted_words, index + 1)


def all_permutations(words: dict[str, int]) -> dict[str, int]:
    all_possibilities = {}
    for word, nb_changes in words.items():
        all_possibilities |= all_permutations_for_word({word: nb_changes}, 0)

    return all_possibilities


def all_possibilities(word: str):
    pended_word = allpend(word, 0)
    return all_permutations(pended_word)


def estimate_complexity():
    print("Estimating complexity...")
    ESTIMATION_COMPLEXITY = 300
    possibilities = []
    for _ in range(ESTIMATION_COMPLEXITY):
        # Estimate complexity using ESTIMATION_COMPLEXITY random words
        possibilities += list(all_possibilities(random.choice(wordslist)).keys())

    possibilities_per_word = len(possibilities) / ESTIMATION_COMPLEXITY
    complexity = pow(len(wordslist) * possibilities_per_word, NUMBER_OF_WORDS)

    nb_chars = math.log(complexity, 82)

    print(f"Passphrases generated with this generator have an estimated complexity of {complexity}, which is equivalent to a {int(nb_chars)} characters long random password (using lowercase, uppercase, numbers and 10 symbols).")


def generate_passphrase():
    passphrase = []
    for _ in range(NUMBER_OF_WORDS):
        chosen_word = random.choice(wordslist)
        possibilities = list(all_possibilities(chosen_word).keys())

        final_word = random.choice(possibilities)
        print(f'Chose {final_word} from {len(possibilities)} possibilities. Original word {chosen_word}')

        passphrase.append(final_word)
    
    print(f'Generated passphrase {SEPARATOR.join(passphrase)}')


generate_passphrase()
estimate_complexity()
