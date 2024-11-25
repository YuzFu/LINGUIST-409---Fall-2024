# Define a function that takes in tur.out, test the vowel harmony info - frotness, replace the vowel if needed
# bonus: compare to tur.dev (correct version) to see if the problem is solved

def evaluate_vowel_harmony_correction(out_file, dev_file):
    def is_front_vowel(v):
        return v in "eiöü"

    def is_back_vowel(v):
        return v in "aıou"

    def determine_suffix(lemma):
        for char in reversed(lemma):
            if char in "aeıioöuü":
                if is_back_vowel(char):
                    return "lar"
                if is_front_vowel(char):
                    return "ler"
        return None

    def correct_pl_frontness(output, lemma):
        suffix_start = len(lemma)
        suffix = output[suffix_start:]

        expected_suffix = determine_suffix(lemma)

        if suffix in ["lar", "ler"] and suffix != expected_suffix:
            return output[:suffix_start] + expected_suffix
        return output

    with open(out_file, 'r', encoding='utf8') as tur_out, open(dev_file, 'r', encoding='utf8') as tur_dev:
        out_lines = [line.strip() for line in tur_out if line.strip()]
        dev_lines = [line.strip() for line in tur_dev if line.strip()]

    total = 0
    correct_before = 0
    correct_after = 0

    for out_line, dev_line in zip(out_lines, dev_lines):
        lemma, msd, predicted = out_line.split('\t')
        lemma_dev, msd_dev, correct = dev_line.split('\t')

        assert lemma == lemma_dev and msd == msd_dev

        if predicted == correct:
            correct_before += 1

        corrected = correct_pl_frontness(predicted, lemma)

        if corrected == correct:
            correct_after += 1

        total += 1

    accuracy_before = correct_before / total
    accuracy_after = correct_after / total

    return accuracy_before, accuracy_after

out_file = 'data/tur.out'
dev_file = 'data/tur.dev'

accuracy_before, accuracy_after = evaluate_vowel_harmony_correction(out_file, dev_file)
print(f"Accuracy Before Correction: {accuracy_before:.2%}")
print(f"Accuracy After Correction: {accuracy_after:.2%}")

