import numpy as np

# Si el segmento esta al final de la palabra, es decir que su
# estructura es -x
sufix ={
    "(ae)" : "#",
    # "(a)e" : "#",
    # "ae" : "#",
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
    "(er)go": "¬°",
    "(er)g°": "¬°",
    "e(t)" : "^",
    "(et)": "^",
    # "e(st)" : "e~"
}

# Si el segmento esta en el medio de la palabra, es decir que su
# estructura es -x-

extras = {
    # "(a)e" : "_",
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
        print("Searching word: " + word + " for terms.")
        print("Size of word: " + str(len(word)))

        res = {ele: [] for ele in word}
        for idx, ele in enumerate(word):
            res[ele].append(idx)

        if '(' in res:
            cnt = 0
            sufCond = 0

            openings = res['(']
            endings = res[')']
            pairs = np.array([openings,endings])


            for i in range(len(openings)):
                if cnt == 0:
                    currentPair = pairs[:,i]
                else:
                    res = {ele: [] for ele in word}
                    for idx, ele in enumerate(word):
                        res[ele].append(idx)
                    openings = res['(']
                    endings = res[')']

                    pairs = np.array([openings, endings])
                    currentPair = pairs[:, 0]

                # print("Abrev. #" + str(i))
                # print("Pair: " + str(pairs))
                # print(word[currentPair[0]:currentPair[1]+1])

                if len(word) - 1 == currentPair[1] and currentPair[0] != 0:
                    # print('Sufix in word')
                    sufCond = 1

                wordAsList = list(word)
                newWord = ""

                if sufCond:
                    wordSegment = word[currentPair[0]-1:currentPair[1]+1]
                    foundSuf = 0
                    for j in range(len(sufKeys)):
                        if sufKeys[j] in wordSegment:
                            whereSuf = wordSegment.find(sufKeys[j])

                            if whereSuf == 0:
                                wordAsList[currentPair[0] - 1:currentPair[1] + 1] = sufix[sufKeys[j]]
                            else:
                                wordAsList[currentPair[0]:currentPair[1] + 1] = sufix[sufKeys[j]]

                            newList = wordAsList
                            foundSuf = 1

                    if not foundSuf :
                        wordAsList[currentPair[0]:currentPair[1] + 1] = ""
                        newList = wordAsList

                    sufCond = 0
                    newWord = newWord.join(newList)

                else:
                    zeroChk = 0

                    if currentPair[0] == 0:
                        wordSegment = word[currentPair[0]:currentPair[1] + 3]
                    else:
                        wordSegment = word[currentPair[0] - 1:currentPair[1] + 3]

                    for k in range(len(prefKeys)):
                        if prefKeys[k] in wordSegment:
                            if prefKeys[k][0] == '(':
                                wordAsList[currentPair[0]:currentPair[1] + 1] = prefix[prefKeys[k]]
                            else:
                                wordAsList[currentPair[0] - 1:currentPair[1] + 1] = prefix[prefKeys[k]]
                            newList = wordAsList
                            zeroChk = 1

                    for l in range(len(wordKeys)):
                        if wordKeys[l] in wordSegment:
                            if l < 2:
                                wordAsList[currentPair[0]:currentPair[1] + 3] = words[wordKeys[l]]
                            else:
                                if wordKeys[l][0] == '(':
                                    wordAsList[currentPair[0]:currentPair[1] + 1] = words[wordKeys[l]]
                                else:
                                    wordAsList[currentPair[0]-1:currentPair[1] + 1] = words[wordKeys[l]]
                            newList = wordAsList
                            zeroChk = 1


                    for m in range(len(extKeys)):
                        if extKeys[m] in wordSegment:
                            wordAsList[currentPair[0]:currentPair[1] + 1] = extras[extKeys[m]]
                            newList = wordAsList
                            zeroChk = 1

                    if not zeroChk:
                        wordAsList[currentPair[0]:currentPair[1] + 1] = ""
                        newList = wordAsList

                    newWord = newWord.join(newList)

                word = newWord
                print("Final Word:")
                print(word)
                cnt+=1
                print("Abrev. analized")
                print("Counter: " + str(cnt))

        processedText+=word
        processedText+=" "

        print (processedText)
    return processedText

text = "Locus defi[ni]t(ur) a phylosopho 4 Physicor(um) textu 29, ultima superficies corporis " \
       "immobilis (con)tinentis prima. Su(per)ficies e(st) extrem(um) illius, quod (con)tinet aliud " \
       "ponit(ur) corporis (con)tinentis, ut sig[nifi]cet(ur) loc(um) n(on) e(ss)e su(per)fici(em) " \
       "locati, s(e)d loc(um) e(ss)e extrin[se]c(um) locato; atq(ue) adeo pellis a[n]i[m]alis n(on) " \
       "e(st) locus illius. Ponit(ur) ultima, quod in[te]llige r[espect]u loci. D(icitu)r prima, q(ui)a " \
       "n(on) qu(a)elibet su(per)ficies corp[or]is (con)tinentis e(st) locus, s(e)d illa, qu(a)e e(st) " \
       "(pro)xima rei locat(a)e."

wordPreparation(text)