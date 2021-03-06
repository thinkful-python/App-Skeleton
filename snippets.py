import psycopg2
import logging
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='ubuntu' password='thinkful' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    try:
        with connection, connection.cursor() as cursor:
           command = "insert into snippets values (%s, %s)"
           cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
       with connection, connection.cursor() as cursor:
           command = "update snippets set message=%s where keyword=%s"
           cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet
								
def get(name):
    """Retrieve the snippet with a given name. If there is no such snippet, program will not retrieve anything. Be aware that this will not auto populate due to security risks. Return snippet. """
    with connection, connection.cursor() as cursor:
    	cursor.execute("select message from snippets where keyword=%s", (name,))
    	row = cursor.fetchone()
    if not row: 
		#No snippet was found with that name
		print "no such avail"
    return row	
    
def catalog(): 
	""" list available snippets """ 
	with connection, connection.cursor() as cursor: 
		cursor.execute("select * from snippets order by keyword") 
		return cursor.fetchall()
    
def main(): 
	"""Main function"""
	logging.info("Constructing parser")
	parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
	
	subparsers = parser.add_subparsers(dest="command", help="Available commands")
	
	#subparser for the put command
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help = "Store a snippet")
	put_parser.add_argument("name", help = "The name of the snippet")
	put_parser.add_argument("snippet", help = "The snippet text")
	
	get_parser = subparsers.add_parser("get", help = "Get a snippet")
	get_parser.add_argument("name", help = "The name of the snippet")
	
	list_parser = subparsers.add_parser("list", help = "list available snippets to retrieve") 
	
	arguments = parser.parse_args(sys.argv[1:])
	
	# Convert parsed arguments from Namesapce to dictionary 
	arguments = vars(arguments)
	command = arguments.pop("command")
	
	if command == "put":
		name, snippet = put (**arguments)
		print("Stored {!r} as {!r}".format(snippet, name))
	elif command == "get":
		snippet = get(**arguments)
		print("Retrieved snippet: {!r}".format(snippet))
	elif command == "list": 
		all_snippets = catalog(**arguments)
		print("Here's all the snippets: {!r}".format(all_snippets)) 
	
if __name__ == "__main__":
	main()
								