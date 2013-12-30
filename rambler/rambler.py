__author__ = 'Lars Djerf <lars.djerf@gmail.com'

import argparse
import random
import re
import sys
import textwrap


def build_table(data_file):
    """Builds and return 'probability' table."""

    table = {}
    words = []
    with open(data_file, "r") as fd:
        for line in fd:
            tmp = re.split("\s|--|([.,;:?!\"]|[()[\]{}])", line)
            tmp = [word for word in tmp if word]
            if words:
                tmp.insert(0, words[-1])
            words = tmp

            for i in range(len(words) - 1):
                choices = table.get(words[i], [])
                choices.append(words[i + 1])
                table[words[i]] = choices  # Yes, yes, stupid. My poor defense
                                           # is that these days memory is
                                           # cheap. And fixing this is on the
                                           # TODO-list which is also on the
                                           # TODO-list.
    return table


def get_start_word(table):
    """Possibly returns a random start word."""

    words = [word for word in table.keys() if word[0].isupper()]
    return random.choice(words)


def ramble(table):
    """Yield random lines.

    Keyword argument(s):
    table -- 'probability' table
    """

    left_par = {"(": ")",
                "[": "]",
                "{": "}"}
    right_par = {")": "(",
                 "]": "[",
                 "}": "{"}
    punctuation = (".", "!", "?", ",", ":", ";", "\"",
                   "\(", "\)", "{", "}", "[", "}")

    word = get_start_word(table)
    sentence = [word]
    par_stack = []
    word_count = 1
    odds = 1
    while word not in punctuation[0:3]:
        if word_count < 28:
            odds = 28 - word_count
        if (not random.randint(0, odds) and
                filter(lambda n: n in punctuation[0:3], table[word])):
            word = random.choice(punctuation[0:3])
        else:
            word = random.choice(table.get(word, ["."]))

        if word in left_par.keys():
            par_stack.append(word)
        elif word in right_par.keys():
            if (len(par_stack) > 0 and
                        right_par[word] == par_stack[-1]):
                par_stack.pop()
            else:
                continue  # Illegal parenthesis, pick new word!
                          # This could probably fail horribly and
                          # loop forever!
        if word in punctuation[0:3]:
            for par in reversed(par_stack):
                sentence.append(left_par[par])
            sentence.append(word + " ")
        elif word in punctuation[3:]:
            sentence.append(word)
        else:
            sentence.append(" " + word)
        word_count += 1
    return "".join(sentence)


def main():
    parser = argparse.ArgumentParser(description="This machine is a ramblin' one.")
    parser.add_argument("file", metavar="FILE", help="Data to chew on.")
    parser.add_argument("-c", "--count", dest="count", metavar="N", type=int,
                        default=random.randint(5, 20), help="Number of sentences.")
    args = parser.parse_args()

    table = build_table(args.file)
    sentences = []
    for sentence in range(args.count):
        sentences.append(ramble(table))
    print textwrap.fill("".join(sentences), 60)

    sys.exit(0)
