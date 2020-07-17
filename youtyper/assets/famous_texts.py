from importlib.resources import read_text

universal_declaration_of_human_rights_text = read_text(
    "youtyper.assets", "universal_declaration_of_human_rights.txt"
)

# https://ja.wikipedia.org/wiki/%E3%83%91%E3%83%B3%E3%82%B0%E3%83%A9%E3%83%A0
pangrams_text = read_text("youtyper.assets", "pangrams.txt")

# http://phrasesinenglish.org/explore.html
# "Phrases in English" (PIE) incorporates data from the British National Corpus,
# but is not affiliated with it. This site was developed by William H. Fletcher
# of the US Naval Academy in consultation with Michael Stubbs
# of the University of Trier. Development was funded in part by
# the Naval Academy Research Council. To help ensure continued support for
# this and follow-on projects, users are kindly requested to cite it
# by name and URL in their work and to provide the developer bibliographic data
# and electronic copies of any publications or papers which use data from this site.
common_english_6_grams = read_text("youtyper.assets", "common_english_6_grams.txt")
