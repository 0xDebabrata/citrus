import citrusdb
import numpy as np

citrus = citrusdb.Client()

citrus.create_index(max_elements=100)

documents = [
        "Apple is a great company",
        "An apple a day keeps the doctor away",
        "The weather is fking hot today"
        ]

ids = np.arange(3)

citrus.add(ids, documents=documents)

labels, distances = citrus.query("Name a fruit", k=2)

for i in range(0, len(labels)):
    print(documents[labels[i]])
