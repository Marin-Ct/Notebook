import sys, os
from file_reader import FileReader
from text_data import TextData

if __name__ == "__main__":
    # Ensure a file path is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python task2_main.py <text_file_path>")
        sys.exit(1)

    # Get the file path from arguments and read the file
    file_path = sys.argv[1]
    text = FileReader.read_file_to_string(file_path)

    # Create a TextData object to analyze the text
    file_name = os.path.basename(file_path)  # just the file name for reporting
    data = TextData(file_name, text)

    # Print the analyzed data
    print(f"File: {data.getFilename()}")
    print(f"Number of letters: {data.getNumberOfLetters()}")
    print(f"Number of vowels: {data.getNumberOfVowels()}")
    print(f"Number of consonants: {data.getNumberOfConsonants()}")
    print(f"Number of sentences: {data.getNumberOfSentences()}")
    print(f"Longest word: {data.getLongestWord()}")
