# REIF-SAT Image Processing


The goal of the Rectangular Earth-Imaging Fast-Spinning Aperture Telescope (REIF-SAT) project is to demonstrate the feasibility of a spinning-aperture space telescope that is capable of achieving high resolution images. REIF-SAT is the deliverable of MIT's Aerospace Engineering capstone course: 16.83 - Space Systems Engineering. In order to demonstrate the feasiblity of a spinning-aperture space telescope, we must develop image processing algorithms that can combine a series of frames into a final synthesized image. 


### Our first approach is to implement a version of the Minimum Mean Square Error (MSE) on a single test image. To simulate the effect of the rectangular aperture, individual frames are generated from this single test image, and then the frames are synthesized using a simplified version of the MSE algorithm. The general process underlying this approach can be found below:

1. Frame Generation
    1. Take the two-dimensional Fast Fourier Transform (FFT) of of the pupil mask 
    2. Multiply this transform by it's complex conjugate to yield the auto-correlation function
    3. Take the inverse FFT (iFFT) of the autocorrelation function to yield the modulation transfer function (MTF), which is a complex-valued array in the spatial domain 
    4. Take the FFT of the test image and multiply with the MTF, and then take the iFFT of the result to yield an individual frame
    5. Rotate the pupil mask by some angle and repeat this process to produce the desired number of frames

2. Image Synthesis
    1. Perform a simplified version of the MSE algorithm by implementing Wiener-deconvolution: sum the individual frames in frequency domain, multiply this sum by the average MTF function, and then finally take the iFFT of the result to yield a single synthesized image in the spatial domain 


### Assumptions:
* Image processing can be implemented on grayscale images to boost runtime, and the synthesis results can easily be extended to colored images
* White (255 on grayscale) represents mirror surface, black (0 on grayscale) represents a lack of mirror surface


### Some helpful NumPy and OpenCV commands:
* Read in image file in black and white:
    * ```img = cv2.imread('img_file', 0)```
* Read in image file in color:
    * ```img = cv2.imread('img_file', 1)```
* Split color channels of a color image:
    * ```b,g,r = cv2.split(img)```
* Merge color channels into one array:
    * ```rgb = cv2.merge([r,g,b])```
* Get the dimensions of an image: 
    * ```print(img.shape)```
* Convert the image file from spatial domain to frequency domain:
    * ```freq_img = np.fft.fft2(img)```
* Convert the image file from frequency domain to spatial domain:
    * ```img = np.fft.ifft2(freq_img)```
* Get complex conjugate of frequency domain array:
    * ```conj = np.conjugate(freq_img)```
* Shift an image in the frequency domain:
    * ```fshift = np.fft.fftshift(freq_img)```


### Some of our ongoing concerns include:

- [ ] Formalize run time analysis of image processing algorithm
- [ ] Introduce noise into different stages of the image processing algorithms to demonstrate robustness
    - [ ] Quantify jitter in terms of pixel blur
    - [ ] Quantify radial smear due to rotation during exposure
    - [ ] Quanitfy error created by a rapidly evolving scene
    - [ ] Determine how to georegistrate frames and rerotate frames in the event of a moving camera
- [ ] Compare and contrast image processing algorithms, namely MSE and PMAP
    - [ ] Compare single frame PMAP (SF-PMAP) and multi frame PMAP (MF-PMAP)
    - [ ] Compare different methods of selecting the initial image estimate when using the PMAP algorithm
- [ ] Assess methods used to compare the synthesized image and the circular aperture equivalent image
    - [ ] Histogram method that take advantage of vector math
    - [ ] Pixel-to-pixel direct comparison method
    - [ ] Perceptual hash (pHash) method
    - [ ] Keypoint Matching method, that utilizes image features similar to the SIFT algorithm
- [ ] Develop a plot that shows how accuracy of image processing varies depending on the number of frames used
- [ ] Implement the image processing algorithms on the Raspberry Pi itself 

