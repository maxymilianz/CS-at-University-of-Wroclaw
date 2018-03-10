// 6.2.cpp : Defines the entry point for the console application.
//

#include "stdio.h"
#include "time.h"
#include <stdlib.h>

#define size 9
#define bombs 10

int bombBoard[size][size] = { 0 };
int board[size][size];
int board2Display[size][size];
int checkedForSafety[size][size] = { 0 };
int safeFields = size * size - bombs, alive = 1;

void checkSafeNeighbours(int x, int y) {
	for (int i = x - 1; i < x + 2; i++) {
		for (int j = y - 1; j < y + 2; j++) {
			if (i >= 0 && i <= 8 && j >= 0 && j <= 8 && bombBoard[i][j] == 0 && board[i][j] == 0 && checkedForSafety[i][j] == 0) {
				board2Display[i][j] = '.';
				checkedForSafety[i][j] = 1;
				checkSafeNeighbours(i, j);
			}
		}
	}
}

void setBombs() {
	int x, y;
	time_t tt;
	srand(time(&tt));

	for (int i = 0; i < bombs; i++) {
		x = rand() % size;
		y = rand() % size;

		while (bombBoard[x][y] == 1) {
			x = rand() % size;
			y = rand() % size;
		}

		bombBoard[x][y] = 1;
	}
}

void checkNeighbourBombs(int x, int y) {
	int neighbourBombs = 0;

	for (int i = x - 1; i < x + 2; i++) {
		for (int j = y - 1; j < y + 2; j++) {
			if (i >= 0 && i <= 8 && j >= 0 && j <= 8 && bombBoard[i][j] == 1) {
				neighbourBombs++;
			}
		}
	}

	if (bombBoard[x][y] == 1 && neighbourBombs > 0)
		neighbourBombs--;

	board[x][y] = neighbourBombs;
	board2Display[x][y] = 'x';
}

void display() {
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			putchar(board2Display[i][j]);
		}

		putchar('\n');
	}

	if (safeFields == 0) {
		printf("\nWygrales!\n");
		exit(0);
	}
	else if (alive)
		printf("\nPozostale niezaminowane pola: %d.\nPodaj pozycje x, y pola do odkrycia (oddzielone znakiem bialym).\n", safeFields);
	else
		printf("Przegrales.\n");
}

void input() {
	int x, y;
	scanf("%d", &y);
	scanf("%d", &x);

	while (x < 0 || x > 8 || y < 0 || y > 8) {
		printf("Podaj liczby z przedzialu 0 - 8.\n");
		scanf("%d", &y);
		scanf("%d", &x);
	}

	putchar('\n');

	if (bombBoard[x][y] == 0 && board2Display[x][y] == 'x') {
		if (board[x][y] == 0) {
			board2Display[x][y] = '.';
			checkSafeNeighbours(x, y);
		}
		else
			board2Display[x][y] = board[x][y] + '0';
		
		safeFields--;

		if (safeFields == 0) {
			for (int i = 0; i <= 8; i++) {
				for (int j = 0; j <= 8; j++) {
					if (bombBoard[i][j] == 1)
						board2Display[i][j] = '*';
				}
			}
		}
	}
	else if (bombBoard[x][y] == 1) {
		board2Display[x][y] = '*';
		alive = 0;
	}
}

int main()
{
	setBombs();

	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			checkNeighbourBombs(i, j);
		}
	}

	printf("Wspolrzedne pol rosna w dol i w prawo.\n\n");

	while (alive) {
		display();
		input();
	}

	display();

    return 0;
}

