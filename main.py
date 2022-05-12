
#author: Senjuti Dutta
# This code works as a Search engines that take text-based queries as input and provide a list of
#relevant documents as output. This project requires that your build a search engine that includes

import engine as se
import interface as si
import sys
import argparse

class Error(Exception):
    pass
class ValueError1(Error):
    pass
class ValueError2(Error):
    pass
class ValueError3(Error):
    pass
class ValueError4(Error):
    pass






if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    #parser.add_argument('--root', help = 'This is a valid value', choices = ("http", "https"), required=True, dest = self.root, type=str)
    parser.add_argument('-root', help = 'Put your root here', type=str, required=True)
    #parser.add_argument('--mode', help = 'This is a valid value', choices = ("C", "I"), dest = self.mode, typetype=str, required=True)
    parser.add_argument('-mode', help = 'Put your mode here', type=str, required=True)

    parser.add_argument('-query', type=str, required =False)
    parser.add_argument('-verbose', type=str, required = False)

    try:
        args = vars(parser.parse_args())
        if not ((args['root'].startswith('http') or args['root'].startswith('https')) and (args['mode'] == "C" or args['mode'] == "I")):
            raise ValueError2
        elif args['mode'] =="C":
            if args['query']=="":
                raise ValueError3
        elif args['mode'] =="I":
            if args['verbose']=="":
                raise ValueError4
        else:
            raise ValueError1
    except ValueError1:
        print("ERROR: Missing required arguments")
        sys.exit(1)
    except ValueError2:
        print("“ERROR: Invalid arguments provided")
        sys.exit(1)
    except ValueError3:
        print("ERROR: Missing query argument")
        sys.exit(1)
    except ValueError4:
        print("ERROR: Missing verbose argument")
        sys.exit(1)


    if args['mode']== "C":
        # I have hard coded the depth vale as 0 or 1
        engine = se.SearchEngine(args['mode'], "", args['query'], args['root'], 0)
        s = si.SearchInterface(args['mode'],engine, args['query'])
        s.listen()

    elif args['mode']== "I":
        #self.mode == "I":
        print("-------------------------------")
        print("| \tUTK EECS SEARCH\t      |")
        print("-------------------------------")
        command = input("> ")
        engine = se.SearchEngine(args['mode'], args['verbose'], command, args['root'], 0)
        s = si.SearchInterface(args['mode'],engine, command)
        s.listen()
