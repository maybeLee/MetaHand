import cv2
import numpy as np
#from google.colab.patches import cv2_imshow
import glob, os
from matplotlib import pyplot as plt
import argparse
import random

class mutation_operation:
  
  def __init__(self,image_path,label_path,write_path,WIDTH,HEIGHT):
    self.image_path = image_path
    self.label_path = label_path
    self.write_path = write_path
    self.WIDTH = WIDTH
    self.HEIGHT = HEIGHT
  
  def get_label(self,filename):
    labels = []
    f = open(filename, "r")
    for line in f.readlines():
      line = line[:-1]
      arr = line.split(' ')
      arr = list(map(float, arr))
      arr[0] = int(arr[0])
      labels.append(arr)
    return labels

  def center_to_topleft(self,label):
    return [label[0]-label[2]/2, label[1]-label[3]/2, label[2], label[3]]

  def unnormalize(self,labels):
    return_labels = []
    for label in labels:
      return_labels.append(self.center_to_topleft([label[1]*self.WIDTH, label[2]*self.HEIGHT, label[3]*self.WIDTH, label[4]*self.HEIGHT]))
    return return_labels

  def gen_labels(self, id, labels):
    cnt = 0
    for label in labels:
      filename = id[:-4] + "-" + str(cnt) + "L.txt"
      filepath = os.path.join(self.write_path+"label", filename)
      f = open(filepath, "w")
      temp = ""
      for value in label:
        temp = temp + str(value) + " "
      f.write(temp)
      f.close()
      cnt+=1

  def gen_labels_OB(self, id, labels):
    cnt = 0
    for label in labels:
      
      # save labels for object
      filename = id[:-4] + "-" + str(cnt) + "O.txt"
      filepath = os.path.join(self.write_path+'label', filename)#/ for ubuntu, \\ for window
      f = open(filepath, "w")
      temp = ""
      for value in label:
        temp = temp + str(value) + " "
      f.write(temp)
      f.close()

      # save labels for other hands in background
      filename = id[:-4] + "-" + str(cnt) + "B.txt"
      filepath = os.path.join(self.write_path+'label', filename)
      f = open(filepath, "w")
      for i in range(len(labels)):
        if i!=cnt:
          temp = ""
          for value in labels[i]:
            temp = temp + str(value) + " "
          f.write(temp+'\n')
      f.close()
      cnt+=1
      
      filename = id[:-4] + "-" + "B.txt"
      filepath = os.path.join(self.write_path+'label', filename)
      f = open(filepath, "w")
      for i in range(len(labels)):
        f.write('\n')
      f.close()
      cnt+=1
      
      filename = id[:-4] + "-" + "'B-random-erase.txt"
      filepath = os.path.join(self.write_path+'label', filename)
      f = open(filepath, "w")
      for i in range(len(labels)):
        f.write('\n')
      f.close()
      cnt+=1
      
  def rm_object(self, filename, bbox):
    img = cv2.imread(self.image_path+filename)
    #cv2_imshow(img)

    if len(bbox)!=0:
      cnt = 0
      for box in bbox:
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        crop_img = img.copy()
        for i in range(h):
          for j in range(w):
            crop_img[y+i][x+j] = [int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255))]
        #cv2_imshow(crop_img)
        cv2.imwrite(self.write_path + "bkg/" + filename[:-4] + "-"+ str(cnt) + "B" + ".jpg", crop_img)      #save image
        #cv2.waitKey(0)
        cnt+=1
        
  #Remove background of the image, only one object left

  def rm_bg(self, filename, bbox):
    # bg = np.uint8(0 * np.ones((480, 640, 3)))       #generate black background
    bg = np.random.randint(0,high=256,size=(480, 640, 3),dtype=np.uint8)
    # for i in bg:
    #   for j in bg[i]:
    #     for k in bg[i][j]:
    #       bg[i][j][k] = int(random.uniform(0,255))
    img = cv2.imread(self.image_path+filename)
    if len(bbox) != 0:
      cnt = 0
      for box in bbox:
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        obj = bg.copy()
        for i in range(h):
          for j in range(w):
            obj[y+i][x+j] = img[y+i][x+j]

        cv2.imwrite(self.write_path + "objects/" + filename[:-4] + "-"+ str(cnt) + "O" + ".jpg", obj)      #save image
        cnt+=1
        
  #Remove hands other than the label object
  def rm_not_obj(self,filename, bbox):
      img = cv2.imread(self.image_path+filename)


      if len(bbox)!=0:
      
          for obj in range(len(bbox)):
              cnt = 0
              crop_img = img.copy()
              for box in bbox:
                  if obj==cnt:
                      cnt+=1
                      continue
                      
                  x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3]) 
                  cnt+=1
                  for i in range(h):
                      for j in range(w):
                          crop_img[y+i][x+j] = [int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255))]

              #cv2.imshow('image',crop_img)
              #img2 = crop_img.copy()
              #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
              #plt.figure(figsize=(12, 12))
              #plt.axis('off')
              #plt.imshow(img2)
              cv2.imwrite(self.write_path + "BwO/" + filename[:-4] + "-"+ str(obj) + "BwO" + ".jpg", crop_img)      #save image
              print("the bwo path is: " + "BwO/" + filename[:-4] + "-"+ str(obj) + "BwO" + ".jpg")
    
  # def random_erasing_hand(self):
    
  #Remove all hands in the image
  def rm_all_obj(self, filename, bbox, random_erase=False):
      img = cv2.imread(self.image_path+filename)

      if len(bbox)!=0:
      
          cnt = 0
          crop_img = img.copy()
          for box in bbox:
              x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3]) 
              original_area = (x+w)*(y+h)
              if random_erase == True:
                x = int(x+w*random.uniform(0.0, 0.3))
                y = int(y+h*random.uniform(0.0, 0.3))
                h = int(h*random.uniform(0.01, 1.0))
                w = int(w*random.uniform(0.01, 1.0))
              print("the random erase shrinks by " + str((x+w)*(y+h)/original_area*100))
              for i in range(h):
                  for j in range(w):
                    #y+i can exceed 480, x+j cannot exceed 640 i.e., image size
                      # print("y+i: " + str(y+i))
                      # print("x+j: " + str(x+j))
                      crop_img[min(y+i,479)][min(x+j,639)] = [int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255))]
          
          if random_erase == False:
              cv2.imwrite(self.write_path + "object_removal_/" + filename[:-4] + "-"+ "B" + ".jpg", crop_img)      #save image
          else:
              cv2.imwrite(self.write_path + "object_removal_random_erase/" + filename[:-4] + "-"+ "B-random-erase" + ".jpg", crop_img)      #save image
          #cv2.waitKey(0)

