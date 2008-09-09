// plist.h
// Header file for PList class

#ifndef PLIST_H
#define PLIST_H

class PList {
public:
	PList();
	
	int count();
	bool member( int );
	bool solved();
	int solution();
	
	static const int not_solved = -1;

	PList& include( int );
	PList& include_all();
	PList& exclude( int );
	PList& exclude_all();

	PList& combine( const PList& );
	
private:
	int state;
};

#endif // PLIST_H