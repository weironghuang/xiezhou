# coding: utf-8
# pylint: disable=no-member
import numpy as np
from astropy.io import fits

import config
from module.Frame import Frame


def frame_init():
    '''Frame的初始化
    初始化Frame的所有参数，为之后孔径测光所用
    '''
    img_path, bias_path, flat_path = config.path_init()
    bias, flat = bias_and_flat(bias_path, flat_path)
    # 生成Frame对象
    frame_list = [Frame((fits.open(path)[0].data - bias) /
                        (flat - bias)) for path in img_path]
    # 计算并添加参数：连通区表、星中心表、星半径表、星距离表
    count_list = []
    id = 0
    for frame in frame_list:
        frame.id = id
        id += 1
        img = frame.img
        med = np.median(img)
        value = np.array(img[img < med])
        avg = np.mean(value)
        std = (sum(((value - med) / avg) ** 2) / len(value)) ** 0.5 * avg
        frame.set_islands(std, config.dSigma)
        count_list.append(frame.set_center_radius(config.island_filter))
        frame.set_norm()
        frame.sort_para()
    # 计算并添加参数：偏移量、旋转中心、旋转弧度
    min_idx = np.argmin(count_list)
    num = config.sample_count if config.sample_count is not None else len(frame_list[min_idx].center_list)
    frame_0 = frame_list[min_idx]
    for frame in frame_list:
        if frame is frame_0:
            continue
        point_list = []
        for norms in frame.norm_list[0:num]:
            row = []
            for norms_0 in frame_0.norm_list[0:num]:
                point = 0
                norms_0 = np.array(norms_0)
                for norm in norms:
                    temp = abs(norms_0 - norm)
                    point += len(np.argwhere(temp < 2))
                row.append(point)
            point_list.append(row)
        point_list = np.array(point_list)
        idx_max = np.argsort(point_list, axis=None)[::-1][0]
        center_max_0 = frame_0.center_list[int(idx_max % num)]
        center_max_now = frame.center_list[int(idx_max / num)]
        # radian_list = []
        # for points, center_now in zip(point_list, frame.center_list[-num-1: -1]):
        #     idx = np.argmax(points)
        #     center_0 = frame_0.center_list[int(idx % num) - num-1]
        #     if center_0[0] - center_max_0[0] == 0.0 and center_0[1] - center_max_0[1] == 0.0:
        #         continue
        #     vector_0 = center_0 - center_max_0
        #     vector_now = center_now - center_max_now
        #     norm_0 = np.linalg.norm(vector_0)
        #     norm_now = np.linalg.norm(vector_now)
        #     radian = np.arccos(
        #         np.dot(vector_0, vector_now) / (norm_0 * norm_now))
        #     vector_rotation = vector_now - vector_0
        #     if vector_0[1] * vector_rotation[0] > 0:
        #         radian_list.append(radian)
        #     else:
        #         radian_list.append(-radian)
        frame.rotation_center = center_max_0
        frame.radian = 0  #  np.mean(radian_list)
        frame.vector = center_max_now - center_max_0
        print('id:', frame.id, 'init finished')
    return frame_list, min_idx


def bias_and_flat(bias_path, flat_path):
    '''bias和flat的操作函数。
    Para:
            bias_path: bias文件的路径表
            flat_path: flat文件的路径表
    Return:
            假如有bias与flat，则返回合并后的两张图；否则返回0与1
    '''
    if not bias_path or not flat_path:
        return 0, 1
    else:
        bias_list = readfits(bias_path)
        flat_list = readfits(flat_path)
        return combine(bias_list), combine(flat_list)


def readfits(path_list):
    '''读取fits文件
    Para:
            path_list: fits文件的路径表
    Return:
            返回根据路径表读取的fits类的对象表
    '''
    fits_list = []
    for path in path_list:
        fits_list.append(fits.open(path))
    return fits_list


def combine(fits_list):
    '''合并
    比较每幅图同坐标的值, 选取中值作为返回图片中这个坐标的值
    Para:
            fits_list: fits对象表
    Return:
            返回合并后的单个图像
    '''
    '''
	'''
    data_list = [fits[0].data for fits in fits_list]
    return np.median(data_list, axis=0)


def draw_a_circle(shape, radius, center):
    '''圈个圆
    Para:
            shape: 原图形状
            radius: 圆的半径
            center: 圆的中心坐标
    Return:
            返回圆内的坐标集合
    '''
    circle_set = set()
    h, w = shape
    x, y = center
    x_begin = int(np.around(x - radius)) if x - radius > 0 else 0
    x_end = int(np.around(x + radius)) if x + radius < h else h
    y_begin = int(np.around(y - radius)) if y - radius > 0 else 0
    y_end = int(np.around(y + radius)) if y + radius < w else w
    for i in range(x_begin, x_end):
        for j in range(y_begin, y_end):
            if (x - i)**2 + (y - j)**2 <= radius**2:
                circle_set.add((i, j))
    return circle_set
