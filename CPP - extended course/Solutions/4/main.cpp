
#include "string.h"
#include <iostream>

#include <stdexcept>
#include <vector>

// From the lecture. Not needed for the task:

/*void fail_often( )
{
   srand( time( NULL ));
   if( rand( ) & 1 )
      throw std::runtime_error( "i failed" );
}

void f( )
{
   string s = "this is a string";
   
   std::vector< string > vect = { "these", "are", "also", "string" };
   string more [] = {"these", "are", "even", "more", "string" };

   // fail_often( );
}*/

int main( int argc, char* argv [ ] )
{
   // Add more tests by yourself. Untested code = unwritten code. 

   string s;
   string s2 = "hello";

   s = s2;  // Assignment, not initialization.
   s = s;

   // std::cout << "s = " << s << "\n";
   
   // excercise 5: ==============================================
   
	s = "this is a string";
	std::cout << s << "\n";
	for( char& c : s )
		c = toupper(c);
	std::cout << s << "\n";
	
	// my tests: ================================================
	
	std::cout << s[8] << '\n';
	std::cout << "Some test string."[5] << '\n';
	
	s += 's';
	std::cout << s << '\n';
	s += " Another test string";
	std::cout << s << '\n';
	
	string s3 = s + s2;
	std::cout << s3 << '\n';
	s3 = s2 + "Just a part of a string ";
	std::cout << s3 << '\n';
	
	std::cout << ("foo" == "bar") << '\n';
	std::cout << ("foo" != "bar") << '\n';
	std::cout << ("It's" < "tricky") << '\n';
	std::cout << ("It's" > "too") << '\n';
	std::cout << ("No idea" <= "what to write") << '\n';
	std::cout << ("Still" >= "no idea") << '\n';
}


