import csv
from os.path import join, basename, isfile
from glob import glob
import numpy as np
from shutil import copyfile

methods = sorted(['DST', 'SAE', 'stargan2', 'STROTSS', 'WCT2', 'WST'])
img_pairs = sorted(glob(join('image_pairs', 'set*')))
base_url = 'https://zzhang-amt.s3.us-west-1.amazonaws.com/'
rows = []

for img_pair in img_pairs:
    set_name = basename(img_pair)
    img_source = join(img_pair, 'source.jpg')
    img_target = join(img_pair, 'target.jpg')
    img_ours = join('ours', set_name + '.png')
    assert isfile(img_source) and isfile(img_target) and isfile(img_ours)

    for method in methods:
        img_others = join(method, set_name + '.jpg')
        if not isfile(img_others):
            img_others = join(method, set_name + '.png')
            if not isfile(img_others):
                continue

        if np.random.rand() >= .5:
            imgs = [img_source, img_target, img_ours, img_others]
        else:
            imgs = [img_source, img_target, img_others, img_ours]

        imgs_new = ['_'.join(_.split('/')) for _ in imgs]
        for s, t in zip(imgs, imgs_new):
            copyfile(s, t)
        rows.append(imgs_new)

        # rows.append([base_url + _ for _ in imgs])

with open('input.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['image_source_url', 'image_style_url', 'image_A_url', 'image_B_url'])
    for row in rows:
        writer.writerow(row)





