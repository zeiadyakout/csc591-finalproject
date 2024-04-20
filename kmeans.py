import processdata as proc
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score

data, x, y = proc.processWine()
# kmeans fit and predict
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(x)

# pca setup 
pca = PCA(n_components=2)
pcs = pca.fit_transform(x)
df = pd.DataFrame(data=pcs, columns=['PC1', 'PC2'])

# plot
plt.scatter(df['PC1'], df['PC2'], c=clusters)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('KMeans Clusters Visualized using PCA')
plt.show()