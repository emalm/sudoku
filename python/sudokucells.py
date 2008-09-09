#!/usr/bin/env python

from sets import Set

class SudokuCell:
	def __init__(self, marks = range(1,10), dirty = False):
		self.marks = Set(marks)
		self.dirty = dirty
		
	def __str__(self):
		return "SudokuCell(" + repr(list(self.marks)) + ")"

	def __repr__(self):
		return "SudokuCell(" + repr(list(self.marks)) + ", " \
							 + repr(self.dirty) + ")"
							
	def setmarks(self, marks):
		self.marks = Set(marks)

class SudokuCellContainer:
	def __init__(self, parent, cells = []):
		self.cells = cells
		self.parent = parent
		
class SudokuCellTopContainer(SudokuCellContainer):
	def __init__(self, parent, cells = []):
		self.cells = cells
		self.cellpartitions = [self.cells[:]]
		self.parent = parent
		
	
	def partitionallcells(self):
		newpartitions = []
		
		while self.cellpartitions:
			nextlist = self.cellpartitions.pop(0)
			self.partitioncelllist(nextlist, newpartitions)
			
		self.cellpartitions = newpartitions
		
		return
		
		
	def partitioncelllist(self, celllist, partitions):
		if len(celllist) <= 2:
			partitions.append(celllist)
			return
			
		# generate all proper subsets of cell list
		cellsubsets = propersubsets(celllist)

		# sort by subset length
		lencmp = lambda a,b: cmp(len(a), len(b))
		cellsubsets.sort(cmp=lencmp)

		# storage for block + marks, if we find one
		subblock = None
		subblockmarks = None

		# look through subsets for a subblock (number of marks = number of cells)
		# since cellsubsets sorted by length, will find a minimal one
		for sset in cellsubsets:
			ssetmarks = Set()
			for cell in sset:
				ssetmarks = ssetmarks.union(cell.marks)

			# if we find one, save it off, break the loop
			if (len(ssetmarks) == len(sset)):
				subblock = sset
				subblockmarks = ssetmarks
				break
		else:
			# no proper subblocks found
			partitions.append(celllist)
			return

		# print "Subblock:\n\t", subblock, subblockmarks

		partitions.append(subblock)
		
		# collect cells not in this subblock
		# should never be empty
		outercells = [cell for cell in celllist if cell not in subblock]

		# print "Cells outside block:\n\t", outercells

		if outercells:
			# remove marks in block from the marks of the other cells
			# mark the cell as dirty if we changed it
			for cell in outercells:
				if cell.marks.intersection(subblockmarks):
					cell.marks = cell.marks.difference(subblockmarks)
					cell.dirty = True

			# print "Cells outside block after subtraction:\n\t", outercells

			# check for new subblocks in the outer cells
			self.partitioncelllist(outercells, partitions)

		# print "Cells after partition:\n\t", cells
		return
		
	
	
