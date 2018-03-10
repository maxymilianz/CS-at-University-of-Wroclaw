// 5.2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <math.h>


int main()
{
	double a, b, c, delta;
	printf("Podaj wspolczynnik a rownania kwadratowego postaci: a*x^2 + b*x + c = 0.\n");
	scanf_s("%lf", &a);
	printf("Podaj wspolczynnik b rownania kwadratowego postaci: a*x^2 + b*x + c = 0.\n");
	scanf_s("%lf", &b);
	printf("Podaj wspolczynnik c rownania kwadratowego postaci: a*x^2 + b*x + c = 0.\n");
	scanf_s("%lf", &c);

	if (a == 0) {
		if (b == 0) {
			if (c == 0)
				printf("Rownanie ma nieskonczenie wiele rozwiazan.\n");
			else
				printf("Rownanie nie ma rozwiazan rzeczywistych.\n");

			return 0;
		}

		printf("x = %.6g\n", -c / b);
		return 0;
	}

	delta = pow(b, 2) - 4 * a * c;

	if (delta < 0) {
		printf("Rownanie nie ma rozwiazan rzeczywistych.\n");
		return 0;
	}
	else if (delta == 0) {
		printf("x = %.6g\n", (-b / (2 * a)));
		return 0;
	}

	printf("x1 = %.6g\n", (-b + sqrt(delta)) / (2 * a));
	printf("x2 = %.6g\n", (-b - sqrt(delta)) / (2 * a));

    return 0;
}

