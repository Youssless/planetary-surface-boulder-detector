
import util.data_loader as dl

import torch
from torch.utils.data import Dataset, DataLoader, random_split

import torchvision
from torchvision import transforms
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

import math
import time
import numpy as np

import cv2
import matplotlib.pyplot as plt


transform = transforms.Compose(
        [
            transforms.Grayscale(),
            transforms.ToTensor()
        ]
    )

dataset = dl.LunarSurfaceDataset("../data", "test.csv", transform=transform)

# randomly split the dataset 80/20
train_size = math.ceil(0.8*len(dataset))
test_size = math.floor(len(dataset) - train_size)

train_split, test_split = random_split(dataset, [train_size, test_size])

trainloader = DataLoader(train_split, batch_size=4, shuffle=True, collate_fn=lambda batch: list(zip(*batch)))
testloader = DataLoader(test_split, batch_size=4, shuffle=True, collate_fn=lambda batch: list(zip(*batch)))

images, labels = next(iter(trainloader))

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

num_epochs = 1
losses = []
for epoch in range(num_epochs):
    start_time = time.time()
    
    print("Epoch {0}".format(epoch+1))
    for images, targets in trainloader:
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        train_losses = model(images, targets)
        total_loss = sum(loss for loss in train_losses.values())
        
        optimiser.zero_grad()
        total_loss.backward()
        optimiser.step()

    print("Loss: {0}".format(np.mean(total_loss.item())))

    end_time = time.time() - start_time
    print("Epoch training time {0}m{1}s\n".format(end_time // 60, end_time % 60))
    


# testing the model
with torch.no_grad():
    #images, targets = next(iter(testloader))
    
    for i, (images, targets) in enumerate(testloader):
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        print(len(images))

        # setting the model to testing mode
        model.eval()

        #cpu = torch.device('cpu')

        outputs = model(images)
        outputs = [{k: v.to(device) for k, v in t.items()} for t in targets]
        
        print(outputs)

        sample_image = images[0].permute(1, 2, 0).cpu().data.numpy()
        sample_bbox = outputs[0]['boxes']

        fig, ax = plt.subplots(1)
        plt.rcParams['figure.figsize'] = [40, 40]
        for bbox in sample_bbox:
            xy_min = tuple(bbox[:2])
            xy_max = tuple(bbox[2:])
            cv2.rectangle(sample_image, xy_min, xy_max, (0, 0, 255), thickness=1)

        ax.imshow(sample_image)