class SudokuCellRow(SudokuCellTopContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellTopContainer.__init__(self, parent, cells)
		self.rowindex = index
	
class SudokuCellColumn(SudokuCellTopContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellTopContainer.__init__(self, parent, cells)
		self.columnindex = index
	
class SudokuCellSquare(SudokuCellTopContainer):
	def __init__(self, parent, cells = [], index = (0,0)):
		SudokuCellTopContainer.__init__(self, parent, cells)
		self.squareindex = index


class SudokuCellSubContainer(SudokuCellContainer):
	def __init__(self, parent):
		self.cells = []
		self.parent = parent
		self.included = []
		self.excluded = []

class SudokuBoard:
	def __init__(self):
		self.cells = []
		
		# create cells on board
		for row in range(9):
			self.cells.append([])
			for col in range(9):
				self.cells[row].append(SudokuCell())
				
		# set up row structures
		self.rows = self.cells[:]
		self.rowobjs = []
		for row in self.cells:
			self.rowobjs.append(SudokuCellRow(self, row, self.cells.index(row)))
		
		self.columns = []
		self.columnobjs = []
		
		for index in range(9):
			column = []
			for row in self.cells:
				column.append(row[index])
			
			self.columns.append(column)
			self.columnobjs.append(SudokuCellColumn(self, column, index))
		
		self.squares = []
		self.squareobjs = []
		
		for index in range(9):
			square = []
			rowindex = index / 3
			colindex = index % 3

			for i in range(3):
				for j in range(3):
					cell = self.cells[3 * rowindex + i][3 * colindex + j]
					square.append(cell)

			self.squares.append(square)
			self.squareobjs.append(SudokuCellSquare(self, square, index))
			
		self.allstructures = self.rows + self.columns + self.squares
		self.allstructureobjs = self.rowobjs + self.columnobjs + self.squareobjs
		
		
					
	def __str__(self):		
		boardstring = ""
		for row in self.cells:
			if (self.cells.index(row) % 3) == 0:
				boardstring += "+" + "---+" * 3 + "\n"
				
			for cell in row:
				if (row.index(cell) % 3) == 0:
					boardstring += "|"
				if len(cell.marks) == 1:
					boardstring += str(list(cell.marks)[0])
				else:
					boardstring += "."
			boardstring += "|\n"
		
		boardstring += "+" + "---+" * 3 + "\n"
		return boardstring
		
	def changemarks(self, marksdict, dirty = True):
		for (ri, ci) in marksdict.keys():
			self.cells[ri][ci].marks = Set(marksdict[(ri, ci)])
			if dirty:
				self.cells[ri][ci].dirty = True
	
def makemarksdict(markstring):
	marklist = list(markstring)
	markdict = {}
	
	index = 0;
	digitstring = [str(digit) for digit in range(1,10)]
	
	for char in marklist:
		if char == "-" or char == ".":
			index += 1
		elif char in digitstring:
			markdict[(index / 9, index % 9)] = [int(char)]
			index += 1
			
	return markdict
	
def propersubsets(l):
	"Generate all proper subsets of list l."
	# allsubsets returns empty subset as first element
	# and full subset as last element
	# so we shear those ones off
	return allsubsets(l)[1:-1]
	
	
def allsubsets(l):
	"Generate all subsets of list l."
	# base case: no elements in list l
	if len(l) == 0:
		return [[]]

	# pick off last element
	last = l[-1]
	rest = l[:-1]
	
	# generate subsets for all but last element
	restsubsets = allsubsets(rest)
	
	# add those subsets, then same subsets with last element added to each
	subsets = restsubsets
	subsets.extend([sset + [last] for sset in restsubsets])
	
	return subsets
	
	
def partitioncellmarks(cells):
	"Breaks marks for a list of cells into subblocks. Changes cells in place."
	
	# generate all proper subsets of cell list
	cellsubsets = propersubsets(cells)

	# sort by subset length
	lencmp = lambda a,b: cmp(len(a), len(b))
	cellsubsets.sort(cmp=lencmp)
	
	# storage for block + marks, if we find one
	subblock = None
	subblockmarks = None
	
	# look through subsets for a subblock (number of marks = number of cells)
	# since cellsubsets sorted by length, will find a minimal one
	for sset in cellsubsets:
		ssetmarks = Set()
		for cell in sset:
			ssetmarks = ssetmarks.union(cell.marks)
			
		# if we find one, save it off, break the loop
		if (len(ssetmarks) == len(sset)):
			subblock = sset
			subblockmarks = ssetmarks
			break
	else:
		# no proper subblocks found
		return
	
	# print "Subblock:\n\t", subblock, subblockmarks
		
	# collect cells not in this subblock
	# should never be empty
	outercells = [cell for cell in cells if cell not in subblock]

	# print "Cells outside block:\n\t", outercells
	
	if outercells:
		# remove marks in block from the marks of the other cells
		# mark the cell as dirty if we changed it
		for cell in outercells:
			if cell.marks.intersection(subblockmarks):
				cell.marks = cell.marks.difference(subblockmarks)
				cell.dirty = True

		# print "Cells outside block after subtraction:\n\t", outercells
		
		# check for new subblocks in the outer cells
		partitioncellmarks(outercells)
	
	# print "Cells after partition:\n\t", cells
	return
	
def partitionboardstructures(board):
	dirtycells = [cell for r in board.cells for cell in r if cell.dirty]
	dirtystructures = []
	adddirtystructures(board, dirtycells, dirtystructures)
	
	while dirtystructures:
		structure = dirtystructures.pop(0)
		#print "before:", structure
		
		structureobject = SudokuCellTopContainer(board, structure)
		structureobject.partitionallcells()
		
		print structureobject.cellpartitions
		
		# partitioncellmarks(structure)
		#print "after: ", structure
		newdirties = [cell for cell in structure if cell.dirty]
		#print "new dirties:", newdirties, "\n"
		adddirtystructures(board, newdirties, dirtystructures)
		print board
		
	
def adddirtystructures(board, dirtycells, dirtystructures):
	while dirtycells:
		cell = dirtycells.pop(0)

		cellstructures = [s for s in board.allstructures if cell in s]
		for struct in cellstructures:
			if struct not in dirtystructures:
				dirtystructures.append(struct)
				
		cell.dirty = False
