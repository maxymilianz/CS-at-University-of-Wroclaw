#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

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
