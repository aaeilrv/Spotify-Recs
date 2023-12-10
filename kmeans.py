import pandas as pd
import numpy as np

class Kmeans:
    def __init__(self, data, k, min_diff):
        self.data = data
        self.data_size = self.data.shape[-1]
        self.k = k
        self.centroids = None
        self.min_diff = min_diff

    def distance(puntos, centroides):
        '''Calcula la distancia entre los puntos y los centroides'''
        return np.sqrt(np.sum((centroides - puntos) ** 2, axis = 1))

    def clustering(self, max_iter):
        '''Realiza el clustering de los datos'''
        max_val = np.amin(self.data, axis = 0)
        min_val = np.amax(self.data, axis = 0)

        self.centroids = np.random.uniform(max_val, min_val, size=(self.k, self.data_size))

        for _ in range(max_iter):
            cluster_labels = [] # Guarda el índice del cluster al que pertenece cada punto

            for punto in self.data.values:
                distances = Kmeans.distance(punto, self.centroids)
                asignacion_a_centroide = np.argmin(distances) # se asigna el punto al centroide mas cercano
                cluster_labels.append(asignacion_a_centroide)

            cluster_labels = np.array(cluster_labels)
            
            # se guarda el valor de los puntos que hay en cada cluster
            cluster_index = []
            for i in range(self.k):
                cluster_index.append(np.argwhere(cluster_labels == i))

            # se calcula el nuevo centroide de cada cluster
            cluster_centers = []
            for i, index in enumerate(cluster_index):
                if len(index) == 0:
                    cluster_centers.append(self.centroids[i])
                else:
                    cluster_centers.append(np.mean(self.data.values[index], axis = 0)[0])

            if np.max(self.centroids - np.array(cluster_centers)) < self.min_diff:
                break
            else:
                #reasignar los centroides
                self.centroids = np.array(cluster_centers)

        return cluster_labels
    
    def assign(self, x):
        return np.argmin(Kmeans.distance(x, self.centroids))
    
    def get_inertia(self, cluster_labels):
        inertia = 0
        for i in range(self.k):
            cluster_points = self.data.values[cluster_labels == i]
            centroid = self.centroids[i]
            inertia += np.sum(Kmeans.distance(cluster_points, centroid)**2)
        return inertia