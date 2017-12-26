import os

OPTIMIZE = os.environ.get("OPTIMIZE", "1") == "1"

# basic (non-accuracy loss) optimization
REMOVE_REDUNDANT_OPERATOR = os.environ.get("REMOVE_REDUNDANT_OPERATOR", "1") == "1"
SIMPLIFY_ELEMENTWISE = os.environ.get("SIMPLIFY_ELEMENTWISE", "1") == "1"
REPLACE_SCALAR_OPERATOR = os.environ.get("REPLACE_SCALAR_OPERATOR", "1") == "1"
REMOVE_NO_EFFECT_OPERATOR = os.environ.get("REMOVE_NO_EFFECT_OPERATOR", "1") == "1"
REMOVE_NO_EFFECT_SCALAR_ADD = os.environ.get("REMOVE_NO_EFFECT_SCALAR_ADD", "1") == "1"
REMOVE_NO_EFFECT_SCALAR_MUL = os.environ.get("REMOVE_NO_EFFECT_SCALAR_MUL", "1") == "1"
REMOVE_NO_EFFECT_SCALAR_POW = os.environ.get("REMOVE_NO_EFFECT_SCALAR_POW", "1") == "1"
REMOVE_NO_EFFECT_RESHAPE = os.environ.get("REMOVE_NO_EFFECT_RESHAPE", "1") == "1"
REMOVE_NO_EFFECT_TRANSPOSE = os.environ.get("REMOVE_NO_EFFECT_TRANSPOSE", "1") == "1"
REMOVE_NO_EFFECT_BROADCAST = os.environ.get("REMOVE_NO_EFFECT_BROADCAST", "1") == "1"
REMOVE_NO_EFFECT_ELEMENTWISE_ADD = os.environ.get("REMOVE_NO_EFFECT_ELEMENTWISE_ADD", "1") == "1"
REMOVE_NO_EFFECT_ELEMENTWISE_MUL = os.environ.get("REMOVE_NO_EFFECT_ELEMENTWISE_MUL", "1") == "1"
REMOVE_NO_EFFECT_ELEMENTWISE_DIV = os.environ.get("REMOVE_NO_EFFECT_ELEMENTWISE_DIV", "1") == "1"
REMOVE_NO_EFFECT_ELEMENTWISE_POW = os.environ.get("REMOVE_NO_EFFECT_ELEMENTWISE_POW", "1") == "1"
REMOVE_NO_EFFECT_REINTERPRET_AXIS = os.environ.get("REMOVE_NO_EFFECT_REINTERPRET_AXIS", "1") == "1"
ELEMENTWISE_KERNEL_FUSION = os.environ.get("ELEMENTWISE_KERNEL_FUSION", "1") == "1"
SIMPLIFY_ELEMENTWISE_SEQUENCE = os.environ.get("SIMPLIFY_ELEMENTWISE_SEQUENCE", "1") == "1"
SIMPLIFY_ASSOCIATIVE_OPERATOR = os.environ.get("SIMPLIFY_ASSOCIATIVE_OPERATOR", "1") == "1"
SIMPLIFY_ASSOCIATIVE_OPERATOR_LEFT_HAND = os.environ.get("SIMPLIFY_ASSOCIATIVE_OPERATOR_LEFT", "1") == "1"
SIMPLIFY_ASSOCIATIVE_OPERATOR_RIGHT_HAND = os.environ.get("SIMPLIFY_ASSOCIATIVE_OPERATOR_RIGHT", "1") == "1"
SIMPLIFY_CHANNEL_MODE_CONVERSION = os.environ.get("SIMPLIFY_CHANNEL_MODE_CONVERSION", "1") == "1"
SIMPLIFY_NONSENSE_CHANNEL_MODE_CONVERSION = os.environ.get("SIMPLIFY_NONSENSE_CHANNEL_MODE_CONVERSION", "1") == "1"
SIMPLIFY_REDUNDANT_CHANNEL_MODE_CONVERSION = os.environ.get("SIMPLIFY_REDUNDANT_CHANNEL_MODE_CONVERSION", "1") == "1"
SIMPLIFY_IN_OUT_CHANNEL_MODE_CONVERSION = os.environ.get("SIMPLIFY_IN_OUT_CHANNEL_MODE_CONVERSION", "1") == "1"
SIMPLIFY_COMMUTATIVE_OPERATOR = os.environ.get("SIMPLIFY_COMMUTATIVE_OPERATOR", "1") == "1"
MERGE_TENSORDOT_AND_ELEMENTWISE_MUL = os.environ.get("MERGE_TENSORDOT_AND_ELEMENTWISE_MUL", "1") == "1"
MERGE_TENSORDOT_AND_ELEMENTWISE_ADD = os.environ.get("MERGE_TENSORDOT_AND_ELEMENTWISE_ADD", "1") == "1"
OPTIMIZE_CHANNEL_MODE = os.environ.get("OPTIMIZE_CHANNEL_MODE", "1") == "1"
EXTRACT_UNIFORM_LITERAL = os.environ.get("EXTRACT_UNIFORM_LITERAL", "0") == "1"
CONSTANT_FOLDING = os.environ.get("CONSTANT_FOLDING", "1") == "1"
OPTIMIZE_ORDER = os.environ.get("OPTIMIZE_ORDER", "1") == "1"

# compression
CONV_FILTER_PRUNING = os.environ.get("CONV_FILTER_PRUNING", "0") == "1"
CONV_SVD_COMPRESSION = os.environ.get("CONV_SVD_COMPRESSION", "0") == "1"

# memory allocation
VALIDATE_GENERATED_SOURCE = os.environ.get("VALIDATE_GENERATED_SOURCE", "1") == "1"
OPTIMIZE_INPLACE_OPERATION = os.environ.get("OPTIMIZE_INPLACE_OPERATION", "1") == "1"
OPTIMIZE_MEMORY_ALLOCATION = os.environ.get("OPTIMIZE_MEMORY_ALLOCATION", "1") == "1"

# webgl backend
WEBGL_OPTIMIZE_TEXTURE_SIZE = os.environ.get("WEBGL_OPTIMIZE_TEXTURE_SIZE", "1") == "1"
