#pragma once

#include <math.h>
#include <stdlib.h>

enum typfig {		// trojkat - takim komentarzem oznaczam miejsca, ktore wymagaja modyfikacji celem dodania do programu obslugi trojkatow
	PUNKT, KOLO, KWADRAT		// trojkat
};

typedef struct {
	float x, y;		// srodek lub lewy dolny wierzcholek
	enum typfig typ;
	float a;		// promien lub bok
} Figura;

void narysuj(Figura *f) {
	printf_s("x = %.6g, y = %.6g\n", (*f).x, (*f).y);
	
	if ((*f).typ == KOLO)
		printf_s("promien = %.6g\n", (*f).a);
	else if ((*f).typ == KWADRAT)		// trojkat
		printf_s("bok = %.6g\n", (*f).a);
}

void przesun(Figura *f, float x, float y) {
	(*f).x += x, (*f).y += y;
}

int zawiera(Figura *f, float x, float y) {
	if ((*f).x == x && (*f).y == y)
		return 1;
	else if ((*f).typ == KOLO && sqrt(((*f).x - x) * ((*f).x - x) + ((*f).y - y) * ((*f).y - y)) <= (*f).a)
		return 1;
	else if ((*f).typ == KWADRAT && (*f).x <= x && (*f).x + (*f).a >= x && (*f).y <= y && (*f).y + (*f).a >= y)
		return 1;
	else		// trojkat
		return 0;
}

Figura * nowyPunkt(float x, float y) {
	Figura *punkt = (Figura *)malloc(sizeof *punkt);
	(*punkt).typ = PUNKT, (*punkt).x = x, (*punkt).y = y;
	return punkt;
}

Figura * noweKolo(float x, float y, float a) {
	Figura *kolo = (Figura *)malloc(sizeof *kolo);
	(*kolo).typ = KOLO, (*kolo).x = x, (*kolo).y = y, (*kolo).a = a;
	return kolo;
}

Figura * nowyKwadrat(float x, float y, float a) {
	Figura *kwadrat = (Figura *)malloc(sizeof *kwadrat);
	(*kwadrat).typ = KWADRAT, (*kwadrat).x = x, (*kwadrat).y = y, (*kwadrat).a = a;
	return kwadrat;
}

// trojkat