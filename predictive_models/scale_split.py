from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

def scalesplit(X, y, test_size, sets=1, normalize=True, shuffle=True, seed=None):
    if seed:
        np.random.seed(seed)

    X_sets = {}
    y_sets = {}
    for set in range(sets):
        X, X_test, y, y_test = train_test_split(X, y,
                                        test_size=test_size, shuffle=shuffle)
        X_sets[0] = X
        X_sets[set+1] = X_test
        y_sets[0] = np.array(y).reshape(-1,)
        y_sets[set+1] = np.array(y_test).reshape(-1,)
        print(y_sets[0].shape, y_sets[set+1].shape)

    if normalize:
        sc = StandardScaler().fit(X_sets[0])
        X_sets[0] = sc.transform(X_sets[0])

        for set in range(sets):
            X_sets[set+1] = sc.transform(X_sets[set+1])

    return X_sets, y_sets