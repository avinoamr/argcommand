import argcommand
import argparse

##
class Say( argcommand.Command ):
    """ Prints a message to the screen """

    what = argcommand.Argument( "WORD", default = "Something", help = "the text you want to print" )
    times = argcommand.Argument( "--times", "-t", type = int, default = 1, metavar = "T", help = "how many times you want to repeat the text" )

    #
    def run( self ):
        print self.times * self.what

class FirstLine( argcommand.Command ):
    """ Prints the first line of any file in the input """

    files = argcommand.Argument( "FILE", type = argparse.FileType( "r" ), nargs = "+",
                                 help = "The files to read" )

    def run( self ):
        for file_ in self.files:
            print file_.readline()

class TestCommand( argcommand.Command ):

    subcommands = [ Say, FirstLine ]

if "__main__" == __name__:
    TestCommand.execute()