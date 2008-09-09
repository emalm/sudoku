#include <iostream>
#include "plist.h"

using namespace std;

int main() {
	PList p, q, r;
	
	p.include_all();
	q.include_all();
	
	cout << p.count() << endl;
	
	p.exclude( 9 ).exclude( 8 );
	
	q.exclude( 1 ).exclude( 2 ).exclude( 3 ).exclude( 9 );

	cout << p.count() << endl;
	cout << q.count() << endl;
	
	p.exclude_all().include( 4 );
	
	if ( p.solved() ) {
		cout << "p is solved: " << p.solution() << endl;
	} else {
		cout << "p is not solved: " << p.solution() << endl;
	}
	
	r.combine( p ).combine( q );
	
	cout << r.count() << endl;
	
	return 0;
}