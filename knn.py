import numpy as np

class KNN:
    def __init__(self, k):
        self.k = k
        self.points = None

    def eucledian_distance(p, q):
        return np.sqrt(np.sum((p - q) ** 2, axis = 1))

    def fit(self, points):
        self.points = points

    def predict(self, new_point):
        distances = []
        
        for category in self.points:
            for point in self.points[category]:
                distance = KNN.eucledian_distance(point, new_point)
                distances.append([distance, category])

        categories = [category[1] for category in sorted(distances)[:self.k]]

        result = Counter(categories).most_common(1)[0][0]
        return result