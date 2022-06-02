import json
import pathlib
import shutil
import argparse
import os
import logging
class coco_train_mut_class:
    
    def __init__(self,source_image_path,source_label_path,working_dir_path,object_category):
        self.source_image_path = source_image_path
        self.source_label_path = source_label_path
        self.working_dir_path = working_dir_path
        self.object_category = object_category
        self.object_dir_path = working_dir_path + object_category + "/"
        
    def other_object_label_removal(self):
        dummy = 1
        
    def preserve_label_of_one_object(self,json_data):
        file_name_to_category_bbox_dict = {}
        # image_file_prefix = "000000"
        for each_image_label in json_data["annotations"]:
            # image_file_name = "000000" + each_image_label["image_id"] + ".jpg"
            image_category = str(each_image_label["category_id"])
            # print("category_id is: " + str(image_category))
            if image_category == self.category_to_id(self.object_category):
                image_id = str(each_image_label["image_id"])
                bbox = each_image_label["bbox"]
                counter = 0
                if image_id not in file_name_to_category_bbox_dict:
                        file_name_to_category_bbox_dict[image_id] = []  
                
                write_to_file_line = "0 "
                for each_coordinate in bbox:
                    if each_coordinate == bbox[-1]:
                        write_to_file_line = write_to_file_line + str(each_coordinate) + "\n"
                    else:
                        write_to_file_line = write_to_file_line + str(each_coordinate) + " "
                file_name_to_category_bbox_dict[image_id].append(write_to_file_line)
                
                if __debug__:
                    # file_name_to_category_bbox_dict[image_id].append(bbox)
                    logging.debug("file_name_to_category_bbox_dict[image_id] is: image id " + str(image_id) + ", value: " + str(file_name_to_category_bbox_dict[image_id]))
                        # break
                #     write_to_file_line = write_to_file_line + str(each_coordinate) + " "
                # if image_id not in file_name_to_category_bbox_dict:
                #     file_name_to_category_bbox_dict[image_id] = [write_to_file_line]
                # else:
                #     file_name_to_category_bbox_dict[image_id].append([write_to_file_line])
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
                #         file_name_to_category_bbox_dict[image_id].append(write_to_file_line)
                #     else:
                #         write_to_file_line += write_to_file_line + str(each_coordinate) + " "
                #     counter += 1
                    
                    # if each_coordinate == bbox[-1]:
                    #     write_to_file_line = write_to_file_line + str(each_coordinate)
                    #     break
                    # write_to_file_line = write_to_file_line + str(each_coordinate) + " "

                # else:
                    
            # if len(file_name_to_category_bbox_dict[image_id]) == 0:
            #     raise ValueError("no")
        return file_name_to_category_bbox_dict

    def create_empty_file(self):
        # path_
        filename_list = ["training.txt","testing.txt"]
        for filename in filename_list:
            # filepath = os.path.join(self.working_dir_path+'label', filename)
            f = open(self.object_dir_path + filename, "w+")
            # for i in range(len(labels)):
            f.write('\n')
            f.close()
            # cnt+=1

    def write_label(self,file_name_to_category_bbox_dict,each_image_id,file_name):
        f = open(self.object_dir_path + "labels/" + file_name + "-" + "B.txt", 'w+')
        for each_label in file_name_to_category_bbox_dict[each_image_id]:
            f.write(each_label)
        f.close()

    def cp_file_to_working_directory(self, file_name_to_category_bbox_dict,object_name="person"):
        pathlib.Path(self.working_dir_path + object_name).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.object_dir_path + "images").mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.object_dir_path + "labels").mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.object_dir_path + "mutate").mkdir(parents=True, exist_ok=True)
        num_image_processed = 0
        num_image_found = 0
        self.create_empty_file()
        for each_image_id in file_name_to_category_bbox_dict:
            num_image_processed += 1
            each_image_id_with_zero_ahead = "000000" + each_image_id
            file_name = "000000" + each_image_id_with_zero_ahead[-6:] + ".jpg"
            # logging.info("each_image_id_with_zero_ahead[-6:] is: " + str(each_image_id_with_zero_ahead[-6:]))
            if os.path.isfile(self.source_image_path + file_name):
                num_image_found += 1
                shutil.copy2(self.source_image_path + file_name, self.object_dir_path + "images")
            else:
                # if len(file_name) != 16:
                logging.info("the image cannot be found is: " + str(file_name))
            self.write_label(file_name_to_category_bbox_dict,each_image_id,file_name)
        logging.info("num_image_processed: " + str(num_image_processed) + ", num_image_found: " + str(num_image_found))
            # shutil.copy2(self.source_image_path + file_name, self.object_dir_path + "images")
            


        # shutil.copyfile(self.source_data_path + , dst)
        # for each_file_name in file_name_to_category_bbox_dict:
            
        
    def read_label(self,label_json_path):
        json_data = None
        with open(label_json_path, "r") as read_file:
            # json_dump = json.dumps(read_file)
            json_data = json.loads(read_file.read())
        return json_data
        # labels = json_data["annotations"][0]["bbox"]
        # print("labels: " + str(labels))
        # return labels
        
    def category_to_id(self,category):
        category_to_id_dict = {
            "person":"1",
            "airplane":"5"
        }
        return category_to_id_dict[category]
        
def test1():
    source_image_path = "source_data/data/"
    source_label_path = "source_data/label/label_example.json"
    working_dir_path = "working_dir/"
    object_category = "airplane"
    # json_path = source_label_path + ""
    cc_o = coco_train_mut_class(source_image_path,source_label_path,working_dir_path,object_category)
    json_data = cc_o.read_label(source_label_path)
    file_name_to_category_bbox_dict = cc_o.preserve_label_of_one_object(json_data)
    #print(str(file_name_to_category_bbox_dict))
    cc_o.cp_file_to_working_directory(file_name_to_category_bbox_dict,object_name="person")
        # datastore = json.loads(json_string)1

def parse_arguement():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_image_path', help='path to original images',required=True)
    parser.add_argument('--source_label_path', help="path to original labels",required=True)
    parser.add_argument('--working_dir_path', help="path to working directory (i.e., dir for gen mutated ",required=True)
    parser.add_argument('--object_category', help="object category",required=True)
    parser.add_argument('--json', help="which json file to read",required=True)
    flags, unknown = parser.parse_known_args()
    return flags

def main():
    flags = parse_arguement()
    source_image_path = flags.source_image_path
    source_label_path = flags.source_label_path
    working_dir_path = flags.working_dir_path
    object_category = flags.object_category
    json_file = flags.json
    cc_o = coco_train_mut_class(source_image_path,source_label_path,working_dir_path,object_category)
    json_data = cc_o.read_label(source_label_path + json_file) #get label data
    file_name_to_category_bbox_dict = cc_o.preserve_label_of_one_object(json_data)
    cc_o.cp_file_to_working_directory(file_name_to_category_bbox_dict,object_name="airplane")
    
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test1()