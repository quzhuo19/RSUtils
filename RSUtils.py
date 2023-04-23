import os
import shutil

import numpy as np
import tifffile as tf

from PIL import Image
from osgeo import gdal


def read_tiff(tiff_file_path, bands_order):
    """
    读取tiff图像中的rgb条带 [3, 2, 1] -> [R, G, B]
    :param tiff_file_path:
    :param bands_order:
    :return:
    """
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()

    ds = gdal.Open(tiff_file_path, gdal.GA_ReadOnly)

    cols = ds.RasterXSize
    rows = ds.RasterYSize

    data = np.empty([rows, cols, 3], dtype=float)

    for i in range(3):
        band = ds.GetRasterBand(bands_order[i])
        data1 = band.ReadAsArray()
        data[:, :, i] = data1

    return data


def tiff2rgb(tiff_file_path, save_path, draw_percent=0.02, format='png', bands_order=[3, 2, 1]):
    """
    tiff线性拉伸,16位->8位
    :param tiff_file_path:
    :param save_path:
    :param draw_percent: 线性拉伸比例，[max * draw_percent, max * (1 - draw_percent)] -> [0, 255]
    :param format:
    :param bands_order: [3, 2, 1] -> [R, G, B]
    :return:
    """
    data = read_tiff(tiff_file_path, bands_order)
    n = data.shape[2]
    out = np.zeros_like(data, dtype=np.uint8)

    # print(n)

    for i in range(n):
        a = 0
        b = 255
        c = np.percentile(data[:, :, i], int(draw_percent * 100))
        d = np.percentile(data[:, :, i], int((1 - draw_percent) * 100))
        t = a + (data[:, :, i] - c) * (b - a) / (d - c)
        t[t < a] = a
        t[t > b] = b
        out[:, :, i] = t
        # out[:, :, i] = data[:, :, i]
    out_img = Image.fromarray(np.uint8(out))

    if format == 'png':
        out_img.save(os.path.join(save_path, tiff_file_path.split('\\')[-1][:-3] + 'png'))
    else:
        out_img.save(os.path.join(save_path, tiff_file_path.split('\\')[-1][:-3] + 'jpg'))

    # move_path = r'E:\train\save'
    # shutil.move(tiff_file_path, os.path.join(move_path, tiff_file_path.split('\\')[-1]))


# def read_l2(tiff_file_path, save_path, split_size=256, bands_order=[3, 2, 1], format='png'):
#     """
#     读取tiff图像中的真彩色条带 [3, 2, 1] -> [R, G, B]
#     :param tiff_file_path:
#     :param bands_order:
#     :return:
#     """
#     driver = gdal.GetDriverByName('GTiff')
#     driver.Register()
#
#     ds = gdal.Open(tiff_file_path, gdal.GA_ReadOnly)
#
#     cols = ds.RasterXSize
#     rows = ds.RasterYSize
#
#     step_x = cols // split_size + 1
#     step_y = rows // split_size + 1
#
#     for x in range(step_x):
#         for y in range(step_y):
#             data = np.empty([split_size, split_size, 3], dtype=float)
#
#             for i in range(3):
#                 band = ds.GetRasterBand(bands_order[i])
#                 data_l2 = band.ReadAsArray(xoff=x*split_size, yoff=y*split_size, win_xsize=split_size, win_ysize=split_size)
#                 data[:, :, i] = data_l2
#
#             img = Image.fromarray(np.uint8(data))
#
#             if format == 'png':
#                 img.save(os.path.join(save_path, tiff_file_path.split('\\')[-1][:-5] + '_' + str(x*split_size) + '_' + str(y*split_size) + '.png'))
#             else:
#                 img.save(os.path.join(save_path, tiff_file_path.split('\\')[-1][:-5] + '_' + str(x*split_size) + '_' + str(y*split_size) + '.jpg'))
#
#     print(11)


if __name__ == '__main__':

    # ------------------------------------------------------------------------
    # tiff2rgb
    file_path = r'E:\train\intc'
    save_path = r'E:\train\png_16bit'

    file_list = os.listdir(file_path)
    for i in file_list:
        tiff2rgb(os.path.join(file_path, i), save_path, bands_order=[1, 2, 3])
        print(i + ' has completed !')

    # image_path = r'E:\train\16bit\2.tif'
    # tiff2rgb(image_path, save_path, bands_order=[1, 2, 3])
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # file_path = r'E:\train\16bit\109.tif'
    # img = tf.imread(file_path)
    # print(11)
    # ------------------------------------------------------------------------


