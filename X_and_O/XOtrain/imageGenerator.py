import os, random
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import numpy as np

def generate(path, count):
    for r,d,f in os.walk(path):

        for img_file in f:


            orig = Image.open(img_file)
            image = orig.copy()
            name_split = img_file.split(".")
            extension = "." + name_split[-1]
            for i in range(2,10):
                sharpness(image, i, count, extension,path)
                count+=1
            for j in range(1,4):
                #rotate(image, j*45, count, extension)
                contrast(image, j, count, extension,path)
                color(image, j, count + 1, extension,path)
                gaussianBlur(image, j, count + 2, extension,path)
                unsharpMask(image, j, count + 3, extension,path)
                brightness(image, j, count+4, extension,path)
                count+=6

            transpose(image, Image.ROTATE_90, count, extension,path)
            transpose(image, Image.ROTATE_180, count+1, extension,path)
            transpose(image, Image.ROTATE_270, count+2, extension,path)
            minFilter(image, 3, count+3, extension,path)
            maxFilter(image, 3, count + 4, extension,path)
            modeFilter(image, 3, count + 5, extension,path)
            medianFilter(image, 3, count + 6, extension,path)
            count+=7



def crop_all_pic(path, count):
    pathh = path
    for r,d,f in os.walk(pathh):
        for img_file in f:
            orig = Image.open(img_file)
            image = orig.copy()
            name_split = img_file.split(".")
            extension = "." + name_split[-1]
            crop_bottom_half(image, count, extension,pathh)
            count+=4

def save_cropped_images(path, count, extension,enh):
    enh.save(path + str(count) + extension)

def save_image(enh,n,count,extension,path):
    enhanced_im = enh.enhance(n)
    enhanced_im.save(path + str(count) + extension)

def save_image_without_enhance(path, count, extension,enh):
    enh.save(path + str(count) + extension)

def contrast(image, n, count, extension,path):
    im = image.copy()
    enh = ImageEnhance.Contrast(im)
    save_image(enh, n, count, extension,path)

def color(image, n, count, extension,path):
    im = image.copy()
    enh = ImageEnhance.Color(im)
    save_image(enh, n, count, extension,path)

def brightness(image, n, count, extension,path):
    im = image.copy()
    enh = ImageEnhance.Brightness(im)
    save_image(enh, n, count, extension,path)

def sharpness(image, n, count, extension,path):
    im = image.copy()
    enh = ImageEnhance.Sharpness(im)
    save_image(enh, n, count, extension,path)


def gaussianBlur(image, n, count, extension,path):
    im = image.copy()
    enh = im.filter(ImageFilter.GaussianBlur(n))
    save_image_without_enhance(path, count, extension, enh)

def unsharpMask(image, n, count, extension,path):
    im = image.copy()
    enh = im.filter(ImageFilter.UnsharpMask(n, n*50, n))
    save_image_without_enhance(path, count, extension, enh)

def minFilter(image, n, count, extension,path):
    im = image.copy()
    enh = im.filter(ImageFilter.MinFilter(3*n))
    save_image_without_enhance(path, count, extension, enh)

def maxFilter(image, n, count, extension,path):
    im = image.copy()
    enh = im.filter(ImageFilter.MaxFilter(n))
    save_image_without_enhance(path, count, extension, enh)

def modeFilter(image, n, count, extension,path):
    im = image.copy()
    enh = im.filter(ImageFilter.ModeFilter(n))
    save_image_without_enhance(path, count, extension, enh)

def medianFilter(image, n, count, extension,path):
    im = image.copy()
    enh = im.filter(ImageFilter.MedianFilter(n))
    save_image_without_enhance(path, count, extension, enh)

def rotate(image, deg, count, extension,path):
    im = image.copy()
    rotated = im.rotate(deg)
    save_image_without_enhance(path, count, extension, rotated)

def transpose(image, deg, count, extension,path):
    im = image.copy()
    transposed = im.transpose(deg)
    save_image_without_enhance(path, count, extension, transposed)


def crop_bottom_half(img,count,extension,path):
    w,h = img.size
    img_left_area = (0,0,w//2,h)
    #  left, upper, right, and lower
    img_right_area = (w//2, 0, w, h)
    img_bottom_area = (0,0,w,h//2)
    img_lower_area = (0,h//2,w,h)

    img_left = img.crop(img_left_area)
    img_right = img.crop(img_right_area)
    img_bottom = img.crop(img_bottom_area)
    img_lower = img.crop(img_lower_area)
    save_cropped_images(path, count, extension, img_left)
    save_cropped_images(path, count+1, extension, img_right)
    save_cropped_images(path, count+2, extension, img_bottom)
    save_cropped_images(path, count+3, extension, img_lower)


generate("C:/Users/kpetr/Aschool/marek", 0)