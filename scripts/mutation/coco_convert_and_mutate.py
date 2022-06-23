import json
import pathlib
import shutil
import argparse
import os
import logging
import xml.etree.ElementTree as ET
import glob
import scipy.io

class coco_train_mut_class:
    
    def __init__(self,source_image_path,source_label_path,working_dir_path,object_category="dummy"):
        self.source_image_path = source_image_path
        self.source_label_path = source_label_path
        self.working_dir_path = working_dir_path
        self.object_category = object_category
        self.object_dir_path = working_dir_path + object_category + "/"
        
    def other_object_label_removal(self):
        dummy = 1
    
    def add_corr_to_file(self,image_id_to_category_bbox_dict,image_id,category_id,bbox):
        if image_id not in image_id_to_category_bbox_dict:
            image_id_to_category_bbox_dict[image_id] = []
        write_to_file_line = str(category_id) + " "
        for counter, each_coordinate in enumerate(bbox):
            if counter == 3:
                write_to_file_line = write_to_file_line + str(each_coordinate) + "\n"
            else:
                write_to_file_line = write_to_file_line + str(each_coordinate) + " "
        image_id_to_category_bbox_dict[image_id].append(write_to_file_line)
    
    def preserve_label_of_one_object(self,json_data,type="none"):
        image_id_to_category_bbox_dict = {}
        # image_file_prefix = "000000"
        if type == "json":
            for counter, each_image_label in enumerate(json_data["annotations"]):
                print("processing " + str(counter) + "th image\n")
                # image_file_name = "000000" + each_image_label["image_id"] + ".jpg"
                image_category = str(each_image_label["category_id"])
                # print("category_id is: " + str(image_category))
                # if image_category == self.category_to_id(self.object_category):
                image_id = str(each_image_label["image_id"])
                bbox = each_image_label["bbox"]
                counter = 0
                category_id = each_image_label["category_id"]
                self.add_corr_to_file(image_id_to_category_bbox_dict,image_id,category_id,bbox)
        elif type == "xml":
            classes = ["person","bird", "cat", "cow", "dog", \
                    "horse", "sheep", "aeroplane", "bicycle", "boat", \
                    "bus", "car", "motorbike", "train", \
                    "bottle", "chair", "diningtable", "pottedplant", "sofa", "tvmonitor"]
            image_id = json_data.find('filename').text.replace(".jpg","")
            for each_object in json_data.findall('object'):
                bbox = []
                category = each_object.find('name').text
                print("name: " + str(category))
                category_id = classes.index(category)
                # for each_object in json_data.findall('object'):
                #     print("got list: " + str(each_object.find('name').text))
                # print("each_object.find('bndbox'): " + str(each_object.find('bndbox')))
                # for bndbox_corr in each_object.find('bndbox'):
                    # bbox.append(bndbox_corr.text)
                x_max = each_object.find('bndbox').find('xmax').text
                x_min = each_object.find('bndbox').find('xmin').text
                y_max = each_object.find('bndbox').find('ymax').text
                y_min = each_object.find('bndbox').find('ymin').text
                h = float(y_max) - float(y_min) 
                w = float(x_max) - float(x_min)
                    # print("bndbox corrdination: " + str(bndbox_corr.text))
                bbox = [x_min,y_min,w,h]
                self.add_corr_to_file(image_id_to_category_bbox_dict,image_id,category_id,bbox)
        else:
            raise ValueError("invalid parameter, expected json or xml but got " + type)
            # for counter, each_image_label in enumerate(json_data["annotations"]):
            #     print("processing " + str(counter) + "th image\n")
            #     # image_file_name = "000000" + each_image_label["image_id"] + ".jpg"
            #     image_category = str(each_image_label["category_id"])
            #     # print("category_id is: " + str(image_category))
            #     # if image_category == self.category_to_id(self.object_category):
            #     image_id = str(each_image_label["image_id"])
            #     bbox = each_image_label["bbox"]
            #     counter = 0
            #     if image_id not in image_id_to_category_bbox_dict:
            #             image_id_to_category_bbox_dict[image_id] = []  
                
            #     write_to_file_line = str(each_image_label["category_id"]) + " "
            #     for counter, each_coordinate in enumerate(bbox):
            #         if counter == 3:
            #             write_to_file_line = write_to_file_line + str(each_coordinate) + "\n"
            #         else:
            #             write_to_file_line = write_to_file_line + str(each_coordinate) + " "
            #     image_id_to_category_bbox_dict[image_id].append(write_to_file_line)

        if __debug__:
            # image_id_to_category_bbox_dict[image_id].append(bbox)
            logging.debug("image_id_to_category_bbox_dict[image_id] is: image id " + str(image_id) + ", value: " + str(image_id_to_category_bbox_dict[image_id]))
                        # break
                #     write_to_file_line = write_to_file_line + str(each_coordinate) + " "
                # if image_id not in image_id_to_category_bbox_dict:
                #     image_id_to_category_bbox_dict[image_id] = [write_to_file_line]
                # else:
                #     image_id_to_category_bbox_dict[image_id].append([write_to_file_line])
            # else:
            #     raise ValueError("category id not exists")     
                # for each_coordinate in bbox:
                #     # logging.info("counter is: " + str(counter))
                #     if counter > 3:
                #         logging.info("counter larger than4, the bbox is: " + str(bbox))
                #     if counter%4 == 0:
                #         write_to_file_line = "0 " + str(each_coordinate) + " "
                #     elif counter%4 == 3:
                #         write_to_file_line += write_to_file_line + str(each_coordinate) + "\n"
                #         image_id_to_category_bbox_dict[image_id].append(write_to_file_line)
                #     else:
                #         write_to_file_line += write_to_file_line + str(each_coordinate) + " "
                #     counter += 1
                    
                    # if each_coordinate == bbox[-1]:
                    #     write_to_file_line = write_to_file_line + str(each_coordinate)
                    #     break
                    # write_to_file_line = write_to_file_line + str(each_coordinate) + " "

                # else:
                    
            # if len(image_id_to_category_bbox_dict[image_id]) == 0:
            #     raise ValueError("no")
        return image_id_to_category_bbox_dict
    
    def convert_matlab_label(self):
        all_boxes = scipy.io.loadmat('test_case\mat\Buffy_1.mat')
        max_x = None
        min_x = None
        max_y = None
        min_y = None
        for each_box in all_boxes:
            for all_coordinate in each_box:
                for each_coordinate in all_coordinate:
                    if max_x == None or min_x == None:
                        max_x = each_coordinate[0]
                    
        print(mat)

    def create_empty_file(self):
        # path_
        filename_list = ["training.txt","testing.txt"]
        for filename in filename_list:
            # filepath = os.path.join(self.working_dir_path+'label', filename)
            f = open(self.working_dir_path + filename, "w+")
            # for i in range(len(labels)):
            f.write('\n')
            f.close()
            # cnt+=1

    def write_label(self,image_id_to_category_bbox_dict,each_image_id,file_name):
        f = open(self.working_dir_path + "labels/" + file_name.replace(".jpg",".txt"), 'w+')
        for each_label in image_id_to_category_bbox_dict[each_image_id]:
            f.write(each_label)
        f.close()

    def cp_file_to_working_directory(self, image_id_to_category_bbox_dict,type="none"):
        pathlib.Path(self.working_dir_path + "images").mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.working_dir_path + "labels").mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.working_dir_path + "mutate").mkdir(parents=True, exist_ok=True)
        num_image_processed = 0
        num_image_found = 0
        self.create_empty_file()
        for each_image_id in image_id_to_category_bbox_dict:
            num_image_processed += 1
            each_image_id_with_zero_ahead = "000000" + each_image_id
            file_name = "000000" + each_image_id_with_zero_ahead[-6:] + ".jpg"
            if type == "xml":
                file_name = each_image_id + ".jpg"
            # logging.info("each_image_id_with_zero_ahead[-6:] is: " + str(each_image_id_with_zero_ahead[-6:]))
            if os.path.isfile(self.source_image_path + file_name):
                num_image_found += 1
                shutil.copy2(self.source_image_path + file_name, self.working_dir_path + "images")
            else:
                # if len(file_name) != 16:
                logging.info("the image cannot be found is: " + str(file_name))
            self.write_label(image_id_to_category_bbox_dict,each_image_id,file_name)
        logging.info("num_image_processed: " + str(num_image_processed) + ", num_image_found: " + str(num_image_found))
            # shutil.copy2(self.source_image_path + file_name, self.object_dir_path + "images")
            


        # shutil.copyfile(self.source_data_path + , dst)
        # for each_file_name in image_id_to_category_bbox_dict:
            
        
    def read_label(self,label_path,type="none"):
        label_data = None
        if type == "json":
            with open(label_path, "r") as read_file:
                # json_dump = json.dumps(read_file)
                label_data = json.loads(read_file.read())
        elif type == "xml":
            tree = ET.parse(label_path)
            label_data = tree.getroot()
        else:
            raise ValueError("invalid file type")       
        return label_data
        # labels = json_data["annotations"][0]["bbox"]
        # print("labels: " + str(labels))
        # return labels
        
    def category_to_id(self,category):
        category_to_id_dict = {
            "person":"1",
            "airplane":"5"
        }
        return category_to_id_dict[category]

