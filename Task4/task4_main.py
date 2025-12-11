import sys, os
from file_reader import FileReader
from text_data import TextData

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task4_main.py <text_file_1> [<text_file_2> ... <text_file_n>]")
        sys.exit(1)

    # Loop through each file path provided in arguments
    for file_path in sys.argv[1:]:
        try:
            text = FileReader.read_file_to_string(file_path)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            continue

        file_name = os.path.basename(file_path)
        data = TextData(file_name, text)

        # Print statistics for this file
        print(f"File: {data.getFilename()}")
        print(f"  Letters: {data.getNumberOfLetters()},  Vowels: {data.getNumberOfVowels()},  Consonants: {data.getNumberOfConsonants()}")
        print(f"  Sentences: {data.getNumberOfSentences()},  Longest word: {data.getLongestWord()}")
        print("-" * 50)  # separator line between files
