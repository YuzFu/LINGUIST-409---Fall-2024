import pynini

# Define alphabet
turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"

# Define front vowels
front_vowels = pynini.union("e", "i", "ö", "ü")

# List of words to process
words = ["mane", "mana", "ni", "nin", "asimptot"]

# Define the rule: Replace "a" with "e"
rule_front_vowel = pynini.cdrewrite(
    pynini.cross("la", "le"),  # Replace "la" with "le"
    front_vowels + pynini.union(*"bcçdfgğhjklmnprsştvyz").ques,  # Left context: front vowel + optional consonant
    "r",  # Right context: before "r"
    pynini.union(*turkish_alphabet).closure()
)

# Process each word
for word in words:
    # Add the "lar" suffix
    word_with_suffix = pynini.accep(word) + pynini.accep("lar")

    # Apply the rule
    pluralized_word_fst = word_with_suffix @ rule_front_vowel

    # get paths
    paths = pluralized_word_fst.paths()
    outputs = list(paths.ostrings())

    # output 1st path
    if outputs:
        print(word, "→", outputs[0])
    else:
        print(word, "→", "failoutput")