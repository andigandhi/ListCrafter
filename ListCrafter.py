#!/usr/bin/env python3

from datetime import datetime
import sys, argparse, os

colors = {
    "blue": "\033[94m",
    "green": "\x1b[38;5;2m",
    "red": "\x1b[38;5;124m",
    "no": "\033[0m"
}

# Generate the base wordlist
def gen_base_wordlist(level):
    base_wordlist = []
    # Trivial passwords
    trivial_passwords = []
    trivial_passwords.append(company)
    trivial_passwords.append(town)
    trivial_passwords += seasons
    if level > 1: trivial_passwords.append(street)
    trivial_passwords += other_words
    base_wordlist += trivial_passwords

    # All lowercase
    for s in trivial_passwords:
        base_wordlist.append(s.lower())

    # All UPPERCASE
    if level > 1:
        for s in trivial_passwords:
            base_wordlist.append(s.upper())

    return base_wordlist

# Combine two strings in different ways
def combine_strings(base_wordlist, append_str):
    candidates = []
    candidates += append_string_to_list(base_wordlist, append_str)
    candidates += append_string_to_list(base_wordlist, "."+append_str)
    candidates += append_string_to_list(base_wordlist, append_str[2:])
    return candidates

def append_string_to_list(pwlist, string):
    return [s + string for s in pwlist]

def write_array_to_file(array, filename):
    with open(filename, "w") as txt_file:
        for line in array:
            txt_file.write(line + "\n")


# Command Line Arguments
parser = argparse.ArgumentParser(prog='ListCrafter',
                                 description='This script creates a custom wordlist for cracking hashes in company networks',
                                 epilog='python3 ListCrafter.py -c "SySS" -t Tuebingen -s "Schaffhausenstrasse 77" -o Pentest Cyber -H hashes.txt')
parser.add_argument("-c", "--company", help="The companies name")
parser.add_argument("-t", "--town", help="The town of the company")
parser.add_argument("-s", "--street", help="The street of the company")
parser.add_argument("-o", "--other", nargs='*', help="Other important keywords (Branch,...)")
parser.add_argument("-l", "--level", type=int, default=2, help="The level of verbosity of the wordlist (0-3)")
parser.add_argument("-H", "--hashes", help="The file containing the hashes (for auto-cracking)")
args = parser.parse_args()


print(colors["blue"] + "  _    _    _   "+colors["green"]+" ___           __ _           ")
print(colors["blue"] + " | |  (_)__| |_ "+colors["green"]+"/ __|_ _ __ _ / _| |_ ___ _ _ ")
print(colors["blue"] + " | |__| (_-<  _|"+colors["green"]+" (__| '_/ _` |  _|  _/ -_) '_|")
print(colors["blue"] + " |____|_/__/\__|"+colors["green"]+"\___|_| \__,_|_|  \__\___|_|  "+colors["no"])
print()
print(colors["red"]+"generate custom wordlists for cracking hashes in company networks"+colors["no"])
print()
print()
level = args.level
if ((company := args.company) is None):
    print("Name of the company:")
    company = input(colors["red"]+"> "+colors["no"])
if ((town := args.town) is None):
    print("Town of "+company+":")
    town = input(colors["red"]+"> "+colors["no"])
if ((street_and_no := args.street) is None):
    print("Street and No. of "+company+":")
    street_and_no = input(colors["red"]+"> "+colors["no"])
street = street_and_no.split(" ")[0]
if len(street_and_no.split(" "))>1:
    street_no = street_and_no.split(" ")[1]
else:
    street_no = ""

# Custom Words
print("Do you want to add other words to the base wordlist? Add each one by pressing Enter. Press Enter without any input to start generating the wordlist.")
other_words = []
other_words += args.other
print(args.other)
while (custom_word := input(colors["red"]+"> "+colors["no"])) != "":
    other_words.append(custom_word)

# Year and Seasons
year = datetime.now().year
seasons = ["Frühling","Sommer","Herbst","Winter"]

print("Generating wordlist for "+company+" based in "+town+"...")
print()

candidates = []

# Generate the base wordlist 
base_wordlist = gen_base_wordlist(level)
candidates += base_wordlist

# Add current year to entities of base wordlist
candidates += combine_strings(base_wordlist, str(year))

# Add last year to entities of base wordlist
if level > 1:
    candidates += combine_strings(base_wordlist, str(year-1))

# Add last 60 years to entities of base wordlist
if level > 2:
    for i in range(2,60):
        candidates += combine_strings([company, town]+other_words, str(year-i))

# Add street no to entities of base wordlist
if level > 1:
    candidates += combine_strings([company, town, street], street_no)




filename = "wordlist_"+company+"_"+str(year)+".wordlist"
# Write the wordlist file
write_array_to_file(candidates, filename)

# Write the hashcat rule file
rules = [
    ":", # No modification
    "$!", # Append exclamation mark
    "s.&" # Replace the dot separator with an and symbol
]
if level>1:
    rules += [
        "t", # Toggle case
        "s.:", # Append :
        "s.$", # Append $
        "s.;" # Append ;
    ]
write_array_to_file(rules,"ListCrafter.rule")

print("Generated wordlist has " + str(len(candidates)) + " entries and is " + str(sys.getsizeof(candidates) / 1024).split(".")[0] + " kB large.")
print("Combined with the ListCrafter rules this creates " + str(len(candidates)*len(rules)) + " passwords.")
print()

print("How to use it to crack different hashes:")
print(colors["red"]+"NTLM "+colors["blue"]+"hashcat -m 1000 hashes.txt "+filename+" -r ListCrafter.rules")
print(colors["red"]+"DCC2 "+colors["blue"]+"hashcat -m 2100 hashes.txt "+filename+" -r ListCrafter.rules"+colors["no"])

if args.hashes is not None:
    print(colors["red"]+"Cracking "+args.hashes+" automatically..."+colors["no"])
    os.system('hashcat '+args.hashes+' '+filename+' -r ListCrafter.rules')