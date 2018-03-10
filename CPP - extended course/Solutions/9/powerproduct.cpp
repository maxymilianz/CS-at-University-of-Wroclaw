
#include "powerproduct.h"
#include <algorithm>


std::ostream& operator << ( std::ostream& out, const powvar & p )
{
   if( p.n == 0 )
   {
      out << "1"; // Should not happen, but we still have to print something.
      return out;
   }

   out << p.v;
   if( p.n == 1 )
      return out;

   if( p.n > 0 )
      out << "^" << p.n;
   else
      out << "^{" << p.n << "}";
   return out;
}


std::ostream& operator << ( std::ostream& out, const powerproduct& c )
{
   if( c. isunit( ))
   {
      out << "1";
      return out;
   }

   for( auto p = c. repr. begin( ); p != c. repr. end( ); ++ p )
   {
      if( p != c. repr. begin( ))
         out << ".";
      out << *p;
   }

   return out;
}


int powerproduct::power( ) const
{
   int p = 0;
   for( auto pv : repr )
      p += pv. n;
   return p;
}

powerproduct operator * ( powerproduct c1, const powerproduct& c2 ) {
    powerproduct temp = c1;

    for (size_t i = 0; i < c2.repr.size(); i++)
        temp.repr.insert(temp.repr.end(), c2[i]);

    temp.normalize();
    return temp;
}
