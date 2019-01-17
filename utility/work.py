# coding: utf-8
import numpy as np

import config


def aperture_photometry(center, radius, frame):
    '''孔径测光
    Para:
        center: 测光目标坐标
        radius: 测光目标半径
        frame: 被测光的帧
    return:
        1: L
        2: err
    '''
    a, b, c = config.aperture_para
    h, w = frame.img.shape
    rx, ry = tuple(np.add(frame.rotation_center, frame.vector))
    (x, y) = center + np.array(frame.vector)
    radian = frame.radian
    frame_center = ((x - rx) * np.cos(radian) - (y - ry) * np.sin(radian) + rx,
                    (y - ry) * np.cos(radian) + (x - rx) * np.sin(radian) + ry)
    fx, fy = frame_center
    if fx < 0 or fx > h or fy < 0 or fy > w:
        return None, None
    value_idx_set = draw_a_circle((h, w), radius * a+1, frame_center)
    ring_idx_set_in = draw_a_circle((h, w), radius * b, frame_center)
    ring_idx_set_out = draw_a_circle((h, w), radius * c, frame_center)
    ring_idx_set = ring_idx_set_out - ring_idx_set_in
    value_idx_array = np.array(list(value_idx_set))
    ring_idx_array = np.array(list(ring_idx_set))
    value_array = frame.img[value_idx_array[:, 0], value_idx_array[:, 1]]
    ring_array = frame.img[ring_idx_array[:, 0], ring_idx_array[:, 1]]
    median = np.median(ring_array)
    return -2.5 * np.log10(np.abs(sum(value_array - median))), -2.5 * np.log10(np.abs(np.std(ring_array) * (len(ring_array)) ** 0.5))


def draw_a_circle(shape, radius, center):
    '''画圆
    假如圆圈到了图外 集合不会超出
    para:
        shape: 被画圆的图的shape
        radius: 半径
        center: 圆心坐标
    return:
        圆内的坐标集合
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

def get_circle(centerYX, r):  # r**2=(x-x0)**2+(y-y0)**2
    y0, x0 = centerYX  # ;print(y0,x0)
    x = np.linspace(x0-r, x0+r, 101)  # x离散取不到x0不会导致左右平移
    up_y = np.sqrt(abs(r**2-(x-x0)**2))+y0  # 末尾不准导致出现开方负数
    dn_y = -1*np.sqrt(abs(r**2-(x-x0)**2))+y0
    # ;print(min(x1),max(x1),(min(x1)+max(x1))/2,x0) #圆心和中心完全一致
    x1 = np.append(x, x[::-1])
    y1 = np.append(up_y, dn_y[::-1])
    return x1, y1  # 视觉上圆向左上偏移只是视觉问题？数据没发现偏移