#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#define ROZMIAR 10000

int n, m;
int A[ROZMIAR];
int mniejsze[ROZMIAR];
int rowne[ROZMIAR];
int B[ROZMIAR];

void C_K_E();
void C_K_L();
void Reorg();
void C_S();
bool input_and_check_data();
void output_data();

void C_K_E() {
	for (int i = 0; i < m; i++)
		rowne[i] = 0;
	
	for (int i = 0; i < n; i++)
		rowne[A[i]]++;
}

void C_K_L() {
	mniejsze[0] = 0;
	mniejsze[1] = rowne[0];
	
	for (int i = 2; i < m; i++)
		mniejsze[i] = mniejsze[i-1] + rowne[i-1];
}

void Reorg() {
	for (int i = 0; i < n; i++)
		B[mniejsze[A[i]]++] = A[i];
}

void C_S() {
	C_K_E();
	C_K_L();
	Reorg();
}

bool input_and_check_data() {
	scanf("%d %d", &n, &m);
	
	if (n > ROZMIAR || n <= 0) {
		printf ("\nError: size of input table out of range;\n"
		" must be between 1 and %d (inclusive).\n", ROZMIAR);
		return 0;
	}
	
	if (m > n || m <= 0) {
		printf("\nError: cardinality of key set out of range;\n"
		" must be between 1 and %d (inclusive).\n", n);
		return 0;
	}
	
	for (int i = 0; i < n; i++) {
		scanf("%d ", &A[i]);
		
		if (A[i] < 0 || A[i] > m-1) {
			printf("\nError: value of element of input data out of range;\n"
			" must be between 0 and %d (inclusive).\n", m-1);
			return 0;
		}
	}
	
	return 1;
}

void output_data() {
	printf("Tablica nieposortowana:\n\n");
	
	for (int i = 0; i < n; i++)
		printf("%d ", A[i]);
	
	printf("\nTablica posortowana:\n\n");
	
	for (int i = 0; i < n; i++)
		printf("%d ", B[i]);
	
	printf("\n");
}

int main() {
	bool sprawdz = 1;
	sprawdz = input_and_check_data();
	
	if (!sprawdz)
		return 0;
	
	C_S();
	output_data();
}
