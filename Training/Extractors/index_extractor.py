import torch


class IndexExtractor:
    def __init__(self):
        pass

    def init(self, params: dict = None):
        self.params = params
        self.all_vals = self.params["all_vals"]
        self.total_size = len(self.all_vals)
        self.all_vals.sort()
        self.eval_vals = self.all_vals
        self.index_dict = {}
        for i, element in enumerate(self.all_vals):
            self.index_dict[element] = i

    def encode(self, value: str):
        return self.index_dict[value]

    def decode(self, index):
        if type(index) == torch.Tensor:
            probabilities = {}
            for i, val in enumerate(self.all_vals):
                if index[i] > 0:
                    probabilities[val] = index[i]
            return probabilities
        return self.all_vals[index]
