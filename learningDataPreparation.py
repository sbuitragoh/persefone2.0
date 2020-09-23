# import numpy as np
# import re
import specialTerms as sTerm


def dataPreparation(word, abrevdict):
    charTerms = list(word)
    strSet = ''
    inWord = 0
    textSet = []
    # FOUND TERMS INSIDE PARENTHESIS

    for i in range(len(charTerms)):
        if not inWord:
            textSet.append(charTerms[i])

        if charTerms[i] == ')' or charTerms[i] == ']':
            strSet = strSet.replace(charTerms[i], "")
            textSet.append(abrevdict[strSet]) if strSet in abrevdict else textSet.append("")
            strSet = ''
            inWord = 0

        if charTerms[i] == '(' or charTerms[i] == '[' or inWord == 1:
            strSet += charTerms[i + 1]
            inWord = 1

    # REPLACE TERMS INSIDE PARENTHESIS WITH THE DICT VALUES
    newWord = ''
    newWord = newWord.join(textSet)
    newWord = newWord.replace("(", "").replace("[", "").replace(")", "").replace("]", "")
    # NEW WORD TAKING OUT THE PARENTHESIS
    return newWord


# class Sentence:
#     def __init__(self, text):
#         self.text = text
#         self.words = self.text.split(' ')
#
#     def simplifySentence(self):
#         self.newWords = self.words
#         self.modSentence = ''
#         for i in range(len(self.newWords)):
#             # Check if inside the parenthesis there's a simplified term
#             self.newWords[i] = dataPreparation(self.newWords[i])
#             self.modSentence += self.newWords[i]
#             if i < len(self.newWords):
#                 self.modSentence += " "
#
#         return self.modSentence


text = "Locus defi[ni]t(ur) a phylosopho 4 Physicor(um) textu 29, ultima superficies corporis " \
       "immobilis (con)tinentis prima. Su(per)ficies e(st) extrem(um) illius, quod (con)tinet aliud " \
       "ponit(ur) corporis (con)tinentis, ut sig[nifi]cet(ur) loc(um) n(on) e(ss)e su(per)fici(em) " \
       "locati, s(e)d loc(um) e(ss)e extrin[se]c(um) locato; atq(ue) adeo pellis a[n]i[m]alis n(on) " \
       "e(st) locus illius. Ponit(ur) ultima, quod in[te]llige r[espect]u loci. D(icitu)r prima, q(ui)a " \
       "n(on) qu(a)elibet su(per)ficies corp[or]is (con)tinentis e(st) locus, s(e)d illa, qu(a)e e(st) " \
       "(pro)xima rei locat(a)e."

# HERE IS THE PROCESS EXPLAINED SENTENCE BY SENTENCE
# sentences_with_point = re.split("[,.]", text)
# S = [None] * len(sentences_with_point)
# for i in range(len(sentences_with_point)):
#    S[i] = Sentence(sentences_with_point[i])

# for i in range(len(S)):
#    print("Sentence N " + str(i + 1))
#    S[i].simplifySentence()
#    print("Sin Modificar: ")
#    print(S[i].text)
#    print("Modificada: ")
#    print(S[i].modSentence)

# ALTHOUGH, THIS PROCESS IS ACTUALLY USELESS BECAUSE THE FUNCTION CAN TAKE A WHOLE STRING
# WITH THIS, I KEEP THE PUNCTUATION
processedText = dataPreparation(text)
print(processedText)
