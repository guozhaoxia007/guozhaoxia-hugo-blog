---
date: "2016-02-21T01:09:41+08:00"
title: "函数式编程"
categories:
    - python

---

# 函数式编程
## 高阶函数
``` python
def add(x, y, f):
    return f(x) + f(y)
    
>>> add(-3, 2, abs)
5
>>> map(abs, [1, -2, -5])
[1, 2, 5]
``` 
常见的内置高阶函数
map/filter/reduce/sorted
## 返回函数
``` python
def f():
    print 'call f()...'
    # 定义函数g:
    def g():
        print 'call g()...'
    # 返回函数g:
    return g

>>> x = f()   # 调用f()
call f()...
>>> x   # 变量x是f()返回的函数：
<function g at 0x1037bf320>
>>> x()   # x指向函数，因此可以调用
call g()...   # 调用x()就是执行g()函数定义的代码
```
延迟计算
## 闭包
``` python
def f():
    print 'f()...'
    def g():
        print 'g()...'
    return g

# 希望一次返回3个函数，分别计算1x1,2x2,3x3:
def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
```
## 匿名函数
``` python
>>> map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])
[1, 4, 9, 16, 25, 36, 49, 64, 81]

>>> sorted([1, 3, 9, 5, 0], lambda x,y: -cmp(x,y))
[9, 5, 3, 1, 0]

>>> myabs = lambda x: -x if x < 0 else x 
>>> myabs(-1)
1
>>> myabs(1)
1
```
## decorator装饰器
``` python
>>> def f1(x):
...     return x * x
...
>>> def f2(x):
...     return x * 2
...
>>> def new_fn(f):
...     def fn(x):
...         print 'call ' + f.__name__ + '()'
...         return f(x)
...     return fn
...
>>> g2 = new_fn(f2)
>>> g2(5)
call f2()
10
>>>
>>> @new_fn
... def f1(x):
...     return x * 2
...
>>> f1(5)
call f1()
10
```
Q1: 如果被装饰的函数函数个数不一样怎么办
``` python
import time

def performance(f):
    def fn(*args, **kw):
        t1 = time.time()
        r = f(*args, **kw)
        t2 = time.time()
        print 'call %s() in %fs' % (f.__name__, (t2 - t1))
        return r
    return fn

performance
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print factorial(10)
```
带参数的decorator, @log("INFO")
```python
def log(prefix):
    def log_decorator(f):
        def wrapper(*args, **kw):
            print '[%s] %s()...' % (prefix, f.__name__)
            return f(*args, **kw)
        return wrapper
    return log_decorator

@log('DEBUG')
def test():
    pass
print test()
```
```python
import time

def performance(unit):
    def performance_decorator(f):
        def wrapper(*args, **kw):
            t1 = time.time()
            r = f(*args, **kw)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit == 'ms' else (t2 - t1)
            print 'call %s() in %f %s' % (f.__name__, t, unit)
            return r
        return wrapper
    return performance_decorator

@performance('ms')
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))

print factorial(10)
```
## 完善decorator
```python
import functools
def log(f):
    @functools.wraps(f)
    def wrapper(*args, **kw):
        print 'call...'
        return f(*args, **kw)
    return wrapper
```
## 偏函数
