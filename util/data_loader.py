import torch
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import PIL
import pandas as pd
import os

class lunar_dataset(Dataset):

    def __init__(self, csv_file, root_dir, transform=None):
        self.truths = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return(len(self.data))

    '''
    
    '''    
    def __getitem__(self, index):
        # image path in the csv
        img_path = os.path.join(self.root_dir, self.truths.iloc[index, 0])
        image = io.imread(img_path)

        # image y_label
        y_label = torch.tensor(float(self.truths.iloc[index, 1]))

        # apply any image preprocessing 
        if self.transform:
            image = self.transform(image)

        return [image, y_label]