# coding: utf-8
import copy
import csv

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

import config
from utility import fit_setting, work


frame_list, min_idx = fit_setting.frame_init()
num = config.sample_count if config.sample_count is not None else len(
    frame_list[min_idx].center_list)
center_list_0 = frame_list[min_idx].center_list[0:num]
radius_list_0 = frame_list[min_idx].radius_list[0:num]
all_list = []
err_list = []
plt.figure(figsize=(19.2,10.8))
plt.subplot(121)
img_label = copy.deepcopy(frame_list[min_idx].img_label)
img_label[img_label > 0] = 1
f = config.island_filter * 2 + 1
img_med = signal.medfilt(img_label, (f, f))
plt.imshow(img_med)
plt.gray()
i = 0
for center, radius in zip(center_list_0, radius_list_0):
    print('star:', center)
    i += 1
    plt.scatter(center[1], center[0], c='red',s=5)
    plt.text(center[1] - radius*2, center[0] - radius*2, i, fontdict=config.font)
    x, y = work.get_circle(center, radius*1.3)
    plt.plot(x, y, color='red', linewidth=0.88888)
    L_list = []
    e_list = []
    for frame in frame_list:
        L, e = work.aperture_photometry(center, radius, frame)
        L_list.append(L)
        e_list.append(e)
    all_list.append(L_list)
    err_list.append(e_list)
with open('result/out.csv', 'a', newline='') as out:
    csv_write = csv.writer(out, dialect='excel')
    for line in all_list:
        csv_write.writerow(line)
with open('result/err.csv', 'a', newline='') as out:
    csv_write = csv.writer(out, dialect='excel')
    for err in err_list:
        csv_write.writerow(err)
plt.subplot(122)
i = 0
mark = []
for L in all_list:
    plt.plot(L)
    i += 1
    mark.append(str(i))
plt.legend(mark)

plt.savefig('result/out.png')
print('finish all!')
