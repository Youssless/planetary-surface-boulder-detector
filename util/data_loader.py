import torch
from torch.utils.data import Dataset, DataLoader, random_split

from PIL import Image
import cv2
import pandas as pd
import numpy as np
import os

class LunarSurfaceDataset(Dataset):

    def __init__(self, root_dir, csv_file, transform=None):
        '''formats and loads the dataset into an object ready for training and testing
            
            LunarSurfaceDataset contains images and labels that are loaded into and object.
                The images are artificial images of the lunar surface, in a top down view
                generated with PANGU.

                The images contain boulders which are targets for detection. The boulders
                are all labelled with labels either 0 or 1 (0 = no boulder, 1 = boulder).
                
                In this dataset all the boulders are labelled 1. This will be used in the
                region proposal network (RPN) to calculate the objectness score to be used
                in predicting the bounding boxes.

                The bounding boxes in the dataset is in the format [x, y, w, h]. This is then
                formatted in __get_item__(index) to [x_min, y_min, x_max, y_max] for training.

                Args:
                    root_dir (str): root directory of the dataset
                    csv_file (str): file name for the csv containing the image name and 
                        the bounding box dimensions for each boulder
                    transform(list): list of image transformations to apply to each image
        '''
        self.root_dir = root_dir
        self.transform = transform
        self.data = pd.read_csv(os.path.join(self.root_dir, csv_file))

        # convert bbox string to a list
        self.data = self.data.assign(bbox=self.data['bbox'].str.strip('[]').str.split(','))

        # get image names
        self.imgs = list(os.listdir(os.path.join(self.root_dir, "frames")))

    def __len__(self):
        '''number of items in the dataset

            Returns:
                (int): length of the image dataset
        '''
        return (len(self.imgs))


    def __getitem__(self, index):
        '''formats and querys the dataset based on the index
        
            Args:
                index (int): index of the item in the dataset
            Returns:
                image (torch.tensor): the loaded image
                targets (dict): {boxes: torch.int64, labels: torch.int64}
        '''
        image = Image.open(os.path.join(self.root_dir, "frames", self.imgs[index]))

        # extract only the bouding boxes with the current index
        df = self.data[self.imgs[index] == self.data["image_id"]]

        # split the bbox list into x, y, w, h columns in the csv
        bbox_split = df['bbox'].apply(lambda s: pd.Series(
            {
                'x': int(s[0]),
                'y': int(s[1]),
                'w': int(s[2]) + int(s[0]),
                'h': int(s[3]) + int(s[1])
            } 
        ))

        df.reset_index(drop=True, inplace=True)
        bbox_split.reset_index(drop=True, inplace=True)

        # combine the original csv and the x, y, w, h columns
        df = pd.concat([df, bbox_split], axis=1)

        # get the bounding box columns from the data frame
        bboxes = df[['x', 'y', 'w', 'h']].values

        # set the labels to all 1's (true)
        labels = np.ones(len(bboxes))

        targets = {
            "boxes": torch.from_numpy(bboxes).type(torch.int64),
            "labels": torch.from_numpy(labels).type(torch.int64)
        }

        # apply any image preprocessing 
        if self.transform:
            image = self.transform(image)

        return image, targets 

    
if __name__ == '__main__':
    dataset = LunarSurfaceDataset('../data', 'test.csv')
    print("<---- LunarSurfaceDataset Details ---->\n")

    print("Dataset Shape: {0}".format(np.shape(dataset)))

    sample_image = np.array(dataset[0][0])
    sample_targets = dataset[0][1]

    print("Image Shape: {0}".format(sample_image.shape[:2]))
    print("Targets [boxes, labels (0 = no boulder, 1 = boulder)]: {0}\n".format(len(sample_targets)))

    print("<---- Dataset Sample ---->\n")

    print("< Image array >")
    print(sample_image)
    print("< Targets [boxes, labels] >")
    print(sample_targets)

    sample_image = np.array(Image.fromarray(np.uint8(dataset[0][0])).convert('RGB'))
    for box in sample_targets['boxes']:
        xy_min = tuple(box[:2].numpy())
        xy_max = tuple(box[2:].numpy())
        cv2.rectangle(sample_image, xy_min, xy_max, (0, 0, 255), thickness=1)

    cv2.imshow("Sample Image (from dataloader)", sample_image)
    cv2.waitKey(0)