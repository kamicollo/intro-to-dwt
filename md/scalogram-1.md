## Interpreting DWTs

So far, we saw that DWT is useful in de-noising signal data and can be used as a compression technique (hopefully you can now wavelet applications in image compression, such as JPEG2000 mentioned earlier).

But are the DWT coefficients meaningful in representing the signal beyond that? Could we treat them as **features that represent structural signal patterns**?

### Problem statement

Remember what was the signal used in the examples so far? It's a sweep of signal quality accross a wide frequency range that cable companies can use to remotely detect issues. The signal we were working so far was unimpaired. Here are a few examples of impaired signals. 