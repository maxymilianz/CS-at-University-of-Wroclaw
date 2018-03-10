
#include "listtest.h"

#include <random>
#include <chrono>
#include <algorithm>

#include "vectortest.h"

void listtest::sort_assign( std::list< std::string > & v ) {
	for (auto i = v.begin(); i != v.end(); ++i) {
		for (auto j = v.begin(); j != i; ++j) {
			if (*i < *j) {
				std::string s = *i;
				*i = *j;
				*j = s;
			}
		}
	}
}

void listtest::sort_move( std::list< std::string > & v )
{
	for (auto i = v.begin(); i != v.end(); ++i) {
		for (auto j = v.begin(); j != i; ++j) {
			if (*i < *j)
				std::swap(*i, *j);
		}
	}
}

void listtest::sort_std( std::list< std::string > & v ) {
	std::vector<std::string> vec;
	
	for (auto a = v.begin(); a != v.end(); ++a)
		vec.push_back(*a);
	
	vectortest::sort_std(vec);
	v = listtest::vecToList(vec);
}

std::list<std::string> listtest::vecToList(std::vector<std::string> &vec) {
	std::list<std::string> l;
	
	for (size_t i = 0; i < vec.size(); ++i)
		l.push_back(vec[i]);
	
	return l;
}

std::ostream& 
operator << ( std::ostream& out, const std::list< std::string > &l ) {
	for (auto a = l.begin(); a != l.end(); ++a) {
		if (a != l.begin())
			out << ", ";
		out << *a;
	}
	
	return out;
}


