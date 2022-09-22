import os
import random

nfiles = 0
def split_input(inputfile):
  # Function to split the several trajectories in the input configuration file.
  with open(inputfile) as f:
    data = f.readlines()
  for c, file in enumerate(zip(*[iter(data)]*204)):
    with open(f'input_split_{c}.cfg', 'w') as f:
      f.writelines(file)
      global nfiles
      nfiles += 1

def train_test_split(trainsize_percentage, dir_with_files):
  # Function to generate the test and train sets for MLIP. Trainsize_percentage should be a number between 0 and 1.
  trainsize = round(trainsize_percentage * nfiles)
  random_list = list(range(nfiles))
  random.shuffle(random_list)
  train_list = random_list[0:trainsize]
  test_list = random_list[trainsize:]
  os.chdir(dir_with_files)
  # Helper function to write the train and test merged files
  def filewriter(setlist, filename):
    with open('input_split_{}.cfg'.format(setlist[0])) as fp:
      data = fp.read()
    setlist.pop(0)
    for i in setlist:
      with open(f'input_split_{i}.cfg') as fp:
        data2 = fp.read()
        data += data2
    with open ('{}.cfg'.format(filename), 'w') as fp:
      fp.write(data)
  filewriter(test_list, "test_set")
  filewriter(train_list, "train_set")
  
