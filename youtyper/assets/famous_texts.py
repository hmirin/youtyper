from importlib.resources import read_text

universal_declaration_of_human_rights_text = read_text(
    "youtyper.assets", "universal_declaration_of_human_rights.txt"
)

# https://ja.wikipedia.org/wiki/%E3%83%91%E3%83%B3%E3%82%B0%E3%83%A9%E3%83%A0
pangrams_text = read_text(
    "youtyper.assets", "universal_declaration_of_human_rights.txt"
)
