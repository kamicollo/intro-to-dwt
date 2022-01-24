### An important implementation note

You want to rely on sparse structures as much as possible when working with thresholded DWT coefficients! Here is an illustration:

 1. Let's assume you already performed DWT and have a Pandas dataframe where each row represents a signal, with its thresholded DWT coefficients stored as a lattened list.
 2. Then, let's create two matrices where rows represent signals and columns represent coefficients - a sparse and a dense version
 3. Then, let's run hierarchical clustering with identical parameters but different approaches:
     * In the one case, we will use `pairwise_distances` function from `scikit-learn` that supports sparse matrices to compute pairwise distances which we will pass to the clustering algorithm.
     * In the other case, we will simply pass the dense matrix to the clustering algorithm (we could also precompute distances for a like-for-like comparison, but that is even slower and unnecessary).

I include code example below. In my tests with 1000 signals, the code leveraging sparse matrix performed 3x as fast when coefficients were thresholded at 95% level and **10-15x as fast with 99% thresholding level.** 