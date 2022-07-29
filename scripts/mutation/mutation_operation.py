import cv2
import numpy as np
#from google.colab.patches import cv2_imshow
import glob, os
from matplotlib import pyplot as plt
import argparse
import random
import pathlib
import os
from multiprocessing import Pool
import time
import math
import random

random.seed(10)

class mutation_operation:
  
  def __init__(self,image_path,label_path,write_path,WIDTH,HEIGHT,dataset):
    self.image_path = image_path
    self.label_path = label_path
    self.write_path = write_path
    self.WIDTH = WIDTH
    self.HEIGHT = HEIGHT
    self.dataset = dataset
  
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

  def unnormalize(self,labels,dataset):
    return_labels = []
    for label in labels:
      # if __debug__:
        # print("DEBUG: label original: " + str(label))
      if dataset == "company":
          return_labels.append(self.center_to_topleft([label[1]*self.WIDTH, label[2]*self.HEIGHT, label[3]*self.WIDTH, label[4]*self.HEIGHT]))
      elif dataset == "coco":
          return_labels.append([label[1], label[2], label[3], label[4]])
      else:
          raise ValueError("invalid dataset")
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

  def gen_labels_OB(self, id, labels, object_or_background, random_erase=0.0, random_erase_mode="fixMutRatio_varyXY", guassian_sigma=0.0):
    for label in labels:
      if object_or_background == "background":
      # save labels for object
        filename = id[:-4] + "-" + "O" + "_" + str(guassian_sigma) + ".txt"
        filepath = os.path.join(self.write_path+'label', filename)#/ for ubuntu, \\ for window
        f = open(filepath, "w")
        temp = ""
        for value in label:
          temp = temp + str(value) + " "
        f.write(temp)
        f.close()
      else:
        filename_list = []
        if random_erase > 0.0 and guassian_sigma == 0.0:
          filename_list.append(id[:-4] + "-" + "B_random_erase_" + random_erase_mode + "_" + str(random_erase).replace(".","") + ".txt")
        elif guassian_sigma > 0.0:
          filename_list.append(id[:-4] + "-" + "B_guassian_" + str(guassian_sigma).replace(".","") + "_" + random_erase_mode + "_" + str(random_erase).replace(".","") + ".txt")
        if guassian_sigma == 0.0 and random_erase == 0.0:
          raise RuntimeError("invalid operation: guassian_sigma and random_erase must be larger than zero at the same time.")
        
        for filename in filename_list:
          filepath = os.path.join(self.write_path+'label', filename)
          f = open(filepath, "w")
          for i in range(len(labels)):
            f.write('\n')
          f.close()
        
  #Remove background of the image, only one object left

  def add_guassian_noise_to_bg(self, filename, bbox, guassian_sigma=0.0):
    # bg = np.uint8(0 * np.ones((480, 640, 3)))       #generate black background
    img = cv2.imread(self.image_path+filename)
    mean = 0.0
    obj = img.copy()
    max_i = len(obj)
    max_j = len(obj[0])
    # bg = np.random.randint(0,high=256,size=(480, 640, 3),dtype=np.uint8)
    if __debug__:
        print("DEBUG: img height length " + str(len(obj)))
        print("DEBUG: img width length " + str(len(obj[0])))
    assert self.HEIGHT == len(obj), "given height (self.HEIGHT) does not match detected height"        
    assert self.WIDTH == len(obj[0]), "given width (self.WIDTH) does not match detected width"
    for i in range(0,len(obj)):
      for j in range(0,len(obj[i])):
        # if __debug__:
          # print("DEBUG: i and j in processing: " + str(i) + "," + str(j))
        # print("obj[i][j]: " + str(obj[i][j]))
        # for k in obj[i][j]:
        #   print("obj[i][j][k] is: " + str())
        obj[i][j] = [obj[i][j][0] + np.random.normal(mean, guassian_sigma),obj[i][j][1] + np.random.normal(mean, guassian_sigma),obj[i][j][2] + np.random.normal(mean, guassian_sigma)]
    if len(bbox) != 0:
      # cnt = 0
      if __debug__:
        print("DEBUG: bbox is " + str(bbox))
      for box in bbox:
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        
        for i in range(h):
          for j in range(w):
            target_i = min(y+i,max_i-1)
            target_j = min(x+j,max_j-1)
            obj[target_i][target_j] = img[target_i][target_j]
      print("saving mutated image")
      writeStatus = cv2.imwrite(self.write_path + "objects/" + filename[:-4] + "-" + "O" + "_" + str(guassian_sigma) + ".jpg", obj)      #save image
      if writeStatus is False:
        print("cv2 write failed")
      else:
        print("cv2 write successful")
        # raise ValueError("cv2 write failed")
    else:
      raise ValueError("Should not encounter empty bbox")
        # cnt+=1
        
  #Remove hands other than the label object
  # def rm_not_obj(self,filename, bbox):
  #     img = cv2.imread(self.image_path+filename)


  #     if len(bbox)!=0:
      
  #         for obj in range(len(bbox)):
  #             cnt = 0
  #             crop_img = img.copy()
  #             for box in bbox:
  #                 if obj==cnt:
  #                     cnt+=1
  #                     continue
                      
  #                 x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3]) 
  #                 cnt+=1
  #                 for i in range(h):
  #                     for j in range(w):
  #                         crop_img[y+i][x+j] = [int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255))]

  #             #cv2.imshow('image',crop_img)
  #             #img2 = crop_img.copy()
  #             #img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
  #             #plt.figure(figsize=(12, 12))
  #             #plt.axis('off')
  #             #plt.imshow(img2)
  #             cv2.imwrite(self.write_path + "BwO/" + filename[:-4] + "-"+ str(obj) + "BwO" + ".jpg", crop_img)      #save image
  #             print("the bwo path is: " + "BwO/" + filename[:-4] + "-"+ str(obj) + "BwO" + ".jpg")
    
  # def random_erasing_hand(self):
    
  #Remove all hands in the image
  def rm_all_obj(self, filename, bbox, random_erase=0.0, random_erase_mode="fixMutRatio_varyXY", guassian_sigma=0.0):
      img = cv2.imread(self.image_path+filename)
      # print("DEBUG: the file path is " + str(self.image_path+filename))
      # print("height of an img: " + str(len(img)))
      height, width, channels = img.shape
      assert self.WIDTH == width, "given width (self.WIDTH) does not match detected width"
      assert self.HEIGHT == height, "given height (self.HEIGHT) does not match detected height"
      if len(bbox)!=0:
          cnt = 0
          crop_img = img.copy()
          for box in bbox:
              if __debug__:
                print("the bbox being proceesed: " + str(box))
              x, y, w, h = int(box[0]), int(box[1]), max(int(box[2]),1), max(int(box[3]),1)
              original_area = w*h
              if __debug__:
                print("DEBUG: w is : " + str(w))
                print("DEBUG: h is : " + str(h))
                print("DEBUG: original_area is : " + str(original_area))
              if random_erase > 0.0:
                if "varyXY" in random_erase_mode:
                  x = int(x+w*random.uniform(0.0, 1.0-random_erase))
                  y = int(y+h*random.uniform(0.0, 1.0-random_erase))
                  h = int(h*random.uniform(random_erase, 1.0))
                  w = int(w*random.uniform(random_erase, 1.0))
                elif "centerXY" in random_erase_mode:
                  # height_randomize_factor = random.uniform(0.1, 1.0)
                  x = int(x+w/2)
                  y = int(y+h/2)    
                  h = min(int(h*math.sqrt(random_erase)),h)
                  w = min(int(w*math.sqrt(random_erase)),w)   
                else:
                  if "fixXY" not in random_erase_mode:
                    raise ValueError("invalid operation, random erase mode must be varyXY, centerXY and fixXY")
                  h = int(h*random_erase)
                  w = int(w*random_erase)
                # if h == -1 or w == -1:
                #   raise ValueError("invlid operation, random erase mode must be varyMutRatio or fixMutRatio")
                
              print("the random erase shrinks by " + str(w*h/original_area*100))
              
              y_start = y if "varyXY" in random_erase_mode or "fixXY" in random_erase_mode else y-h/2
              y_end = y+h if "varyXY" in random_erase_mode or "fixXY" in random_erase_mode else y+h/2
              x_start = x if "varyXY" in random_erase_mode or "fixXY" in random_erase_mode else x-w/2
              x_end = x+w if "varyXY" in random_erase_mode or "fixXY" in random_erase_mode else x+w/2
              if __debug__:
                print("DEBUG: y_start is : " + str(y_start))
                print("DEBUG: y_end is : " + str(y_end))
                print("DEBUG: x_start is : " + str(x_start))
                print("DEBUG: x_end is : " + str(x_end))
              for i in range(int(y_start),int(y_end) + 1):
                  for j in range(int(x_start),int(x_end)+1):
                    #y+i can exceed 480, x+j cannot exceed 640 i.e., image size
                      # print("y+i: " + str(y+i))
                      # print("x+j: " + str(x+j))
                      if guassian_sigma > 0.0:
                          mean = 0.0
                          # sd = 0.0
                          r_g_b = crop_img[max(min(i,height-1),0)][max(min(j,width-1),0)]
                          r_noise = np.random.normal(mean, guassian_sigma)
                          g_noise = np.random.normal(mean, guassian_sigma)
                          b_noise = np.random.normal(mean, guassian_sigma)
                          crop_img[max(min(i,height-1),0)][max(min(j,width-1),0)] = [int(r_g_b[0] + r_noise), int(r_g_b[1]+g_noise), int(r_g_b[2]+b_noise)]
                      else:
                          # if __debug__:
                          #     print("DEBUG: the coordinate being erased: " + str(max(min(i,height-1),0)) + "," + str(max(min(j,width-1),0)))
                          crop_img[max(min(i,height-1),0)][max(min(j,width-1),0)] = [int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255))]


          
          # if random_erase == 0.0 and guassian_sigma == 0.0:
          #   pathlib.Path(self.write_path + 'B').mkdir(parents=True, exist_ok=True)
          #   cv2.imwrite(self.write_path + "B/" + filename[:-4] + "-"+ "B" + ".jpg", crop_img)      #save image
          if guassian_sigma > 0.0:
            # print("INFO: creating")
            pathlib.Path(self.write_path + "B_guassian_" + str(guassian_sigma).replace(".","") + "_" + random_erase_mode + "_" + str(random_erase).replace(".","")).mkdir(parents=True, exist_ok=True)
            cv2.imwrite(self.write_path + "B_guassian_" + str(guassian_sigma).replace(".","") + "_" + random_erase_mode + "_" + str(random_erase).replace(".","") + "/" + filename[:-4] + "-"+ "B_guassian_" + str(guassian_sigma).replace(".","") + "_" + random_erase_mode + "_" + str(random_erase).replace(".","") + ".jpg", crop_img) #save image
          elif random_erase > 0.0:
            # print("INFO: creating")
            pathlib.Path(self.write_path + "B_random_erase_" + random_erase_mode + "_" + str(random_erase).replace(".","")).mkdir(parents=True, exist_ok=True)
            cv2.imwrite(self.write_path + "B_random_erase_" + random_erase_mode + "_" + str(random_erase).replace(".","") + "/" + filename[:-4] + "-"+ "B_random_erase_" + random_erase_mode + "_" + str(random_erase).replace(".","") + ".jpg", crop_img) #save image
          #cv2.waitKey(0)
          
  # def gen_log_name(self,random_erase=0.0, random_erase_mode="fixMutRatio_varyXY", guassian_sigma=0.0):
  #   log_name = ""
  #   if random_erase > 0.0 and guassian_sigma == 0.0:
  #     log_name = "B_random_erase_" + random_erase_mode + "_" + str(random_erase).replace(".","") + ".txt"
  #   elif guassian_sigma > 0.0:
  #     log_name = "B_guassian_" + str(guassian_sigma).replace(".","") + "_" + random_erase_mode + "_" + str(random_erase).replace(".","") + ".txt"
  #   return log_name
  
  # def remove_log(self,log_name):
  #   if os.path.exists(self.write_path + "log/" + log_name):
  #     # print("file exists")
  #     os.remove(self.write_path + "log/" + log_name)
  
  # def log_finish(self,log_name):
  #   f = open(self.write_path + "log/" + log_name, "w") 
  #   f.write("finished") 
  #   f.close()
    
