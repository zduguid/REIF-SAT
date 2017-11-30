<a href="https://zduguid.github.io">
    <img src="readme_images/project_logo.jpg" alt="project_logo" align="right" height="80">
</a>


# REIF-SAT Image Processing
The goal of the Rectangular Earth-Imaging Fast-Spinning Aperture Telescope (REIF-SAT) project is to demonstrate the feasibility of a spinning-aperture space telescope that is capable of producing high quality images that are of equivalent resolution to the images produced by an equivalent length circular aperture system. REIF-SAT is the deliverable of MIT's Aerospace Engineering capstone course for undergraduate students: 16.83 - Space Systems Engineering. To demonstrate the feasibility of a spinning-aperture space telescope, image processing algorithms must be developed to synthesize a high resolution image from a series of individual frames. 


## Table of Contents
- [Getting Started](#getting-started)
    - [Dependencies](#dependencies)
- [Image Processing](#image-processing)
    - [Frame Generation](#frame-generation)
    - [Wiener Filter](#wiener-filter)
    - [Synthesis Accuracy](#synthesis-accuracy)
    - [Helpful Commands](#helpful-commands)
- [Future Work](#future-work)
- [Acknowledgements](#acknowledgements)


## Getting Started 
The image processing software tools found in this repository represent the initial phase of testing for the REIF-SAT project. As such, the software tools take in a test image instead of live images directly from a camera. From this test image, artificial frames are generated to simulate the effect of using a rectangular aperture system instead of a circular aperture. Then, the frames are synthesized using a Wiener Filter approach. The image processing script itself is written in Python ( ```wiener_filter.py```). Python is used because it is readily compatible to run on a Raspberry Pi, and the image processing for this project is intended to be conducted with a Raspberry Pi. To run this script, the following dependencies must be satisfied.


### Dependencies 
* The image processing script is written in ```Python3``` [(Python3 Download)](https://www.python.org/downloads/)
* ```NumPy``` is used to create array objects for graphing [(NumPy)](http://www.numpy.org)
* ```OpenCV``` is used for reading in, manipulating, and displaying images [(OpenCV)](https://opencv.org)
* ```imutils``` is used for image rotations [(imutils)](https://github.com/jrosebr1/imutils)
* ```matplotlib``` is used for creating custom plots [(matplotlib)](https://matplotlib.org)


## Image Processing 
To demonstrate the feasibility of the REIF-SAT image processing software, a set of artificial frames are generated to simulate the effect of the rectangular aperture system. Then, a Wiener Filter algorithm is used to synthesize the set of frames into an individual image.


### Frame Generation 
The set of frames is created by rotating an aperture pupil mask across a series of linearly spaced angles between 0 and 180 degrees, computing the modulation transfer function (MTF) associated with each rotated pupil mask, and then resolving the individual frames by multiplying each MTF with the original test image. By doing so, frames are shown to have high resolution in the direction parallel to the rectangular aperture orientation and low resolution in the direction orthogonal to the rectangular aperture orientation. The diagram below demonstrates the frame generation process.


### Wiener Filter


### Synthesis Accuracy


### Helpful Commands
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


## Future Work


## Acknowledgements
* Massachusetts Institute of Technology (MIT)
* MIT Lincoln Laboratories (MITLL)
* Jet Propulsion Laboratory (JPL)
* Faculty and staff for 16.83, Space Systems Engineering 

