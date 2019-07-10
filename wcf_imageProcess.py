from PIL import Image
import numpy.numpy as np
import os.path
import os
from os import listdir


path = 'Z:/WCF/MARKETING/WCF_Maya_Project/sourceimages/_CARDARTDUMP/fromDrive_cropped_v3'
#path = os.path.dirname(os.path.realpath(__file__))

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        ispng = os.path.splitext(file)[1]
        if ispng == '.png':
            files.append(os.path.join(r, file))

def crop(png_image_name):
    print(png_image_name)
    fileName = os.path.splitext(png_image_name)[0]
    fileExt = os.path.splitext(png_image_name)[1]
    pil_image = Image.open(png_image_name)
    pil_image = pil_image.convert("RGBA")

    bands = pil_image.split()
    resample = Image.NEAREST
    bands = [b.resize((256, 512), resample) for b in bands]
    pil_image = Image.merge('RGBA', bands)
    #pil_image = pil_image.convert("RGBa")

    pil_origImage = pil_image
    print(pil_image.width, pil_image.height)

    np_array = np.array(pil_image)
    #print(np_array)
    blank_px = [255, 255, 255, 0]
    mask = np_array != blank_px
    coords = np.argwhere(mask)
    x0, y0, z0 = coords.min(axis=0)
    x1, y1, z1 = coords.max(axis=0) + 1
    cropped_box = np_array[x0:x1, y0:y1, z0:z1]
    try:
        pil_image = Image.fromarray(cropped_box, 'RGBA')
    except:
        print("Something is wrong with this image, trying inverted")
        blank_px = [0, 0, 0, 0]
        mask = np_array != blank_px
        coords = np.argwhere(mask)
        x0, y0, z0 = coords.min(axis=0)
        x1, y1, z1 = coords.max(axis=0) + 1
        cropped_box = np_array[x0:x1, y0:y1, z0:z1]
        pil_image = Image.fromarray(cropped_box, 'RGBA')

    #ValueError: buffer is not large enough on an image thats all white on a alpha bg, skipping for now

    pil_origImage.save(png_image_name)
    print(pil_image.width, pil_image.height)
    if (pil_origImage.width != pil_image.width) or (pil_origImage.height != pil_image.height):
        print("transparency detected")
        u = pil_origImage.width - pil_image.width
        v = pil_origImage.height - pil_image.height

        pil_image.save(fileName + "_CROP_" + "coordu" + str(u) + "coordv" + str(v) + fileExt )

    #save resized


for f in files:
    crop(f)

#crop("C:/Users/Yates/Documents/TEST_FOLDER/1/diner_panel2.png")
