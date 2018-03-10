
#include <fstream>
#include <iostream>
#include <random>

#include "listtest.h"
#include "vectortest.h"
#include "timer.h"


int main( int argc, char* argv [] )
{
	std::vector<std::string> v = vectortest::randomstrings(20000, 50);
	std::vector<std::string> v2 = std::vector<std::string>(v);
	std::vector<std::string> v3 = std::vector<std::string>(v);
	
	std::list<std::string> l = listtest::vecToList(v);
	std::list<std::string> l2 = std::list<std::string>(l);
	std::list<std::string> l3 = std::list<std::string>(l);
	
	// each one faster with optimization (-O3 -flto)
	{
		timer t("vector assign sort", std::cout);		// O(n^2)
		vectortest::sort_assign(v);
	}

	{
		timer t("vector move sort", std::cout);		// O(n^2) fast
		vectortest::sort_move(v2);
	}
	
	{
		timer t("vector std sort", std::cout);		// O(n*log(n))
		vectortest::sort_std(v3);
	}
	
	// here as well
	{
		timer t("list assign sort", std::cout);		// O(n^2)
		listtest::sort_assign(l);
	}

	{
		timer t("list move sort", std::cout);		// O(n^2) fast
		listtest::sort_move(l2);
	}
	
	{
		timer t("list std sort", std::cout);		// O(n*log(n))
		listtest::sort_std(l3);
	}

   /*std::vector< std::string > vect;

   std::cout << vect << "\n";

   // Or use timer:

   auto t1 = std::chrono::high_resolution_clock::now( ); 
   vectortest::sort_move( vect );
   auto t2 = std::chrono::high_resolution_clock::now( );

   std::chrono::duration< double > d = ( t2 - t1 );
   std::cout << vect << "\n";

   std::cout << "sorting took " << d. count( ) << " seconds\n";*/
   return 0;
}


