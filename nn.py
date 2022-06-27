import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        self.weights = []
        self.biases = []

        self.number_of_layers = len(layer_sizes)  # Number of NeuralNetwork
        mu, sigma = 0, 1                          # mean and standard deviation
        for i in range(1, self.number_of_layers):
            self.weights.append(np.random.normal(mu, sigma, size=(layer_sizes[i], layer_sizes[i - 1])))
            self.biases.append(np.zeros((layer_sizes[i], 1)))

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        return self.get_activation("Sigmoid", x)

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # Output of first layer must be calculated separately
        output = self.activation(np.dot(self.weights[0], x) + self.biases[0])
        # then output of each layer is the input of next layer
        for i in range(1,self.number_of_layers-1):
            output = self.activation(np.dot(self.weights[i], output) + self.biases[i])
        return output

    def get_activation(self, activation_name, x):
        """
        Receives input vector and activation name input parameters and applying activation function.
        :param activation_name: Name of activation function that we want to use and it is a string.
        :param x: Input vector which is a numpy array.
        :return: output of activation function that applied on x
        """
        if activation_name == "Sigmoid":
            return 1 / (1 + np.exp(-x))
        elif activation_name == "ReLU":
            return np.maximum(0, x)
        elif activation_name == "tanh":
            return np.tanh(x)
        else:
            raise ValueError("The activation function isn't valid")