def test_mat_converter():
    source_image_path = "source_data/data/"
    source_label_path = "source_data/label/label_example.json"
    working_dir_path = "working_dir/"
    object_category = "airplane"
    # json_path = source_label_path + ""
    cc_o = coco_train_mut_class(source_image_path,source_label_path,working_dir_path,object_category)
    cc_o.convert_matlab_label()

def test_coco():
    source_image_path = "source_data/data/"
    source_label_path = "source_data/label/label_example.json"
    working_dir_path = "working_dir/"
    object_category = "airplane"
    # json_path = source_label_path + ""
    cc_o = coco_train_mut_class(source_image_path,source_label_path,working_dir_path,object_category)
    label_data = cc_o.read_label(source_label_path)
    image_id_to_category_bbox_dict = cc_o.preserve_label_of_one_object(label_data)
    #print(str(image_id_to_category_bbox_dict))
    cc_o.cp_file_to_working_directory(image_id_to_category_bbox_dict,object_name="person")
        # datastore = json.loads(json_string)1
        
def test_voc():
    source_image_path = "source_data/data/voc/"
    source_label_path = "source_data/label/voc/"
    working_dir_path = "working_dir/voc/"
    # json_path = source_label_path + ""
    for each_label_file_path in glob.glob(source_label_path + "*.xml"):
        print("each_label_file_path: " + each_label_file_path)
        cc_o = coco_train_mut_class(source_image_path,each_label_file_path,working_dir_path)
        label_data = cc_o.read_label(each_label_file_path,type="xml")
        image_id_to_category_bbox_dict = cc_o.preserve_label_of_one_object(label_data,type="xml")
        cc_o.cp_file_to_working_directory(image_id_to_category_bbox_dict,type="xml")
    # for child in bndbox_corr:
    #     print("getting object name child")
    #     print("object name: " + str(child.text))
    
    # image_id_to_category_bbox_dict = cc_o.preserve_label_of_one_object(label_data)
    #print(str(image_id_to_category_bbox_dict))
    # cc_o.cp_file_to_working_directory(image_id_to_category_bbox_dict,object_name="person")
        # datastore = json.loads(json_string)1

