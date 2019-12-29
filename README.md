# PyLambdaFlows
[![Documentation Status](https://readthedocs.org/projects/pylambdaflows/badge/?version=latest)](https://pylambdaflows.readthedocs.io/en/latest/?badge=latest)

PyLambdaFlows lets you run your program on AWS Lambda for a large scale execution. It make you able to easily use AWS service without major alteration on your code. Moreover, you can define very complexe dependancies between your step and create your own dependancie function ! 
This project was inspired by *[PyWren](https://github.com/pywren/pywren)* library.   

In order to create a lambda gesture, pylambdaFlow use dynamodb.

## Table of Contents
-   [Documentation](https://github.com/Enderdead/pyLambdaFlows#docs) : This section contains some ways to get few docs.
-   [Examples](https://github.com/Enderdead/pyLambdaFlows#examples) :  This section will describe you how can you use pyLambdaFlows.
-   [Installation](https://github.com/Enderdead/pyLambdaFlows#installation) : This section will explain you how can you install this library
-   [Features](https://github.com/Enderdead/pyLambdaFlows#features) : This section will explain you shorlty all available features on pylambdalflows (computational graph, custom op, and so on).
-   [AWS setup](https://github.com/Enderdead/pyLambdaFlows#aws-setup) : This section will show you how can you correctly setup your AWS credentials to be ready to go !

## Documentation
You can either find out the documentation [here at readthedocs](https://pylambdaflows.readthedocs.io/en/latest/index.html) or generate your own using the provided makefile or just read through the source code ;-).

## Examples
Firsly you have to split your code into kernel file. One file kernel per operation is the common way to work with. 
In this example, we want to apply a map and a reduce onto a int array. 
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
def  lambda_handler(inputData):
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
Finally we are able to call the AWS api for uploading and calling lambda function.
```python
with pyLambdaFlows.Session(credentials_csv="./accessKeys.csv") as sess:
	mean_squared.compile()
	result = mean_squared.eval(feed_dict={array:[1,2,3]})
	print(result)
```
Output : 
```
4.666666666666667
```
## Installation
Firstly you need to clone this repo on your computer with this git command : 
```
git clone https://github.com/Enderdead/pyLambdaFlows.git
```
Then it's recommanded to install dependancies using pip3 tool : 
```
pip3 install -r requirements.txt
```
Finaly you can install pylambdaflow with the setup script : 
```
python3 setup.py install --user
```

## Features
##### TODO

## AWS setup
##### TODO
