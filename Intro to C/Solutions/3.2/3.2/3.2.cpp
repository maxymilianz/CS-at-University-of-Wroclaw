// 3.2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <math.h>


int main()
{
	int systemOut, exponent = 0, systemIn, ch, iterator = 0;
	long long int dec = 0;
	char input[63];
	char output[63];
	printf("W jakim systemie pozycyjnym bedzie twoja liczba? (Wpisz liczbe z zakresu 2 - 16.)\n");
	scanf_s("%d", &systemIn);

	if (systemIn < 2 || systemIn > 16) {
		printf("Brak obslugi takiego systemu.\n");
		return 0;
	}

	printf("Podaj swoja liczbe. %s\n", systemIn > 10 ? "Uzywaj malych liter." : "");
	ch = getchar();
	ch = getchar();

	while (ch != '\n') {
		if (systemIn < 11 && (ch < '0' || ch >= '0' + systemIn) || systemIn > 10 && (ch < '0' || ch > '9' && (ch < 'a' || ch >= 'a' + systemIn - 10))) {
			printf("Podales niepoprawna liczbe.\n");
			return 0;
		}

		input[iterator] = ch;
		iterator++;
		ch = getchar();
	}

	iterator--;
	exponent = iterator;

	for (int i = 0; i <= iterator; i++) {
		if (input[i] >= '0' && input[i] <= '9')
			dec += (input[i] - 48) * pow(systemIn, exponent);
		else
			dec += (input[i] - 87) * pow(systemIn, exponent);

		exponent--;
	}

	printf("W jakim systemie chcesz wyswietlic ta liczbe? (2 - 16)\n");
	scanf_s("%d", &systemOut);

	if (systemOut < 2 || systemOut > 16) {
		printf("Brak obslugi takiego systemu.");
		return 0;
	}

	printf("WYNIK: ");
	iterator = 0;

	while (dec > 0) {
		if (dec % systemOut < 10)
			output[iterator] = dec % systemOut + 48;
		else
			output[iterator] = dec % systemOut + 87;

		iterator++;
		dec /= systemOut;
	}

	for (int i = iterator - 1; i >= 0; i--) {
		printf("%c", output[i]);
	}

	putchar('\n');

    return 0;
}

