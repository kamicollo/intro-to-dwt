Let's see if we can use DWT coefficients to detect differences between such signals.

### Scalograms

First tool we can use is called a **scalogram**. When playing around with thresholding, you probably got a sense that different resolution levels capture different aspects of the signal. We can think of coefficients as "energy" captured at different resolutions. What if we threshold coefficients to reduce noise, sum energy at each resolution level and visualize it? 

Here's how it looks (at 95% thresholding level) - you can see that differentiating between signals is possible from the scalogram alone in some cases, though it is definitely not clear-cut in others.