#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef struct wez* kolejka;

typedef struct wez
{
bool czy_liczba;
kolejka A;
kolejka B;
kolejka C;
kolejka D;
bool liczba;
bool czy_jednobarwny;
bool jak_jednobarwny;
bool czy_szachownica;
}wezel;

int tablica[1024][1024];
int rozn=0, szach=0;


void interfejs();
kolejka wczytaj(int *n);
void utworz_i_zapisz(kolejka ktory, int n, int x, int y);
void rotacja(kolejka ktory);
void negacja(kolejka ktory, int n);
void zeruj(kolejka ktory, int n);
void jedynki(kolejka ktory, int n);
void roznorodnosc(kolejka ktory, int n);
void szachownice(kolejka ktory, int n);

kolejka jak_gleboko(char *c, kolejka pomocniczy, int *n);
void czy_jednobarwny_i_szachownica(kolejka ktory);
void od_gory(kolejka ktory, kolejka dokad);



void buildMap(kolejka t, int n, int x, int y) {
    if (n == 1) {
        tablica[x][y] = t->liczba;
        return;
    }
    buildMap(t->A, n / 2, x, y);
    buildMap(t->B, n / 2, x, y + n / 2);
    buildMap(t->C, n / 2, x + n / 2, y + n / 2);
    buildMap(t->D, n / 2, x + n / 2, y);

}



void printMap( int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%d ", tablica[i][j]);
        }
        printf("\n");
    }
}





int main()
{
    interfejs();
}


void interfejs()
{
    int n;
    char c=0;
    kolejka pierwszy=(kolejka)malloc(sizeof(wezel));
    pierwszy=wczytaj(&n);
    if (n == 0)
        return;
    kolejka pomocniczy=(kolejka)malloc(sizeof(wezel));
    pomocniczy=pierwszy;

    int npom=n;
    /*printMap(n);
    printf("\n\n");
    buildMap(pierwszy, n, 0, 0);
    printMap(n);*/

    while (c!='.')
    {
        c=getchar();
        switch(c)
        {
            case '*':
            c=getchar();
            pomocniczy=jak_gleboko(&c, pomocniczy, &npom);
            if (pomocniczy)
                rotacja(pomocniczy);
            break;

            case '-':
            c=getchar();
            pomocniczy=jak_gleboko(&c, pomocniczy, &npom);
            if (pomocniczy)
            {
                negacja(pomocniczy, npom);
                if (pomocniczy != pierwszy)
                    od_gory(pierwszy, pomocniczy);
            }
            break;

            case '0':
            c=getchar();
            pomocniczy=jak_gleboko(&c, pomocniczy, &npom);
            if (pomocniczy)
            {
                zeruj(pomocniczy, npom);
                if (pomocniczy != pierwszy)
                    od_gory(pierwszy, pomocniczy);
            }
            break;

            case '1':
            c=getchar();
            pomocniczy=jak_gleboko(&c, pomocniczy, &npom);
            if (pomocniczy)
            {
                jedynki(pomocniczy, npom);
                if (pomocniczy != pierwszy)
                    od_gory(pierwszy, pomocniczy);
            }
            break;

            case '=':
            c=getchar();
            pomocniczy=jak_gleboko(&c, pomocniczy, &npom);
            if (pomocniczy)
                roznorodnosc(pomocniczy, npom);
            printf("%d\n", rozn);
            break;

            case '#':
            c=getchar();
            pomocniczy=jak_gleboko(&c, pomocniczy, &npom);
            if (pomocniczy)
                szachownice(pomocniczy, npom);
            printf("%d\n", szach);
            break;
        }
    rozn=szach=0;
    pomocniczy=pierwszy;
    npom=n;

    /*printf("\n\n");
    buildMap(pierwszy, n, 0, 0);
    printMap(n);*/
    }
}



