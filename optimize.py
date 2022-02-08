"""If images are too large in the images folder, this will run over them and optimize them all."""

from PIL import Image
import os

images = os.listdir('static/images')

for image_path in images:
    basewidth = 1600

    im = Image.open('static/images/'+image_path)
    if (im.size[0] <= basewidth):
        print(image_path + ' already proper size or smaller')
        continue
    wpercent = basewidth / im.size[0]
    hsize = int(im.size[1] * wpercent)
    print((basewidth, hsize))
    im = im.resize((basewidth, hsize), Image.ANTIALIAS)
    im.save('static/images/'+image_path, optimize=True, quality=85)
    print(image_path + ' resized')
