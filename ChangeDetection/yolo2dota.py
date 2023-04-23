import os
import cv2
from tqdm import tqdm


def yolo2dota(image_path, label_path, save_path):
    image_list = os.listdir(image_path)
    label_list = os.listdir(label_path)

    for label_item in tqdm(range(len(label_list))):
        img = cv2.imread(os.path.join(image_path, image_list[label_item]))
        img_size = img.shape

        with open(os.path.join(label_path, label_list[label_item]), 'r') as f1:
            label_lines = [x.strip() for x in f1.readlines() if len(x.strip()) > 0]

        write_lines = []

        for line in label_lines:
            target_id = int(line.split(' ')[0])
            c_x = float(line.split(' ')[1])
            c_y = float(line.split(' ')[2])
            w = float(line.split(' ')[3])
            h = float(line.split(' ')[4])

            x1 = int(img_size[1] * (c_x - w / 2))
            y1 = int(img_size[0] * (c_y - h / 2))
            x2 = int(img_size[1] * (c_x + w / 2))
            y2 = int(img_size[0] * (c_y - h / 2))
            x3 = int(img_size[1] * (c_x + w / 2))
            y3 = int(img_size[0] * (c_y + h / 2))
            x4 = int(img_size[1] * (c_x - w / 2))
            y4 = int(img_size[0] * (c_y + h / 2))

            write_line = ''
            write_line = str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(x3) + ' ' + str(y3) + ' ' + str(x4) + ' ' + str(y4) + ' ' + str(target_id) + ' ' + '0'
            write_lines.append(write_line)

        with open(os.path.join(save_path, label_list[label_item]), 'w') as f2:
            for i in write_lines:
                f2.write(i + '\n')


def dota2yolo(image_path, label_path, save_path):
    image_list = os.listdir(image_path)
    label_list = os.listdir(label_path)

    for label_item in tqdm(range(len(label_list))):
        img = cv2.imread(os.path.join(image_path, image_list[label_item]))
        img_size = img.shape

        with open(os.path.join(label_path, label_list[label_item]), 'r') as f1:
            label_lines = [x.strip() for x in f1.readlines() if len(x.strip()) > 0]

        write_lines = []

        for line in label_lines:
            x1 = int(line.split(' ')[0])
            y1 = int(line.split(' ')[1])
            x2 = int(line.split(' ')[2])
            y2 = int(line.split(' ')[3])
            x3 = int(line.split(' ')[4])
            y3 = int(line.split(' ')[5])
            x4 = int(line.split(' ')[6])
            y4 = int(line.split(' ')[7])
            target_id = int(line.split(' ')[8])

            c_x = (x1 + x2) / 2 / img_size[1]
            c_y = (y1 + y4) / 2 / img_size[0]
            w = (x2 - x1) / img_size[1]
            h = (y4 - y1) / img_size[0]

            write_line = ''
            # write_line = str(target_id) + ' ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w) + ' ' + str(h)
            write_line = '0' + ' ' + str(c_x) + ' ' + str(c_y) + ' ' + str(w) + ' ' + str(h)
            write_lines.append(write_line)

        with open(os.path.join(save_path, label_list[label_item]), 'w') as f2:
            for i in write_lines:
                f2.write(i + '\n')


if __name__ == '__main__':
    image_path = r'E:\train\640\images'
    label_path = r'E:\train\640\labels-dota'
    save_path = r'E:\train\640\labels'

    dota2yolo(image_path, label_path, save_path)
