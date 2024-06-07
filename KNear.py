from sklearn.neighbors import NearestNeighbors
import numpy as np

def main(query, dataset,selected_data, k=10, distance_metric='euclidean'):
    # Convert data into numpy arrays
    X = np.array(selected_data)
    query1 = np.array([query[1:]])

    # Initialize the k-NN model
    nn = NearestNeighbors(n_neighbors=k, metric=distance_metric)

    # Fit the model with the list of tuples
    nn.fit(X)

    # Find k closest tuples
    distances, indices = nn.kneighbors(query1)

    # Return the k closest tuples
    closest_tuples = [dataset[i] for i in indices[0]]

    return closest_tuples
