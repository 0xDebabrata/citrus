import citrusdb
import numpy as np
import json

# Instantiate citrusdb
citrus = citrusdb.Client()

# Create index
citrus.create_index(
    name="pokemon",
    max_elements=50,
    persist_directory="demo/db"
)

pokemons = []
documents = []
with open("demo/pokemon.jsonl", "r") as f:
    for line in f:
        pokemon = json.loads(line)
        pokemons.append(pokemon)
        documents.append(pokemon["info"]["description"])


ids = np.arange(len(documents))

# Insert documents to index
#citrus.add("pokemon", ids, documents=documents)
citrus.get_status("pokemon")

# Query with a text input
res = citrus.query(
    "pokemon",
    documents=["Likes to sleep", "eats bugs"],
    k=5
)

if res:
    results, distances = res

def format(pokemon):
    return f"""Name: {pokemon["name"]}
Pokedex ID: {pokemon["info"]["id"]}
Type: {pokemon["info"]["type"]}
Description: {pokemon["info"]["description"]}
"""

# Print results
for res in results:
    for id in res:
        print(format(pokemons[id]))
