import processdata as proc
import pandas as pd
import matplotlib.pyplot as plt
from sklearn_extra.cluster import KMedoids
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score

data, x, y = proc.processWine()
# kmeans fit and predict
kmedoids = KMedoids(n_clusters=3)
clusters = kmedoids.fit_predict(x)

data['Clusters'] = clusters

for i in range(3):
    clustered_data = data[data['Clusters'] == i]
    clustered_data = clustered_data.drop(columns=['Clusters'])
    clustered_data.to_csv("clusteredData/kmedoids_wine" + str(i) + ".csv ", index=False)

# pca setup 
pca = PCA(n_components=2)
pcs = pca.fit_transform(x)
df = pd.DataFrame(data=pcs, columns=['PC1', 'PC2'])

# plot
plt.scatter(df['PC1'], df['PC2'], c=clusters)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('KMedoids Clusters Visualized using PCA')
plt.show()