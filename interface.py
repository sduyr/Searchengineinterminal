
import engine as se
import argparse
import sys
import main



class SearchInterface():
    def __init__(self, mode, engine, query):
        self.mode = mode
        self.engine = engine # reference of class Search Engine
        self.query = query # user_input query only for command line mode
        #self.command = command # user_input only for interactive mode
    def listen(self):
        ''' This function works based on the specified mode'''


        #if root_arg.startswith('http') or root_arg.startswith('https') and mode_arg == "T" or "F":


        if self.mode == "C":
            '''
            parser = argparse.ArgumentParser()
            parser.add_argument('-query', type=str, required =True)
            try:
                args = vars(parser.parse_args())
                # send query to the SearchEngine's handle query function
                self.engine.query = args ['query']
                # hanle.query should handle self. query
                # print the result to the terminal
            except:
                print("ERROR: Missing query argument")
                sys.exit(1)
            '''
            #self.query = main.args['query']
            self.engine.handle_query()



        elif self.mode == "I":

            '''
            print("-------------------------------")
            print("| \tUTK EECS SEARCH\t      |")
            print("-------------------------------")
            self.query = input("> ")
            '''

            #parser.parse_args()

            #if (str(self.query).startswith(":")):
            self.handle_input()

            #else:
                #self.engine.handle_query()
            #parser = argparse.ArgumentParser(exit_on_error = False, description="Verbose argument")
            #parser.add_argument('-verbose', help = 'Put your verbose argument', choices=('T','F'), required=True)
            #try:
                #parser.parse_args()

            #except:
                #print("ERROR: Missing verbose argument")
                #sys.exit(1)



    def handle_input(self):
        ''' This method should facilitate the routing of queries to functions in the search engine '''
        if self.query == ":delete" :
            self.engine.delete()
        elif self.query == ":train" :
            self.engine.train()
        elif self.query == ":exit" :
            sys.exit(1)
        else:
            self.engine.handle_query()
