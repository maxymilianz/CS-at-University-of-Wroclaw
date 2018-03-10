#include "structs.h"
#include <vector>

std::ostream& operator << ( std::ostream& stream, const std::vector< surface > & table )
{
    for( size_t i = 0; i < table. size( ); ++ i )
    {
        stream << i << "-th element = " << table [i] << "\n";
    }
    return stream;
}

void print_statistics( const std::vector< surface > & table )
{
    double total_area = 0.0;
    double total_circumference = 0.0;
    for( const auto& s : table )
    {
        std::cout << "adding info about " << s << "\n";
        total_area += s. getsurf( ). area( );
        total_circumference += s. getsurf( ). circumference( );
    }
    std::cout << "total area is " << total_area << "\n";
    std::cout << "total circumference is " << total_circumference << "\n";
}

int main() {
    std::vector<surface> vec;       // task 4
    vec.push_back(rectangle(1, 2, 3, 4));
    vec.push_back(triangle(0, 0, 0, 10, 10, 0));
    vec.push_back(circle(11, 12, 13));
    std::cout << vec << "\n";
    print_statistics(vec);
    std::cout << "\n";

    rectangle r(14, 15, 16, 17);        // task 5
    std::cout << r;
    rectangle &r3 = *new rectangle(22, 23, 24, 25);
    std::cout << r3;
    rectangle *r4 = new rectangle(26, 27, 28, 29);
    std::cout << *r4;
    rectangle *r5 = r.clone();
    std::cout << *r5;
    rectangle &r7 = *(*r4).clone();
    std::cout << r7;
	
	delete &r3; delete r4; delete r5; delete &r7;

    return 0;
}
