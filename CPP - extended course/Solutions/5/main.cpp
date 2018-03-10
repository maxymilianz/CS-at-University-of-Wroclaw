
#include "tree.h"


int main( int argc, char* argv [ ] )
{
   /*tree t1( std::string( "a" ));
   tree t2( std::string( "b" )); 
   tree t3 = tree( std::string( "f" ), { t1, t2 } ); 

   std::vector< tree > arguments = { t1, t2, t3 };
   std::cout << tree( "F", std::move( arguments )) << "\n";

   t2 = t3;
   t2 = std::move(t3);*/
   
   const tree t1("t1");
   tree t2(t1);
   tree t3 = t1;
   tree &t4 = t2;
   
   cout << t2 << endl;
   cout << t3 << endl;
   cout << t4 << endl;
   
   cout << t1.functor() << endl;
   
   const tree t5("t5", {t1, t2, t3, t4});
   tree t6 = t5[0];
   
   cout << t6 << endl;
   cout << t5.nrsubtrees() << endl;
   
   tree t7("t7", {t1, t2, t3, t4});
   tree t8 = t7[0];
   
   cout << t8 << endl;
   cout << t7.nrsubtrees() << endl;
   
   tree t9 = subst(t1, "t1", t5);
   cout << t9 << endl;
}



