import processdata as proc
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA

data, x, y = proc.processWine()
# dbscan fit and predict
dbscan = DBSCAN(eps=3, min_samples=25)
clusters = dbscan.fit_predict(x)

# pca setup
pca = PCA(n_components=2)
pcs = pca.fit_transform(x)
df = pd.DataFrame(data=pcs, columns=['PC1', 'PC2'])

# plot
plt.scatter(df['PC1'], df['PC2'], c=clusters)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Clusters Visualized using PCA and DBSCAN')
plt.show()
