// 9.1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

int i = 0;
char roman[24] = { 0 };
char underscore[12] = { ' ' };

void arab2Roman(int a, int underscored) {
	if (a >= 4000) {
		arab2Roman(a / 1000, 1);
		arab2Roman(a % 1000, 0);
	}
	else {
		if (a >= 1000) {
			for (int i2 = 0; i2 < a / 1000; i2++, i++) {
				roman[i] = 'M';

				if (underscored)
					underscore[i] = '_';
			}

			a %= 1000;
		}

		if (a >= 900) {
			roman[i] = 'C';

			if (underscored)
				underscore[i] = '_';

			i++;
			roman[i] = 'M';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 900;
		}

		if (a >= 500) {
			roman[i] = 'D';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 500;
		}

		if (a >= 400) {
			roman[i] = 'C';

			if (underscored)
				underscore[i] = '_';

			i++;
			roman[i] = 'D';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 400;
		}

		if (a >= 100) {
			for (int i2 = 0; i2 < a / 100; i2++, i++) {
				roman[i] = 'C';

				if (underscored)
					underscore[i] = '_';
			}

			a %= 100;
		}

		if (a >= 90) {
			roman[i] = 'X';

			if (underscored)
				underscore[i] = '_';

			i++;
			roman[i] = 'C';
			
			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 90;
		}

		if (a >= 50) {
			roman[i] = 'L';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 50;
		}

		if (a >= 40) {
			roman[i] = 'X';

			if (underscored)
				underscore[i] = '_';

			i++;
			roman[i] = 'L';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 40;
		}

		if (a >= 10) {
			for (int i2 = 0; i2 < a / 10; i2++, i++) {
				roman[i] = 'X';

				if (underscored)
					underscore[i] = '_';
			}

			a %= 10;
		}

		if (a >= 9) {
			roman[i] = 'I';

			if (underscored)
				underscore[i] = '_';

			i++;
			roman[i] = 'X';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 9;
		}

		if (a >= 5) {
			roman[i] = 'V';

			if (underscored)
				underscore[i] = '_';

			i++;
			a %= 5;
		}

		if (!underscored) {
			if (a >= 4) {
				roman[i] = 'I';
				i++;
				roman[i] = 'V';
				i++;
				a %= 4;
			}

			for (int i2 = 0; i2 < a; i2++, i++)
				roman[i] = 'I';
		}
		else {
			if (a >= 4) {
				roman[i] = 'I';
				underscore[i] = '_';
				i++;
				roman[i] = 'V';
				underscore[i] = '_';
				i++;
				a %= 4;
			}

			for (int i2 = 0; i2 < a; i2++, i++)
				roman[i] = 'M';
		}
	}
}

int main()
{
	int a;
	printf("Podaj liczbe calkowita z zakresu 1-999999: ");
	scanf_s("%d", &a);

	while (a < 1 || a > 999999) {
		printf("Podaj liczbe calkowita z zakresu 1-999999: ");
		scanf_s("%d", &a);
	}

	arab2Roman(a, 0);

	for (int j = 0; j < 12; j++)
		printf("%c", underscore[j]);

	printf("\n");

	for (int j = 0; j < i; j++)
		printf("%c", roman[j]);

	printf("\n");

    return 0;
}

