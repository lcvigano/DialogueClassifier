import torch
import torch.utils.data as data
import gzip
import tqdm
import numpy as np

class FullSimpsonsDataset(data.Dataset):

    def __init__(self, file_path, word_to_indx, label_map, max_length=17):
        self.file_path = file_path
        self.dataset = []
        self.word_to_indx  = word_to_indx
        self.label_map = label_map
        self.max_length = max_length

        lines = file(file_path).readlines()
        for line in tqdm.tqdm(lines):
            sample = self.processLine(line)
            self.dataset.append(sample)

    ## Convert one line from simpson dataset to {Text, Labels}
    def processLine(self, line):
        line = line.split('|')

        speaker_num = self.label_map[line[0]]

        text_arr = line[1].strip().split(' ')
        x =  getIndicesTensor(text_arr, self.word_to_indx, self.max_length)
        sample = {'x':x, 'y':speaker_num}
        return sample

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self,index):
        sample = self.dataset[index]
        return sample


def getIndicesTensor(text_arr, word_to_indx, max_length):
    nil_indx = 0
    text_indx = [ word_to_indx[x] if x in word_to_indx else nil_indx for x in text_arr]
    if len(text_indx) < max_length:
        text_indx.extend( [nil_indx for _ in range(max_length - len(text_indx))])

    x =  torch.LongTensor(text_indx)

    return x