def perform_mutation(mo,id,random_erase,random_erase_mode,guassian_sigma,object_or_background):
      print("INFO: processing id: " + str(id) + "\n")
      labels = mo.get_label(id)
      id = os.path.basename(id)
      if len(labels)==0:#print message to show that the label does not exist
          print(id+" -- no label")
          # no_label+=1
          return
        
      bbox = None
      mo.gen_labels_OB(id, labels, object_or_background, random_erase=random_erase, random_erase_mode=random_erase_mode, guassian_sigma=guassian_sigma) #use os.path.basename() to keep only base directory for id        
      
      bbox = mo.unnormalize(labels,mo.dataset)
      
      
      # mo.rm_bg(id[:-4]+".jpg", bbox) #make background becomes black
      
      # #remove the hand object
      # mo.rm_object(id[:-4]+".jpg", bbox) #make hands become black
      # mo.rm_not_obj(id[:-4]+".jpg", bbox) #make objects other than hands become black
      # mo.rm_all_obj(id[:-4]+".jpg", bbox, random_erase=False) #make all objects (including hands) become black
      if object_or_background == "background":
          print("INFO: mutation operator: guassian noise to background")
          mo.add_guassian_noise_to_bg(id[:-4]+".jpg", bbox, guassian_sigma)
      elif object_or_background == "object":
          print("INFO: mutation operlsator: random erase object")
          mo.rm_all_obj(id[:-4]+".jpg", bbox, random_erase=random_erase,random_erase_mode=random_erase_mode,guassian_sigma=guassian_sigma)
      else:
        raise ValueError("invalid parameter value: expected background or object but got " + str(object_or_background))
      print(id+" -- done", len(labels), "labels")
      # hv_label += 1
      # mut += len(labels)
      return 
  

