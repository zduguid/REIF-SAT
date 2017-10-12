# REIF-SAT Image Processing


The goal of the Rectangular Earth-Imaging Fast-Spinning Aperture Telescope (REIF-SAT) project is to demonstrate the feasibility of a spinning-aperture space telescope that is capable of achieving high resolution images. REIF-SAT is the deliverable of MIT's Aerospace Engineering capstone course: 16.83 - Space Systems Engineering. In order to demonstrate the feasiblity of a spinning-aperture space telescope, we must develop image processing algorithms that can combine a series of frames into a final synthesized image. 


Our first approach is to implement a version of the Minimum Mean Square Error (MSE) algorithm that is to run on a set of test images. The general process underlying this approach can be found below:

1. Take the two-dimensional Fourier Transform of aperture pattern (pupil mask) 
2. Multiply this transform by it's complex conjugate (this is known as the auto-correlation)
3. Take the inverse Fourier Transform (results in Modulation Transfer Function, or MTF, in spatial frequency)
4. Take Fast Fourier Transform (FFT) of our intended image, multiply pairwise with MTF, take inverse FFT to get the resulting frame. (here, we are creating the individual image frames)
5. Rotate the MTF and repeat this to achieve the desired number of frames
6. Perform Weiner-deconvolution: sum frames in frequency domain and multiply the sum by the average of all the MTF functions




Some of our ongoing concerns include:

[ ] Formalize run time analysis of image processing algorithm
[ ] Intentionally introduce noise into the image processing algorithms to demonstrate robustness
[ ] Assess accuracy and runtime trade-offs of different image processing algorithms 
[ ] Assess radial smear due to rotation during exposure
[ ] Make comparison between synthesized image and circular aperture equivalent (potentially using color histogram vector methods)
[ ] Compare different image estimate methods for PMAP alogorithm (first frame vs. composite frame)
[ ] Compare PMAP with Weiner-Filtering method 
[ ] Analyze the trade-off between number of frames and final synthesized image quality (seems like 15 frames should be enough to achieve high resolution image)
[ ] Quantify jitter in terms of pixel blur
[ ] Analyze the error caused by imaging a rapidly moving scene
[ ] Georegistrate each of the frames in orde to apply appropriate image rotation (handle the spinning camera effect)
[ ] Look into different spin speeds to handle different SNR ratios



