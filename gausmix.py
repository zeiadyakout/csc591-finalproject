import processdata as proc
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

data, x, y = proc.processWine()

# gaussian mix fit and predict
gmm = GaussianMixture(n_components=3)
clusters = gmm.fit_predict(x)

# pca setup 
pca = PCA(n_components=2)
pcs = pca.fit_transform(x)
df = pd.DataFrame(data=pcs, columns=['PC1', 'PC2'])

# plot
plt.scatter(df['PC1'], df['PC2'], c=clusters)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Gaussian Mix Clusters Visualized using PCA and GMM')
plt.show()
