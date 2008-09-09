#!/usr/bin/env python

from sets import Set

class SudokuCell:
	"Stores single sudoku cell"
	def __init__(self, marks = range(1,10), dirty = False):
		self.marks = Set(marks)
		self.dirty = dirty
		self.topcontainers = {}
		
	def __repr__(self):
		return "SudokuCell(" + repr(list(self.marks)) + ", " \
							 + repr(self.dirty) + ")"

	def prettyprint(self):
		"More readable cell representation, as '(*marks)'"
		pprint = "("
		if self.dirty:
			pprint += "*"
			
		for digit in list(self.marks):
			pprint += str(digit)
			
		pprint += ")"
		return pprint

	def setmarks(self, marks):
		"Redefine cell marks from a list"
		self.marks = Set(marks)

class SudokuCellContainer:
	"Generic container class for SudokuCells"
	def __init__(self, parent, cells = []):
		self.cells = cells
		self.parent = parent
		
class SudokuCellTopContainer(SudokuCellContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellContainer.__init__(self, parent, cells)
		self.cellpartitions = [self.cells[:]]
		self.dirty = False
		self.index = index
		self.substructures = {}
		
	def prettyprint(self):
		pprint = "[ "
		for block in self.cellpartitions:
			pprint += "["
			for cell in block:
				pprint += cell.prettyprint()
			pprint += "] "
			
		pprint += "]"
		return pprint
		
	def partitioncellswithsubblocks(self):
		self.includeexcludesubcontainers()
		self.adjustcellsfromsubcontainers()
		self.partitionallcells()
		self.updatesubstructuresfromcells()
		self.includeexcludesubcontainers()
		self.dirtystructuresfromdirtysubcontainers()
		
	
	def partitionallcells(self):
		newpartitions = []

		while self.cellpartitions:
			nextlist = self.cellpartitions.pop(0)
			self.partitioncelllist(nextlist, newpartitions)

		self.cellpartitions = newpartitions

		return

	def includeexcludesubcontainers(self):
		for key in self.substructures.keys():
			subconset = self.substructures[key]
			length = len(subconset)
			for i in range(length):
				subcontainer = subconset[i]
				othersubcons = subconset[:i] + subconset[i+1:]
				
				# exclude marks in other subcons if included in
				for other in othersubcons:
					# this subcon has new info for other subcon
					if subcontainer.included.difference(other.excluded):
						other.excluded |= subcontainer.included
						other.dirty = True
						print "Added subcontainer " + other.prettyprint() + " to dirty list"
						
				allexcluded = Set(range(1,10))
				for other in othersubcons:
					allexcluded &= other.excluded
					
				if allexcluded.difference(subcontainer.included):
					subcontainer.included |= allexcluded
					subcontainer.dirty = True
					print "Added subcontainer " + subcontainer.prettyprint() + " to dirty list"
		
	def adjustcellsfromsubcontainers(self):
		dirtysubcons = [subcon for key in self.substructures.keys() 
							   for subcon in self.substructures[key] 
							   if subcon.dirty]
		for subcon in dirtysubcons:
			for cell in subcon.cells:
				if cell.marks.intersection(subcon.excluded):
					cell.marks -= subcon.excluded
					cell.dirty = True
					
	def dirtystructuresfromdirtysubcontainers(self):
		dirtysubcons = [subcon for key in self.substructures.keys() 
							   for subcon in self.substructures[key] 
							   if subcon.dirty]
		for subcon in dirtysubcons:
			for key in subcon.topcontainers.keys():
				subcon.topcontainers[key].dirty = True
				
			subcon.dirty = False
			
	def updatesubstructuresfromcells(self):
		allsubcons = [subcon for key in self.substructures.keys() 
							 for subcon in self.substructures[key]]
		for subcon in allsubcons:
			newexcludes = Set(range(1,10))
			newincludes = Set([])
			for cell in subcon.cells:
				if len(cell.marks) == 1:
					newincludes |= cell.marks
				newexcludes -= cell.marks
				
			# update subcon's excluded lists
			if newexcludes.difference(subcon.excluded):
				subcon.excluded |= newexcludes
				subcon.dirty = True
				print "Added subcontainer " + subcon.prettyprint() + " to dirty list"

			# update subcon's included list
			if newincludes.difference(subcon.included):
				subcon.included |= newincludes
				subcon.dirty = True
				print "Added subcontainer " + subcon.prettyprint() + " to dirty list"
				
			
		
	def partitioncelllist(self, celllist, partitions):
		# if celllist is length 1 or less, no need to partition further
		if len(celllist) <= 1:
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
			# put this block back in the list, exit
			partitions.append(celllist)
			return

		# print "Subblock:\n\t", subblock, subblockmarks

		# put found subblock into partition list
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
		SudokuCellTopContainer.__init__(self, parent, cells, index)
		self.substructures["subrows"] = []
		
	def partitionallcells(self):
		print "Processing Row", self.index
		SudokuCellTopContainer.partitionallcells(self)
		print "Subrows:", [row.prettyprint() for row in self.substructures["subrows"]]
		
class SudokuCellColumn(SudokuCellTopContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellTopContainer.__init__(self, parent, cells, index)
		self.substructures["subcolumns"] = []
	
	def partitionallcells(self):
		print "Processing Column", self.index
		SudokuCellTopContainer.partitionallcells(self)
		print "Subcolumns:", [col.prettyprint() for col in self.substructures["subcolumns"]]

class SudokuCellSquare(SudokuCellTopContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellTopContainer.__init__(self, parent, cells, index)
		self.substructures["subrows"] = []
		self.substructures["subcolumns"] = []

	def partitionallcells(self):
		print "Processing Square", self.index
		SudokuCellTopContainer.partitionallcells(self)
		print "Subrows:", [row.prettyprint() for row in self.substructures["subrows"]]
		print "Subcolumns:", [col.prettyprint() for col in self.substructures["subcolumns"]]

class SudokuCellSubContainer(SudokuCellContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellContainer.__init__(self, parent, cells)
		self.topcontainers = {}
		self.included = Set([])
		self.excluded = Set([])
		self.index = index
		self.dirty = False
		
	def prettyprint(self):
		pprint = "[" + str(self.index)
		
		if self.dirty:
			pprint += "*"
			
		pprint += ": "
			
		for cell in self.cells:
			pprint += cell.prettyprint()
			
		pprint += " i" + "".join(map(str,list(self.included)))
		pprint += " e" + "".join(map(str,list(self.excluded)))
		pprint += " ]"
		return pprint

class SudokuCellSubrow(SudokuCellSubContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellSubContainer.__init__(self, parent, cells, index)
		
class SudokuCellSubcolumn(SudokuCellSubContainer):
	def __init__(self, parent, cells = [], index = 0):
		SudokuCellSubContainer.__init__(self, parent, cells, index)


class SudokuBoard:
	def __init__(self):
		self.cells = []
		
		# create cells on board
		for row in range(9):
			self.cells.append([])
			for col in range(9):
				self.cells[row].append(SudokuCell())
				
		# set up row objects
		self.rowobjs = []
		for row in self.cells:
			rowobj = SudokuCellRow(self, row[:], self.cells.index(row))
			self.rowobjs.append(rowobj)
			for cell in row:
				cell.topcontainers["row"] = rowobj
		
		# set up column objects
		self.columnobjs = []
		
		for index in range(9):
			column = []
			for row in self.cells:
				column.append(row[index])
			
			columnobj = SudokuCellColumn(self, column, index)
			self.columnobjs.append(columnobj)
			for cell in column:
				cell.topcontainers["column"] = columnobj
		
		# set up square objects
		self.squareobjs = []
		
		for index in range(9):
			square = []
			rowindex = index / 3
			colindex = index % 3

			for i in range(3):
				for j in range(3):
					cell = self.cells[3 * rowindex + i][3 * colindex + j]
					square.append(cell)
					
			squareobj = SudokuCellSquare(self, square, index)
			self.squareobjs.append(squareobj)
			for cell in square:
				cell.topcontainers["square"] = squareobj
			
		self.allstructureobjs = self.rowobjs + self.columnobjs + self.squareobjs
		
		# set up subrow objects
		
		self.subrowobjs = []
		
		for index in range(27):
			subrow = []
			rowindex = index / 3
			colindex = index % 3
			
			for i in range(3):
				cell = self.cells[rowindex][3 * colindex + i]
				subrow.append(cell)
				
			subrowobj = SudokuCellSubrow(self, subrow, index);
			self.subrowobjs.append(subrowobj)
			
			self.rowobjs[rowindex].substructures["subrows"].append(subrowobj)
			subrowobj.topcontainers["row"] = self.rowobjs[rowindex]
			
			squareindex = (rowindex / 3) * 3 + colindex
			self.squareobjs[squareindex].substructures["subrows"].append(subrowobj)
			subrowobj.topcontainers["square"] = self.squareobjs[squareindex]
		
		# set up subcolumn objects
					
		self.subcolumnobjs = []
		
		for index in range(27):
			subcolumn = []
			rowindex = index / 9
			colindex = index % 9
			
			for i in range(3):
				cell = self.cells[3 * rowindex + i][colindex]
				subcolumn.append(cell)
				
			subcolumnobj = SudokuCellSubcolumn(self, subcolumn, index);
			self.subcolumnobjs.append(subcolumnobj)
			
			self.columnobjs[colindex].substructures["subcolumns"].append(subcolumnobj)
			subcolumnobj.topcontainers["column"] = self.columnobjs[colindex]
			
			squareindex = rowindex * 3 + colindex / 3
			self.squareobjs[squareindex].substructures["subcolumns"].append(subcolumnobj)
			subcolumnobj.topcontainers["square"] = self.squareobjs[squareindex]
		
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
	
	def partitiontopstructures(self):
		dirtycells = [cell for r in self.cells for cell in r if cell.dirty]
		dirtystructures = []
		self.dirtycellstodirtystructures(dirtycells)
		self.adddirtystructures(dirtystructures)

		while dirtystructures:
			structure = dirtystructures.pop(0)

			structure.partitioncellswithsubblocks()

			print structure.prettyprint()

			newdirties = [cell for cell in structure.cells if cell.dirty]

			self.dirtycellstodirtystructures(newdirties)
			
			# just processed this structure, so don't re-add to dirty list
			structure.dirty = False
			
			self.adddirtystructures(dirtystructures)
			print self

	def dirtycellstodirtystructures(self, dirtycells):
		while dirtycells:
			cell = dirtycells.pop(0)
			
			for key in cell.topcontainers.keys():
				cell.topcontainers[key].dirty = True
				
			cell.dirty = False
				
	def adddirtystructures(self, dirtystructures):
		for topstruct in self.allstructureobjs:
			if topstruct.dirty and topstruct not in dirtystructures:
				dirtystructures.append(topstruct)
				topstruct.dirty = False
				print "Added top structure " + \
				      str(self.allstructureobjs.index(topstruct)) + \
					  " to dirty list"
	
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
