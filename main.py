import math
import random

import pandas as pd
from torch import le

K = 2
M = 8
Y = 4

def get_c_df(words : pd.DataFrame, yellow, green, tested):
    rows = []
    matches = []

    for w in words.itertuples():
        mtch = True
        for letter in green.keys():
            if w.word[green[letter]] != letter: # type: ignore
                mtch = False
                break  
        for letter in yellow.keys():
            if letter not in w.word:
                mtch = False
                break
            else:
                for i in yellow[letter]:
                    if w.word[i] == letter: # type: ignore
                        mtch = False
                        break

        for letter in w.word: # type: ignore
            if letter in tested: # type: ignore
                mtch = False
                break  
        
        if mtch:
            matches.append(w.word)

        u_letters = []
        c = 0
        for indx, letter in enumerate(str(w.word)):
            letter_not_tested = not letter in tested and not letter in yellow and not letter in green
            if not letter in u_letters and letter_not_tested:
                u_letters.append(letter)
                c += float(K * fq.loc[letter, "frequency"]) # type: ignore
            if letter in yellow:
                if indx not in yellow[letter]:
                    c += Y
        if mtch:
            c += M

        rows.append({'word': w.word, "c": c})

    df = pd.DataFrame(rows, columns=["word", "c"])

    if len(matches) == 1:   
        df.loc[df["word"] == matches[0], "c"] = 9999999999
        print("Just one Match!:", matches[0])
    if len(matches) == 2:   
        df.loc[df["word"] == matches[0], "c"] = 9999999999
        print("Two Matches!:", matches[0])

    df.sort_values('c', ascending=False, inplace=True)
    return df


fq = pd.read_csv("lettersFrequency.csv", header=0)
fq.set_index("letter", inplace=True)
words = pd.read_csv("valid-wordle-words.csv", header=0)

y = {}
g = {}
t = []

while True:
    word = get_c_df(words, y, g, t).iloc[0]['word']
    if (word):
        print(word)

    ans = input()
    if ans == "RESET":
        print("------------------------------------------------\n\n")

        y = {}
        g = {}
        t = []
        continue

    for indx, l in enumerate(ans):
        l = l.capitalize()
        if l == "Y":
            if y.get(word[indx]) and not word[indx] in g.values():
                if indx not in y.get(word[indx]): # type: ignore
                    y[word[indx]].append(indx)
            else:
                y[word[indx]] = [indx]
        elif l == "G":
            g[word[indx]] = indx
            if word[indx] in y:
                y.pop(word[indx])
        elif l == "X":
            if l not in t:
                t.append(word[indx])
            

    print(y)
    print(g)
    print(t)