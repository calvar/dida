import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def lighten(x, thres):
    if x < thres / 2:
        return 2*x 
    elif x < thres:
        return 3*x/2
    else:
        return x

#def mask_coverage(mask):
     
    
#-------------------------------------------------------------------
    
im = Image.open('images/241.png')
lb = Image.open('labels/241.png')
#im.show()
#lb.show()

print("IMAGE: format: {0} size: {1} mode: {2}".format(im.format,im.size,im.mode))
print("LABEL: format: {0} size: {1} mode: {2}".format(lb.format,lb.size,lb.mode))

left = 32
upper = 32
right = 64
bottom = 64
window = (left,upper,right,bottom) #l,u,r,b
cropped_im = im.crop(window)
#cropped_im.show()

rotated_im = im.rotate(45)
#rotated_im.save("241_rot.png")
rotated_im.show()
print("ROT_IMAGE: size: {0}".format(rotated_im.size))

graysc_im = im.convert("L")
#graysc_im.show()

smooth_im = graysc_im.filter(ImageFilter.SMOOTH)

edge_im = smooth_im.filter(ImageFilter.FIND_EDGES)
#edge_im.show()

emboss_im = smooth_im.filter(ImageFilter.EMBOSS)
#emboss_im.show()

sharp_im = graysc_im.filter(ImageFilter.SHARPEN)
#sharp_im.show()

#lighten up dark sections of the picture, applying a map
mask = sharp_im.point(
    lambda x: lighten(x,150)
)
smooth2 = mask.filter(ImageFilter.SMOOTH)

#smooth2.show()


#sharp_lb = lb.filter(ImageFilter.SHARPEN)

#sz = im.size[0]*im_size[1]
w = 64
h = 64
stride = 64
for i in range(0,im.size[0]-w,stride):
    l = i
    r = i+w
    for j in range(0,im.size[1]-h,stride):
        u = j
        b = j+h
        cr = lb.crop((i,u,i+w,j+h))
        sz = cr.size[0]*cr.size[1]
        print(cr.histogram()[255]/sz)
        cr.show()

im.close()
lb.close()