def main(image_path,label_path,write_path):
    # image width and height
    WIDTH = 640
    HEIGHT = 480
    mo = mutation_operation(image_path,label_path,write_path,WIDTH,HEIGHT)
    #create folder for mutated images
    # os.chdir(write_path)
    if not os.path.exists(write_path + 'objects'):
        os.mkdir(write_path + 'objects')
    if not os.path.exists(write_path + 'bkg'):
        os.mkdir(write_path + 'bkg')
    if not os.path.exists(write_path + 'label'):
        os.mkdir(write_path + 'label')
    if not os.path.exists(write_path + 'BwO'):
        os.mkdir(write_path + 'BwO')
    if not os.path.exists(write_path + 'B'):
        os.mkdir(write_path + 'B')
    if not os.path.exists(write_path + 'B-random-erase'):
        os.mkdir(write_path + 'B-random-erase')

    # copy list of labels
    # os.chdir(label_path)
    label_list = glob.glob(label_path + "*.txt")
    # label_list = [os.path.basename(i) for i in all_paths] #drop parent directory path
    # print("label path is : " + str(label_path + "*.txt"))
    # print("number of labels obtained: " + str(len(label_list)))


    no_label = 0
    hv_label = 0
    mut = 0
    #iterate through a list of labels
    if __debug__:
      label_list = label_list[:5]
    for id in label_list:
        labels = mo.get_label(id)
        id = os.path.basename(id)
        if len(labels)==0:#print message to show that the label does not exist
            print(id+" -- no label")
            no_label+=1
            continue

        mo.gen_labels_OB(id, labels) #use os.path.basename() to keep only base directory for id

        bbox = mo.unnormalize(labels)  
        # mo.rm_bg(id[:-4]+".jpg", bbox) #make background becomes black
        
        # #remove the hand object
        # mo.rm_object(id[:-4]+".jpg", bbox) #make hands become black
        # mo.rm_not_obj(id[:-4]+".jpg", bbox) #make objects other than hands become black
        # mo.rm_all_obj(id[:-4]+".jpg", bbox, random_erase=False) #make all objects (including hands) become black
        mo.rm_all_obj(id[:-4]+".jpg", bbox, random_erase=True)
        print(id+" -- done", len(labels), "labels")
        hv_label += 1
        mut += len(labels)

    print("--------finished-------")
    print("total: ", no_label+hv_label, "images")
    print("images with labels: ", hv_label)
    print("images without labels: ", no_label)
    print(mut, " sets of obj and bg generated")

if __name__ == "__main__":
    image_path = None
    label_path = None
    mutate_path = None
    if __debug__:
      image_path = "data/ImageSet/"
      label_path = "data/labels/"
      mutate_path = "data/mutate/"
    else:
      parser = argparse.ArgumentParser()
      parser.add_argument('--image_path', help='path to original images',required=True)
      parser.add_argument('--label_path', help="path to labels",required=True)
      parser.add_argument('--mutate_path', help="path to mutated images",required=True)
      flags, unknown = parser.parse_known_args()
      image_path = flags.image_path
      label_path = flags.label_path
      mutate_path = flags.mutate_path
      
    
    # image_path = "/data1/wcleungag/ImageSet/"
    # label_path = "/data1/wcleungag/labels/"
    # write_path = "/data1/wcleungag/mutated_dataset_all/"
    main(image_path,label_path,mutate_path)
