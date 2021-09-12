import time
import re
from typing import Mapping
import numpy as np


if __name__ == "__main__":
    # Getting the corrupted text and the 10000 word file. In this example, "try.txt" is a shorter version
    text = open("try.txt", "r")
    data = text.read()
    text.close()
    # Reading 10000 words
    tenh = open("tenth.txt", "r")
    tenhd = tenh.read()
    tenh.close()

    # putting the 10000 words in an array
    tenlist = tenhd.split("\n")
    tenlist = np.array(tenlist)

    # Using regex to tokenize our text data
    patte = r"""(([A-Z]\.)+|\w+(-\w+)*|[][.,;""?():-_])"""
    newlist = re.split(patte, data)
    ll = []  # this is the list containing corrupted tokenization
    for i in newlist:
        if i is not None:
            ll.append(i)

    # Levenshtein distance-based function that returns the distance between two words
    def min_edit_dist(source, target):
        n = len(source)
        m = len(target)
        source = " " + source
        target = " " + target
        D = [[0 for i in range(m + 1)] for j in range(n + 1)]
        # Initialization:the zeroth column is the distance from the empty string
        for i in range(1, n + 1):
            D[i][0] = D[i - 1][0] + 1
        for j in range(1, m + 1):
            D[0][j] = D[0][j - 1] + 1
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if source[i] == target[j]:
                    D[i][j] = D[i - 1][j - 1]
                elif source[i] != target[j]:
                    D[i][j] = min(
                        [D[i - 1][j] + 1, D[i - 1][j - 1] + 1, D[i][j - 1] + 1]
                    )
        return D[i][j]

    # This function uses the min_edit function to replace the corrrupted word with the right one
    def getReplaceWord(string1, reference=tenlist):
        replace = string1
        min_dist = len(string1)
        for i in range(len(tenlist) - 1):
            if min_edit_dist(string1, tenlist[i]) < min_dist:
                replace = tenlist[i]
                min_dist = min_edit_dist(string1, tenlist[i])
            else:
                pass
        return replace

    # function that finds strings with non words
    def keepThis(str):
        pattern = '(^[^A-Z0-90-9.,;""?():-_][^A-Z0-9.,;""?():-_]+)'
        if re.fullmatch(pattern, str):
            return True
        else:
            return False

    # creates a list that organized the correct words and punctuations back in their original space.
    referenceList1 = np.array(tenlist)
    p = []
    for i in ll:
        if (keepThis(i) == True) and (i not in tenlist):
            p.append(getReplaceWord(i, tenlist))
        else:
            p.append(i)

    # Puts final list into a string. FINAL!
    string1 = "".join(p)
    print(string1)
