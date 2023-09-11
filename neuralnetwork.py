import numpy as np


class NNetwork:

    @staticmethod
    def getTotalWeights(*layers):
        return sum([(layers[i] + 1) * layers[i + 1] for i in range(len(layers) - 1)])

    def __init__(self, inputs, *layers):
        self.layers = []
        self.acts = []

        self.n_layers = len(layers)
        for i in range(self.n_layers):
            self.acts.append(self.act_relu)
            if i == 0:
                self.layers.append(self.getInitialWeights(layers[0], inputs + 1))
            else:
                self.layers.append(self.getInitialWeights(layers[i], layers[i - 1] + 1))

        self.acts[-1] = self.acts_softmax

    def getInitialWeights(self, n, m):
        return np.random.triangular(-1, 0, 1, size=(n, m))

    @staticmethod
    def act_relu(x):
        x[x < 0] = 0

        return x

    @staticmethod
    def act_th( x):
        x[x > 0] = 1
        x[x <= 0] = 0
        return x

    @staticmethod
    def acts_softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def get_weights(self):
        return np.hstack([w.ravel() for w in self.layers])

    def set_weights(self, weights):
        off = 0
        for i, w in enumerate(self.layers):
            w_set = weights[off:off + w.size]
            off += w.size
            self.layers[i] = np.array(w_set).reshape(w.shape)

    def predict(self, inputs):
        f = inputs
        for i, w in enumerate(self.layers):
            f = np.append(f, 1.0)
            f = self.acts[i](w @ f)
        return f
