
import sys

from ProcessSaves import ProcessSaves
from FlaskRestEndpoints import RestInterface

if __name__ == '__main__':

    print('Connecting to reddit, gathering saved data')
    ps = ProcessSaves(sys.argv[1])
    ps.process_saves()
    print('Reddit setup complete')

    print('Setting up REST interface')
    ri = RestInterface()

    print('We\'re ready to go !!!')
    