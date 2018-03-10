// 1.4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Drzewo.h"

int main()
{
	int amount;
	str v;

	printf_s("Jaka wartoscia zainicjalizowac drzewo?\n");
	scanf_s("%d", &v);
	DrzewoBinarne *d = noweDrzewo(v);

	printf_s("Ile elementow chcesz dodac do drzewa?\n");
	scanf_s("%d", &amount);

	for (int i = 0; i < amount; i++) {
		printf_s("Podaj %d. element: ", i);
		scanf_s("%d", &v);		// dla typedef int str
		wstaw(d, v);
	}

	printf_s("Drzewo ma %d elementow.\n", rozmiar(d));

	printf_s("Jakiego elementu chcesz wyszukac?\n");
	scanf_s("%d", &v);

	if (szukaj(d, v) != NULL)
		printf_s("W drzewie istnieje taki element.\n");
	else
		printf_s("W drzewie nie istnieje taki element.\n");

    return 0;
}