def main(image_path,label_path,write_path,random_erase,guassian_sigma,random_erase_mode,dataset_normalization_type,object_or_background,dataset):
    # image width and height
    WIDTH = None
    HEIGHT = None
    if dataset == "ego":
      WIDTH = 1280
      HEIGHT = 720
    elif dataset == "company":
      WIDTH = 640
      HEIGHT = 480
    else:
      raise ValueError(f"Expected dataset as ego or company, but got {dataset}")
    mo = mutation_operation(image_path,label_path,write_path,WIDTH,HEIGHT,dataset_normalization_type)
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
    # if not os.path.exists(write_path + 'B_r:andom_erase'):
    #     os.mkdir(write_path + 'B_random_erase')
    # if not os.path.exists(write_path + 'B_random_erase'):
    #     os.mkdir(write_path + 'B_random_erase')

    # copy list of labels
    # os.chdir(label_path)
    label_list = glob.glob(label_path + "*.txt")
    # label_list = [os.path.basename(i) for i in all_paths] #drop parent directory path
    # print("label path is : " + str(label_path + "*.txt"))
    # print("number of labels obtained: " + str(len(label_list)))
    # log_name = mo.gen_log_name(random_erase=random_erase, random_erase_mode=random_erase_mode, guassian_sigma=guassian_sigma)
    # mo.remove_log(log_name)
    no_label = 0
    hv_label = 0
    mut = 0
    #iterate through a list of labels
    print("Initiating multi-processes")
    n_jobs_parameter=15
    # if __debug__:
    #   label_list = label_list[:12]
    #   n_jobs_parameter=5
    # Parallel(n_jobs=n_jobs_parameter)(delayed(perform_mutation)(mo,id,random_erase,random_erase_mode,guassian_sigma) for id in label_list)
    pool = Pool(processes=n_jobs_parameter)
    start_time = time.time()
    print("label_list: " + str(len(label_list)))
    for id in label_list:
      print("INFO: processing id " + str(id))
      if os.name == 'nt':
          print(f"processing label id {id}")
          perform_mutation(mo,id,random_erase,random_erase_mode,guassian_sigma,object_or_background)
      else:
          # perform_mutation(mo,id,random_erase,random_erase_mode,guassian_sigma,object_or_background)
          result = pool.apply_async(perform_mutation, args=(mo,id,random_erase,random_erase_mode,guassian_sigma,object_or_background))
    # print("Number of seconds by using multi-processing: " + str(time.time() - start_time))
    pool.close()
    pool.join()
      # p = Process(target=perform_mutation, args=(mo,id,random_erase,random_erase_mode,guassian_sigma))
      # p.start()
      # p.join()
    # print("--------finished-------")
    # print("total: ", no_label+hv_label, "images")
    # print("images with labels: ", hv_label)
    # print("images without labels: ", no_label)
    # print(mut, " sets of obj and bg generated")
    # mo.log_finish(log_name)

