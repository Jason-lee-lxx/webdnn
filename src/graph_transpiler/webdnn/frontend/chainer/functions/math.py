import chainer
import numpy as np

from webdnn.frontend.chainer.converter import ChainerConverter
from webdnn.frontend.chainer.util import unary_op_handler
from webdnn.frontend.util import check_broadcast_constraints
from webdnn.graph.operators.acos import Acos
from webdnn.graph.operators.asin import Asin
from webdnn.graph.operators.atan import Atan
from webdnn.graph.operators.cos import Cos
from webdnn.graph.operators.cosh import Cosh
from webdnn.graph.operators.exp import Exp
from webdnn.graph.operators.greater import Greater
from webdnn.graph.operators.log import Log
from webdnn.graph.operators.max import Max
from webdnn.graph.operators.min import Min
from webdnn.graph.operators.sin import Sin
from webdnn.graph.operators.sinh import Sinh
from webdnn.graph.operators.sum import Sum
from webdnn.graph.operators.tan import Tan
from webdnn.graph.operators.tensordot import Tensordot
from webdnn.graph.order import Order
from webdnn.util import console

# TODO: BatchL2NormSquared

# TODO: Ceil

# TODO: Clip

# TODO: BatchDet

ChainerConverter.register_handler("Exp")(unary_op_handler(Exp))

ChainerConverter.register_handler("Log")(unary_op_handler(Log))


