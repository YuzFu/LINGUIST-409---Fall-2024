# import os
import difflib 

# os.chdir()
# os.getcwd()

# Load data
with open('data/tur.trn', 'r') as file:
    tur_training = [line.strip().split('\t') for line in file if line.strip()]
with open('data/tur.trn', 'r') as file:
    tur_development = [line.strip().split('\t') for line in file if line.strip()]
with open('data/tur.out', 'r') as file:
    tur_out = [line.strip().split('\t') for line in file if line.strip()]

# Analyze patterns
# morph_features = set(msd for _, msd, _ in tur_training)
# for feature in morph_features:
#     part_of_speech, 
# print("\nUnique Morphosyntactic Features in Training Data:")
# for i in morph_features:
#     print(i)

# compare development data
with open('data/tur.dev') as tur_dev, open('data/tur.out') as tur_out:
    tur_dev_text = tur_dev.readlines()
    tur_out_text = tur_out.readlines()

diff = difflib.unified_diff(
    tur_dev_text, tur_out_text,
    fromfile='tur.out',
    tofile='tur.dev',
    lineterm=''
)

# Write all differences to 'diff.txt' and filtered differences to 'diff_filtered.txt'
with open('data/diff.txt', 'w') as diff_file, open('data/diff_filtered.txt', 'w') as filtered_file:
    added, removed = [], []
    for line in diff:
        diff_file.write(line + '\n')
        if line.startswith('-'):
            removed.append(line)
        elif line.startswith('+'):
            added.append(line)
    
    # Ensure equal number of removals and additions
    for rem, add in zip(removed, added):
        filtered_file.write(rem + '\n')
        filtered_file.write(add + '\n')
