import json
import pathlib 
class coco_train_mut_class:
    
    def __init__(self):
        self.dummy = 1
        
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
                image_file_name = str(each_image_label["image_id"])
                bbox = each_image_label["bbox"]
                write_to_file_line = image_category + " "
                for each_coordinate in bbox:
                    if each_coordinate == bbox[-1]:
                        write_to_file_line = write_to_file_line + str(each_coordinate)
                        break
                    write_to_file_line = write_to_file_line + str(each_coordinate) + " "
                file_name_to_category_bbox_dict[image_file_name] = write_to_file_line
        return file_name_to_category_bbox_dict
    
    def cp_file_to_working_directory(file_name_to_category_bbox_dict):
        pathlib.Path('person').mkdir(parents=True, exist_ok=True)
        pathlib.Path('person/ImageSet').mkdir(parents=True, exist_ok=True)
        pathlib.Path('person/labels').mkdir(parents=True, exist_ok=True)
        pathlib.Path('person/mutate').mkdir(parents=True, exist_ok=True)
        for each_file_name in file_name_to_category_bbox_dict:
            
        
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
    path = "source_data\label_example.json"
    cc_o = coco_train_mut_class()
    json_data = cc_o.read_label(path)
    file_name_to_category_bbox_dict = cc_o.preserve_label_of_one_object(json_data)
    print(str(file_name_to_category_bbox_dict))
        # datastore = json.loads(json_string)
        
if __name__ == "__main__":
    test1()