// 1.2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Figury.h"

int main()
{
	int which;
	float x, y, a;

	printf_s("Podaj wspolrzedna x punktu: ");
	scanf_s("%f", &x);
	printf_s("Podaj wspolrzedna y punktu: ");
	scanf_s("%f", &y);
	Figura *punkt = nowyPunkt(x, y);

	printf_s("Podaj wspolrzedna x kola: ");
	scanf_s("%f", &x);
	printf_s("Podaj wspolrzedna y kola: ");
	scanf_s("%f", &y);
	printf_s("Podaj promien kola: ");
	scanf_s("%f", &a);
	Figura *kolo = noweKolo(x, y, a);

	printf_s("Podaj wspolrzedna x kwadratu: ");
	scanf_s("%f", &x);
	printf_s("Podaj wspolrzedna y kwadratu: ");
	scanf_s("%f", &y);
	printf_s("Podaj dlugosc boku kwadratu: ");
	scanf_s("%f", &a);
	Figura *kwadrat = nowyKwadrat(x, y, a);

	printf_s("Ktora figure chcesz przesunac? (0 - punkt, 1 - kolo, >1 - kwadrat)\n");
	scanf_s("%d", &which);
	printf_s("O ile poziomo chcesz ja przesunac?\n");
	scanf_s("%f", &x);
	printf_s("O ile pionowo chcesz ja przesunac?\n");
	scanf_s("%f", &y);

	if (!which) {
		przesun(punkt, x, y);
		narysuj(punkt);
	}
	else if (which == 1) {
		przesun(kolo, x, y);
		narysuj(kolo);
	}
	else {
		przesun(kwadrat, x, y);
		narysuj(kwadrat);
	}

	printf_s("Podaj wspolrzedna x punktu do przetestowania: ");
	scanf_s("%f", &x);
	printf_s("Podaj wspolrzedna y punktu do przetestowania: ");
	scanf_s("%f", &y);
	printf_s("Z jaka figura chcesz sprawdzic zawieranie?\n");
	scanf_s("%d", &which);

	if (!which)
		printf_s(zawiera(punkt, x, y) ? "Zawiera\n" : "Nie zawiera\n");
	else if (which == 1)
		printf_s(zawiera(kolo, x, y) ? "Zawiera\n" : "Nie zawiera\n");
	else
		printf_s(zawiera(kwadrat, x, y) ? "Zawiera\n" : "Nie zawiera\n");

	free(punkt), free(kolo), free(kwadrat);

    return 0;
}

