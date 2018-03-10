// 4.2.cpp : Defines the entry point for the console application.
//

#include <stdio.h>
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
	int n, t;
	printf("Ktory wyraz ciagu Fibonacciego wyswietlic?\n");
	scanf("%d", &n);

	t = clock();
	printf("%d\n", fibRec(n));
	printf("Obliczenia fibRec zajely %d ms.\n", clock() - t);
	t = clock();
	printf("%d\n", fibIte(n));
	printf("Obliczenia fibIte zajely %d ms.\n", clock() - t);
	t = clock();
	printf("%d\n", fibRecMem(n));
	printf("Obliczenia fibRecMem zajely %d ms.\n", clock() - t);

    return 0;
}