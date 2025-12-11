import re

class TextData:
    def __init__(self, file_name, text):
        self.fileName = file_name
        self.text = text
        vowels_set = set("aeiouAEIOU")
        self.numberOfVowels = sum(1 for ch in text if ch in vowels_set)
        self.numberOfConsonants = sum(1 for ch in text if ch.isalpha() and ch not in vowels_set)
        self.numberOfLetters = sum(1 for ch in text if ch.isalpha())
        self.numberOfSentences = sum(1 for ch in text if ch in ".!?")
        words = re.findall(r"[A-Za-z]+", text)
        self.longestWord = max(words, key=len) if words else ""
    def getFilename(self): return self.fileName
    def getNumberOfVowels(self): return self.numberOfVowels
    def getNumberOfConsonants(self): return self.numberOfConsonants
    def getNumberOfLetters(self): return self.numberOfLetters
    def getNumberOfSentences(self): return self.numberOfSentences
    def getLongestWord(self): return self.longestWord
