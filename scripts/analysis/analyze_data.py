from cgitb import handler
import os


class DatasetAnalyzer(object):
    def __init__(self, label_dir):
        self.label_dir = label_dir
        self.label_dict = {}  # {img_name: [obj1, obj2, ...]}

    def load_labels(self):
        img_list = os.listdir(self.label_dir)
        for img_path in img_list:
            self.label_dict[img_path] = []
            content = None
            with open(os.path.join(self.label_dir, img_path), "r") as file:
                content = file.read().split("\n")[:-1]
            for line in content:
                self.label_dict[img_path].append(line)

    def total_objects(self):
        total_num = 0
        for img in self.label_dict:
            total_num += len(self.label_dict[img])
        return total_num

    def total_imgs(self):
        return len(self.label_dict)

    def avg_objects(self):
        return self.total_objects()/self.total_imgs()

    def total_sizes(self):
        total_size = 0
        for img, hand_list in self.label_dict.items():
            for hand in hand_list:
                hand = hand.strip()
                w = float(hand.split(" ")[-2])
                h = float(hand.split(" ")[-1])
                total_size += w*h
        return total_size

    def avg_objects_types(self):
        total_obj_type = 0
        for img, hand_list in self.label_dict.items():
            type_list = []
            for hand in hand_list:
                hand = hand.strip()
                obj_type = int(hand.split(" ")[0])
                if obj_type not in type_list:
                    type_list.append(obj_type)
            total_obj_type += len(type_list)
        return total_obj_type / self.total_imgs()
        
    def avg_objects_size(self):
        return self.total_sizes()/self.total_imgs()
    
    def empty_imgs(self):
        empty_num = 0
        for img in self.label_dict:
            if len(self.label_dict[img]) == 0:
                empty_num += 1
        return empty_num

    def analyze(self):
        self.load_labels()
        print(f"The total img of is: {self.total_imgs()}, "
              f"The total number of hands is: {self.total_objects()}, "
              f"The average hands is: {self.avg_objects()},"
              f"The average hands' size is: {self.avg_objects_size()},"
              f"The average object type number is: {self.avg_objects_types()},"
              f"The total number of empty img is: {self.empty_imgs()}")


if __name__ == "__main__":
    company_label_dir = "/ssddata1/users/dlproj/MetaHand/data_company/Labels"
    egohands_label_dir = "/ssddata1/users/dlproj/MetaHand/data_egohands/labels"
    coco_label_dir = "/ssddata1/users/dlproj/MetaHand/data_coco/labels"
    # DatasetAnalyzer(company_label_dir).analyze()
    # DatasetAnalyzer(egohands_label_dir).analyze()
    DatasetAnalyzer(coco_label_dir).analyze()

