### How DWT works

To repeat, Discrete Wavelet Transformation, in a nutshell, is a decomposition of a signal into multiple components represented by a base wavelet shape. This is achieved by "fitting" the base signal shape at different resolution levels.

In very crude terms: take a signal and divide into 2 equal parts, and fit the base wavelet shape to each, obtaining associated coefficients. Then, split each of those 2 parts into two further parts, and repeat the process until the individual windows include just enough data points to fit a base wavelet. E.g., if a signal has 1024 data points, you can fit up to 10 levels of Haar wavelet, 8 levels of Daubechies 2 wavelet or 5 levels of Daubechies 16 wavelet.

If you prefer a more robust mathematical definition, a couple of great resources I can recommend include [Wavelets for kids](http://www.isye.gatech.edu/~brani/wp/kidsA.pdf) by Brani Vidakovic and Peter Mueller (trust me, it's not for kids..), [Matlab's Wavelet Toolbox documentation](https://www.mathworks.com/help/wavelet/getting-started-with-wavelet-toolbox.html?s_tid=CRUX_lftnav) and [A Concise Introduction to Wavelets](https://rafat.github.io/sites/wavebook/intro/intro.html).

### A practical example

In this guide, I will be using signal data obtained via Full Band Capture (FBC) sweeps in cable modems. This data effectively shows the quality of a signal across 6-1026MHz spectrum at the consumer end of a cable network. It allows cable providers to remotely identify transmission issues. It's a pretty cool technology - you can learn more about it in this [easy-to-digest blog post](https://broadbandlibrary.com/full-band-capture-revisited/).

Here's an example signal.

