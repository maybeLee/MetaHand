import json
import pathlib
import shutil

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
            print("category_id is: " + str(image_category))
            if image_category == "0":
                image_id = str(each_image_label["image_id"])
                bbox = each_image_label["bbox"]
                write_to_file_line = image_category + " "
                for each_coordinate in bbox:
                    if each_coordinate == bbox[-1]:
                        write_to_file_line = write_to_file_line + str(each_coordinate)
                        break
                    write_to_file_line = write_to_file_line + str(each_coordinate) + " "
                if image_id not in file_name_to_category_bbox_dict:
                    file_name_to_category_bbox_dict[image_id] = [write_to_file_line]
                else:
                    file_name_to_category_bbox_dict[image_id].append([write_to_file_line])
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
        self.create_empty_file()
        for each_image_id in file_name_to_category_bbox_dict:
            file_name = "000000" + each_image_id + ".jpg"
            shutil.copy2(self.source_image_path + file_name, self.object_dir_path + "images")
            self.write_label(file_name_to_category_bbox_dict,each_image_id,file_name)
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
        
def test1():
    source_image_path = "source_data/data/"
    source_label_path = "source_data/label/"
    working_dir_path = "working_dir/"
    object_category = "person"
    json_path = source_label_path + "label_example.json"
    cc_o = coco_train_mut_class(source_image_path,source_label_path,working_dir_path,object_category)
    json_data = cc_o.read_label(json_path)
    file_name_to_category_bbox_dict = cc_o.preserve_label_of_one_object(json_data)
    print(str(file_name_to_category_bbox_dict))
    cc_o.cp_file_to_working_directory(file_name_to_category_bbox_dict,object_name="person")
        # datastore = json.loads(json_string)

def parse_arguement():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_image_path', help='path to original images',required=True)
    parser.add_argument('--source_label_path', help="path to original labels",required=True)
    parser.add_argument('--working_dir_path', help="path to working directory (i.e., dir for gen mutated ",required=True)
    parser.add_argument('--object_category', help="object category",required=True)
    flags, unknown = parser.parse_known_args()
if __name__ == "__main__":
    test1()