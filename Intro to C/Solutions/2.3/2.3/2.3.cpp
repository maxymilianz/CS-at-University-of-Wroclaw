// 2.3.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"


int main()
{
	int ch = getchar(), size = 0, xB, xW, max = 19;
	int board[19][19];

	while (ch != EOF) {
		if (ch == 'S') {
			ch = getchar();

			if (ch == 'Z') {
				ch = getchar();

				if (ch == '[') {
					ch = getchar();

					while (ch >= '0' && ch <= '9') {
						size = 10 * size + ch - '0';
						ch = getchar();
					}
				}
			}
		}

		ch = getchar();

		if (ch == ';') {
			ch = getchar();

			if (ch == 'B') {
				ch = getchar();

				if (ch == '[') {
					ch = getchar();

					if (ch >= 'a' && ch <= 'z') {
						xB = ch;
						ch = getchar();

						if (ch >= 'a' && ch <= 'z') {
							board[xB - 97][ch - 97] = 'X';
						}
					}
				}
			}

			if (ch == 'W') {
				ch = getchar();

				if (ch == '[') {
					ch = getchar();

					if (ch >= 'a' && ch <= 'z') {
						xW = ch;
						ch = getchar();

						if (ch >= 'a' && ch <= 'z') {
							board[xW - 97][ch - 97] = 'O';
						}
					}
				}
			}
		}
	}

	if (size > 19)
		max = size;

	for (int i = 0; i <= size; i++) {		//ZLIKWIDOWAC PRZESUNIECIE W LEWO
		if (i == 0) {
			putchar(' ');
			putchar(' ');
		}

		for (int j = 0; j < size; j++) {
			if (i == 0) {
				printf("%c ", ('A' + j));

				/*putchar('A' + j);
				putchar(' ');*/
			}
			else {
				if (j == 0) {
					printf("%c ", ('A' + i - 1));
				}
				else {
					if (board[j - 1][i - 1] == 'X')
						putchar('X');
					else if (board[j - 1][i - 1] == 'O')
						putchar('O');
					else
						putchar('.');

					putchar(' ');
				}
			}
		}

		putchar('\n');
	}

    return 0;
}

