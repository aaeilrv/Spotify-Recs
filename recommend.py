import pandas as pd
from kmeans import Kmeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

df = pd.read_csv('./data.csv')
user_songs, recommended_pool = train_test_split(df, test_size=0.2)
user_songs = user_songs.drop(columns=['id', 'name', 'artist'])

# inertia = []
# for k in range(1,10):
#     model = Kmeans(train, k, 0.001)
#     clusters = model.clustering(1000)
#     inertia.append(model.get_inertia(clusters))

# plt.plot(range(1,10), inertia, 'bx-')
# plt.xlabel('Cantidad de clusters (k)')
# plt.ylabel('Inercia')
# plt.title('Elbow Method')
# plt.show()

# inertia = np.array([inertia[i-1] - inertia[i] - (inertia[i]-inertia[i+1]) for i in range(1, len(inertia)-1)])
k = 5#np.argmax(inertia)+1

model = Kmeans(user_songs, k, 0.001)
clusters = model.clustering(1000)

cluster_percentages = [(clusters == i).sum()/len(clusters) for i in range(k)]

n_reccomended = 20
recommended_proportion = [round(n_reccomended*i) for i in cluster_percentages]
recommended_clusters = np.array([model.assign(i) for i in recommended_pool.drop(columns=['id', 'name', 'artist']).values])

indexes = []
for cluster in range(k):
    cluster_indexes = np.argwhere(recommended_clusters==cluster).flatten()
    random_indexes = np.random.choice(cluster_indexes, size=(1,recommended_proportion[cluster]), replace=False).flatten()
    indexes = np.concatenate((indexes, random_indexes))

print(indexes)
print(recommended_pool.iloc[indexes,:])

