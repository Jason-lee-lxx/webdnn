from typing import Tuple

from graph_builder.backend.webgpu.operators.sgemm import Sgemm
from graph_builder.graph.axis import Axis
from graph_builder.graph.graph import Graph
from graph_builder.graph.operators.axiswise_bias import AxiswiseBias
from graph_builder.graph.variables.constant_variable import ConstantVariable
from graph_builder.optimize_rule import util
from graph_builder.optimize_rule.optimize_rule import OptimizeRule
from graph_builder.util import flags


class ConcatSgemmBias(OptimizeRule):
    """
    sgemm + axis_wise_bias -> sgemm
    """

    def optimize(self, graph: Graph) -> Tuple[Graph, bool]:
        if not flags.optimize.CONCAT_SGEMM_BIAS:
            return graph, False

        matches = util.search_sub_structure(graph, [Sgemm, AxiswiseBias])
        if len(matches) == 0:
            return graph, False

        flag_changed = False
        for match in matches:
            sgemm: Sgemm = match[0]
            axiswise_bias: AxiswiseBias = match[1]

            if axiswise_bias.parameters["axis"] != Axis.C:
                continue

            h = sgemm.outputs["C"]
            b = axiswise_bias.inputs["b"]
            y = axiswise_bias.outputs["y"]

            if not isinstance(b, ConstantVariable):
                continue

            if len(h.input_to) != 1:
                continue

            if "b" in sgemm.inputs:
                sgemm.inputs["b"].data += b.data
            else:
                sgemm.append_input("b", b)

            axiswise_bias.remove_all()
            sgemm.replace_output(h, y)
            flag_changed = True

        return graph, flag_changed
