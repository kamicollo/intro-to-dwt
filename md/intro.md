>"Any sufficiently advanced technology is indistinguishable from magic"

> *- Arthur C. Clarke*

The first time I learned about discrete wavelet transformation (DWT), it struck me exactly as that. **Magic**. An approach to take highly noisy data, approximate it using only 5% of the original data points and still recover the underlying data pattern? Impossible!

Alas, it works and is highly useful for anyone working with signal-like data. DWT can be used to remove noise from the signal, reduce dimensionality of the data, and can also be directly used for tasks such as clustering or classification. Fun fact: wavelet transformation is a behind data compression of [JPEG2000](https://en.wikipedia.org/wiki/JPEG_2000) image format and FBI's methodology for [storing fingerprints](https://en.wikipedia.org/wiki/Wavelet_scalar_quantization).

However, finding practical, easy to follow information on how DWT works and how to use it real life is not easy. This guide aims to fill the gap. I won't delve deep into the mathematics (because, frankly, I don't fully follow it myself); instead, I will focus on intuition and practical examples.

Ready? Put on your invisibility cloak and let's go.

P.S. Best viewed on a laptop / a larger screen!
