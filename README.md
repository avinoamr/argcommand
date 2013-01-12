argcommand
==========

A Python module that provides simple object-oriented abstraction layer for creating command-line interfaces. 

## Getting Started 

After installing the `argcommand` module somewhere on your system, begin by subclassing the `argcommand.Command` class that represents a command that needs to be executed from the command line, and calling the `.execute()`:

```python
import argcommand

class Say( argcommand.Command ):
    pass

if "__main__" == __name__:
    Say.execute()
```

The call to the `.execute()` **class-method** will attempt to parse command line arguments and run the Say command. We can test it now by running this example from the command line (with the `-h` argument:

```
$ python test.py -h
usage: test.py [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## Adding logic

The example above does nothing. In fact, if we try to run it without the `-h` argument, we'll get uncaught `NotImplementedError` exception. That's because we didn't implement the `.run()` abstract method:

```python
class Say( argcommand.Command ):
    def run( self ):
        print "Something"
```

That's it. Executing the say command will invoke its `.run()` method:

```
$ python test.py
Something
```

## Arguments

Of course that's a lot of overhead for such a simple task. It gets more interesting when we need to add command-line arguments:

```python
class Say( argcommand.Command ):

    what = argcommand.Argument( "WORD", default = "Something", help = "the text you want to print" )
    times = argcommand.Argument( "--times", "-t", type = int, default = 1, metavar = "T", 
                                 help = "how many times you want to repeat the text" )

    ...
```

The `Argument` class represents a command-line argument. It simply forwards its arguments to the `ArgumentParser.add_argument` method of the `argparse` built-in library. <a href="http://docs.python.org/2/library/argparse.html#the-add-argument-method">Read the argparse docs for the complete API specification</a>.

Since we didn't change the `.run()` method (we'll do that in a bit) the command will produce the same results. However, it now supports two arguments (one required positional, and one named optional). This is reflected in the command's help message:

```
$ python test.py -h
usage: test.py [-h] [--times T] WORD

positional arguments:
  WORD             the text you want to print

optional arguments:
  -h, --help       show this help message and exit
  --times T, -t T  how many times you want to repeat the text
```

Next, we'll change the `.run()` method implementation to use the values of these arguments. These values get assigned directly to the Command's instance:

```python
class Say( argcommand.Command ):
    ...
    def run( self ):
        print self.what * self.times
```

Run it to test the results:

```
$ python test.py hello --times 3
hellohellohello
```

## Subcommands
Sometimes we'll want to break down complex commands into several separate ones (using *subparsers* from `argparse`). We'll start by creating another Command:

```python
import argparse

class FirstLine( argcommand.Command ):

    files = argcommand.Argument( "FILE", type = argparse.FileType( "r" ), nargs = "+",
                                 help = "The files to read" )

    def run( self ):
        for file_ in self.files:
            print file_.readline()
```

This command will read the first line of every file passed as a command-line argument. Read more about <a href="http://docs.python.org/2/library/argparse.html#argparse.FileType">argparse.FileType</a>.

Now, we'll need to define both `Say` and `FirstLine` classes as subcommands of a single parent Command object:

```python
class TestCommand( argcommand.Command ):

    subcommands = [ Say, FirstLine ]
```

Finally, we need to replace the call to `Say.execute()` with our new `TestCommand` class:

```python
if "__main__" == __name__:
    TestCommand.execute() # replaces: Say.execute()
```

Run `test.py -h` again to see the changes in the help message, or run the specific subcommands:

```
$ python test.py say hello --times 3
hellohellohello

$ python test.py firstline README.*
argcommand

```

Calling `test.py say -h` will print the the help message of the `Say` subcommand.