def parse_arguement():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_image_path', help='path to original images',required=True)
    parser.add_argument('--source_label_path', help="path to original labels",required=True)
    parser.add_argument('--working_dir_path', help="path to working directory (i.e., dir for gen mutated ",required=True)
    # parser.add_argument('--object_category', help="object category",required=True)
    parser.add_argument('--json', help="which json file to read",required=True)
    parser.add_argument('--dataset', help="coco or voc",required=True)
    flags, unknown = parser.parse_known_args()
    return flags

def main():
    flags = parse_arguement()
    source_image_path = flags.source_image_path
    source_label_path = flags.source_label_path
    working_dir_path = flags.working_dir_path
    # object_category = flags.object_category
    json_file = flags.json
    dataset_name = flags.dataset
    if dataset_name == "coco":
        cc_o = coco_train_mut_class(source_image_path,source_label_path,working_dir_path)
        json_data = cc_o.read_label(source_label_path + json_file) #get label data
        image_id_to_category_bbox_dict = cc_o.preserve_label_of_one_object(json_data)
        cc_o.cp_file_to_working_directory(image_id_to_category_bbox_dict,type="xml")
    elif dataset_name == "voc":
        for each_label_file_path in glob.glob(source_label_path + "*.xml"):
            # print("each_label_file_path: " + each_label_file_path)
            cc_o = coco_train_mut_class(source_image_path,each_label_file_path,working_dir_path)
            label_data = cc_o.read_label(each_label_file_path,type="xml")
            image_id_to_category_bbox_dict = cc_o.preserve_label_of_one_object(label_data,type="xml")
            cc_o.cp_file_to_working_directory(image_id_to_category_bbox_dict,type="xml")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if __debug__:
        # test_voc()
        test_mat_converter()
    else:
        main()