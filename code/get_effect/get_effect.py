import numpy as np
import time
import pickle
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import random
import sam
import math
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--data', default = 'mind', type = str)
parser.add_argument('--s_len', default = 1000, type = int)

args = parser.parse_args()
data_dir = '../../data/{}'.format(args.data)
log_dir = 'result/{}'.format(args.data)

f = open('{}/log.txt'.format(log_dir), 'w')

with open('{}/data.pkl'.format(data_dir), 'rb') as file:
    data = pickle.load(file)
with open('{}/iu_data.pkl'.format(data_dir), 'rb') as file:
    iu_data = pickle.load(file)
with open('{}/i2c.pkl'.format(data_dir), 'rb') as file:
    i2c = pickle.load(file)
print('read finished')
f.write('read finished\n')
f.flush()

# pre-processing
i_num = len(iu_data)

c_num = max(i2c) + 1
c2i = [[] for c in range(c_num)]
for i in range(len(i2c)):
    c = i2c[i]
    c2i[c].append(i)

i_click = []
i_rec = []
i_rate = []
for i in range(i_num):
    rec, click = 0, 0
    for u_data in iu_data[i]:
        for c, t in u_data[1:]:
            rec += 1
            click += c
    i_click.append(click)
    i_rec.append(rec)
    i_rate.append(float(click) / rec)

u_click = []
u_rec = []
u_rate = []
c_u_rate = [[] for cate in range(c_num)]
for u in range(len(data)):
    rec, click = 0, 0
    c_rec, c_click = [0 for cate in range(c_num)], [0 for cate in range(c_num)]
    for l in range(len(data[u])):
        for i, c, t in data[u][l]:
            rec += 1
            click += c
            c_rec[i2c[i]] += 1
            c_click[i2c[i]] += c
    
    u_click.append(click)
    u_rec.append(rec)
    u_rate.append(float(click) / rec)
    for cate in range(c_num):
        if c_rec[cate] == 0:
            c_u_rate[cate].append(0.)
        else:
            c_u_rate[cate].append((c_click[cate] / c_rec[cate]) + u_rate[u])
del data

with open('{}/i_data.pkl'.format(data_dir), 'rb') as file:
    i_data = pickle.load(file)
print('pre-processing finished')

with open('../policy_news/policy_id.pkl'.format(data_dir), 'rb') as file:
    policy_id = pickle.load(file)

policy_effect_o2j = {}
cal_cnt = 0
all_cnt = len(policy_id)

for j in policy_id:
    policy_effect_o2j[j] = {}
    for v in range(i_num):
        cnt, effect = sam.cal_effect(v, j, i_data, iu_data, c_u_rate[i2c[v]], args.s_len)
        if cnt > 0:
            policy_effect_o2j[j][v] = effect
    cal_cnt += 1
    f.write('{} {}\n'.format(cal_cnt, all_cnt))
    f.flush()
with open('{}/policy_effect_o2j.pkl'.format(log_dir), 'wb') as file:
    pickle.dump(policy_effect_o2j, file)

policy_effect_random_o2j = {}
cal_cnt = 0
all_cnt = 1500
random_id = set()
while len(random_id) < 1500:
    random_id.add(random.randint(0, i_num - 1));

for j in random_id:
    policy_effect_random_o2j[j] = {}
    for v in range(i_num):
        cnt, effect = sam.cal_effect(v, j, i_data, iu_data, c_u_rate[i2c[v]], args.s_len)
        if cnt > 0:
            policy_effect_random_o2j[j][v] = effect
    cal_cnt += 1
    f.write('{} {}\n'.format(cal_cnt, all_cnt))
    f.flush()
with open('{}/policy_effect_random_o2j1500.pkl'.format(log_dir), 'wb') as file:
    pickle.dump(policy_effect_random_o2j, file)

f.close()
