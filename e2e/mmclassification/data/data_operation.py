import os


def imagenet_gen_ann(image_path="imagenet", ann_path="imagenet/meta/val.txt"):
    """
    Function: make class annotation for imagenet

    """

    content = ""

    # train and val
    for i_set in os.listdir(image_path):
        if i_set == "train":
            continue

        class_cnt = -1
        # each class
        set_path = os.path.join(image_path, i_set)
        for i_dir in os.listdir(set_path):
            class_cnt += 1
            for home, dirs, files in os.walk(os.path.join(set_path, i_dir)):
                for j_files in files:
                    content = content + str(i_dir) + "/" + j_files      # add the file path
                    content = content + " " + str(class_cnt)        # add the class
                    content = content + '\n'

    if not os.path.exists(os.path.dirname(ann_path)):
        os.makedirs(os.path.dirname(ann_path))
    with open(ann_path, 'w+') as ann:
        ann.write(content)

    return True


def imagenet_1PicPerClass(image_path="imagenet"):
    # train and val
    for i_set in os.listdir(image_path):
        # each class
        set_path = os.path.join(image_path, i_set)
        for i_dir in os.listdir(set_path):
            # each picture
            class_path = os.path.join(set_path, i_dir)
            for j_cnt, j_file in enumerate(os.listdir(class_path)):
                if j_cnt > 0:
                    os.remove(os.path.join(class_path, j_file))

    return True


if __name__ == '__main__':
    # imagenet_1PicPerClass()
    imagenet_gen_ann()

