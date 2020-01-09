import torch
import torch.nn.functional as F
import torch.nn as nn

# Neural Network Model (1 hidden layer)
class Net(nn.Module):
    def __init__(self, input_size):
        super(Net, self).__init__()
        num_classes = 2
        hidden_size = (input_size + num_classes) / 2
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out =  F.log_softmax(self.fc2(out))
        return out