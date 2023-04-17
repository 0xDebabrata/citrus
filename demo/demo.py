import citrusdb
import numpy as np
import json

# Instantiate citrusdb
citrus = citrusdb.Client()

# Create index
citrus.create_index(max_elements=1000)

pokemons = []
documents = []
with open("demo/pokemon.jsonl", "r") as f:
    for line in f:
        pokemon = json.loads(line)
        pokemons.append(pokemon)
        documents.append(pokemon["info"]["description"])


ids = np.arange(len(documents))

# Insert documents to index
citrus.add(ids, documents=documents)

# Query with a text input
results, distances = citrus.query("Has multiple forms of evolution", k=5)

def format(pokemon):
    return f"""Name: {pokemon["name"]}
Pokedex ID: {pokemon["info"]["id"]}
Type: {pokemon["info"]["type"]}
Description: {pokemon["info"]["description"]}
"""

# Print results
for i in range(0, len(results)):
    print(format(pokemons[results[i]]))
