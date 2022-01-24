### Clustering

 Given it's a very sparse dataset (we only use 5% of ~8700 coefficients for each signal), ideal clustering candidates are algorithms that can work with sparse matrix representations. [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/) is one of them.

In this example, we will go ahead with a simple hierarchical (aglomerative) clustering with a complete linkage function, though. While it is a bit slower, it gives us control over distance threshold to be used which allows us more easily control how comparable the clusters are to each other. 

Why hierarchical clustering in this case to begin with? Well, impairment in signals are often introduced by upstream devices. So when you look at the signal patterns at the customer locations, they may be impacted by multiple impairments introduced by devices the signal passed on its way. Hierarchical clustering helps us recreate such an impairment structure.

Below I illustrate the dendogram created with hierarchical clustering algorithm and using 95% thresholding (I picked a cut-off value to have a reasonable number of clusters for illustration purposes).   