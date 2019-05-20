#####################################################################################################
# Name: Kristopher Carroll
# CSCE A311
# Extra Credit Assignment
# Purpose: Generate random text based on Markov states created from user-defined orders of n-grams
#           and user-defined source text serving as the corpus.
# Data Structures: Python dict (hashmap) with n-gram keys and list of possible next characters as
#                   values for text prediction
#                  List of possible n-grams used to start a sentence used to begin resulting text
#                   generation to ensure proper grammar.
# Runtime: Populating n-grams from corpus text runs in O(n) time where n is the number of characters
#           in the corpus as a sliding window of order n is used to populate a dict with possible
#           n-grams and their associated Markov states for successive characters. Generating
#           predictive text runs in expected O(1) time to access n-gram keys in n-gram dict
#           but runs k times where k is the number of characters of text the user wishes to generate.
#          Overall runtime is thus O(n + k) where n is the number of characters in the corpus and
#           k is the number of characters of text the user wishes to generate.
# Space complexity: O(n) space used for all lists where n is the number of items in the list
#                     Documentation and discussion of Python dict hashmapping suggests space is
#                       between (3/2)*n and 2n depending on load of hashmap at n entries
# Comments on outputs: With smaller orders used for the n-grams used to populate the Markov state
#                       machine, variability of text generated increases. Monograms or bi-grams (order
#                       1 and 2 respectively) will generate text containing many words likely
#                       not found in the corpus text as words are generated around smaller combinations
#                       of characters. As order of the n-gram used increases, variability of output
#                       text decreases as fewer possible values exist following each successive n-gram.
#####################################################################################################
import random

n_gram_order = 0;
n_grams = {}
starting_grams = []
text_options = [("Alice and Wonderland", "alice.txt"),
                ("Romeo and Juliet", "romeoandjuliet.txt"),
                ("C++ Implementation of Red Black Tree", "redblack.txt")]

####################################################
# Function: load_grams()
# Inputs: string for filename, int for order of n-gram=
# Outputs: None
# Purpose: Populate the n_grams and starting_grams dict with input from the source file
####################################################
def load_grams(filename, n_gram_order):
    with open(filename, "r") as f:
        text = f.read()
        index = 0
        # Parse n-grams from text as well as next character
        while index + n_gram_order < len(text):
            n_gram = text[index:(index + n_gram_order)]
            n_gram_next = text[index + n_gram_order]
            # Checking if n_gram is already in n_grams dictionary
            if n_gram in n_grams:
                n_grams[n_gram].append(n_gram_next) # append to next list if n_gram found
            else:
                n_grams[n_gram] = [n_gram_next] # add n_gram to n_grams dictionary
            # If n_gram starts a sentence (capital letter followed by a lowercase letter)
            if len(n_gram) > 1:
                if n_gram[0].isupper() and n_gram[1].islower():
                    starting_grams.append(n_gram) # add it to starting_grams for creation of text later
            elif n_gram[0].isupper():
                starting_grams.append(n_gram)
            index += 1

####################################################
# Function: generate_text
# Inputs: int for desired text length, optional boolean for textfile generation
# Outputs: string for random text
# Purpose: Generates random text using Markov probability of possible options following
#           each progressive n-gram generated. Always starts from an n-gram in the form of
#           the beginning of a sentence. Can generate a textfile for the generated text
#           sample by specifying True for the optional parameter.
####################################################
def generate_text(text_length, text_create = False):
    current_gram = random.choice(starting_grams)
    result = current_gram
    for i in range(text_length):
        possibilities = n_grams[current_gram]
        next = random.choice(possibilities)
        result += next
        current_gram = result[len(result)-n_gram_order: len(result)]
    print(result)
    # Generate sample textfile if specified
    if text_create:
        f = open(text_options[choice - 1][1].split('.')[0] + "order" + str(n_gram_order) + ".txt", "w+")
        f.write(result)

print("Welcome to the Markov Text Generator!")
# Ask the user for the order of the n-gram to be used to parse text
while n_gram_order <= 0 or n_gram_order > 100:
    n_gram_order = int(input("Enter the order of n-gram you'd like to use (integer > 0): "))
    # order must be greater than 0
    if int(n_gram_order) <= 0:
        print("Order must be an integer greater than zero.")
    # discourage overly large orders as this just causes the text to be reprinted with no variability
    elif int(n_gram_order) > 100:
        print("Excessively large order values will produce very low variability. Try something smaller.")
    print()

# Ask user to pick which source text to use for populating n_grams dict
print("Please select from the following text sources to generate your text.")
for index, option in enumerate(text_options):
    print("  " + str(index + 1) + ": ", text_options[index][0])
choice = 0
while choice < 1 or choice > 3:
    choice = int(input("Enter a value from 1-3: "))
print()

# Load n-grams for chosen corpus text
print("Loading", text_options[choice - 1][0] + "...")
load_grams(text_options[choice - 1][1], n_gram_order)
print("Done.\n")

# Ask user for desired length of Markov text to be generated
text_length = int(input("Enter the desired text length to be generated: "))

#generate_text(text_length, True) # uncomment to generate textfiles for resulting text
