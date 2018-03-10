// 5.1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <math.h>


int main()
{
	float boki[3];
	int sorted = 0;
	float sup;
	int trojkat[4] = { 0 };		//[0] - jakikolwiek, [1] - prostokatny, [2] - rownoboczny, [3] - rownoramienny

	for (int i = 0; i < 3; i++) {
		printf("Podaj dlugosc %d. boku.\n", i + 1);
		scanf_s("%f", &boki[i]);
	}

	while (sorted == 0) {
		sorted = 1;

		for (int i = 0; i < 2; i++) {
			if (boki[i] > boki[i + 1]) {
				sup = boki[i];
				boki[i] = boki[i + 1];
				boki[i + 1] = sup;
				sorted = 0;
			}
		}
	}

	if (boki[0] + boki[1] > boki[2]) {
		trojkat[0] = 1;

		if (boki[0] == boki[1] || boki[1] == boki[2]) {
			trojkat[3] = 1;

			if (boki[0] == boki[2])
				trojkat[2] = 1;
		}

		if (boki[1] != boki[2] && pow(boki[0], 2) + pow(boki[1], 2) == pow(boki[2], 2))
			trojkat[1] = 1;
	}

	if (trojkat[0] == 0)
		printf("Z podanych bokow nie mozna zbudowac zadnego trojkata.\n");
	else if (trojkat[1] == 0 && trojkat[2] == 0 && trojkat[3] == 0) {
		printf("Z podanych bokow mozna zbudowac jakis trojkat.\n");
	}
	else {
		printf(trojkat[1] == 1 ? "Z podanych bokow mozna zbudowac trojkat prostokatny.\n" : "");
		printf(trojkat[2] == 1 ? "Z podanych bokow mozna zbudowac trojkat rownoboczny.\n" : "");
		printf(trojkat[3] == 1 ? "Z podanych bokow mozna zbudowac trojkat rownoramienny.\n" : "");
	}

    return 0;
}