if __name__ == "__main__":
    image_path = None
    label_path = None
    mutate_path = None
    random_erase = None
    guassian_sigma = None
    random_erase_mode = None
    if __debug__ and os.name == 'nt': #os.name == 'nt' is for checking whether the os is window
      image_path = "ego_hand/train/"
      label_path = "ego_hand/train/"
      mutate_path = "working_dir/mutate/"
      random_erase = 0.9
      guassian_sigma = 0.0
      random_erase_mode = "fixMutRatio_centerXY"
      dataset = "company"
      object_or_background = "object"
    else:
      #random_erase_mode
      parser = argparse.ArgumentParser()
      parser.add_argument('--image_path', help='path to original images',required=True)
      parser.add_argument('--label_path', help="path to labels",required=True)
      parser.add_argument('--mutate_path', help="path to mutated images",required=True)
      parser.add_argument('--random_erase', help="proportion of an object region being erased",required=True)
      parser.add_argument('--guassian_sigma', help="the guassian noise's variance",required=True)
      parser.add_argument('--object_or_background', help="mutate object or background",required=True)
      parser.add_argument('--random_erase_mode', help="random erase mode: fixMutRatio, varyMutRatio, fixXY, varyXY, centerXY. fixMutRatio means every hand has exactly the same mutaton ratio e.g., 0.7, varyMutRatio means every hand has slightly different mutation ratio, but on average a particular value. Use underscore to connect the parameters, e.g., fixMutRatio_fixXY",required=True)
      parser.add_argument('--dataset', help="company or ego",required=True)
      flags, unknown = parser.parse_known_args()
      image_path = flags.image_path
      label_path = flags.label_path
      mutate_path = flags.mutate_path
      random_erase = flags.random_erase
      guassian_sigma = flags.guassian_sigma
      dataset = flags.dataset
      object_or_background = flags.object_or_background
      random_erase_mode = flags.random_erase_mode
      dataset_normalization_type = "company"
      
    
    # image_path = "/data1/wcleungag/ImageSet/"
    # label_path = "/data1/wcleungag/labels/"
    # write_path = "/data1/wcleungag/mutated_dataset_all/"
    main(image_path,label_path,mutate_path,float(random_erase),float(guassian_sigma),random_erase_mode,dataset_normalization_type,object_or_background,dataset)
