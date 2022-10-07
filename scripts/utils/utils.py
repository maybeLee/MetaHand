import os


def deprecated(func):
    """
    This is a decorator for deprecated functions.
    """
    def wrapper(*args, **kwargs):
        print(f"[Warning] Function '{func.__name__}' is deprecated.")
        return func(*args, **kwargs)
    return wrapper


def get_files(target_dir, end_pattern):
    # input: root path of specific frameworks
    # output: list format: ["file_dir_1", "file_dir_2", ...]
    # function, go through all files in the framework and only find python files
    file_lists = []
    for root, subdirs, files in os.walk(target_dir):
        for file in files:
            if not file.endswith(end_pattern):
                continue
            file_lists.append(os.path.join(root, file))
    return file_lists

class YoloUtils:

    @staticmethod
    def center_to_topleft(label):
        return [label[0] - label[2] / 2, label[1] - label[3] / 2, label[2], label[3]]

    @staticmethod
    def overlapping(label, pred):
        # calculation of overlapping ratio in IoU
        label = [label[0]] + YoloUtils.center_to_topleft(label[1:5])
        x1 = label[1]
        y1 = label[2]
        w1 = label[3]
        h1 = label[4]

        x2 = pred[1]
        y2 = pred[2]
        w2 = pred[3]
        h2 = pred[4]

        XA1 = x1
        XA2 = x1 + w1
        YA1 = y1
        YA2 = y1 + h1
        XB1 = x2
        XB2 = x2 + w2
        YB1 = y2
        YB2 = y2 + h2

        SI = max(0, min(XA2, XB2) - max(XA1, XB1)) * max(0, min(YA2, YB2) - max(YA1, YB1))
        SA = w1 * h1
        SB = w2 * h2
        SU = SA + SB - SI

        return SI / SU
