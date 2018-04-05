import sys

# PYPERCLIP MODULE FOR USING CLIPBOARD TO COPY/PASTE ITEMS
try:
	import pyperclip
except:
	print "Pyperclip is not installed"
	print "run \"sudo pip install pyperclip\""
	print "for Linux, also run \"sudo apt-get install xclip\""

# CUSTOM CHECKS FOR INTEGERS, NO. OF ARGUMENTS AND INDEXES
from checks import checkIntegers, argLenCheck, indexCheck

def display(inputLine, text):
	textShow = text
	start = 1

	# VALIDATING INPUT
	if len(inputLine)>1:
		if not argLenCheck(inputLine, 0, 2):
			return True
		if not checkIntegers(inputLine[1], inputLine[2]):
			return True
		start = int(inputLine[1])
		end = int(inputLine[2])

		if not indexCheck(text, start, end):
			return True

		textShow = text[start-1:end]
	print "\n----- "+sys.argv[1]+" -----"
	for n, line in enumerate(textShow):
		print n+start, line,
	print ""
	return True

# SHOW HELP MENU
def showHelp(functions):
	print "\n\t\tHelp Menu\n"
	print "Command\t|Description\t\t\t|Format"
	for i in range(47): 
		print "\b-",
	print ""

	#PRINT FUNCTION DICTIONARY
	for i, j in functions.items():
		print i,"\t|", j[1],"\t|", j[2]
	print "\n"
	return True

# QUIT EDITOR
def quit(inputLine, text):

	# SAVE FILE AND QUIT
	with open (sys.argv[1], 'w') as f:
		f.write("".join(text))
	print "\n-- Exit LEdit! --"
	return False

# INSERT TEXT AT LINE NUMBER 
# undoStack="skip" IS USED BECAUSE INSERT ID BEING CALLED
# BY INSERT OPERATION AND ALSO IN UNDO/REDO OPERATIONS
# WE NEED TO SKIP PUSHING TO STACK IN CASE OF UNDO/REDO
# OPERATIONS WHICH DO NOT PASS "undoStack" AND VALUE OF
# undoStack BECOMES "skip"
def insert(inputLine, text, undoStack="skip"):
	# VALIDATING INPUT
	if not argLenCheck(inputLine, 2):
		return True
	lineNo = inputLine[1]
	insertText = inputLine[2]

	if not checkIntegers(lineNo):
		return True

	lineNo = int(lineNo)
	if len(text) < lineNo:
		diff = lineNo - len(text)
		text.extend(['\n' for x in range(diff-1)])
		text.append(insertText+"\n")
	else:
		text.insert(lineNo-1, insertText+"\n")

	# NOT PUSHING TO STACK IF UNDO/REDO OPERATION
	if undoStack != "skip":
		undoStack.append(inputLine[:])
	return True

# DELETE TEXT AT LINE NUMBERS
# undoStack="skip" IS USED BECAUSE DELETE ID BEING CALLED
# BY DELETE OPERATION AND ALSO IN UNDO/REDO OPERATIONS
# WE NEED TO SKIP PUSHING TO STACK IN CASE OF UNDO/REDO
# OPERATIONS WHICH DO NOT PASS "undoStack" AND VALUE OF
# undoStack BECOMES "skip"
def delete(inputLine, text, undoStack="skip"):
	deletion = []
	start = 0
	#VALIDATING INPUT
	if not argLenCheck(inputLine, 1, 2):
		return True
	else:
		if not checkIntegers(inputLine[1]):
			return True
		start = int(inputLine[1])
		if not indexCheck(text, start):
			return True
		# DELETE AND SAVE DELETED DATA FOR UNDO/REDO
		if len(inputLine) == 2:
			deletion = [text.pop(start-1)]
		else:
			if not checkIntegers(inputLine[2]):
				return True
			end = int(inputLine[2])
			if not indexCheck(text, start, end):
				return True
			# SAVE DELETED DATA FOR UNDO/REDO
			deletion = text[start-1:end]
			text[:] = text[:start-1] + text[end:]

	# NOT PUSHING TO STACK IF UNDO/REDO OPERATION
	if undoStack != "skip":
		undoStack.append(["dd", str(start), deletion])
	return True

# COPY TO CLIPBOARD
def copy(inputLine, text):
	if not argLenCheck(inputLine, 2):
		return True
	if not checkIntegers(inputLine[1], inputLine[2]):
		return True
	start = int(inputLine[1])
	end = int(inputLine[2])
	if not indexCheck(text, start, end):
		return True

	tempText = text[start-1:end]
	tempText = filter(lambda x: x if x!="\n" else "", tempText)
	pyperclip.copy("".join(tempText))
	return True

# PASTE FROM CLIPBOARD
def paste(inputLine, text, undoStack):
	lineNo = 0
	pasteText = []
	if not argLenCheck(inputLine, 1):
		return True
	if not checkIntegers(inputLine[1]):
		return True

	lineNo = int(inputLine[1])
	pasteText = pyperclip.paste().strip().splitlines(True)

	# APPEND '\n' FOR NEW LINE
	if len(pasteText) != 0 and pasteText[-1][-1] != '\n':
			pasteText[-1] += '\n'
	if(lineNo>len(text)):
		diff = lineNo - len(text)
		text.extend(['\n' for x in range(diff-1)])
		text.extend(pasteText)
	else:
		text[:] = text[:lineNo-1] + pasteText + text[lineNo-1:]

	# SAVE RECORD TO STACK
	undoStack.append(['p', str(lineNo), str(lineNo+len(pasteText)), pasteText])
	return True

# UNDO LAST OPERATION
def undo(text, undoStack, redoStack):
	if len(undoStack) == 0:
		print "There is no operation to undo."
		return True
	# POP FROM UNDO AND PUSH TO REDO STACK
	lastOperation = undoStack.pop()
	redoStack.append(lastOperation)

	func = undoFunctions[lastOperation[0]]
	func(text, lastOperation)
	return True

# REDO LAST OPERATION
def redo(text, undoStack, redoStack):
	if len(redoStack) == 0:
		print "there is no operation to redo."
		return True

	# POP FROM REDO AND PUSH TO UNDO STACK
	lastOperation = redoStack.pop()
	undoStack.append(lastOperation)

	func = redoFunctions[lastOperation[0]]
	func(text, lastOperation)
	return True

# UNDO OPERATIONS
def undoInsert(text, lastOperation):
	delete(["dd", lastOperation[1]], text)
	return

def undoDelete(text, lastOperation):
	for i in lastOperation[2][::-1]:
		insert(["i", lastOperation[1], i.rstrip('\n')], text)
	return

def undoPaste(text, lastOperation):
	delete(["dd", lastOperation[1], str(int(lastOperation[2])-1)], text)

# REDO OPERATIONS
def redoInsert(text, lastOperation):
	insert(lastOperation, text)
	return

def redoDelete(text, lastOperation):
	end = str(int(lastOperation[1]) + len(lastOperation[2])-1)
	delete(["dd", lastOperation[1], end],text)
	return

def redoPaste(text, lastOperation):
	for i in lastOperation[3][::-1]:
		insert(["i", lastOperation[1], i.rstrip('\n')], text)
	return

# UNDO LOOKUP DICTIONARY
undoFunctions = {
	"i": undoInsert,
	"dd": undoDelete,
	"p": undoPaste
}

# REDO LOOKUP DICTIONARY
redoFunctions = {
	"i":redoInsert,
	"dd": redoDelete,
	"p":redoPaste,
}