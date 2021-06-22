import os
import random


def deletor(root):
    files = os.listdir(root)
    for each in files:
        path = os.path.join(root, each)
        imgfiles = os.listdir(path)
        for each_img in imgfiles:
            os.remove(os.path.join(path, each_img))




def delete_randomly(dir, number):
    images = os.listdir(dir)
    rlist = []
    for i in range(number):
          r=random.randint(1,len(images))
          if r not in rlist:
              rlist.append(r)
    for i in rlist:
        os.remove(os.path.join(dir, images[i-1]))






if __name__ == '__main__':
    #root = 'data-to-be-augmented'
    #root2 = 'data-augmented'

    #deletor(root2)
    label = ['i','ii','iii','iv', 'v', 'vi', 'vii','viii', 'ix', 'x']

    deletor('data-augmented')
    """
    for each in label:
        dir1 = os.path.join("data-augmented", each)
        number = 50
        delete_randomly(dir1, number)
    """
