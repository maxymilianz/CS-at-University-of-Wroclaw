#pragma once

#include <stdlib.h>

typedef int str;

typedef struct DrzewoBinarne {
	str w;
	DrzewoBinarne *l = NULL;
	DrzewoBinarne *p = NULL;
};

DrzewoBinarne * noweDrzewo(str w) {
	DrzewoBinarne *d = (DrzewoBinarne *)malloc(sizeof *d);
	(*d).w = w, (*d).l = NULL, (*d).p = NULL;
	return d;
}

void wstaw(DrzewoBinarne *d, str w) {
	if (w < (*d).w) {
		if ((*d).l != NULL)
			wstaw((*d).l, w);
		else
			(*d).l = noweDrzewo(w);
	}
	else {
		if ((*d).p != NULL)
			wstaw((*d).p, w);
		else
			(*d).p = noweDrzewo(w);
	}
}

DrzewoBinarne * szukaj(DrzewoBinarne *d, str w) {
	if (d == NULL)
		return NULL;
	else if (w < (*d).w) {
		if ((*d).l != NULL)
			szukaj((*d).l, w);
		else
			return NULL;
	}
	else if (w > (*d).w) {
		if ((*d).p != NULL)
			szukaj((*d).p, w);
		else
			return NULL;
	}
	else
		return d;
}

int rozmiar(DrzewoBinarne *d) {
	if (d == NULL)
		return 0;
	else if ((*d).l == NULL && (*d).p == NULL)
		return 1;
	else if ((*d).l == NULL)
		return rozmiar((*d).p) + 1;
	else if ((*d).p == NULL)
		return rozmiar((*d).l) + 1;
	else
		return rozmiar((*d).l) + rozmiar((*d).p) + 1;
}