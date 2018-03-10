#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int tabMem[1000000][6];
int tab[6];

void cond2(int n, int k) {
	int w = 0;

	for (int i = 0; i < k; i++) {
		for (int j = 0; j < k; j++) {
			tab[0] = i;
			tab[1] = j;

			for (int c = 0; c < n + 1; c++) {
				tabMem[w][c] = tab[c];
			}

			w++;
		}
	}
}

void cond3(int n, int k) {
	int w = 0;

	for (int h = 0; h < k; h++) {
		for (int i = 0; i < k; i++) {
			for (int j = 0; j < k; j++) {
				tab[0] = h;
				tab[1] = i;
				tab[2] = j;

				for (int c = 0; c < n + 1; c++) {
					tabMem[w][c] = tab[c];
				}

				w++;
			}
		}
	}
}

void cond4(int n, int k) {
	int w = 0;

	for (int g = 0; g < k; g++) {
		for (int h = 0; h < k; h++) {
			for (int i = 0; i < k; i++) {
				for (int j = 0; j < k; j++) {
					tab[0] = g;
					tab[1] = h;
					tab[2] = i;
					tab[3] = j;

					for (int c = 0; c < n + 1; c++) {
						tabMem[w][c] = tab[c];
					}

					w++;
				}
			}
		}
	}
}

void cond5(int n, int k) {
	int w = 0;

	for (int f = 0; f < k; f++) {
		for (int g = 0; g < k; g++) {
			for (int h = 0; h < k; h++) {
				for (int i = 0; i < k; i++) {
					for (int j = 0; j < k; j++) {
						tab[0] = f;
						tab[1] = g;
						tab[2] = h;
						tab[3] = i;
						tab[4] = j;

						for (int c = 0; c < n + 1; c++) {
							tabMem[w][c] = tab[c];
						}

						w++;
					}
				}
			}
		}
	}
}

int iter(int x, int n, int combinations, int *tab1) {
	int suma = 0, amount = 0;

	for (int z = 0; z < 1000; z++) {
		for (int i = 0; i < combinations; i++) {
			suma = 0;

			for (int j = 0; j < n + 1; j++) {
				suma += (tabMem[i][j] + z) * tab1[j];
			}

			if (suma == x)
				amount++;
		}
	}

	return amount;
}

void sort(int *table, int size) {
	int i, j, temp;

	for (i = 0; i < size - 1; i++) {
		for (j = 0; j < size - 1 - i; j++) {
			if (table[j] > table[j + 1]) {
				temp = table[j + 1];
				table[j + 1] = table[j];
				table[j] = temp;
			}
		}
	}
}

int main() {
	int n, x, d, combinations, amount = 0, wieksze = 0;
	scanf_s("%d", &x);
	scanf_s("%d", &d);
	scanf_s("%d", &n);
	int * tab1 = (int*)malloc(sizeof(int) * n);

	for (int i = 0; i < n; i++) {
		scanf_s("%d", &tab1[i]);
	}

	sort(tab1, n);

	for (int i = 0; i < n; i++) {
		if (tab1[i] > x)
			wieksze++;
		else if (tab1[i] == x) {
			wieksze++;
			amount++;
		}
	}

	n = n - wieksze;
	combinations = (int)ceil(pow((double)(d + 1), (double)n));

	if (n == 1 && tab1[0] != 0 && x % tab1[0] == 0) {
		printf("%d", 1);
		return 0;
	}

	if (n == 1 && tab1[0] != 0 && x % tab1[0] != 0) {
		printf("%d", 0);
		return 0;
	}

	if (n == 2)
		cond2(n, d + 1);
	else if (n == 3)
		cond3(n, d + 1);
	else if (n == 4)
		cond4(n, d + 1);

	amount += iter(x, n, combinations, tab1);
	printf("%d", amount);
	free(tab1);

	return 0;

}
