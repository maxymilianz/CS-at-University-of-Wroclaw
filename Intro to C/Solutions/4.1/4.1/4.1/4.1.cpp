#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{
	int l[128] = { 0 };
	int min[128] = { 0 };
	int ch = getchar(), i, j, started, lDl, minDl = 0, zero = 0, ltz = 0;

	while (ch != EOF) {
		lDl = 0;
		i = 0;
		started = 0;

		if (ch == '-' || ch == '+') {
			l[i] = ch;
			ch = getchar();
			i++;

			while (ch >= '0' && ch <= '9') {
				if (ch != '0' || started == 1) {
					if (l[0] == '-')
						ltz = 1;

					l[i] = ch;
					lDl++;
					i++;
					started = 1;

					if (ltz == 1)
						zero = 0;
				}
				else {
					if (ltz != 1)
						zero = 1;
				}

				ch = getchar();
			}
		}
		else if (ch >= '0' && ch <= '9') {
			while (ch >= '0' && ch <= '9') {
				if (ch != '0' || started == 1) {
					l[i] = ch;
					lDl++;
					i++;
					started = 1;
					
					if (ltz == 1)
						zero = 0;
				}
				else {
					if (ltz != 1)
						zero = 1;
				}

				ch = getchar();
			}
		}
		else
			ch = getchar();

		j = 0;

		if ((l[0] == '-' && (min[0] != '-' || min[0] == '-' && lDl > minDl) || l[0] != '-' && min[0] != '-' && lDl < minDl || minDl == 0) && lDl > 0) {
			if (l[0] == '+') {
				for (int i = 0; i < lDl; i++) {
					min[i] = l[i + 1];
				}
			}
			else if (l[0] == '-') {
				for (int i = 0; i <= lDl; i++) {
					min[i] = l[i];
				}
			}
			else {
				for (int i = 0; i < lDl; i++) {
					min[i] = l[i];
				}
			}

			minDl = lDl;
		}
		else if (lDl == minDl && (l[0] == '-' || min[0] != '-') && lDl > 0) {
			if (l[0] == '-') {
				for (int i = 0; i < lDl; i++) {
					if (l[i + 1] >= min[i + 1])
						j++;
				}

				if (j == lDl) {
					for (int i = 0; i <= lDl; i++) {
						min[i] = l[i];
					}

					minDl = lDl;
				}
			}
			else if (l[0] == '+') {
				for (int i = 0; i < lDl; i++) {
					if (l[i + 1] <= min[i])
						j++;
				}

				if (j == lDl) {
					for (int i = 0; i < lDl; i++) {
						min[i] = l[i];
					}

					minDl = lDl;
				}
			}
			else {
				for (int i = 0; i < lDl; i++) {
					if (l[i] <= min[i])
						j++;
				}

				if (j == lDl) {
					for (int i = 0; i < lDl; i++) {
						min[i] = l[i];
					}

					minDl = lDl;
				}
			}
		}
	}

	if (zero == 1) {
		printf("Najmniejsza liczba to 0\n");
		return 0;
	}

	if (minDl == 0) {
		printf("W podanym ciagu znakow nie ma zadnych liczb.\n");
		return 0;
	}

	printf("Najmniejsza liczba to ");

	if (min[0] != '-') {
		for (int i = 0; i < minDl; i++) {
			//putchar(min[i]);
			printf("%c", min[i]);
		}
	}
	else if (minDl > 0) {
		for (int i = 0; i <= minDl; i++) {
			//putchar(min[i]);
			printf("%c", min[i]);
		}
	}

	putchar('\n');

	return 0;
}
