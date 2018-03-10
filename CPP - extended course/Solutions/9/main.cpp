
#include "powerproduct.h"
#include "polynomial.h"
#include "bigint.h"
#include "rational.h"


template< typename N >
polynomial< N > exptaylor( unsigned int n )
{
    powerproduct v;

    N fact = 1;

    polynomial< N > result;
    for( unsigned int i = 0; i < n; ++ i )
    {
        result[v] += fact;
        v = v * powvar( "x" );
        fact = fact / (i+1);
    }

    return result;
}

int main( int argc, char* argv [] )
{
    polynomial<int> p(1);       // here starts (1+x)^5

    powerproduct pp("x");
    polynomial<int> px(pp);
	powerproduct pp2("x", 0);
	polynomial<int> px2(pp2);

    px += px2;

    polynomial<int> p2 = px;
    for (int i = 1; i < 5; i++)
        px = px * p2;

    std::cout << px << '\n';

    polynomial<int> p3(1);      // here starts (1+x^2yz^3)^4
    powerproduct pp3("x", 2);
    powerproduct pp4("y");
    powerproduct pp5("z", 3);
    pp3 = pp3 * pp4 * pp5;
    std::cout << pp3 << '\n';
    p3 += polynomial<int>(pp3);
    std::cout << p3 << '\n';

    polynomial<int> p4 = p3;
    for (int i = 1; i < 4; i++)
        p3 = p3 * p4;
    std::cout << p3 << '\n';

    polynomial<int> p5(3);      // here starts (3+xy)^6
    polynomial<int> p6(pp * pp4);
    std::cout << p6 << '\n';
    p5 += p6;
    polynomial<int> p7 = p5;
    for (int i = 1; i < 6; i++)
        p5 = p5 * p7;
    std::cout << p5 << '\n';

    // taylor below

    polynomial< rational > pol;

    int N = 50;

    pol[ { } ] = 1;
    pol[ { "x" } ] = rational( 1, N );


    polynomial< rational > res = 1;


    for( int i = 0; i < N; ++ i )
    	res = res * pol;

    std::cout << "rsult = " << res << "\n";

    std::cout << " taylor expansion = " << exptaylor<rational>(20) << "\n";

    std::cout << "difference = " ;
    std::cout << res - exptaylor<rational> ( 40 ) << "\n";

    if (false) {       // testing every feature separately
        powerproduct p("x", 0);
        std::cout << p << '\n';

        powerproduct p2("y", 2);
        powerproduct p3("x", 1);
        p = p * p3 * p2;
        std::cout << p << '\n';

        std::cout << p2 << '\n' << powerproduct::compare(p, p2) << '\n';

        polynomial<int> pol(p);
        polynomial<int> pol2(p2);
        std::cout << pol - pol2 << '\n';
        std::cout << pol << '\n';
    }

    return 0;
}
