import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import *

class NumpyDataset:
  def __init__(self, X, y, one_hot_target=False, split=False, 
              normalize=False, shuffle=True, seed=None):
    if len(X.shape) > 1:
      self.n_features = X.shape[1]
      self.X = X
    else:
      self.n_features = 1
      self.X = X.reshape(-1, self.n_features)

    if len(y.shape) > 1:
      self.n_labels = y.shape[1]
      self.y = y
    else:
      self.n_labels = 1
      self.y = y.reshape(-1, self.n_labels)
    
    self.sc = StandardScaler().fit(self.X)

    if one_hot_target:
      self.y_oh = self.one_hot(self.y)
    
    if normalize:
      self.normalize()

    if split:
      self.split(seed)
  
  def __getitem__(self, idx):
    return self.X[idx], self.y[idx]

  def __len__(self):
      return len(self.X)

  def one_hot(self, y):
    """ For a categorical array y, returns a matrix of the one-hot encoded data. """
    m = y.shape[0]
    onehot = np.zeros((m, int(torch.max(y)+1)))
    onehot[range(m), y] = 1
    return onehot

  def normalize(self, data=None):
    if data == None:
      self.X_raw = self.X
      self.X = self.sc.transform(self.X)
      return self.X
    else:
      return self.sc.transform(data)

  def split(self, X=None, y=None, test_size=0.25, sets=2, shuffle=True, seed=None):
    if X == None:
      features = self.X
    else:
      features = X

    if y == None:
      labels = self.y
    else:
      labels = y

    X_sets = {}
    y_sets = {}
    for set in range(sets):
        X, X_test, y, y_test = train_test_split(features, labels, test_size=test_size, 
                                        shuffle=shuffle, random_state=seed)
        X_sets[0] = X
        X_sets[set+1] = X_test
        y_sets[0] = np.array(y).reshape(-1,)
        y_sets[set+1] = np.array(y_test).reshape(-1,)
        print(y_sets[0].shape, y_sets[set+1].shape)
    
    if X == None and y == None:
      self.X_sets = X_sets
      self.y_sets = y_sets
    
    return X_sets, y_sets
      
class TorchDataset(Dataset):
  """
  Class that implements torch.utils.data.Dataset
  """
  def __init__(self, X, y, one_hot_target=False, split=False, 
              normalize=False, shuffle=True, seed=None):
    super().__init__()

    if len(X.shape) > 1:
      self.n_features = X.shape[1]
      self.X = torch.Tensor(X).float()
    else:
      self.n_features = 1
      self.X = torch.Tensor(X.reshape(-1, self.n_features)).float()

    if len(y.shape) > 1:
      self.n_labels = y.shape[1]
      self.y = torch.Tensor(y).float()
    else:
      self.n_labels = 1
      self.y = torch.Tensor(y.reshape(-1, self.n_labels)).float()

    self.mean = torch.mean(self.X, axis=0)
    self.std = torch.std(self.X, axis=0)

    if one_hot_target:
      self.y_oh = self.one_hot(self.y)

    if normalize:
      self.normalize()

    if split:
      self.split(seed)

  def __getitem__(self, idx):
    return self.X[idx], self.y[idx]

  def __len__(self):
      return len(self.X)
  
  def one_hot(self, y):
    """ For a categorical array y, returns a matrix of the one-hot encoded data. """
    m = y.shape[0]
    y = y.long()
    onehot = torch.zeros((m, int(torch.max(y)+1)))
    onehot[range(m), y] = 1
    return onehot

  def normalize(self, data=None):
    if data == None:
      self.X_raw = self.X
      self.X = (self.X - self.mean)/self.std
      return self.X
    else:
      return (data - self.mean)/self.std

  def split(self, seed, sizes=[0.7, 0.15, 0.15], shuffle=True):
    lengths = [round(len(self)*size) for size in sizes]
    lengths[-1] = len(self) - sum(lengths[:-1])

    if seed == None:
      self.splits = random_split(self, lengths)
    else:
      self.splits = random_split(self, lengths,
        generator=torch.Generator().manual_seed(seed))