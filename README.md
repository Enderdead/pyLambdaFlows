# PyLambdaFlows
[![Documentation Status](https://readthedocs.org/projects/pylambdaflows/badge/?version=latest)](https://pylambdaflows.readthedocs.io/en/latest/?badge=latest)

PyLambdaFlows lets you run your program on AWS Lambda for a large scale execution. It makes you able to use AWS service without major alteration on your code. Moreover, you can define very complex dependencies between your step and create your own dependencies function !
This project was inspired by *[PyWren](https://github.com/pywren/pywren)* library.

In order to create a lambda gesture, pylambdaFlow use dynamodb.

## Table of Contents

- [Documentation](https://github.com/Enderdead/pyLambdaFlows#docs) : This section contains some ways to get few docs.
- [Examples](https://github.com/Enderdead/pyLambdaFlows#examples) :  This section will describe to you how you can use pyLambdaFlows.
- [Installation](https://github.com/Enderdead/pyLambdaFlows#installation) : This section will explain to you how can you install this library
- [Features](https://github.com/Enderdead/pyLambdaFlows#features) : This section will explain to you shortly all available features on pylambdalflows (computational graph, custom op, and so on).
- [AWS setup](https://github.com/Enderdead/pyLambdaFlows#aws-setup) : This section will show you how can you correctly set up your AWS credentials to be ready to go!

## Documentation

You can either find out the documentation [here at readthedocs](https://pylambdaflows.readthedocs.io/en/latest/index.html) or generate your own using the provided makefile or just read through the source code ;-).

## Examples

Firstly you have to split your code into kernel file. One file kernel per operation is the common way to work with.
In this example, we want to apply a map and a reduce onto an int array.
The kernel map can be defined as follow :

```python
from pyLambdaFlows.decorator import kernel
@kernel
def  lambda_handler(inputData):
   return inputData*inputData
```

And the reduce op can be written like this :
from pyLambdaFlows.decorator import kernel

```python
from statistics import mean
from pyLambdaFlows.decorator import kernel
@kernel
def lambda_handler(inputData):
   result = mean(inputData)
   return result
```

Then, we need to create the call graph on a main file:

```python
import pyLambdaFlows
array = pyLambdaFlows.op.Source()
squared_array = pyLambdaFlows.op.Map(array, "map.py", name="square_op")
mean_squared = pyLambdaFlows.op.Reduce(squared_array, "mean.py", name="mean_op")
```

Finally, we can call the AWS API for uploading and calling lambda function.

```python
with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv") as sess:
   mean_squared.compile()
   result = mean_squared.eval(feed_dict={array:[1,2,3]})
   print(result)
```

Output :

``` bash
4.666666666666667
```

## Installation

Firstly you need to clone this repo on your computer with this git command :

``` bash
git clone https://github.com/Enderdead/pyLambdaFlows.git
```

Then it's recommended to install dependencies using pip3 tool :

``` bash
pip3 install -r requirements.txt
```

Finally, you can install pylambdaflow with the setup script :

``` bash
python3 setup.py install --user
```

## Performance

pyLambda is a proof of concept which means that overall implementation isn't as good as it can be. That means pyLambdaFlow can't handle a large scale project, but feel free to improve it yourself. Basic benchmark was done to compare this efficiency against pyrewn.

## AWS setup

To use this library, you have to create your AWS credentials. It's pretty simple using the AWS web interface. You can find out some instructions in the pyLambdaFlow doc.
