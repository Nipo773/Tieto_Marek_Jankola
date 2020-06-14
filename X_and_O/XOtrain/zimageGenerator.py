import os
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

def generate(path, count):
    for r,d,f in os.walk(path):
        for img_file in f:
            orig = Image.open(img_file)
            image = orig.copy()
            for i in range(2,10):
                contrast(image, i, count)
                color(image, i, count+1)
                sharpness(image, i, count + 2)
                count+=3
            for j in range(1,4):
                rotate(image, j*45, count)
                gaussianBlur(image, j, count + 1)
                unsharpMask(image, j, count + 2)
                brightness(image, j, count+3)
                count+=4
            transpose(image, Image.ROTATE_90, count)
            minFilter(image, 3, count + 1)
            maxFilter(image, 3, count + 2)
            modeFilter(image, 3, count + 3)
            medianFilter(image, 3, count + 4)
            count+=5


def contrast(image, n, count):
    im = image.copy()
    enh = ImageEnhance.Contrast(im)
    enhanced_im = enh.enhance(n)
    enhanced_im.save(str(count) +".jpg")

def color(image, n, count):
    im = image.copy()
    enh = ImageEnhance.Color(im)
    enhanced_im = enh.enhance(n)
    enhanced_im.save(str(count) +".jpg")

def brightness(image, n, count):
    im = image.copy()
    enh = ImageEnhance.Brightness(im)
    enhanced_im = enh.enhance(n)
    enhanced_im.save(str(count) +".jpg")

def sharpness(image, n, count):
    im = image.copy()
    enh = ImageEnhance.Sharpness(im)
    enhanced_im = enh.enhance(n)
    enhanced_im.save(str(count) +".jpg")



def gaussianBlur(image, n, count):
    im = image.copy()
    enh = im.filter(ImageFilter.GaussianBlur(n))
    enh.save(str(count) +".jpg")

def unsharpMask(image, n, count):
    im = image.copy()
    enh = im.filter(ImageFilter.UnsharpMask(n, n*50, n))
    enh.save(str(count) +".jpg")

def minFilter(image, n, count):
    im = image.copy()
    enh = im.filter(ImageFilter.MinFilter(3*n))
    enh.save(str(count) +".jpg")

def maxFilter(image, n, count):
    im = image.copy()
    enh = im.filter(ImageFilter.MaxFilter(n))
    enh.save(str(count) +".jpg")

def modeFilter(image, n, count):
    im = image.copy()
    enh = im.filter(ImageFilter.ModeFilter(n))
    enh.save(str(count) +".jpg")

def medianFilter(image, n, count):
    im = image.copy()
    enh = im.filter(ImageFilter.MedianFilter(n))
    enh.save(str(count) +".jpg")

def rotate(image, deg, count):
    im = image.copy()
    rotated = im.rotate(deg)
    rotated.save(str(count) + ".jpg")

def transpose(image, deg, count):
    im = image.copy()
    transposed = im.transpose(deg)
    transposed.save(str(count) + ".jpg")

generate("C:/Users/kpetr/Aschool/marek", 253)