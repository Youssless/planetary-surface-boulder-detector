
import util.data_loader as dl

import torch
from torch.utils.data import Dataset, DataLoader, random_split

import torchvision
from torchvision import transforms
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

import math
import time
import numpy as np

# image preprocessing
transform = transforms.Compose(
    [
        transforms.Grayscale(),
        transforms.ToTensor()
    ]
)

# data set from custom data loader in util.data_loader
dataset = dl.LunarSurfaceDataset("data", "test.csv", transform=transform)

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

# load the hyperparameters in the optimiser (weights and biases)
params = [p for p in model.parameters() if p.requires_grad]
optimiser = torch.optim.SGD(params, lr=0.01)

num_epochs = 1
for epoch in range(num_epochs):
    start_time = time.time()
    losses = []
    print("Epoch {0}".format(epoch+1))
    for images, targets in trainloader:
        # load the images and labels to the specified device
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        # train the model add up the loss for the batch
        train_losses = model(images, targets)
        total_loss = sum(loss for loss in train_losses.values())
        
        # before gradient descent, zero out the gradients from the previous epoch
        optimiser.zero_grad()
        total_loss.backward()
        optimiser.step()

    print("Loss: {0}".format(np.mean(total_loss.item())))

    end_time = time.time() - start_time
    print("Epoch training time {0}m{1}s\n".format(end_time // 60, end_time % 60))
