// 1.3.cpp : Defines the entry point for the console application.
//

#include <stdio.h>
#include "Zespolone.h"

int main()		// NOT WORKING
{
	double x, y;
	Zespolona *a = (Zespolona *)malloc(sizeof *a);
	Zespolona *b = (Zespolona *)malloc(sizeof *b);

	printf_s("Podaj wartosc x pierwszej liczby zespolonej: ");
	scanf_s("%f", &(*a).x);
	printf_s("Podaj wartosc y pierwszej liczby zespolonej: ");
	scanf_s("%f", &(*a).y);

	printf_s("Podaj wartosc x drugiej liczby zespolonej: ");
	scanf_s("%f", &x);
	printf_s("Podaj wartosc y drugiej liczby zespolonej: ");
	scanf_s("%f", &y);
	(*b).x = x, (*b).y = y;

	dodaj(a, b);
	printf_s("Wynik dodawania: ");
	wypisz(b);
	(*b).x = x, (*b).y = y;

	odejmij(a, b);
	printf_s("Wynik odejmowania: ");
	wypisz(b);
	(*b).x = x, (*b).y = y;

	pomnoz(a, b);
	printf_s("Wynik mnozenia: ");
	wypisz(b);
	(*b).x = x, (*b).y = y;

	podziel(a, b);
	printf_s("Wynik dzielenia: ");
	wypisz(b);
	(*b).x = x, (*b).y = y;

    return 0;
}

