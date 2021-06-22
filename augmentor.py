import cv2
import imutils
import os
import random
from deletor import delete_randomly

"""
image = cv2.imread("dataedit3/train/iv/edit.png")
rows = image.shape[0]
cols = image.shape[1]
img_center = (cols / 2, rows / 2)
M = cv2.getRotationMatrix2D(img_center, -30, 1)
rotated_image = cv2.warpAffine(image,M, (cols, rows), borderValue=(255,255,255))

cv2.imshow('window1',rotated_image)
cv2.waitKey(0)
"""



def rotation_augment(source, angle, dest, roman_no):
    print("rotating images by", angle)

    folders = os.listdir(source)

    for each_class in folders:
        path = os.path.join(source, each_class)
        imgfiles = os.listdir(path)
        for each_img in imgfiles:
            imgpath = os.path.join(path, each_img)
            #print("imgoath = ", imgpath)
            image = cv2.imread(imgpath)
            rows = image.shape[0]
            cols = image.shape[1]
            img_center = (cols / 2, rows / 2)
            M = cv2.getRotationMatrix2D(img_center, angle, 1)
            rotated_image = cv2.warpAffine(image,M, (cols, rows), borderValue=(255,255,255))
            pathtosave = os.path.join((dest), str(each_class))
            if not os.path.exists(pathtosave):
                os.makedirs(pathtosave)

            final_path = os.path.join(pathtosave, ("augmented-" + str(angle) + each_img))
            #print("finall path = ", final_path)
            cv2.imwrite(final_path, rotated_image)



def setimages(source_path, label, dest_train_path, dest_val_path):
    images = os.listdir(source_path)
    print("images list = ", images)
    #print("sample image name = ", images[10])
    shuffled_images = random.shuffle(images)
    size = len(images)
    print("size  = ", size)
    train_limit = int((80/100)*size)
    print("split no = ", train_limit)

    for i in range(train_limit+1):
        # getting path of images from 1 - split_no from data augmented folder
        path = os.path.join(source_path, images[i])
        #print("source path = ", path)
        #reading image from that path
        img = cv2.imread(path)
        #print("image read")
        #creating path of final data where images needs to be copied

        temp_path = os.path.join(dest_train_path,label)
        final_path = os.path.join(temp_path, images[i])
        #print("dest path = ", dest_path)
        #print("final path = ", final_path)
        cv2.imwrite(final_path, img)
        #print("image copied")

    for i in range(train_limit+1, size):
        path = os.path.join(source_path, images[i])
        img = cv2.imread(path)
        temp_path = os.path.join(dest_val_path,label)
        final_path = os.path.join(temp_path, images[i])
        cv2.imwrite(final_path, img)









if __name__ == '__main__':
    # creating path for train and val data to pull data for augmentation
    root1 = os.path.join("dataedit3", "train")
    root2 = os.path.join("dataedit3", "val")

    #destination dir where the augmented data will be stored
    dest = "data-augmented"

    #augmentation rotation parameter,for each image 4 copies obtained
    angles = [5,-5, 20,-20]
    angles = [5,-5, 20,-20]

    # instead of numerical lables, we have roman numbers [i,ii,iii,iv,..]
    roman_no = os.listdir('dataedit3/train')
    label = ['i','ii','iii','iv', 'v', 'vi', 'vii','viii', 'ix', 'x']

    # read images from data --> augment it ---> save to another dir (augmented data)
    for angle in angles:
        print("angle = ", angle)
        rotation_augment(root1, angle, dest, roman_no)
        rotation_augment(root2, angle, dest, roman_no)

    # size constraint 10,000 --> read images from augmented data foler -- > delete 500 each
    for each in label:
        dir = os.path.join("data-augmented", each)
        number = 500
        delete_randomly(dir, number)

    # read from augmented data folder -- > copy it to orginal dataset
    for each_class in range(1,11):
        #for each class index [1= i, 2 = ii ,3 = iii.....]
        print(each_class)
        #create src path to read augmented image. label[each_class] = label[0], label[1]....
        src_path = os.path.join("data-augmented", str(label[each_class-1]))
        #create dest path where the augmented image will be copied
        dest_train_path = os.path.join("dataedit3", "train")
        #create val path where the augmented image will be copied
        dest_val_path = os.path.join("dataedit3", "val")
        #call the function to copy the augmented data to orginal data dir
        setimages(src_path , label[each_class-1], dest_train_path , dest_val_path)
