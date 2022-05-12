# Searchengineinterminal

Name: Senjuti Dutta



# ---Overview of Code----#
I have uploaded  4 separate python files.
1. crawler.py: Implements and executes the WebCrawler class which scrapes the parent url and crawl links and collect documents
2. interface.py:  Implements and executes specific mode.
If “Command-Line Mode” is active and a query was supplied, the program
should send the query to the parental SearchEngine component’s “handle_
query” function and print the results to the terminal.
∗ If “Interactive Mode” is active, the program should print the search engine
header shown and then begin interactively accepting queries. The interface
should facilitate an input loop in which a query can be supplied and related
results are printed in the terminal. When a query is received, the query should
be sent to the “handle_input” method below. The interface should stop sending
input to this method when “:exit” is provided
3. engine.py: Implements and executes the search engine , computes tf_idf
4. main.py:  The main function handles all the arguments. In this case I have implemented the -root and -mode as required. In the case of "Command -Line mode" the query needs to passed as -query and if no argument is provided it will provide error and same for "Interactive Mode" the -verbose needs to passed as -verbose and if no argument is provided it will provide error. I have hard coded depth d here as 0 or 1. I have implemented only up to d = 1.


#------Run Command ------#
py main.py - root argument 1 -mode  argument 2
If Command Line mode then py main.py - root argument 1 -mode  argument 2  -query argument ( if query argument is blank it will provide an error)
If Interactive  mode then py main.py - root argument 1 -mode  argument 2  -verbose argument ( if verbose argument is blank it will provide an error)