void utworz_i_zapisz(kolejka ktory, int n, int x, int y)
{
    if (n == 0)
        return;
    else if (n == 1)
    {
        ktory->czy_liczba=1;
        ktory->liczba=tablica[x][y];
        ktory->A=NULL;
        ktory->B=NULL;
        ktory->C=NULL;
        ktory->D=NULL;
        ktory->czy_jednobarwny=1;
        ktory->jak_jednobarwny=ktory->liczba;
        ktory->czy_szachownica=0;
        return;
    }

    kolejka a=(kolejka)malloc(sizeof(wezel));
    kolejka b=(kolejka)malloc(sizeof(wezel));
    kolejka c=(kolejka)malloc(sizeof(wezel));
    kolejka d=(kolejka)malloc(sizeof(wezel));

    ktory->A=a;
    ktory->B=b;
    ktory->C=c;
    ktory->D=d;
    ktory->czy_liczba=0;
    ktory->liczba=0;

    utworz_i_zapisz(ktory->A, n/2, x, y);
    utworz_i_zapisz(ktory->B, n/2, x, y+n/2);
    utworz_i_zapisz(ktory->C, n/2, x+n/2, y+n/2);
    utworz_i_zapisz(ktory->D, n/2, x+n/2, y);
    czy_jednobarwny_i_szachownica(ktory);
}


kolejka wczytaj(int *n)
{
    char P1[2];
    scanf("%s", P1);

    scanf("%d", n);
    scanf("%d", n);

    for (int i=0; i<*n; i++)
    {
    P1[1]=getchar();
        for (int p=0; p<*n; p++)
        {
        tablica[i][p]=getchar();
        tablica[i][p]-='0';
        }
    }
    kolejka pierwszy=(kolejka)malloc(sizeof(wezel));
    utworz_i_zapisz(pierwszy, *n, 0, 0);
    return pierwszy;
}


void rotacja(kolejka zamiana)
{
    kolejka pomocniczaA=zamiana->A;
    kolejka pomocniczaB=zamiana->B;
    kolejka pomocniczaC=zamiana->C;
    kolejka pomocniczaD=zamiana->D;

    zamiana->A=pomocniczaD;
    zamiana->B=pomocniczaA;
    zamiana->C=pomocniczaB;
    zamiana->D=pomocniczaC;
}


void negacja(kolejka ktory, int n)
{
    if (n == 0)
        return;
    if (n == 1)
    {
        if (ktory->liczba == 1)
            ktory->liczba=ktory->jak_jednobarwny=0;
        else
            ktory->liczba=ktory->jak_jednobarwny=1;
        return;
    }

    negacja(ktory->A, n/2);
    negacja(ktory->B, n/2);
    negacja(ktory->C, n/2);
    negacja(ktory->D, n/2);

    czy_jednobarwny_i_szachownica(ktory);
}


void zeruj(kolejka ktory, int n)
{
    if (n == 0)
        return;
    else if (n == 1)
    {
        ktory->liczba=0;
        return;
    }

    zeruj(ktory->A, n/2);
    zeruj(ktory->B, n/2);
    zeruj(ktory->C, n/2);
    zeruj(ktory->D, n/2);

    czy_jednobarwny_i_szachownica(ktory);
}


void jedynki(kolejka ktory, int n)
{
    if (n == 0)
        return;
    else if (n == 1)
    {
    ktory->liczba=1;
    return;
    }

    jedynki(ktory->A, n/2);
    jedynki(ktory->B, n/2);
    jedynki(ktory->C, n/2);
    jedynki(ktory->D, n/2);

    czy_jednobarwny_i_szachownica(ktory);
}


void roznorodnosc(kolejka ktory, int n)
{

    if (n == 0)
        return;

    if (n == 1)
    {
        rozn++;
        return;
    }

    if (ktory->czy_jednobarwny)
    {
        rozn++;
        return;
    }

    else
    {
        roznorodnosc(ktory->A, n/2);
        roznorodnosc(ktory->B, n/2);
        roznorodnosc(ktory->C, n/2);
        roznorodnosc(ktory->D, n/2);
    }
}



void szachownice(kolejka ktory, int n)
{
    if (n == 1)
        return;

    if (ktory->czy_szachownica == 1)
        szach++;

    szachownice(ktory->A, n/2);
    szachownice(ktory->B, n/2);
    szachownice(ktory->C, n/2);
    szachownice(ktory->D, n/2);
}




