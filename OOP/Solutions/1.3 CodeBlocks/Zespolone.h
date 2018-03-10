#ifndef ZESPOLONE_H_INCLUDED
#define ZESPOLONE_H_INCLUDED



#endif // ZESPOLONE_H_INCLUDED

#pragma once

#include <stdlib.h>

struct Zespolona {
	double x, y;
};

/*Zespolona * dodaj(Zespolona *a, Zespolona *b);		// funkcje zwracajace wskaznik do nowoutworzonego elementu typu Zespolona
Zespolona * odejmij(Zespolona *a, Zespolona *b);
Zespolona * pomnoz(Zespolona *a, Zespolona *b);
Zespolona * podziel(Zespolona *a, Zespolona *b);*/

void dodaj(Zespolona *a, Zespolona *b);		// funkcje modyfikujace drugi z argumentow
void odejmij(Zespolona *a, Zespolona *b);
void pomnoz(Zespolona *a, Zespolona *b);
void podziel(Zespolona *a, Zespolona *b);

/*Zespolona * dodaj(Zespolona *a, Zespolona *b) {
Zespolona *c;
c = (Zespolona *)malloc(sizeof *c);

(*c).x = (*a).x + (*b).x;
(*c).y = (*a).y + (*b).y;

return c;
}

Zespolona * odejmij(Zespolona *a, Zespolona *b) {
Zespolona *c;
c = (Zespolona *)malloc(sizeof *c);

(*c).x = (*a).x - (*b).x;
(*c).y = (*a).y - (*b).y;

return c;
}

Zespolona * pomnoz(Zespolona *a, Zespolona *b) {
Zespolona *c;
c = (Zespolona *)malloc(sizeof *c);

(*c).x = (*a).x * (*b).x - (*a).y * (*b).y;
(*c).x = (*a).x * (*b).y + (*a).y * (*b).x;

return c;
}

Zespolona * podziel(Zespolona *a, Zespolona *b) {
Zespolona *c;
c = (Zespolona *)malloc(sizeof *c);

if (!(*b).x && !(*b).y) {
printf_s("Nie mozna dzielic przez zero.");
exit(1);
}

(*c).x = ((*a).x * (*b).x + (*a).y * (*b).y) / ((*b).x * (*b).x + (*b).y * (*b).y);
(*c).y = ((*a).y * (*b).x - (*a).x * (*b).y) / ((*b).x * (*b).x + (*b).y * (*b).y);

return c;
}*/

void dodaj(Zespolona *a, Zespolona *b) {
	(*b).x = (*a).x + (*b).x;
	(*b).y = (*a).y + (*b).y;
}

void odejmij(Zespolona *a, Zespolona *b) {
	(*b).x = (*a).x - (*b).x;
	(*b).y = (*a).y - (*b).y;
}

void pomnoz(Zespolona *a, Zespolona *b) {
	(*b).x = (*a).x * (*b).x - (*a).y * (*b).y;
	(*b).y = (*a).x * (*b).y + (*a).y * (*b).x;
}

void podziel(Zespolona *a, Zespolona *b) {
	if (!(*b).x && !(*b).y) {
		printf_s("Nie mozna dzielic przez zero.");
		exit(1);
	}

	(*b).x = ((*a).x * (*b).x + (*a).y * (*b).y) / ((*b).x * (*b).x + (*b).y * (*b).y);
	(*b).y = ((*a).y * (*b).x - (*a).x * (*b).y) / ((*b).x * (*b).x + (*b).y * (*b).y);
}

void wypisz(Zespolona *a) {
	printf_s("x = %.6g, y = %.6g\n", (*a).x, (*a).y);
}
