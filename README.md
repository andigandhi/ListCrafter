```
 _    _    _    ___           __ _           
| |  (_)__| |_ / __|_ _ __ _ / _| |_ ___ _ _ 
| |__| (_-<  _| (__| '_/ _` |  _|  _/ -_) '_|
|____|_/__/\__|\___|_| \__,_|_|  \__\___|_|  

generate custom wordlists for cracking hashes in company networks
```

# Usage
```
usage: ListCrafter [-h] [-c THE COMPANIES NAME] [-t THE TOWN OF THE COMPANY] [-s THE STREET OF THE COMPANY] [-o [OTHER IMPORTANT KEYWORDS BRANCH,...) ...]] [-l THE LEVEL OF VERBOSITY OF THE WORDLIST (0-3)]
               [-H THE FILE CONTAINING THE HASHES (FOR AUTO-CRACKING]

This script creates a custom wordlist for cracking hashes in company networks

options:
  -h, --help            show this help message and exit
  -c THE COMPANIES NAME, --company THE COMPANIES NAME
  -t THE TOWN OF THE COMPANY, --town THE TOWN OF THE COMPANY
  -s THE STREET OF THE COMPANY, --street THE STREET OF THE COMPANY
  -o [OTHER IMPORTANT KEYWORDS (BRANCH,...) ...], --other [OTHER IMPORTANT KEYWORDS (BRANCH,...) ...]
  -l THE LEVEL OF VERBOSITY OF THE WORDLIST (0-3), --level THE LEVEL OF VERBOSITY OF THE WORDLIST (0-3)
  -H THE FILE CONTAINING THE HASHES (FOR AUTO-CRACKING), --hashes THE FILE CONTAINING THE HASHES (FOR AUTO-CRACKING)
```

# Example Wordlist
```
# ./ListCrafter.py -c GitHub -t SanFrancisco -s "Street 1337" -o Code Microsoft
  _    _    _    ___           __ _           
 | |  (_)__| |_ / __|_ _ __ _ / _| |_ ___ _ _ 
 | |__| (_-<  _| (__| '_/ _` |  _|  _/ -_) '_|
 |____|_/__/\__|\___|_| \__,_|_|  \__\___|_|  

generate custom wordlists for cracking hashes in company networks


Generating wordlist for GitHub based in SanFrancisco...

Generated wordlist has 198 entries and is 1 kB large.
Combined with the ListCrafter rules this creates 1386 passwords.

How to use it to crack different hashes:
NTLM hashcat -m 1000 hashes.txt wordlist_GitHub_2024.wordlist -r ListCrafter.rules
DCC2 hashcat -m 2100 hashes.txt wordlist_GitHub_2024.wordlist -r ListCrafter.rules
```

```
# shuf -n 5 wordlist_GitHub_2024.wordlist

GitHub23
MICROSOFT
Code2024
sanfrancisco24
GitHub.2024
```

# Roadmap
- ☑️ Create basic wordlist
- ☑️ Create hashcat ruleset
- ⬜️ Add english language support
- ⬜️ Extract information from WiFi?
- ⬜️ ??