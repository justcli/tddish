# # tddish
**tddish** is a TDD (Test Driven Development) tool for python coders. The tool gives the Test-As-You-Code experience to code writers. The idea is that as the coder writes a function, he/she would can also write the test code for that function.

## Usage
tddish \<pyhton filename\> [\<argname\>=\<argvalue\> \<argname\>=\<argvalue\> ...]

##### Example:
tddish app.py
tddish app1.py debug=enabled maxdepth=100 level=super

## Install
You can install tddish by either cloning this repo or downloading the tar file.
```
> gh repo clone justcli/tddish
or
> curl -LO https://github.com/justcli/tddish/releases/download/tddish-v1.0/tddish.tar.gz
or
> wget https://github.com/justcli/tddish/releases/download/tddish-v1.0/tddish.tar.gz
```
then running the following commands.
```
> tar -xvf tddish.tar.gz
> cd tddish
> ./install.sh
```


###### To uninstall

```
> tddish -uninstall
```


## How to use
Once you write a function, you can write the test case(s) for the functions next to it. The test code is kept commented between **’’’tddish** and **’’’**. E.g.

```
def add(n1:int, n2:int) -> int:
    return n1 + n2
'''tddish
tdd('add():1', add(2,3) == 5)
tdd('add():2', add(0,3) != 2)
'''
```
The function tddish() takes two arguments, one is the test case name and the other is a condition. If the condition is True, the test is reported as pass. Otherwise, it is reported as failed. In the above example, the tddish tool will  generate a report like
```
tddish : add():1…………………………………………passed
tddish : add():2…………………………………………passed
```


#### Testing with user data

The *tddish* docstring can contain any valid python code. This can be used to define data to test a function. E.g

```
# mycode.py
def srch(needle:str, hay:list):
    if needle in hay:
        return True
    return False
'''tddish
hay = ['ab', 'bc', 'cd']
tdd('srch()1:', srch('ab', hay))
tdd('srch()1:', srch('de', hay) == False)
'''
```

#### Testing with user argument
The coder can also pass command-line argument. Let’s say the file under test is mycode.py. It needs two command-line arguments namely *count* and *logfile*. The coder can pass it to using the following command.

`tddish mycode.py count=10 logfile=./debug.log`

In the tdd code, these user arguments will be available a args[‘count’] and args[‘logfile’]. E.g.

```
# display.py
def verify_user(s:str):
    if s == args['user']:
        return True
    return False
'''tddish
tdd('verify_user()1:', verify_user('Harrier'))
tdd('verify_user()1:', verify_user('Falcon') == False)
'''
```

The above code shows the following tddish report.

```
tddish : verify_user()1:…………………………………passed
tddish : verify_user()1:…………………………………passed
```

#### Using tddish as module
**tddish** can be used as module as well. When you run the following code, tdd report is written out. Note  

```
from tddish import *
def add(n1:int, n2:int) -> int:
    return n1 + n2
#'''tddish
tdd('add():1', add(2,3) == 5)
tdd('add():2', add(0,3) != 2)
#'''
```
that the *‘’’tddish* header and the *‘’’* footer is commented out. This helps the coder run the test code for the latest function from the IDE itself. After the tests are run, the tddish header (‘’’tddish) and the footer (‘’’) can be uncommented.

## Jenkins Integration
To run the test cases as part of Jenkins (or some CI/CD framework), the tddish command should be run with the target source file as argument. While using tddish as part of test automation, you should avoid user arguments. Instead, you can set the data in the testcase. E.g. For the code below
```
def verify_user(s:str):
    if s == args['user']:
        return True
    return False
```
Use the following test case (when under automation test framework)
```
# myapp.py
'''tddish
args = {}
args[‘user’] = ‘Harrier’
tdd('verify_user()1:', verify_user('Harrier'))
tdd('verify_user()1:', verify_user('Falcon') == False)
'''
> tddish myapp.py
```
instead of
```
# myapp.py
'''tddish
tdd('verify_user()1:', verify_user('Harrier'))
tdd('verify_user()1:', verify_user('Falcon') == False)
'''
> tddish myapp.py user=Harrier
```


