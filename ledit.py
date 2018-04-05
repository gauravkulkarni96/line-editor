#!/usr/bin/env python
import sys
import os

# IMPORT FUNCTIONS FOR OPERATIONS
import operations

# FUNCTIONS LOOKUP DICTIONARY
# FOLLOWS THE FORMAT - 
# "<command>": [functionName, <description>, <inputFormat>, <undoable(boolean)>]
functions = {
	"d": [operations.display, "Display contents of File", "d[.n.m]", False],
	"h": [operations.showHelp, "Display editor help menu", "", False],
	"q": [operations.quit, "Quit ledit line editor", "", False],
	"i": [operations.insert, "Insert text at line no.", "i.n.<text>", True],
	"dd": [operations.delete, "Delete lines by line no.", "dd.n[.m]", True],
	"yy": [operations.copy, "Copy lines by line no.", "yy.n.m", False],
	"p": [operations.paste, "Paste contents of clipboard", "p.n", True],
	"z": [operations.undo, "Undo the last command", "", False],
	"zz": [operations.redo, "redo the last undone command", "", False]
}

if __name__ == "__main__":
	text = []
	file = ""

	# IF FILENAME NOT GIVEN CREATE "temp.txt"
	if len(sys.argv) < 2:
		print "No fileName given\nCreating a temporary file temp.txt"
		sys.argv[1] = file = "temp.txt"
	else:
		file = sys.argv[1]

	# IF FILENAME GIVEN OPEN FILE
	if os.path.isfile(file):
		with open (file,'r') as f:
			text = f.readlines()
	else:
		print "File "+file+" does not exist."
		print "New file will be created"

	print "\n\n-- LEdit Line Editor! --"
	print "h for list of commands\n"

	# INITIALIZE UNDO AND REDO STACKS
	undoStack = []
	redoStack = []

	# RUN INFINITE LOOP FOR CONTINUOUS INPUT
	run = True
	while run:
		if len(text) != 0 and text[-1][-1] != '\n':
			text[-1] += '\n'
		inputLine = raw_input("-> ").strip().split(".")

		# EXTRACT COMMAND FROM INPUT
		command = inputLine[0].lower()

		# CALL MATCHING FUNCTION FROM FUNCTION LOOKUP DICTIONARY
		try:
			if command in functions:
				func = functions[command][0]
			
				# IF UNDO/REDO OPERATION, SEND STACKS
				if command in ['z', 'zz']:
					run = func(text, undoStack, redoStack)
				elif command == "h":
					run = func(functions)
				else:
					# IF UNDOABLE FUNCTION, SEND UNDOSTACK
					if functions[command][3]:
						run = func(inputLine, text, undoStack)
					else:
						run = func(inputLine, text)
			else:
				print "Command does not exist.\nh for list of commands"
		except IOError as e:
			print "I/O Error: "+e.strerror  
		except:
			print "Oops! Missed out some bug."