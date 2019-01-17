# coding: utf-8
import os
'''
程序参数在这里直接修改，
'''
# 文件路径 img_path不能为'' bias_path和flat_path可以为'' 但必须两个都不为''时才会计算
# 注意: 路径斜杠使用/ 这个斜杠 别用\
img_path = 'D:/60cmData_V_cleaned'
#img_path = 'D:/60cmData_V_cleaned'
bias_path = ''
flat_path = ''
 
# 孔径参数
# 0: 测光孔径与等价圆半径的比值
# 1: 背景环内径与等价圆半径的比值
# 2: 背景环外径与等价圆半径的比值
aperture_para = (1.5, 3, 4)

# 去掉图像中星星的区域再用剩余区域计算背景的不确定度，
# 但由于星星的提取要用到背景的不确定度，所以不停迭代更新星星区域和背景的不确定度，
# 星星区域会越来越准，背景不确定度趋向于定值，此时相邻两次迭代的不确定度的比值为dSigma
# 越低越精确，不能低于等于0 建议 0 到 10 之间
# 会影响速度 会增加连通区数量
dSigma = 0.1

# 连通区筛选值，筛除像素低于等于 (island_filter * 2 + 1) ** 2 个像素的连通区
# 数字越高，连通区越少，画面越干净，暗星越少 建议根据图像分辨率来定 否则可能会筛除目标星
# 同时最后显示的图像out.png 会用边长为 island_filter * 2 + 1 的中值滤波 过滤图像
island_filter = 3

# 用多少颗星作为偏移量参考，越多匹配的越准，同时计算时间也增加
# None：用所有图中，连通区最少的那张图的连通区数量来作为参考
# 不能高于连通区最少的图的连通区数量
sample_count = None

# out.png中的标注字体参数
font = {'family': 'serif',
        'color':  'yellow',
        'weight': 'normal',
        'size': 12,
        }

def path_init():
    img_path_list = walk_path(img_path)
    bias_path_list = walk_path(bias_path)
    flat_path_list = walk_path(flat_path)
    return img_path_list, bias_path_list, flat_path_list
    
def walk_path(data_dir):
	if data_dir is '':
		return None
	path_lst = []
	for dirpath, dirnames, filenames in os.walk(data_dir):
		for filename in filenames:
			path_lst.append(os.path.join(dirpath, filename))
	return path_lst
