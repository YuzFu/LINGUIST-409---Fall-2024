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

def n_vowel_categorize(lemma):
  for char in reversed(lemma):
    if char in "öü":
      return {"frontness":True, "roundness":True}
    elif char in "ei":
      return {"frontness":True, "roundness":False}
    elif char in "ou":
      return {"frontness":False, "roundness":True}
    elif char in "aı":
      return {"frontness":False, "roundness":False}

def v_vowel_categorize(lemma):
  vowels = "öüeiouaı"
  n = 0
  for char in reversed(lemma):
    if char in vowels:
      n += 1
      if n == 2:
        if char in "öü":
          return {"frontness": True, "roundness": True}
        elif char in "ei":
          return {"frontness": True, "roundness": False}
        elif char in "ou":
          return {"frontness": False, "roundness": True}
        elif char in "aı":
         return {"frontness": False, "roundness": False}

# def is_plural(msd):
#   return "(PL" in msd

def is_str(msd):
  return "ACC" in msd or "GEN" in msd

def is_obl(msd):
  return "DAT" in msd or "LOC" in msd or "ABL" in msd

with open('tur.out', 'r') as file:
    tur_out = [line.strip().split('\t') for line in file if line.strip()]

with open('tur.dev', 'r') as file:
    tur_dev = [line.strip().split('\t') for line in file if line.strip()]

dev = []
for word in tur_dev:
  dev.append(word[2])

# for word in tur_out:
#   lemma, msd, estimation = word[:3]
#   print(lemma, msd, estimation)
#   correct = dev[i]

#   if msd.startswith('N') & is_plural(msd):
#     if (estimation != correct):
#       # print(lemma, msd, estimation, correct)
#       output = (estimation @ plural_correction_rule)
#       paths = list(output.paths().ostrings())
#       if paths:
#           print(estimation, "→", paths[0])
#       else:
#           print(estimation, "→", "failoutput")

#   if msd.startswith('V'):
#     print(lemma, v_vowel_categorize(lemma))

# 12/06 update
# this is for adding noun plural suffix
import pynini

# Define Turkish alphabet
turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz " # add " "(space), so it includes word compounds, like "sözdizimsel tuzlerde" etc.
sigma = pynini.union(*turkish_alphabet).closure()

# Vowel transducer a
# plural_correction_a = pynini.union(pynini.cross(pynini.union(*vowels).closure, "a"),)

# Vowel transducer e
# plural_correction_e = pynini.union(pynini.cross(pynini.union(*vowels).closure, "e"),)

# Plural suffix context for a
plural_correction_rule_a = pynini.cdrewrite(
        pynini.cross("e", "a"),
        "l",    
        "r",    
        sigma)

# Plural suffix context for e
plural_correction_rule_e = pynini.cdrewrite(
        pynini.cross("a", "e"),
        "l",
        "r",
        sigma)

# Process
for i, line in enumerate(tur_out):
  lemma, msd, inflected = line[:3]
  correct = dev[i]

  if msd.startswith("N") and '(PL' in msd:
    v_cat = n_vowel_categorize(lemma)

    if v_cat["frontness"] == False and "ler" in inflected:
      output = inflected @ plural_correction_rule_a
      paths = list(output.paths().ostrings())
      correction = paths[0]
      print(lemma, inflected, "→", correction, correct == correction)

    elif v_cat["frontness"] == True and "lar" in inflected:
      output = inflected @ plural_correction_rule_e
      paths = list(output.paths().ostrings())
      correction = paths[0]
      print(lemma, inflected, "→", correction, correct == correction)

    else:
      correction = inflected