@ChainerConverter.register_handler("Log10")
def _convert_log10(converter: ChainerConverter, c_op: "chainer.functions.Log10"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Log(None)(x) / np.log(10)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("Log2")
def _convert_log2(converter: ChainerConverter, c_op: "chainer.functions.Log2"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Log(None)(x) / np.log(2)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("Expm1")
def _convert_expm1(converter: ChainerConverter, c_op: "chainer.functions.Expm1"):
    console.warning("[ChainerConverter] In WebDNN, \"Expm1(x)\" is converted into \"Exp(x)-1\", which is not enough accurate as Expm1 when"
                    "x is so small that \"Exp(x) == 1\" in floating point accuracy.")
    x = converter.get_variable(c_op.inputs[0])
    y = Exp(None)(x)[0] - 1
    converter.set_variable(c_op.outputs[0](), y)


# TODO: Floor

# TODO: Fmod

ChainerConverter.register_handler("Cosh")(unary_op_handler(Cosh))

ChainerConverter.register_handler("Sinh")(unary_op_handler(Sinh))


@ChainerConverter.register_handler("Identity")
def _convert_identity(converter: ChainerConverter, c_op: "chainer.functions.Identity"):
    x = converter.get_variable(c_op.inputs[0])
    converter.set_variable(c_op.outputs[0](), x)


# TODO: BatchInv

# TODO: Inv

# TODO: LinearInterpolate


@ChainerConverter.register_handler("Log1p")
def _convert_log1p(converter: ChainerConverter, c_op: "chainer.functions.Log1p"):
    console.warning("[ChainerConverter] In WebDNN, \"Log1p(x)\" is converted into \"Log(1+x)\", which is not enough accurate as Log1p when"
                    "x is so small that \"1 + x == 1\" in floating point accuracy.")
    x = converter.get_variable(c_op.inputs[0])
    y, = Log(None)(x + 1)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("LogSumExp")
def _convert_logsumexp(converter: ChainerConverter, c_op: "chainer.functions.LogSumExp"):
    x = converter.get_variable(c_op.inputs[0])

    if c_op.axis is None:
        axes = list(x.order.axes)
    else:
        axes = [x.order.axes[i] for i in c_op.axis]

    max_x = x
    for axis in axes:
        max_x, = Max(None, axis=axis)(max_x)
    exp_delta_x, = Exp(None)(x - max_x)

    sum_exp_delta_x = exp_delta_x
    for axis in axes:
        sum_exp_delta_x, = Sum(None, axis=axis)(sum_exp_delta_x)

    y = Log(None)(sum_exp_delta_x)[0] + max_x
    converter.set_variable(c_op.outputs[0](), y)


# TODO: BatchMatMul

@ChainerConverter.register_handler("MatMul")
def _convert_mat_mul(converter: ChainerConverter, c_op: "chainer.functions.MatMul"):
    x0 = converter.get_variable(c_op.inputs[0])
    x1 = converter.get_variable(c_op.inputs[1])
    if x0.order.axes[1 if c_op.transa else 0] == x1.order.axes[0 if c_op.transb else 1]:
        x1 = x1.reinterpret_axes(Order([None, None]))

    y, = Tensordot(None, axes=[x0.order.axes[0 if c_op.transa else 1], x1.order.axes[1 if c_op.transb else 0]])(x0, x1)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("Maximum")
def _convert_maximum(converter: ChainerConverter, c_op: "chainer.functions.Maximum"):
    x = converter.get_variable(c_op.inputs[0])
    y = converter.get_variable(c_op.inputs[1])

    check_broadcast_constraints(x, y)

    tmp, = Greater(None)(x, y)
    z = x * tmp + y * (1 - tmp)
    converter.set_variable(c_op.outputs[0](), z)


@ChainerConverter.register_handler("Minimum")
def _convert_minimum(converter: ChainerConverter, c_op: "chainer.functions.Minimum"):
    x = converter.get_variable(c_op.inputs[0])
    y = converter.get_variable(c_op.inputs[1])

    check_broadcast_constraints(x, y)

    tmp, = Greater(None)(x, y)
    z = x * (1 - tmp) + y * tmp
    converter.set_variable(c_op.outputs[0](), z)


# TODO: ArgMax

# TODO: ArgMin

@ChainerConverter.register_handler("Max")
def _convert_max(converter: ChainerConverter, c_op: "chainer.functions.Max"):
    x = converter.get_variable(c_op.inputs[0])
    for axis in list(x.order.axes) if c_op.axis is None else [x.order.axes[i] for i in c_op.axis]:
        x, = Max(None, axis=axis)(x)

        if not c_op.keepdims and x.ndim > 1:
            x = x.squeeze(axis)

    converter.set_variable(c_op.outputs[0](), x)


@ChainerConverter.register_handler("Min")
def _convert_min(converter: ChainerConverter, c_op: "chainer.functions.Min"):
    x = converter.get_variable(c_op.inputs[0])
    for axis in list(x.order.axes) if c_op.axis is None else [x.order.axes[i] for i in c_op.axis]:
        x, = Min(None, axis=axis)(x)

        if not c_op.keepdims and x.ndim > 1:
            x = x.squeeze(axis)

    converter.set_variable(c_op.outputs[0](), x)


# TODO: Sqrt

# TODO: Square

# TODO: SquaredDifference

@ChainerConverter.register_handler("Sum")
def _convert_sum(converter: ChainerConverter, c_op: "chainer.functions.Sum"):
    x = converter.get_variable(c_op.inputs[0])
    for axis in list(x.order.axes) if c_op.axis is None else [x.order.axes[i] for i in c_op.axis]:
        x, = Sum(None, axis=axis)(x)

        # chainer.functions.sum supported "keepdims" parameter since v1.24
        if chainer.__version__ >= "1.24" and c_op.keepdims and x.ndim > 1:
            pass

        else:
            x = x.squeeze(axis)

    converter.set_variable(c_op.outputs[0](), x)


ChainerConverter.register_handler("Arccos")(unary_op_handler(Acos))

ChainerConverter.register_handler("Arcsin")(unary_op_handler(Asin))

ChainerConverter.register_handler("Arctan")(unary_op_handler(Atan))

ChainerConverter.register_handler("Cos")(unary_op_handler(Cos))

ChainerConverter.register_handler("Sin")(unary_op_handler(Sin))

ChainerConverter.register_handler("Tan")(unary_op_handler(Tan))
