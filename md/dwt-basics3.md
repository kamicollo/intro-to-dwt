Let's go ahead and decompose this signal with DWT. I'll use Daubechies 2 wavelet as the base wavelet. How do you pick a base wavelet? It depends on your signal patterns and the goal of your analysis. [Matlab's documentation](https://www.mathworks.com/help/wavelet/gs/choose-a-wavelet.html) includes practical tips on how to think about wavelet selection.

Below you can see the size of the coefficients visualized. Observe that the coefficients become increasingly indistinguishable from zero at finer resolution levels. That implies that they are not *that* important in reconstructing the signal. That's an interesting observation! Time to move on to talk about coefficient shrinkage (thresholding).



