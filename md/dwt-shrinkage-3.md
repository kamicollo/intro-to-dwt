Thresholding is a trade-off between signal reconstruction accuracy and "space" required to represent it. While in some applications you may want to choose the threshold directly like you did above (by, say, targetting a certain reconstruction error), in other cases you may be simply interested in an optimal trade-off. Several methods have been proposed in academic literature, with SureShrink and VisuShrink known the most widely.

I was lucky to learn about wavelets in a Georgia Tech's class taught by Proffesor [JC Lu](https://www.isye.gatech.edu/users/jye-chyi-lu) who co-wrote a paper ([PDF](https://smartech.gatech.edu/bitstream/handle/1853/25856/04-11.pdf)) comparing different optimal threshold selection methods. The paper shows that the optimal threshold that performs the best can be defined as follows:

$$\lambda = \left( \frac{1}{N} \sum_{i=1}^{N}d_i^2 \right)^{1/2}$$ where $d_i$ is the $i^{th}$ coefficient out of N. 

So in case you ever need an optimal threshold, I suggest you use this method (called $RRE_h$) instead!

Now, onto the final part of the journey.