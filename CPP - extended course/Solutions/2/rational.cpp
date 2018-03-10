
#include "rational.h"
#include <cstdlib>

using namespace std;

// Complete these methods:

#if 1		// was 0

int rational::gcd( int n1, int n2 ) {
	int n3;
	
	if (n1 < n2) {
		n3 = n1;
		n1 = n2;
		n2 = n3;
	}
	
	while (n2 != 0) {
		n3 = n1 % n2;
		n1 = n2;
		n2 = n3;
	}
	
	return n1;
}

void rational::normalize( ) {
	if (!denum) {
		cout << "Dividing by 0\n";
		exit(1);
	}
	
	int cd = gcd(num, denum);
	num /= cd;
	denum /= cd;
	
	if (denum < 0)
		num *= -1, denum *= -1;
}

rational operator - ( rational r ) {
	rational r2;
	r2.num = -r.num;
	r2.denum = r.denum;
	return r2;
}

rational operator + ( const rational& r1, const rational& r2 ) {
	rational r3;
	
	r3.num = r1.num * r2.denum + r2.num * r1.denum;
	r3.denum = r1.denum * r2.denum;
	r3.normalize();
	
	return r3;
}

rational operator - ( const rational& r1, const rational& r2 ) {
	rational r3;
	
	r3.num = r1.num * r2.denum - r2.num * r1.denum;
	r3.denum = r1.denum * r2.denum;
	r3.normalize();
	
	return r3;
}

rational operator * ( const rational& r1, const rational& r2 ) {
	rational r3;
	
	r3.num = r1.num * r2.num;
	r3.denum = r1.denum * r2.denum;
	r3.normalize();
	
	return r3;
}

rational operator / ( const rational& r1, const rational& r2 ) {
	rational r3;
	
	r3.num = r1.num * r2.denum;
	r3.denum = r1.denum * r2.num;
	r3.normalize();
	
	return r3;
}

bool operator == ( const rational& r1, const rational& r2 ) {
	if (r1.num * r2.denum == r1.denum * r2.num)
		return 1;
	
	return 0;
}
bool operator != ( const rational& r1, const rational& r2 ) {
	if (r1.num * r2.denum == r1.denum * r2.num)
		return 0;
	
	return 1;
}

std::ostream& operator << ( std::ostream& stream, const rational& r ) {
	stream << r.num << "/" << r.denum;
	return stream;
}

#endif

