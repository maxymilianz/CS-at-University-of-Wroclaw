#include <stdio.h>
#include <stdlib.h>

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
