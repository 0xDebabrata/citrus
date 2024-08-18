# 🍋 citrus.
### open-source (distributed) vector database

## Installation

```bash
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
  name="example",
  max_elements=1000,            # increases dynamically as you insert more vectors
)
```

#### 2. Insert elements
```py
ids = [1, 2, 3]
documents = [
  "Your time is limited, so don't waste it living someone else's life",
  "I'd rather be optimistic and wrong than pessimistic and right.",
  "Running a start-up is like chewing glass and staring into the abyss."
]

citrus.add(index="example", ids=ids, documents=documents)
```
You can directly pass vector embeddings as well. If you're passing a list of strings like we have done here, ensure you have your `OPENAI_API_KEY` in the environment. By default we use OpenAI to to generate the embeddings. Please reach out if you're looking for support from a different provider!

#### 3. Search
```py
results = citrus.query(
    index="example",
    documents=["What is it like to launch a startup"],
    k=1,
    include=["document", "metadata"]
)

print(results)
```
You can specify if you want the associated text document and metadata to be returned.
By default, only the IDs are returned.

Go launch a repl on [Replit](https://replit.com) and see what result you get after running the query! `result` will contain the `ids` of the top `k` search hits.

## Example
[chat w/ replit ai podcast](https://replit.searchcitrus.com)

[pokedex search](https://replit.com/@debabratajr/pokedex-search)

## Facing issues?
Feel free to open issues on this repository! Discord server coming soon!

*PS: citrus isn't fully distributed just yet. We're getting there though ;)*

---

<p align="center">
  Special thanks to
</p>
<p align="center">
  <img align="center" src="https://www.getdevkit.com/logo.png" width=100 height=100 alt="DevKit" />
</p>
<p align="center">
  <a href="https://www.getdevkit.com">DevKit - The Essential Developer Toolkit</a><br />
  DSoC 2023
</p>
