import sys

# TO CHECK IF GIVEN INPUTS ARE INTEGERS
def checkIntegers(*args):
	for i in args:
		if not i.isdigit():
			print "line number should be an integer.\n"
			return False
	return True

# TO CHECK NUMBER OF ARGUMENTS GIVEN IN INPUT
def argLenCheck(inputLine, *allowed):
	inLen = len(inputLine) - 1
	if inLen not in allowed:
		if len(allowed) == 1:
			print "operation takes exactly " + str(allowed[0]) + " argument(s), " + str(len(inputLine)-1) + " given."
		else:
			print "operation takes " + " or ".join([str(x) for x in allowed]) + " argument(s), " + str(len(inputLine)-1) + " given."
		print "h for help menu.\n"
		return False
	return True

# TO CHECK INDEXES GIVEN IN INPUT CONDITIONS LIKE
# STARTING INDEX NOT OUT OF FILE
# START INDEX LESS THAN END AND NOT NEGATIVE
def indexCheck(text, start, end = sys.maxint):
	if start > len(text):
		print "Start Index out of file size."
		return False
	if start > end:
		print "Start line no. should be less than end line no."
		return False
	if start <= 0 or end <= 0:
		print "Line numbers should be positive"
		return False
	return True