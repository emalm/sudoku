#!/usr/bin/env python

from sets import Set
from sudokucells import *
import sys
import sudokumarksets

				
	
def oldtestcode():
	print allsubsets([1, 2, 3])
	print propersubsets([1, 2, 3])

	x = SudokuCell([2,3,5])
	y = SudokuCell([4,5])
	z = SudokuCell([6,4])
	w = SudokuCell([6,4])

	print [x, y, z, w]

	partitioncellmarks([x, y, z, w])
	
	print [x, y, z, w]
	
	cells = [SudokuCell([1,2]), SudokuCell([2,3]), SudokuCell([3,4]), SudokuCell([4,5]), SudokuCell([5,6]), SudokuCell([6,7]), SudokuCell([7,8]), SudokuCell([8,9]), SudokuCell([9])]
	
	print cells
	partitioncellmarks(cells)
	print cells
	
	for i in range(9):
		print board.rows[i]
		partitioncellmarks(cells)
		
		print board.columns[i]
		print board.squares[i]
		
def main(argv = None):	
	if argv is None:
		argv = sys.argv


	board = SudokuBoard()
	board.changemarks(makemarksdict(sudokumarksets.ws_ult_99))
	
	print board
	
	oldmarks = board.marks()
		
	board.partitiontopstructures()
	
	newmarks = board.marks()
	
	print board
	
	if oldmarks != newmarks:
		print "Board changed!"
		
	board.partitionrowsbydigits()
	
	return 0
	
if __name__ == "__main__":
	sys.exit(main())
