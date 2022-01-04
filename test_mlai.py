# Importing
import tensorflow as tf
from tensorflow.python.ops.gen_array_ops import shape

# Checking version
print(tf.__version__)

# Creating Tensor
scalar = tf.constant(7)
print(scalar)

# Check number of dim
print(scalar.ndim)

# Create a vector
vector = tf.constant([10,10])
print(vector)
print(vector.ndim)

# Create a matrix
matrix = tf.constant([[10,7],[7,10]])
print(matrix)
print(matrix.ndim)

# Another matrix with dtype
another_matrix = tf.constant([[10.,7.],[7.,10.],[8.,9.]], dtype=tf.float16)
print(another_matrix)
print(another_matrix.ndim)

# Creating a tensor
tensor = tf.constant([
    [[1,2,3],[4,5,6]],
    [[7,8,9],[10,11,12]],
    [[13,14,15], [16,17,18]]])
print(tensor)
print(tensor.ndim)

# Variable tensors allow us to change values
c_tensor = tf.Variable(7)
print(c_tensor)
c_tensor.assign(10)
print(c_tensor)

# Random tensors
random_1 = tf.random.Generator.from_seed(42)
random_1 = random_1.normal(shape=(3,2))
print(random_1)
print(random_1.ndim)
