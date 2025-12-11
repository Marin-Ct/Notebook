import re

class TextData:
    def __init__(self, file_name, text):
        """Initialize TextData for the given text (from file_name) and compute its statistics."""
        self.fileName = file_name
        self.text = text

        # Count letters and categorize into vowels and consonants
        vowels_set = set("aeiouAEIOU")
        self.numberOfVowels = sum(1 for ch in text if ch in vowels_set)
        self.numberOfConsonants = sum(1 for ch in text if ch.isalpha() and ch not in vowels_set)
        self.numberOfLetters = sum(1 for ch in text if ch.isalpha())

        # Count sentences by punctuation (. ! or ? as terminators)
        self.numberOfSentences = sum(1 for ch in text if ch in ".!?")

        # Find the longest word (sequence of alphabetic characters)
        words = re.findall(r"[A-Za-z]+", text)
        if words:
            self.longestWord = max(words, key=len)
        else:
            self.longestWord = ""

    # Getter methods (not strictly necessary in Python, but provided for completeness)
    def getFilename(self):
        return self.fileName

    def getText(self):
        return self.text

    def getNumberOfVowels(self):
        return self.numberOfVowels

    def getNumberOfConsonants(self):
        return self.numberOfConsonants

    def getNumberOfLetters(self):
        return self.numberOfLetters

    def getNumberOfSentences(self):
        return self.numberOfSentences

    def getLongestWord(self):
        return self.longestWord
