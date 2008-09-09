#!/usr/bin/env python

from sets import Set
from sudokucells import *
import sys

				
	
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

	markstring57 = "---2---3-/----9--74/--4--79--/\
				    ---45-2--/-7---6-85/--8------/\
				    ---164---/-4-9--5-8/1--87--4-/"
				
	markstring58 = "95----2--/847------/-3-----6-/\
					---28-5--/4--1-----/---743--8/\
					--3--7--6/-2-83---4/----2-3-9/"

	markstring101 = "-7------9/6-85-3-4-/3--6--7-8/\
					 --6---5--/---41---3/5--7-----/\
					 ------896/-61--4-72/-----8---/"

	markstring151 = "--------4/6-4----57/----8--9-/\
					 --6--37--/---2-----/--7-1--8-/\
					 -1-----29/----7----/-5869----/"

	markstring152 = "--4-71---/687-----3/---3-----/\
					 -------49/2--7--1--/---65-3--/\
					 ---58-9-2/--9--6---/7-6------/"

	markstring153 = "-1----7--/-----2-3-/7386----5/\
					 --5-97--8/--6------/-7-3--9--/\
					 ----1---4/5---8---1/-----6-2-/"

	markstring154 = "-3-7-286-/1----59--/---------/\
					 -8---4---/-6----5-1/2---5-7-9/\
					 --8------/-7-43----/--39----8/"

	markstring155 = "------87-/78-94----/----5--2-/\
					 ---3-----/-56------/8-9--2-1-/\
					 ----9--8-/------4-7/--17-6---/"

	markstring156 = "--45---3-/9---6----/-87--4---/\
					 ----7-9--/-4-6---1-/3--------/\
					 ----5--63/-218-6--5/----9----/"

	markstring157 = "-4-3--6--/------29-/--97-----/\
					 --4-----6/8---1-4--/---5--3--/\
					 ---6----8/7-8---1--/---1-5-47/"

	markstring158 = "-2-7--95-/-3-5-----/------4-6/\
					 -5-------/-----87--/1-----8--/\
					 9--8---1-/4--35--7-/--146-3--/"

	markstring159 = "-4-------/7--6-----/8-9-2-3-4/\
					 5---8---1/-----3---/--6-4-7--/\
					 -821--6--/------4--/--3--5---/"

	markstring160 = "3---75---/1---9--37/2--4-----/\
					 6----4-5-/--4-21--3/-7--6----/\
					 --------4/--62---79/48----3-6/"

	board = SudokuBoard()
	board.changemarks(makemarksdict(markstring160))
	
	print board
		
	board.partitionboardstructures()

	print board
	
	for row in board.cells:
		print "Row " + str(board.cells.index(row) + 1)
		for cell in row:
			l = list(cell.marks)
			l.sort()
			print l
			
		print ""
			
	
	return 0
	
if __name__ == "__main__":
	sys.exit(main())
