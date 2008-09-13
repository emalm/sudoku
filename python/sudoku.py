#!/usr/bin/env python

from sets import Set
from sudokucells import *
import sys
import sudokumarksets
		
def main(argv = None):	
	if argv is None:
		argv = sys.argv
		

	board = SudokuBoard()
	board.changemarks(makemarksdict(sudokumarksets.hard_eastermonster))
	
	boardchanged = True
	boardfirstrun = True
	
	while boardchanged:
		print "Board changed!"

		print board.prettyprint()

		oldmarks = board.marks()

		if boardfirstrun:
			boardfirstrun = False
		else:
			print "Running row block analysis."
			board.partitionrowsbydigits()
			
			print board.prettyprint()
			
		
		board.partitiontopstructures()
		
		if board.solved():
			print "Puzzle solved!"
			print board
			break
		
		newmarks = board.marks()
		
		boardchanged = (oldmarks != newmarks)
	
	return 0
	
if __name__ == "__main__":
	sys.exit(main())
