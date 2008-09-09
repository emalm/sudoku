CPP = g++
OFLAG = -o
CFLAG = -c

test: test.o plist.o
	$(CPP) $(OFLAG) test test.o plist.o

test.o: test.cc plist.h
		$(CPP) $(CFLAG) test.cc

plist.o: plist.cc plist.h
	$(CPP) $(CFLAG) plist.cc



