// 7.3.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

int n, m, p, iter = 1, actualP = 0, iter2 = 10;
char board[100][100][100][100];		// last dimension: 2 P 3 L 4 D 5 G (+4 - maybe)

void checkPossibilities(char ch, short dontKnow, int iter3) {
	int X = 0;

	if (ch == '?') {
		checkPossibilities('L', 1, iter2);
		checkPossibilities('P', 1, iter2);
		checkPossibilities('G', 1, iter2);
		checkPossibilities('D', 1, iter2);
		checkPossibilities('S', 1, iter2);
		iter++;
	}
	else if (ch == 'P') {
		for (int i = 1; i < n; i++) {
			for (int j = 0; j < m; j++) {
				if (board[0][i - 1][j][2] != 1) {
					if (((iter == 1 && board[0][i - 1][j][0] == '.') || board[iter - 1][i - 1][j][0] == 'X') && board[0][i][j][0] != '#' && actualP < p) {
						if (!dontKnow) {
							board[iter][i][j][0] = 'X';
							X = 1;		// board[iter][i][j][0] == 'X'
							board[0][i - 1][j][2] = 1;
						}
						else {
							board[iter][i][j][0] = 'x';
							//board[iter][i][j][1] = actualP + 1;		// MORE RECENT CHANGE
							//board[0][i - 1][j][6] = 1;
							board[0][i][j][iter3]++;
							iter2++;
						}
					}

					if (!X && ((iter == 1 && board[0][i - 1][j][0] == '.') || board[iter - 1][i - 1][j][0] == 'x') && board[0][i][j][0] != '#' && board[iter - 1][i - 1][j][1] < p) {
						board[iter][i][j][0] = 'x';
						//board[iter][i][j][1] = board[iter - 1][i - 1][j][1] + 1;
						//board[0][i - 1][j][6] = 1;
						board[0][i][j][iter3]++;
						iter2++;
					}
				}
			}
		}

		if (!dontKnow) {
			iter++;
			actualP++;
		}
	}
	else if (ch == 'L') {
		for (int i = 0; i < n - 1; i++) {
			for (int j = 0; j < m; j++) {
				if (board[0][i + 1][j][3] != 1) {
					if (((iter == 1 && board[0][i + 1][j][0] == '.') || board[iter - 1][i + 1][j][0] == 'X') && board[0][i][j][0] != '#' && actualP < p) {
						if (!dontKnow) {
							board[iter][i][j][0] = 'X';
							X = 1;
							board[0][i + 1][j][3] = 1;
						}
						else {
							board[iter][i][j][0] = 'x';
							//board[iter][i][j][1] = actualP + 1;
							//board[0][i + 1][j][7] = 1;
							board[0][i][j][iter3]++;
							iter2++;
						}
					}

					if (!X && ((iter == 1 && board[0][i + 1][j][0] == '.') || board[iter - 1][i + 1][j][0] == 'X') && board[0][i][j][0] != '#' && board[iter - 1][i + 1][j][1] < p) {
						board[iter][i][j][0] = 'x';
						//board[iter][i][j][1] = board[iter - 1][i + 1][j][1] + 1;
						//board[0][i + 1][j][7] = 1;
						board[0][i][j][iter3]++;
						iter2++;
					}
				}
			}
		}

		if (!dontKnow) {
			iter++;
			actualP++;
		}
	}
	else if (ch == 'D') {
		for (int i = 0; i < n; i++) {
			for (int j = 1; j < m; j++) {
				if (board[0][i][j - 1][4] != 1) {
					if (((iter == 1 && board[0][i][j - 1][0] == '.') || board[iter - 1][i][j - 1][0] == 'X') && board[0][i][j][0] != '#' && actualP < p) {
						if (!dontKnow) {
							board[iter][i][j][0] = 'X';
							X = 1;
							board[0][i][j - 1][4] = 1;
						}
						else {
							board[iter][i][j][0] = 'x';
							//board[iter][i][j][1] = actualP + 1;
							//board[0][i][j - 1][8] = 1;
							board[0][i][j][iter3]++;
							iter2++;
						}
					}

					if (!X && ((iter == 1 && board[0][i][j - 1][0] == '.') || board[iter - 1][i][j - 1][0] == 'X') && board[0][i][j][0] != '#' && board[iter - 1][i][j - 1][1] < p) {
						board[iter][i][j][0] = 'x';
						//board[iter][i][j][1] = board[iter - 1][i][j - 1][1] + 1;
						//board[0][i][j - 1][8] = 1;
						board[0][i][j][iter3]++;
						iter2++;
					}
				}
			}
		}

		if (!dontKnow) {
			iter++;
			actualP++;
		}
	}
	else if (ch == 'G') {
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < m - 1; j++) {
				if (board[0][i][j + 1][5] != 1) {
					if (((iter == 1 && board[0][i][j + 1][0] == '.') || board[iter - 1][i][j + 1][0] == 'X') && board[0][i][j][0] != '#' && actualP < p) {
						if (!dontKnow) {
							board[iter][i][j][0] = 'X';
							X = 1;
							board[0][i][j + 1][5] = 1;
						}
						else {
							board[iter][i][j][0] = 'x';
							//board[iter][i][j][1] = actualP + 1;
							//board[0][i][j + 1][9] = 1;
							board[0][i][j][iter3]++;
							iter2++;
						}
					}

					if (!X && ((iter == 1 && board[0][i][j + 1][0] == '.') || board[iter - 1][i][j + 1][0] == 'X') && board[0][i][j][0] != '#' && board[iter - 1][i][j + 1][1] < p) {
						board[iter][i][j][0] = 'x';
						//board[iter][i][j][1] = board[iter - 1][i][j + 1][1] + 1;
						//board[0][i][j + 1][9] = 1;
						board[0][i][j][iter3]++;
						iter2++;
					}
				}
			}
		}

		if (!dontKnow) {
			iter++;
			actualP++;
		}
	}
	else if (ch == 'S') {
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < m; j++) {
				board[iter][i][j][0] = board[iter - 1][i][j][0];
				board[iter][i][j][1] = board[iter - 1][i][j][1];
			}
		}

		if (!dontKnow)
			iter++;
	}
}

int main()
{
	int l;
	char ch;
	scanf_s("%d", &n);
	scanf_s("%d", &m);
	getchar();

	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++)
			board[0][j][i][0] = getchar();

		getchar();
	}

	scanf_s("%d", &p);
	scanf_s("%d", &l);
	getchar();

	for (int i = 0; i < l; i++) {
		ch = getchar();

		for (int j = 0; j < iter2; j++)
			checkPossibilities(ch, 0, j);
	}

	iter--;

	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			if (board[0][j][i][0] == '#')
				putchar('#');
			else if ((board[iter][j][i][0] == 'X' && actualP == p) || (board[iter][j][i][0] == 'x' && board[iter][j][i][1] == p)) {
				int k = 0;

				while (k < iter2 && board[0][j][i][k] != p)
					k++;

				if (board[0][j][i][k] == p)
					putchar(board[0][j][i][k]);
			}
			else
				putchar('.');
		}

		putchar('\n');
	}

    return 0;
}

