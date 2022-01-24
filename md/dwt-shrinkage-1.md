## DWT shrinkage (thresholding)

### Impact of thresholding resolution levels

We've seen that a lot of obtained DWT coefficients in the finer resolution levels are small, implying that they may not contribute much to the overall signal. 

To get a better sense of that, let's try setting individual resolution levels of the coefficients to zero and reconstructing the signal. This should also give you a better sense of what different resolution levels are able to capture for this particular signal. 

A side note: you may come across multi-resolution analysis (MRA) in wavelets. It's a plot that shows reconstructed signal from each of the resolution levels individually, providing an overview of how each resolution level coefficients contribute to the signal.