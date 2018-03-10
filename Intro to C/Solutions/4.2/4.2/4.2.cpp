// 4.2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <time.h>

int mem[63] = { 0 };

int fibRec(int n) {
	if (n < 0 || n > 62)
		return -1;

	if (n == 0)
		return 0;
	else if (n == 1)
		return 1;

	return fibRec(n - 1) + fibRec(n - 2);
}

int fibIte(int n) {
	int a = 0, b = 1, wynik = 1;

	if (n < 0 || n > 62)
		return -1;

	if (n == 0)
		return 0;
	else if (n == 1)
		return 1;

	for (int i = 0; i < n - 1; i++) {
		b = a;
		a = wynik;
		wynik = a + b;
	}

	return wynik;
}

int fibRecMem(int n) {
	if (n < 0 || n > 62)
		return -1;
	
	if (n == 0)
		return 0;
	else if (n == 1)
		return 1;

	mem[n] = (mem[n - 1] == 0 ? fibRecMem(n - 1) : mem[n - 1]) + (mem[n - 2] == 0 ? fibRecMem(n - 2) : mem[n - 2]);
	return mem[n];
}

int main()
{
	int f, n, t;
	printf("Jesli chcesz przetestowac funkcje fibRec, wpisz 1, jesli fibIte - 2, a jesli fibRecMem - 3.\n");
	scanf_s("%d", &f);

	while (f < 1 || f > 3) {
		printf("Wpisz 1, 2 lub 3.\n");
		scanf_s("%d", &f);
	}

	printf("Ktory wyraz ciagu Fibonacciego wyswietlic?\n");
	scanf_s("%d", &n);

	if (f == 1) {
		t = clock();
		printf("%d\n", fibRec(n));
		printf("Obliczenia zajely %d ms.", clock() - t);
	}
	else if (f == 2) {
		t = clock();
		printf("%d\n", fibIte(n));
		printf("Obliczenia zajely %d ms.", clock() - t);
	}
	else {
		t = clock();
		printf("%d\n", fibRecMem(n));
		printf("Obliczenia zajely %d ms.", clock() - t);
	}

	printf("\n");
    return 0;
}