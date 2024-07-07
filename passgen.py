from datetime import datetime
import sys

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



print(colors["blue"] + ".__                  .__                           ")
print(colors["blue"] + "|  |__ _____    _____|  |__   "+colors["green"]+"  ____   ____   ____  ")
print(colors["blue"] + "|  |  \\\\__  \  /  ___/  |  \ "+colors["green"]+"  / ___\_/ __ \ /    \ ")
print(colors["blue"] + "|   Y  \/ __ \_\___ \|   Y  \ "+colors["green"]+"/ /_/  >  ___/|   |  \ ")
print(colors["blue"] + "|___|  (____  /____  >___|  /"+colors["green"]+" \___  / \___  >___|  /")
print(colors["blue"] + "     \/     \/     \/     \//"+colors["green"]+" _____/      \/     \/"+colors["no"])
print()
print(colors["red"]+"generate custom wordlists for cracking hashes in company networks"+colors["no"])
print()
print()
level = 3
print("Name of the company:")
company = input(colors["red"]+"> "+colors["no"])
print("Town of the company:")
town = input(colors["red"]+"> "+colors["no"])
print("Street and No. of the company:")
street_and_no = input(colors["red"]+"> "+colors["no"])
street = street_and_no.split(" ")[0]
if len(street_and_no.split(" "))>1:
    street_no = street_and_no.split(" ")[1]
else:
    street_no = ""

# Custom Words
print("Do you want to add other words to the base wordlist? Add each one by pressing Enter. Press Enter without any input to start generating the wordlist.")
other_words = []
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
write_array_to_file(rules,"hashgen.rule")

print("Generated wordlist has " + str(len(candidates)) + " entries and is " + str(sys.getsizeof(candidates) / 1024).split(".")[0] + " kB large.")
print("Combined with the hashgen rules this creates " + str(len(candidates)*len(rules)) + " passwords.")
print()

print("How to use it to crack different hashes:")
print(colors["red"]+"NTLM "+colors["blue"]+"hashcat -m 1000 hashes.txt "+filename+" -r hashgen.rules")