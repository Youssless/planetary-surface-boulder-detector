import torch
import torchvision
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image
import pandas as pd
import os
import math
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt

class LunarSurfaceDataset(Dataset):

    def __init__(self, root_dir, csv_file, transform=None):
        
        self.root_dir = root_dir
        self.transform = transform
        self.data = pd.read_csv(os.path.join(self.root_dir, csv_file))

        # convert bbox string to a list
        self.data = self.data.assign(bbox=self.data['bbox'].str.strip('[]').str.split(','))

        # get image names
        self.imgs = list(os.listdir(os.path.join(self.root_dir, "frames", "frames")))
        
        
    def __len__(self):
        return(len(self.imgs))

    def __getitem__(self, index):
        image = Image.open(os.path.join(self.root_dir, "frames", "frames", self.imgs[index]))
        
        bboxes = labels = 0
        # extract only the bouding boxes with the current index
        df = self.data[self.imgs[index] == self.data["image_id"]]
        
        if not df.empty:
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
        else: 
            bboxes = np.array([[1, 2, 3, 4]])
            labels = np.ones(len(bboxes))

        targets = {
            "boxes": torch.from_numpy(bboxes).type(torch.int64),
            "labels": torch.from_numpy(labels).type(torch.int64)
        }

        # apply any image preprocessing 
        if self.transform:
            image = self.transform(image)

        return image, targets


run = False
show_output = False
if run:
    transform = transforms.Compose(
        [
            transforms.Grayscale(),
            transforms.ToTensor()
        ]
    )

    dataset = LunarSurfaceDataset("../input/lunar-surface-dataset", "test.csv", transform=transform)
    print(len(dataset))

    # randomly split the dataset 80/20
    train_size = math.ceil(0.8*len(dataset))
    test_size = math.floor(len(dataset) - train_size)

    train_split, test_split = random_split(dataset, [train_size, test_size])

    trainloader = DataLoader(train_split, batch_size=4, shuffle=True, collate_fn=lambda batch: list(zip(*batch)))
    validationloader = DataLoader(test_split, batch_size=4, shuffle=True, collate_fn=lambda batch: list(zip(*batch)))

    #images, labels = next(iter(trainloader))

    # faster r-cnn model
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)

    num_classes = 2
    # number of inputs in the fast r-cnn part
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # modify the fast r-cnn part
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    device = torch.device("cuda")
    model = model.to(device)

    params = [p for p in model.parameters() if p.requires_grad]
    optimiser = torch.optim.SGD(params, lr=0.01)

    num_epochs = 25
    epoch_train_losses, epoch_val_losses, epochs = [], [], []
    
    for epoch in range(num_epochs):
        start_time = time.time()

        print("Epoch {0}".format(epoch+1))
        train_losses, val_losses = [], []
        for images, targets in trainloader:
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            losses = model(images, targets)
            train_loss = sum(loss for loss in losses.values())
            train_losses.append(train_loss.item())
                                
            optimiser.zero_grad()
            train_loss.backward()
            optimiser.step()
        
        av_train_loss = np.mean(train_losses)
        print("Loss: {0}".format(av_train_loss))
            
        with torch.no_grad():
            for images, targets in validationloader:
                images = list(image.to(device) for image in images)
                targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

                losses = model(images, targets)
                val_losses.append(sum(loss for loss in losses.values()).item())
                
                
        av_val_loss = np.mean(val_losses)
        print("Validation Loss: {0}".format(av_val_loss))
        
        end_time = time.time() - start_time
        print("Epoch training time {0}m{1}s\n".format(end_time // 60, end_time % 60))
        
        epoch_train_losses.append(av_train_loss)
        epoch_val_losses.append(av_val_loss)
        epochs.append(epoch+1)
    
    print(epoch_train_losses)
    print(epoch_val_losses)
    plt.plot(epochs, epoch_train_losses, label='train loss')
    plt.plot(epochs, epoch_val_losses, label='validation loss')
    plt.title("learning curves")
    plt.xlabel("epochs")
    plt.ylabel("loss / cost")
    plt.legend()
    plt.show()
    # save the model
    torch.save(model.state_dict(), "fasterrcnn_boulder_detector.pt")

    if show_output:
        # testing the model
        with torch.no_grad():
            #images, targets = next(iter(testloader))

            images, targets = next(iter(validationloader))
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            # setting the model to testing mode
            model.eval()

            #cpu = torch.device('cpu')

            outputs = model(images)
            #outputs = [{k: v.to(device) for k, v in t.items()} for t in targets]

            sample_image = images[0].permute(1, 2, 0).cpu().data.numpy()
            sample_bbox = outputs[0]['boxes']

            fig, ax = plt.subplots(1)
            plt.rcParams['figure.figsize'] = [40, 40]
            for bbox in sample_bbox:
                xy_min = tuple(bbox[:2])
                xy_max = tuple(bbox[2:])
                cv2.rectangle(sample_image, xy_min, xy_max, (0, 0, 255), thickness=1)

            ax.imshow(sample_image)