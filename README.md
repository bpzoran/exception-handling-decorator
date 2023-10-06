# ExceptionHandler: Decorator for Exception Handling
ExceptionHandler is an open-source Python library for simplyfying exception handling. It makes Python handling exception code cleaner and more readable.


# Installation
To install **ExceptionHandler**, use **pip** with the following command:

```
pip install exception-handling-decorator
```

# Releases
Latest releases of ExceptionHandler can be found at the PyPI repository: [ExceptionHandler on PyPI](https://pypi.org/project/exception-handling-decorator/)

# Source Code
The source code is stored at the GitHub repository: [ExceptionHandler on GitHub](https://github.com/bpzoran/exception-handling-decorator/)

# Getting started
Import ExceptionHandler:
```python
from exception_handler import ExceptionHandler
```

Use @ExceptionHandler decorator with the following parameters:

**exception**=*Exception* - Exception(s) to be cаught. It can be of type ```Exception``` or its descendant or ```tuple[Exception]```.

**handling_func**=*None* - Function(s) to handle exception(s). It can be of type ```Callable``` or its descendant or ```tuple[Callable]```. If handling_func is *None*, the exception will not be handled. If there more than one handling function (```tuple[Callable]```), every function will handle the corresponding *Exception*.

**reraise**=*True* - Indicates if the excaption(s) should be reraised. It can be of type ```bool``` or its descendant or ```tuple[bool]```. If there more than one *reraise* (```tuple[bool]```), every tuple member will raise the corresponding *Exception*.


## Example 1

The following code handles a ZeroDivisionError with classic try/except catching, prints and re-raise the exception:
```python
def print_exception(ex):
    print(ex)

def divide_by_zero():
    try:
        return 1 / 0
    except ZeroDivisionError as e:
        print_exception(e)   
        raise

divide_by_zero()
```

We can simplify divide_by_zero() function by using ```@ExceptionHandler``` decorator:
```python
@ExceptionHandler(exception=ZeroDivisionError, handling_func=print_exception, reraise=True)
def divide_by_zero():
    return 1 / 0   
```

The final code:
```python
from exception_handler import ExceptionHandler
def print_exception(ex):
    print(ex)

@ExceptionHandler(exception=ZeroDivisionError, handling_func=print_exception, reraise=True)
def divide_by_zero():
    return 1 / 0  

divide_by_zero()  
```

## Example 2
The following code raises randomly one of two custom exceptions:
```python
import random
import logging

class SomeException(Exception):

    def __str__(self) -> str:
        return "SomeException message"

class SomeOtherException(Exception):
    def __str__(self) -> str:
        return "SomeOtherException message"

def get_rand_bool():
    """
    Returns random boolean value
    """
    rand_int = random.getrandbits(1)
    return bool(rand_int)

def log_exception(ex):
    logging.error(ex)


def print_exception(ex):
    print(ex)    


def do_something():
    if get_rand_bool():
        try:
            raise SomeException
        except SomeException as e:
            print_exception(e)
            raise
            
    try:
        raise SomeOtherException
    except SomeOtherException as e:
        log_exception(e)

do_something()
```

We can simplify do_something() function by using ```@ExceptionHandler``` decorator:
```python
@ExceptionHandler(exception=(SomeException, SomeOtherException), 
                  handling_func=(print_exception, log_exception), 
                  reraise=(True,False))
def do_something():
    if get_rand_bool():
        raise SomeException
    raise SomeOtherException
```

The final code:
```python
import random
from exception_handler import ExceptionHandler
import logging

class SomeException(Exception):

    def __str__(self) -> str:
        return "SomeException message"

class SomeOtherException(Exception):
    def __str__(self) -> str:
        return "SomeOtherException message"

def get_rand_bool():
    """
    Returns random boolean value
    """
    rand_int = random.getrandbits(1)
    return bool(rand_int)

def log_exception(ex):
    logging.error(ex)


def print_exception(ex):
    print(ex)  

@ExceptionHandler(exception=(SomeException, SomeOtherException), 
                  handling_func=(print_exception, log_exception), 
                  reraise=(True,False))
def do_something():
    if get_rand_bool():
        raise SomeException
    raise SomeOtherException  

do_something()
```