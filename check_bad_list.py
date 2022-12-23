from tkinter.filedialog import LoadFileDialog


bad_list_path = "./bad.list"
train_path = "./data_coco/training_id.txt"
test_path = "./data_coco/testing_id.txt"

def load_file(file_path):
    img_list = []
    with open(file_path, "r") as file:
        content =file.read().split("\n")[:-1]
    for line in content:
        img_list.append(line)
    return img_list

bad_list = load_file(bad_list_path)
train_list = load_file(train_path)
test_list = load_file(test_path)
train_count = 0
test_count = 0
for bad in bad_list:
    bad = bad.replace(".txt", ".jpg")
    bad = bad.replace("labels", "images")
    if bad in train_list:
        print(f"Find {bad} on training")
        train_count += 1
    if bad in test_list:
        print(f"Find {bad} on testing")
        test_count += 1
    if bad not in train_list and bad not in test_list:
        print(f"ERROR: I don't know where did we get this img: {bad}")

print(f"Training Count: {train_count}, Testing Count: {test_count}")
