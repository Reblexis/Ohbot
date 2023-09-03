class Parameter:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class ContinuousParameter(Parameter):

    def __init__(self, name: str, description: str, minimum: float, maximum: float, default: float):
        super().__init__(name, description)

        self.min = minimum
        self.max = maximum
        self.default = default
        assert self.min <= self.default <= self.max

    def __str__(self):
        answer: str = f"Name: '{self.name}'. Type: Continuous. Description: '{self.description}'. Minimum: {self.min}. Maximum: {self.max}. Default: {self.default}"
        return answer


class DiscreteParameter(Parameter):
    def __init__(self, name: str, description: str, options: list, default: str):
        super().__init__(name, description)

        self.options = options
        self.default = default
        assert self.default in self.options

    def __str__(self):
        answer: str = f"Name: '{self.name}'. Type: Discrete. Description: '{self.description}'. Options: {self.options}. Default: '{self.default}'"
        return answer


class TextParameter(Parameter):
    """
    A parameter that accepts text as input.
    """

    def __init__(self, name: str, description: str, default: str):
        super().__init__(name, description)

        self.default = default

    def __str__(self):
        answer: str = f"Name: '{self.name}'. Type: Text. Description: '{self.description}'. Default: '{self.default}'"
        return answer

