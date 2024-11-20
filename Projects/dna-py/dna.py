import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 dna.py {file.csv} {sequence.txt}")
        sys.exit(1)
    dna_db = []
    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dna_db.append(row)
    with open(sys.argv[2], "r") as dna_file:
        dna_seq = dna_file.read().strip()
    str_count = {}
    for field in reader.fieldnames[1:]:
        str_count[field] = longest_match(dna_seq, field)
    for p in dna_db:
        match = True
        for str_n in str_count:
            if int(p[str_n]) != str_count[str_n]:
                match = False
                break
        if match:
            print(p["name"])
            return
    print("No match")


def longest_match(sequence, subsequence):
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)
    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1            
            else:
                break        
        longest_run = max(longest_run, count)
    return longest_run


main()
