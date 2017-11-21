# /usr/local/lib/python3.6
#
# - Inputs an image in the spatial domain
# - Displays and saves the same image in the frequency domain
#
# Author: Zach Duguid
# Last Updated: 11/16/2017

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
        self.pixel_max = 255.0

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
        # get the average of the frames and MTF functions (norm_avg_frame used for histogram plotting)
        self.avg_MTF = sum(self.MTF_dict.values())/self.num_frames
        self.avg_frame = sum(self.frame_dict.values())/len(self.frame_dict.values())
        self.norm_avg_frame = self.avg_frame * (self.pixel_max/self.avg_frame.max())

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
        self.norm_cir_img = self.cir_img * (self.pixel_max/self.cir_img.max())    


    def get_image_comparison(self):
        ''' plot circular aperture image vs. synthesized image
        '''
        plt.figure(1, figsize=(12,6))
        plt.subplot(1,2,1), plt.imshow(abs(self.cir_img), cmap='gray')
        plt.title('Circular Aperture Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(1,2,2), plt.imshow(abs(self.filtered_img), cmap='gray')
        plt.title('Synthesized Rectangular Aperture Image (' + str(self.num_frames) + ' Frames)'), plt.xticks([]), plt.yticks([])
        plt.show()


    def get_histogram(self):
        ''' calculate the histogram profile of the original image and the synthesized image, and then compare the two
        '''
        plt.figure(1, figsize=(15,6))
        plt.subplot(1,3,1), plt.hist(abs(self.img).ravel(), 256, [0,256])
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(1,3,2), plt.hist(abs(self.filtered_img).ravel(), 256, [0,256])
        plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(1,3,3), plt.hist(abs(self.norm_avg_frame).ravel(), 256, [0,256])
        plt.title('Blurry Image'), plt.xticks([]), plt.yticks([])
        plt.show()


    def get_image_angle(self):
        ''' calculate the dot product between the histograms of the orginal image and synthesized image
            - normalizes the dot product by the euclidian norm of each histogram
            - prints cos(theta), where theta is the angle between the 
        '''
        A,bin1 = np.histogram(abs(self.img).ravel(),256,[0,256])
        B,bin2 = np.histogram(abs(self.filtered_img).ravel(),256,[0,256])
        print('cos(angle):', np.dot(A, B) / (np.linalg.norm(A)*np.linalg.norm(B)))


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
    frame_set.get_histogram()
    frame_set.get_image_angle()
    

