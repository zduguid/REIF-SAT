# /usr/local/lib/python3.6
#
# - Inputs an image in the spatial domain
# - Displays and saves the same image in the frequency domain
#
# Author: Zach Duguid
# Last Updated: 11/14/2017

import cv2
import imutils
import numpy as np
import math
from matplotlib import pyplot as plt


class FrameSet(object):
    def __init__(self, num_frames, img_f_name, pup_f_name, cir_f_name):
        ''' initialize FrameSet object
            - stores relevant information for a half-rotation of frames
        '''
        # specify desired number of frames
        self.num_frames = num_frames

        # read black and white pupil and image files
        self.img = cv2.imread(img_f_name, 0)
        self.cir_pup = cv2.imread(cir_f_name, 0)
        self.f_img = np.fft.fft2(self.img)
        self.pup = cv2.imread(pup_f_name, 0)
        self.angles = np.linspace(0, 180, self.num_frames)
        self.SNR = 10^5

        # initialize dictionary objects to keep track of information at different anlges of rotation
        self.pup_dict = {}
        self.MTF_dict = {}
        self.f_frame_dict = {}
        self.frame_dict = {}


    def get_rotations(self):
        ''' rotate image data using self.angles 
        '''
        for angle in self.angles:
            # rotate the pupil mask
            self.pup_dict[angle] = imutils.rotate(self.pup, angle)

            # get pupil mask in frequency domain, get complex conjugate, get auto-correlation
            f_pup = np.fft.fft2(self.pup_dict[angle])
            f_pup_conj = np.conjugate(f_pup)
            f_pup_auto = abs(f_pup*f_pup_conj)

            # get modulation transfer function
            self.MTF_dict[angle] = np.fft.ifft2(f_pup_auto)

            # get individual frame in the frequency domain using the relevant MTF
            self.f_frame_dict[angle] = self.f_img*self.MTF_dict[angle]

            # get individual frame in the spatial domain
            self.frame_dict[angle] = np.fft.ifft2(self.f_frame_dict[angle])


    def get_sythesized_image(self):
        ''' sythesizes image from individual frames via Wiener deconvolution  
        '''
        # get the average of the frames and MTF functions
        self.avg_MTF = sum(self.MTF_dict.values())/self.num_frames
        self.avg_frame = sum(self.frame_dict.values())/self.num_frames

        # create and apply Wiener filter
        self.wiener_filter = np.conjugate(self.avg_MTF) / (self.avg_MTF**2 + 1/(self.SNR^2))
        self.f_filtered_img = np.fft.fft2(self.avg_frame) * self.wiener_filter
        self.filtered_img = np.fft.ifft2(self.f_filtered_img)


    def get_circular_image(self):
        ''' computes the image that would have been produced with a circular aperture system
        '''
        f_cir_pup = np.fft.fft2(self.cir_pup)
        f_cir_pup_conj = np.conjugate(f_cir_pup)
        f_cir_pup_auto = abs(f_cir_pup*f_cir_pup_conj)
        cir_MTF = np.fft.ifft2(f_cir_pup_auto)
        f_cir_img = self.f_img*cir_MTF
        self.cir_img = np.fft.ifft2(f_cir_img)     


    def get_image_comparison(self):
        ''' plot original test image vs. synthesized image
        '''
        plt.figure(1, figsize=(12,6))
        plt.subplot(1,2,1), plt.imshow(abs(self.cir_img), cmap='gray')
        plt.title('Circular Aperture Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(1,2,2), plt.imshow(abs(self.filtered_img), cmap='gray')
        plt.title('Synthesized Rectangular Aperture Image (' + str(self.num_frames) + ' Frames)'), plt.xticks([]), plt.yticks([])
        plt.show()


if __name__ == '__main__':
    # intialize FrameSet object with correct file names and desired number of frames
    img_f_name = 'test_images/boston.jpg'
    pup_f_name = 'test_images/boston_mask_rec.jpg'
    cir_f_name = 'test_images/boston_mask_cir.jpg'
    num_frames = 5
    frame_set = FrameSet(num_frames, img_f_name, pup_f_name, cir_f_name)
    frame_set.get_rotations()
    frame_set.get_sythesized_image()
    frame_set.get_circular_image()
    frame_set.get_image_comparison()
    
