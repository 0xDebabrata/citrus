import citrusdb
import json

# Instantiate citrusdb
citrus = citrusdb.Client()

# Create index
citrus.create_index(
    name="pokemon",
    max_elements=50,
)

pokemons = []
documents = []
ids = []
with open("demo/pokemon.jsonl", "r") as f:
    for line in f:
        pokemon = json.loads(line)
        pokemons.append(pokemon)
        documents.append(pokemon["info"]["description"])
        ids.append(pokemon["info"]["id"])

# Insert documents to index
citrus.add("pokemon", ids, documents=documents)
citrus.get_status("pokemon")

citrus.delete_vectors("pokemon", ["143"])

# Query with a text input
res = citrus.query(
    "pokemon",
    documents=["Likes to sleep"],
    k=5
)

def find_pokemon(id):
    for pokemon in pokemons:
        if (pokemon["info"]["id"] == int(id)):
            print(format(pokemon))
            break
def format(pokemon):
    return f"""Name: {pokemon["name"]}
Pokedex ID: {pokemon["info"]["id"]}
Type: {pokemon["info"]["type"]}
Description: {pokemon["info"]["description"]}
"""

if res:
    ids_list, distances = res

    # Print results
    for ids in ids_list:
        for id in ids:
            find_pokemon(id)
