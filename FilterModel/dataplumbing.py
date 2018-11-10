#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2018-11-09
# Purpose: Process datasets
##########################################################################################

# Libraries
#
import csv
import numpy as np

# Load data
#
cdr3s_tumor = []
with open('download/TumorCDR3s_training.txt') as stream:
  for line in stream:
    cdr3 = line.strip()
    if 10 <= len(cdr3) and len(cdr3) <= 20:
      cdr3s_tumor.append(cdr3)
cdr3s_nontumor = []
with open('download/NonTumorCDR3s_training.txt') as stream:
  for line in stream:
    cdr3 = line.strip()
    if 10 <= len(cdr3) and len(cdr3) <= 20:
      cdr3s_nontumor.append(cdr3)

print('NUM TUMOR:', len(cdr3s_tumor))
print('NUM NON-TUMOR:', len(cdr3s_nontumor))

# Settings
#
max_steps = 20
num_tumor = len(cdr3s_tumor)
num_nontumor = len(cdr3s_nontumor)
num_features = 5

num_tumor_val = 2000
num_nontumor_val = 1000

num_tumor_train = num_tumor-num_tumor_val
num_nontumor_train = num_nontumor-num_nontumor_val

# Residue factors
#
residue_factors = {}
with open('lib/atchley_factors.csv', 'r') as stream:
  reader = csv.reader(stream, delimiter=',')
  for row in reader:
    aa = row[0]
    values = []
    for value in row[1:]:
      values.append(np.float64(value))
    residue_factors[aa] = values

# Arrays
#
xs_tumor = np.zeros((num_tumor, max_steps, num_features), dtype=np.float32)
ps_tumor = -1.0E16*np.ones((num_tumor, max_steps), dtype=np.float32)
xs_nontumor = np.zeros((num_nontumor, max_steps, num_features), dtype=np.float32)
ps_nontumor = -1.0E16*np.ones((num_nontumor, max_steps), dtype=np.float32)

# Fill arrays
#
for i, cdr3 in enumerate(cdr3s_tumor):
  for j, aa in enumerate(cdr3):
    xs_tumor[i,j,:] = residue_factors[aa]
  ps_tumor[i,j] = 0.0
for i, cdr3 in enumerate(cdr3s_nontumor):
  for j, aa in enumerate(cdr3):
    xs_nontumor[i,j,:] = residue_factors[aa]
  ps_nontumor[i,j] = 0.0

# Split data
#
is_tumor = np.arange(num_tumor, dtype=np.int64)
np.random.shuffle(is_tumor)

xs_tumor_val = xs_tumor[is_tumor[:num_tumor_val],:,:]
ps_tumor_val = ps_tumor[is_tumor[:num_tumor_val],:]
xs_tumor_train = xs_tumor[is_tumor[num_tumor_val:],:,:]
ps_tumor_train = ps_tumor[is_tumor[num_tumor_val:],:]

is_nontumor = np.arange(num_nontumor, dtype=np.int64)
np.random.shuffle(is_nontumor)

xs_nontumor_val = xs_nontumor[is_nontumor[:num_nontumor_val],:,:]
ps_nontumor_val = ps_nontumor[is_nontumor[:num_nontumor_val],:]
xs_nontumor_train = xs_nontumor[is_nontumor[num_nontumor_val:],:,:]
ps_nontumor_train = ps_nontumor[is_nontumor[num_nontumor_val:],:]

# Save data
#
np.save('bin/xs_tumor_val.npy', xs_tumor_val)
np.save('bin/ps_tumor_val.npy', ps_tumor_val)
np.save('bin/xs_tumor_train.npy', xs_tumor_train)
np.save('bin/ps_tumor_train.npy', ps_tumor_train)

np.save('bin/xs_nontumor_val.npy', xs_nontumor_val)
np.save('bin/ps_nontumor_val.npy', ps_nontumor_val)
np.save('bin/xs_nontumor_train.npy', xs_nontumor_train)
np.save('bin/ps_nontumor_train.npy', ps_nontumor_train)


