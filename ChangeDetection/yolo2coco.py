import os
import json
from tqdm import tqdm


def yolo2coco(image_path, txt_path, save_path, save_file_name, categories, start_id=0):
    """
    :param image_path:
    :param txt_path:
    :param save_path:
    :param save_file_name:
    :param categories: 检测类别
    :param start_id: image初始编号
    :return:
    """
    image_list = os.listdir(image_path)
    txt_list = os.listdir(txt_path)

    json_dict = {'info': '1', 'license': []}

    images_list = []
    annotations_list = []
    categories_list = []

    # images
    for i in tqdm(range(len(image_list))):
        images_dict = {}
        images_dict['file_name'] = image_list[i]
        images_dict['height'] = 2000
        images_dict['width'] = 2000
        images_dict['id'] = i + 1 + start_id
        images_list.append(images_dict)

    # annotations
    count = 0
    for j in tqdm(range(len(txt_list))):
        # read_txt
        with open(os.path.join(txt_path, txt_list[j]), 'r') as f1:
            label_lines = [x.strip() for x in f1.readlines() if len(x.strip()) > 0]

        for line in label_lines:
            x_c = float(line.split(' ')[1]) * 2000
            y_c = float(line.split(' ')[2]) * 2000
            w = int(float(line.split(' ')[3]) * 2000)
            h = int(float(line.split(' ')[4]) * 2000)
            x = int(x_c - w / 2)
            y = int(y_c - h / 2)

            annotations_dict = {}
            annotations_dict['id'] = count
            count += 1
            annotations_dict['image_id'] = image_list.index(txt_list[j][:-3] + 'jpg') + 1 + start_id
            annotations_dict['category_id'] = 1
            annotations_dict['segmentation'] = []
            annotations_dict['area'] = w * h
            annotations_dict['bbox'] = [x, y, w, h]
            annotations_dict['iscrowd'] = 0
            annotations_list.append(annotations_dict)

    # categories
    for cate in categories:
        categories_list.append(cate)

    json_dict['images'] = images_list
    json_dict['annotations'] = annotations_list
    json_dict['categories'] = categories_list

    with open(os.path.join(save_path, save_file_name), 'w') as f2:
        json.dump(json_dict, f2)


if __name__ == '__main__':
    # ------------------------------------------------------------------------
    # yolo2coco
    txt_floder = r'D:\Projects\DL\mmdetection-master\8_2\train\labels'
    image_floder = r'D:\Projects\DL\mmdetection-master\8_2\train\images'

    save_floder = r'D:\Projects\DL\mmdetection-master\8_2\train'
    save_file_name = 'train.json'

    categories = [{'id': 1, 'name': 'meconium'}]

    yolo2coco(image_floder, txt_floder, save_floder, save_file_name, categories, start_id=0)
    # ------------------------------------------------------------------------
    # coco2yolo

    # ------------------------------------------------------------------------
