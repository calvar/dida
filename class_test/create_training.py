import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
from pathlib import Path
from sys import argv

def lighten(x, thres):
    if x < thres / 2:
        return 2*x 
    elif x < thres:
        return 3*x/2
    else:
        return x

def img_preprocess(img):
    #graysc_img = img.convert("L")
    sharp_img = img.filter(ImageFilter.SHARPEN)
    ##lighten up dark sections of the picture, applying a map
    #light = sharp_img.point( lambda x: lighten(x,150) )
    #smooth = light.filter(ImageFilter.SMOOTH)
    return sharp_img 


def img_split(img, mask, w, h, strd, prop): #width, height and stride of the split. Proportion to consider roof tile
    images = []
    labels = []
    for i in range(0,img.size[0]-w+1,strd):
        left = i
        right = i+w
        for j in range(0,img.size[1]-h+1,strd):
            upper = j
            bottom = j+h

            #crop image and mask
            rect = (left,upper,right,bottom)
            crp = img.crop(rect)
            mk_crp = mask.crop(rect)
            
            npixels = crp.size[0]*crp.size[1]
            proportion = mk_crp.histogram()[255] / npixels
            
            images.append(crp.resize((48,48)))
            labels.append(1 if proportion > prop else 0)
    return images, labels
#----------------------------------------------

code, w, h, stride, prop = argv
w = int(w)
h = int(h)
stride = int(stride)
prop = float(prop)

filenames = []
for child in Path('../labels/').iterdir():
    filenames.append(child.name)
    
for img_file in filenames:
    img = Image.open('../images/'+img_file)
    mask = Image.open('../labels/'+img_file)

    pimg = img_preprocess(img)
    ###Original--------------------------------------------
    crops, lbls = img_split(pimg, mask, w, h, stride, prop)

    for i in range(len(crops)):
        f = img_file[:-4]+"_o"+str(i).zfill(5)+".png"
        crops[i].save("splitted/"+str(lbls[i])+"/"+f)
        crops[i].close()
        
    ###Rotated---------------------------------------------
    img_rot = pimg.rotate(45)
    mask_rot = mask.rotate(45)
    crops, lbls = img_split(img_rot, mask_rot, w, h, stride, prop)

    for i in range(len(crops)):
        f = img_file[:-4]+"_r"+str(i).zfill(5)+".png"
        crops[i].save("splitted/"+str(lbls[i])+"/"+f)
        crops[i].close()

    img_rot.close()
    mask_rot.close()
        
    ###Flipped vertically-----------------------------------
    img_vf = pimg.transpose(Image.FLIP_TOP_BOTTOM)
    mask_vf = mask.transpose(Image.FLIP_TOP_BOTTOM)
    crops, lbls = img_split(img_vf, mask_vf, w, h, stride, prop)

    for i in range(len(crops)):
        f = img_file[:-4]+"_v"+str(i).zfill(5)+".png"
        crops[i].save("splitted/"+str(lbls[i])+"/"+f)
        crops[i].close()

    img_vf.close()
    mask_vf.close()
    
    ###Flipped horizontally---------------------------------
    img_hf = pimg.transpose(Image.FLIP_LEFT_RIGHT)
    mask_hf = mask.transpose(Image.FLIP_LEFT_RIGHT)
    crops, lbls = img_split(img_hf, mask_hf, w, h, stride, prop)

    for i in range(len(crops)):
        f = img_file[:-4]+"_h"+str(i).zfill(5)+".png"
        crops[i].save("splitted/"+str(lbls[i])+"/"+f)
        crops[i].close()
    
    img_vf.close()
    mask_vf.close()
    
    
    img.close()
    mask.close()
