// 3.1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"


int main()
{
	unsigned long int a;
	int jedynki = 0, ciag0 = 0, ciag1 = 0, ciag02 = 0, ciag12 = 0, potega = 0;
	scanf_s("%lu", &a);

	while (a > 0) {
		while (a % 2 == 0 && a > 0) {
			potega++;
			ciag02++;
			a /= 2;
		}

		while (a % 2 == 1 && a > 0) {
			potega++;
			ciag12++;
			jedynki++;
			a /= 2;
		}

		if (ciag02 > ciag0)
			ciag0 = ciag02;
		
		if (ciag12 > ciag1)
			ciag1 = ciag12;

		ciag02 = 0;
		ciag12 = 0;
	}

	if (32 - potega > ciag0)
		ciag0 = 32 - potega;

	printf("jedynek: %d, najdluzszy ciag zer: %d, najdluzszy ciag jedynek: %d\n", jedynki, ciag0, ciag1);

    return 0;
}

