import torch
import json
from torchvision import transforms
from torchvision.models import resnet34
from PIL import Image

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image')
args = parser.parse_args()

transform = transforms.Compose([            #[1]
    transforms.Resize(256),                    #[2]
    transforms.CenterCrop(224),                #[3]
    transforms.ToTensor(),                     #[4]
    transforms.Normalize(                      #[5]
    mean=[0.485, 0.456, 0.406],                #[6]
    std=[0.229, 0.224, 0.225]                  #[7]
    )])

model = resnet34(pretrained=True)
model.eval()

def predict(model, img):

    img = Image.open(img)
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)

    out = model(batch_t)

    with open('imagenet_classes.txt') as f:
        labels = [line.strip() for line in f.readlines()]

    retJson = {}
    _, indices = torch.sort(out, descending=True)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    # print([(labels[idx], percentage[idx].item()) for idx in indices[0][:5]])
    # out = [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]
    i = 1
    for idx in indices[0][:5]:
        retJson[f'pred_{i}'] = str("label : {} and confidence : {}".format(labels[idx],percentage[idx].item()))
        i += 1
    # print(retJson)
    with open("text.json", "w", encoding="utf-8") as f:
        json.dump(retJson, f, ensure_ascii=False, indent=4)

predict(model, args.image)