kolejka jak_gleboko(char *c, kolejka pomocniczy, int *n)
{
    while ((*c)!='.' && (*c)!='\n')
    {
        (*n)/=2;
        if (pomocniczy->czy_liczba == 1)
            return NULL;
        switch(*c)
        {
        case 'a':
        pomocniczy=pomocniczy->A;
        break;

        case 'A':
        pomocniczy=pomocniczy->A;
        break;

        case 'b':
        pomocniczy=pomocniczy->B;
        break;

        case 'B':
        pomocniczy=pomocniczy->B;
        break;

        case 'c':
        pomocniczy=pomocniczy->C;
        break;

        case 'C':
        pomocniczy=pomocniczy->C;
        break;

        case 'd':
        pomocniczy=pomocniczy->D;
        break;

        case 'D':
        pomocniczy=pomocniczy->D;
        break;

        default:
        break;
        }
    (*c)=getchar();
    }
return pomocniczy;
}


void czy_jednobarwny_i_szachownica(kolejka ktory)
{
    if (ktory->A->czy_liczba == 0)
    {
        if (ktory->A->czy_jednobarwny == 1 && ktory->B->czy_jednobarwny == 1 && ktory->C->czy_jednobarwny == 1 && ktory->D->czy_jednobarwny == 1)
        {
            if(ktory->A->jak_jednobarwny == 1 && ktory->B->jak_jednobarwny == 1 && ktory->C->jak_jednobarwny == 1 && ktory->D->jak_jednobarwny == 1)
            {
                ktory->czy_jednobarwny=1;
                ktory->jak_jednobarwny=1;
            }

            else if (ktory->A->jak_jednobarwny == 0 && ktory->B->jak_jednobarwny == 0 && ktory->C->jak_jednobarwny == 0 && ktory->D->jak_jednobarwny == 0)
            {
                ktory->czy_jednobarwny=1;
                ktory->jak_jednobarwny=0;
            }
        }
        else
        {
            ktory->czy_jednobarwny=0;
            ktory->jak_jednobarwny=0;
        }
    }

    else if (ktory->A->czy_liczba == 1)
    {
        if ( ( ktory->A->liczba == 1 && ktory->B->liczba == 1 && ktory->C->liczba == 1 && ktory->D->liczba == 1))
        {
            ktory->czy_jednobarwny=1;
            ktory->jak_jednobarwny=1;
        }

        else if (( ktory->A->liczba == 0 && ktory->B->liczba == 0 && ktory->C->liczba == 0 && ktory->D->liczba == 0 ))
        {
            ktory->czy_jednobarwny=1;
            ktory->jak_jednobarwny=0;
        }

        else
        {
            ktory->czy_jednobarwny=0;
            ktory->jak_jednobarwny=0;
        }
    }


    //szachownica


    if (ktory->A->czy_liczba == 1)
    {
        if((ktory->A->liczba == 0 && ktory->C->liczba == 0 && ktory->B->liczba == 1 && ktory->D->liczba == 1)
        || (ktory->A->liczba == 1 && ktory->C->liczba == 1 && ktory->B->liczba == 0 && ktory->D->liczba == 0))
            ktory->czy_szachownica=1;
        else
            ktory->czy_szachownica=0;
    }

    else if (ktory->A->czy_liczba == 0)
    {
        if(ktory->A->czy_jednobarwny == 1 && ktory->B->czy_jednobarwny == 1 && ktory->C->czy_jednobarwny == 1 && ktory->D->czy_jednobarwny == 1)
            {if((ktory->A->jak_jednobarwny == 0 && ktory->B->jak_jednobarwny == 1 && ktory->C->jak_jednobarwny == 0 && ktory->D->jak_jednobarwny == 1)
            || (ktory->A->jak_jednobarwny == 1 && ktory->B->jak_jednobarwny == 0 && ktory->C->jak_jednobarwny == 1 && ktory->D->jak_jednobarwny == 0))
                {ktory->czy_szachownica=1;}}
        else
            ktory->czy_szachownica=0;
    }

}




void od_gory(kolejka ktory, kolejka dokad)
{
    if (ktory->czy_liczba == 1)
        return;
    /*if (ktory->A == dokad || ktory->B == dokad || ktory->C == dokad || ktory->D ==dokad)
    {
        czy_jednobarwny_i_szachownica(ktory);
        return;
    }*/
    od_gory(ktory->A, dokad);
    od_gory(ktory->B, dokad);
    od_gory(ktory->C, dokad);
    od_gory(ktory->D, dokad);

    czy_jednobarwny_i_szachownica(ktory);
}