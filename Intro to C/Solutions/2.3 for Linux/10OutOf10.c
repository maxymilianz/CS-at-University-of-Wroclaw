// 2.3.cpp : Defines the entry point for the console application.
//

#include <stdio.h>


int main()
{
	int ch = getchar(), size = 0, xB, xW, yB, yW, b, w, b2 = 0, w2 = 0;
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
							yB = ch;
							ch = getchar();
							
							if (ch == ']') {
								board[xB - 97][yB - 97] = 'X';
							}
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
							yW = ch;
							ch = getchar();
							
							if (ch == ']') {
								board[xW - 97][yW - 97] = 'O';
							}
						}
					}
				}
			}
		}
	}

	for (int i = 0; i <= size; i++) {
		b = 0;
		w = 0;

		if (i == 0) {
			putchar(' ');
			putchar(' ');
		}

		for (int j = 0; j <= size; j++) {
			if (i == 0 && j != size) {
				printf("%c ", ('A' + j));

			}
			else if (i != 0) {
				if (j == 0) {
					printf("%c ", ('A' + i - 1));
				}
				else {
					if (board[j - 1][i - 1] == 'X') {
						putchar('X');
						b++;
					}
					else if (board[j - 1][i - 1] == 'O') {
						putchar('O');
						w++;
					}
					else {
						putchar('.');
					}

					putchar(' ');
				}
			}
		}

		if (b > b2)
			b2 = b;

		if (w > w2)
			w2 = w;

		putchar('\n');
	}

	printf("%d %d", b2, w2);
	putchar('\n');

    return 0;
}
