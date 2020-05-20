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
            nn.Linear(input_size, input_size//2),
            nn.ReLU(),
            nn.Linear(input_size//2, input_size//4),
            nn.ReLU(),
            nn.Linear(input_size//4, 1)
        )

    def forward(self, x):
        return self.fc(x)


END_ARCHITECHTURE = { 'FC' : FC }
def build_end(cfg):
    end = END_ARCHITECHTURE[cfg.LISTENER.END](cfg.LISTENER.CNN_OUTPUT + cfg.LISTENER.GNN_OUTPUT)
    return end



if __name__ == '__main__':
    fc = FC(12)
    x = torch.zeros((1,12))
    output = fc(x)
    print(output)                