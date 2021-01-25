# tddish

## Usage
tddish \<pyhton filename\> [\<argname\>=\<argvalue\> \<argname\>=\<argvalue\> ...]

##### Example:
tddish app.py
tddish app1.py debug=enabled maxdepth=100 level=super

## Details

**tddish** is a TDD (Test Driven Development) tool for python coders. The tool gives the Test-While-Coding experience to code writers. The idea is that as the coder writes a functions, he/she would also write some test code to test the functionality. The test code will be within docstring with *'''tdd* at the start. E.g.

```
def add(n1:int, n2:int) -> int:
    return n1 + n2
'''tdd
tdd('add():1", add(2,3) == 5)
tdd('add():2", add(0,3) != 2)
'''
```
The docstring (starting with ‘’’tdd) tells the tddish that the code within the docstring is test code. The tdd() function is like the python assert. It takes two parameters, 1. the test-case name and 2. the test condition. If the condition is False, it reports the test case as failed. so, tdd(“test1”, add(1,1) == 3) would fail. The test-case name should be such that the coder can easily search for it in the code. One way of naming test case is to use the function name and a seq num together (as shown in the code above).

### Testing with data

The *tdd* docstring can contain any valid python code. This can be used to define data to test a function. E.g

```
# mycode.py
def srch(needle:str, hay:list):
    if needle in hay:
        return True
    return False
'''tdd
hay = ['ab', 'bc', 'cd']
tdd('srch()1:', srch('ab', hay))
tdd('srch()1:', srch('de', hay) == False)
'''
```

### Testing with command line argument
The coder can also pass command-line argument. Let’s say the file under test is mycode.py. It needs two command-line arguments namely *count* and *logfile*. The coder can pass it to using the following command.

`tddish mycode.py count=10 logfile=./debug.log`

In the tdd code, these user arguments will be available a args[‘count’] and args[‘logfile’]. E.g.

```
# display.py
def verify_user(s:str):
    if s == args['user']:
        return True
    return False
'''tdd
tdd('verify_user()1:', verify_user('Harrier'))
tdd('verify_user()1:', verify_user('Falcon') == False)
'''
```

When the above code is tested using tddish like

`tddish display.py user=Harrier`

The test-case will pass.
