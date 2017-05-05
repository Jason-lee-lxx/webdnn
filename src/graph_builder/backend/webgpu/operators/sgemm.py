from typing import Dict

import numpy as np

from graph_builder.graph.operator import Operator
from graph_builder.graph.operators.attributes.have_weights import HaveWeights
from graph_builder.graph.operators.attributes.post_axiswise import PostAxiswise
from graph_builder.graph.operators.attributes.post_elementwise import PostElementwise
from graph_builder.graph.variable import Variable


class Sgemm(Operator):
    attributes = {PostElementwise,
                  PostAxiswise,
                  HaveWeights}

    def __init__(self, name: str, parameters: Dict[str, any]):
        assert "M" in parameters
        assert "N" in parameters
        assert "K" in parameters
        assert "out_shape" in parameters
        assert "out_order" in parameters
        assert "transpose_A" in parameters
        assert "transpose_B" in parameters
        assert np.prod(parameters["out_shape"]) == parameters["M"] * parameters["N"]

        super().__init__(name, parameters)

    def __call__(self, A: Variable, B: Variable):
        self.append_input("A", A)
        self.append_input("B", B)

        C = Variable(
            self.parameters["out_shape"],
            self.parameters["out_order"]
        )
        self.append_output("C", C)

        return C,

    @property
    def M(self) -> int:
        return int(self.parameters["M"])

    @property
    def N(self) -> int:
        return int(self.parameters["N"])

    @property
    def K(self) -> int:
        return int(self.parameters["K"])

    @property
    def transpose_A(self) -> bool:
        return bool(self.parameters["transpose_A"])

    @property
    def transpose_B(self) -> bool:
        return bool(self.parameters["transpose_B"])
