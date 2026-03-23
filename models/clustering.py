from river import cluster

def get_clustering_model():
    """
    Returns a River clustering model for incremental learning.
    KMeans is used as an example.
    """
    model = cluster.KMeans(n_clusters=5, halflife=0.5, sigma=1.5, seed=42)
    return model
