### Thresholding least important coefficients

**Warning: magic ahead!**

In practice, you don't want to be setting entire resolution levels to zero. Instead, you will want to preserve the largest absolute coefficient values. 

Below, you can do exactly that - pick a % of the overall coefficients to be preserved, and see how a reconstructed signal looks like. This is referred to as "hard thresholding" in the DWT literature. 

 Don't be surprised that you don't see any differences before you enter 90%+ territory. That is how amazing DWT is. 