# citrus.
### open-source (distributed) vector database

<p align="center">
  Special thanks to
</p>
<p align="center">
  <img align="center" src="https://www.getdevkit.com/logo.png" width=150 height=150 alt="DevKit" />
</p>
<p align="center">
  <a href="https://www.getdevkit.com">DevKit - The Essential Developer Toolkit</a><br />
  DSoC 2023
</p>


## Installation

```
pip install citrusdb
```

## Getting started

#### 1. Create index
```py
import citrusdb

# Initialize client
citrus = citrusdb.Client()

# Create index
citrus.create_index(
  max_elements=1000,            # increases dynamically as you insert more vectors
  persist_directory="/db"       # save data and load index from disk
)
```

#### 2. Insert elements
```py
ids = [1, 2, 3]
docuemnts = [
  "Your time is limited, so don't waste it living someone else's life",
  "I'd rather be optimistic and wrong than pessimistic and right.",
  "Running a start-up is like chewing glass and staring into the abyss."
]

citrus.add(ids, documents=documents)
```
You can directly pass vector embeddings as well. If you're passing a list of strings like we have done here, ensure you have your `OPENAI_API_KEY` in the environment. By default we use OpenAI to to generate the embeddings. Please reach out if you're looking for support from a different provider!

#### 3. Search
```py
result, distances = citrus.query("What is it like to launch a startup", k=1)
```
Go launch a repl on [Replit](https://replit.com) and see what result you get after runnig the query! `result` will contain the `ids` of the top `k` search hits.

## Example    dfsdfsdfsdfsdsdfsdfs
[pokedex search](https://replit.com/@debabratajr/pokedex-search)
