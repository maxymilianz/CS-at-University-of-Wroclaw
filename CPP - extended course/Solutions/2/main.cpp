
#include "rational.h"
#include "matrix.h"

using namespace std;

int main( int argc, char* argv [ ] )
{
   rational r1( 1, 2 );
   rational r2( -2, 7 ); 
   rational r3( 1, 3 );
   rational r4( 2, 8 );
   
   rational r5( -1, 3 );
   rational r6( 2, 5 ); 
   rational r7( 2, 7 );
   rational r8( -1, 7 );

   matrix m1 = { { r1, r2 }, { r3, r4 } };
   cout << m1 << "\n";

   matrix m2 = { { r5, r6 }, { r7, r8 } }; 
   cout << m2 << "\n";

   matrix m3 = m1 * m2;
   cout << m3 << "\n";
   
   matrix m4 = m1.inverse();
   cout << m4 << "\n";

   m4 = (m1 * m2) * m3;
   matrix m5 = m1 * (m2 * m3);
   cout << m4 - m5 << "\n";
   
   m4 = m1 * (m2 + m3);
   m5 = m1 * m2 + m1 * m3;
   cout << m4 - m5 << "\n";
   
   m4 = (m1 + m2) * m3;
   m5 = m1 * m3 + m2 * m3;
   cout << m4 - m5 << "\n";
   
   m4 = m1 * (m2 * r1);
   m5 = (m1 * m2) * r1;
   cout << m4 - m5 << "\n";
   
   r5 = m1.determinant() * m2.determinant();
   r6 = (m1 * m2).determinant();
   cout << r5 - r6 << "\n\n";
   
   m4 = m1 * m1.inverse();
   cout << m4 << "\n";
   m4 = m1.inverse() * m1;
   cout << m4 << "\n";
   
   matrix algebra = { {0, 0}, {1, 0} };
   cout << algebra * algebra;
}

