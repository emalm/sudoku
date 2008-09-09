// plist.cc
// Implementation of PList class

#include "plist.h"
#include <iostream>

using namespace std;

PList::PList()
	: state(0) {
		
}

int PList::count() {
	int sc = state;
	int count = 0;
	
	while( sc > 0 ) {
		count += ( sc & 0x1 );
		sc >>= 1;
	}
	
	return count;
}

bool PList::solved() {
	if ( this->count() == 1 ) {
		return true;
	} else {
		return false;
	}
}

bool PList::member( int value ) {
	if ( state & ( 1 << value ) ) {
		return true;
	} else {
		return false;
	}
}

int PList::solution() {
	if ( this->solved() ) {
		int sc = state;
		int count  = 0;
		
		while ( ( sc & 0x1 ) == 0 ) {
			count++;
			sc >>= 1;
		}
		
		return count;
	} else {
		return not_solved;
	}
}

PList& PList::include( int value ) {
	
	state |= ( 1 << value );
	
	return *this;
}

PList& PList::include_all() {
	state = 0;
	for( int j = 1; j <= 9; j++ ) {
		state += 1 << j;
	}
	
	return *this;
}

PList& PList::exclude( int value ) {
	
	state &= ~( 1 << value );
	
	return *this;
}

PList& PList::exclude_all() {
	state = 0;
}

PList& PList::combine( const PList & p ) {
	state |= p.state;
	
	return *this;
}

