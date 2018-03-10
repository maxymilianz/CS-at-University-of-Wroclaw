#include "rational.h"
#include <cstdlib>


// Complete these methods:

#if 1

int rational::gcd( int n1, int n2 )
{   int k;
    if (n1<n2) {
        k = n2; n2 = n1; n1 = k;
    }
    while (n2!=0) {
        k = n1 % n2;
        n1 = n2;
        n2 = k;
    }
    return n1;
}

void rational::normalize(){
    if (denum == 0)
		exit(1);
    else {
        int cd = rational::gcd(num,denum);
        num /= cd;
        denum /= cd;
    }
    if (denum < 0){
        num = (-1)*num;
        denum = (-1)*denum;
    }
    
}
rational operator - ( rational r ){
     r.num = (-1)*r.num;
    return r;
}

rational operator + ( const rational& r1, const rational& r2 ){
    return rational(r1.num*r2.denum + r1.denum*r2.num, r1.denum*r2.denum);
}

rational operator - ( const rational& r1, const rational& r2 ){
    rational r3 = (-1)*r2;
    return r1 + r3;
}
rational operator * ( const rational& r1, const rational& r2 ){
    return rational(r1.num*r2.num, r1.denum*r2.denum);
}
rational operator / ( const rational& r1, const rational& r2 ){
    return rational(r1.num*r2.denum, r2.num*r1.denum);
}
bool operator == ( const rational& r1, const rational& r2 ){
    rational x = r1 + (-1)*r2;
    if (x.num == 0)
        return true;
    return false;
}
bool operator != ( const rational& r1, const rational& r2 ){
    rational x = r1 + (-1)*r2;
    if (x.num == 0)
        return false;
    return true;
}
std::ostream& operator << ( std::ostream& stream, const rational& r ){
    stream << r.num << "/" << r.denum;
    return stream;
}

#endif
