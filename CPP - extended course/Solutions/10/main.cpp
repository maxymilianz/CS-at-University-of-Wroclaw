
#include <iostream>

#include "units.h"

// Useful if you want to compute the yield of an atomic bomb:

#if 1
quantity::energy mc2( quantity::mass m )
{
auto C = 299792458.0_mps;
return m * C * C;
}
#endif

int main( int argc, char* argv [ ] )
{
    std::cout << 9.81 * 1.0_m / ( 1.0_sec * 1.0_sec ) << "\n";
    // Acceleration on earth.

    std::cout << 1.0_m << "\n";
    std::cout << 2.0_hr << "\n";

    std::cout << 1000.0_watt << "\n";

	auto capacity = 0.8_A * 1.0_hr;		// task 5
    std::cout << capacity << "\n";
	si<1, 2, -3, -1> voltage(1.2);
	std::cout << voltage << "\n";
	// P = IU
	// E = Pt = IUt = CU
	std::cout << capacity * voltage << "\n";
	
	auto speed = 100.0_kmh + 30.0_kmh;		// task 6
	auto energy = 1200.0_kg * speed * speed / 2;
	std::cout << energy << "\n";
	const auto C = 299792458.0_mps;
	std::cout << (speed + 0.0_kmh) / (1 + speed * 0.0_kmh / C / C) << "\n";
	
	std::cout << mc2(2.3_kg) << "\n";		// task 7
	const auto TNT = 4184.0_joule / 0.001_kg;
	std::cout << TNT << "\n";
	// [TNT] = E / m
	// [TNT]m = E
	// m = E/[TNT]
	std::cout << mc2(2.3_kg) / TNT << "\n";

    return 0;

}
