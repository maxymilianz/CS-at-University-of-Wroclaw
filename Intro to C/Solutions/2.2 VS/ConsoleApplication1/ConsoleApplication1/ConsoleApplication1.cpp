// ConsoleApplication1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{
	int prevCh = EOF, ch = getchar(), znaki = 0, litery = 0, cyfry = 0, wyrazy = 0, bZnaki = 0, samog = 0, spolg = 0, DL = 0, ml = 0, znakiP = 0, wyraz;

	while (ch != EOF) {
		wyraz = 0;

		while (ch >= 'A' && ch <= 'Z' || ch >= 'a' && ch <= 'z') {
			litery++;
			znaki++;

			if (ch == 'a' || ch == 'o' || ch == 'u' || ch == 'e' || ch == 'i' || ch == 'y' || ch == 'A' || ch == 'O' || ch == 'U' || ch == 'E' || ch == 'I' || ch == 'Y') {
				samog++;
			}
			else {
				spolg++;
			}

			if (ch >= 'A' && ch <= 'Z') {
				DL++;
			}
			else {
				ml++;
			}

			if ((prevCh == EOF || prevCh == ' ' || prevCh == '\t' || prevCh == '\n' || prevCh == '\v' || prevCh == '\f' || prevCh == '\r') && wyraz == 0)
				wyraz = 1;

			prevCh = ch;
			ch = getchar();
		}

		if (ch >= '0' && ch <= '9') {
			cyfry++;
		}
		else if (ch == ' ' || ch == '\t' || ch == '\n' || ch == '\v' || ch == '\f' || ch == '\r') {
			bZnaki++;

			if ((prevCh >= 'A' && prevCh <= 'Z' || prevCh >= 'a' && prevCh <= 'z') && wyraz == 1) {
				wyraz = 0;
				wyrazy++;
			}
		}
		else if (ch == ',' || ch == '.' || ch == ':' || ch == '!' || ch == '?') {
			znakiP++;

			if ((prevCh >= 'A' && prevCh <= 'Z' || prevCh >= 'a' && prevCh <= 'z') && wyraz == 1) {
				wyraz = 0;
				wyrazy++;
			}
		}

		prevCh = ch;
		ch = getchar();
		znaki++;
	}

	if ((prevCh >= 'A' && prevCh <= 'Z' || prevCh >= 'a' && prevCh <= 'z') && wyraz == 1) {
		wyrazy++;
	}

	printf("znakow: %d\nliter: %d\ncyfr: %d\nwyrazow: %d\nbialych znakow: %d\nsamoglosek: %d\nspolglosek: %d\nduzych liter: %d\nmalych liter: %d\nznakow przestankowych: %d\n", znaki, litery, cyfry, wyrazy, bZnaki, samog, spolg, DL, ml, znakiP);

	return 0;
}
