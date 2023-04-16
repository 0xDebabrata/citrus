import citrusdb
import numpy as np

citrus = citrusdb.Client()

citrus.create_index(max_elements=100)

vector = []
ids = np.arange(100)
for j in range(0, 100):
    arr = []
    for i in range(0, 1536):
        arr.append(np.random.random())
    vector.append(arr)

citrus.add(vector, ids)
citrus.query(vector[5], 5)




'''
dim = 128
num_elements = 10000

# Generate sample data
data = np.float32(np.random.random((num_elements, dim)))
ids = np.arange(num_elements)

# Declare index
p = hnswlib.Index(space = 'cosine', dim = dim)

p.init_index(max_elements=num_elements, ef_construction=200, M=16)

p.add_items(data, ids)

p.set_ef(50)

labels, distances = p.knn_query(data, k = 1)
#print("Recall for the first batch:", np.mean(labels.reshape(-1) == np.arange(len(data))), "\n")
'''
