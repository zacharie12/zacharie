from abc import ABC
import torch
import torch.nn as nn


class ListenerEnd(ABC, nn.Module):
    def __init__(self):
        super(ListenerEnd, self).__init__()
    
  
    def forward(self):
        pass

class FC(ListenerEnd):
    def __init__(self, input_size):
        super(FC, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, 1)
        )

    def forward(self, x):
        return self.fc(x)


class BNFC(ListenerEnd):
    def __init__(self, input_size):
        super(FC, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, input_size//2),
            nn.BatchNorm1d(input_size//2),
            nn.ReLU(),
            nn.Linear(input_size//2, input_size//4),
            nn.BatchNorm1d(input_size//4),
            nn.ReLU(),
            nn.Linear(input_size//4, 1)
        )

    def forward(self, x):
        return self.fc(x)

# TODO: Dropout
class DropoutFC(ListenerEnd):
    def __init__(self, input_size):
        super(DropoutFC, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(input_size, input_size),
            nn.ReLU(),
            nn.Linear(input_size, 1)
        )

    def forward(self, x):
        return self.fc(x)


class CosineDistance(ListenerEnd):
    def __init__(self, input_size):
        super(CosineDistance, self).__init__()
        self.input_size = input_size
        self.dist = nn.CosineSimilarity()

    def forward(self, x):   
        feature_len = self.input_size // 2
        first_feat = x.t()[:feature_len].t()
        second_feat = x.t()[feature_len:].t()

        return self.dist(first_feat, second_feat)



END_ARCHITECHTURE = { 'FC' : FC , 'BNFC' : BNFC, 'DropoutFC':DropoutFC, 'CosineDistance':CosineDistance}
def build_end(cfg):
    end = END_ARCHITECHTURE[cfg.LISTENER.END](cfg.LISTENER.CNN_OUTPUT + cfg.LISTENER.GNN_OUTPUT)
    return end



if __name__ == '__main__':
    fc = FC(12)
    x = torch.zeros((1,12))
    output = fc(x)
    print(output)                