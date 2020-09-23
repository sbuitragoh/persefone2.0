import numpy as np

# Si el segmento esta al final de la palabra, es decir que su
# estructura es -x
sufix ={
    "(ae)" : "#",
   # "ae" : "#",
    "a(e)" : "#",
    "(am)" : "$",
    "a(m)" : "$",
    "e(m)" : "%",
    "(em)" : "%",
    "t(ur)" : "&",
    "u(m)" : "/",
    "(um)" : "/"
}

# Si el segmento esta al principio de la palabra, es decir que su
# estructura es x-
prefix = {
    "(con)" : "=",
   # "prae" : "|",
    "p(rae)" : "|",
    "(prae)" : "|",
    "p(er)" : "+",
    "(per)" : "+",
    "p(ro)" : "*",
    "(pro)" : "*"
}

# Si el segmento es la palabra, es decir que su
# estructura es x
words = {
    "(er)go": "¬",
    "(er)g°": "¬",
    "e(t)" : "^",
    "(et)": "^"
}

# Si el segmento esta en el medio de la palabra, es decir que su
# estructura es -x-

extras = {
    # "ae" : "_",
    "(ae)" : "_"
}

# LIST OF KEYS

prefKeys = [*prefix.keys()]
sufKeys = [*sufix.keys()]
wordKeys = [*words.keys()]
extKeys = [*extras.keys()]

def wordPreparation(original):
    pre1 = original.replace("[","(")
    pre2 = pre1.replace("]", ")")
    processedText = ''
    originalWords = pre2.split(" ")

    for word in originalWords:
        lnword = len(word)
        print("Searching word: " + word + " for terms.")
        print("Size of word: " + str(lnword))

        res = {ele: [] for ele in word}
        for idx, ele in enumerate(word):
            res[ele].append(idx)

        if '(' in res:
            openings = res['(']
            endings = res[')']

            pairs = np.array([openings,endings])

            amountAbrev = len(openings)

            print("Abreviatures: ")
            print(amountAbrev)
            sufCond = 0

            for i in range(len(openings)):
                currentPair = pairs[:,i]
                print("Abrev. #" + str(i))
                print("Pair: " + str(pairs[:,i]))
                print(word[currentPair[0]:currentPair[1]+1])
                if lnword - 1 == currentPair[1] and currentPair[0] != 0:
                    print('Sufix in word')
                    sufCond = 1

                if sufCond:
                    wordSegment = word[currentPair[0]-1:currentPair[1]+1]
                    for j in range(len(sufKeys)):
                        if sufKeys[j] in wordSegment:
                            print("Sufix in library!")
                            print("Position: ")
                            whereSuf = wordSegment.find(sufKeys[j])
                            print(whereSuf)
                            if whereSuf == 0:
                                word.replace(wordSegment, sufix[sufKeys[j]])
                            else:
                                newSegment = word[currentPair[0]:currentPair[1] + 1]
                                word.replace(newSegment,sufix[sufKeys[j]])
                            print(word)
                    sufCond = 0
                else:
                    wordSegment = word[currentPair[0]:currentPair[1]+3]
                print("Analized Segment: ")
                print(wordSegment)
    # if clean word is in words then.. (remove parenthesis and °)
    # if (,) then check position
        # if ( is first item then dict is prefix
        # if ) is last item then dict is sufix
        # else extras
        input("Press Enter")
    return processedText

text = "Locus defi[ni]t(ur) a phylosopho 4 Physicor(um) textu 29 (et) e(ss)e"
wordPreparation(text)