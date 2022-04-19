import os


def get_part_kitti2015(dataset_path="kitti2015", keep_num=20):
    """
        Function: get part of kitti2015 dataset

        """

    # train and testing
    for i_set in os.listdir(dataset_path):
        set_path = os.path.join(dataset_path, i_set)
        # each class
        for i_dir in os.listdir(set_path):
            class_path = os.path.join(set_path, i_dir)
            # each image
            for j_index, j_image in enumerate(os.listdir(class_path)):
                if j_index >= keep_num:
                    image_path = os.path.join(class_path, j_image)
                    os.remove(image_path)

    return True


def get_part_flyingchairs(dataset_path=""):
    pass

if __name__ == "__main__":
    get_part_kitti2015()
