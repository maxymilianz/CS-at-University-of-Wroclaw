#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>
#define ROZMIAR 1000000

void Clear_Buffer(char* b);
char* Assign_Block(long l);
char* Find_Block(char c, long l);
bool Set_Block(char* b, long l, char c);
bool Release_Block(char* b, long l, char c);
char* Relocate();
bool Process_Request();
void Output_Buffer_State();



char bufor[ROZMIAR];
char* wskaznik=bufor;
int rozmiar;

int main()
{
Process_Request();
}



void Clear_Buffer(char* b)
{
for (int i=0; i<rozmiar; i++, b++)
    (*b)=0;
*b='9';
}

char* Assign_Block(long l)
{
    if (l<=0 || l>rozmiar)
    {
    printf("\nAssign_Block: wrong input data\n");
    exit(0);
    }

char* pomocniczy;
pomocniczy=wskaznik;
long lpom=l;
wskaznik--;
    while(pomocniczy!=wskaznik)
    {
        if (*pomocniczy==0)
            lpom--;
        if (lpom==0)
        {
        wskaznik=(pomocniczy-(l-1));
        return (pomocniczy-(l-1));
        }
        if (*pomocniczy!=0)
            lpom=l;
        pomocniczy++;
        if (*pomocniczy=='9')
        {
        lpom=l;
        pomocniczy=bufor;
        }
    }
wskaznik++;
pomocniczy=Relocate();
lpom=l;
if(!pomocniczy)
{
printf("\nAssign_Block: wrong input data\n");
exit(0);
}

    while(*pomocniczy!='9')
    {
        if (*pomocniczy==0)
            lpom--;
        if (lpom==0)
        {
        wskaznik=(pomocniczy-(l-1));
        return (pomocniczy-(l-1));
        }
        if (*pomocniczy!=0)
            lpom=l;
        pomocniczy++;
    }
printf("\nAssign_Block: wrong input data\n");
exit(0);
}

char* Find_Block(char c, long l)
{
char* pomocniczy=wskaznik;
long lpom=l;
    if (c<'A' || c>'Z')
    {
        if(c<'a' || c>'z')
        {
        printf("\nSet_Block: wrong input data\n");
        exit(0);
        }
        else
            c-=('a'-'A');
    }
//printf("\n%li\n%c\n", l, c);
    while(*pomocniczy!='9')
    {
        if (*pomocniczy==c)
            lpom--;
        if (lpom==0)
        {
        wskaznik=(pomocniczy-(l-1));
        return (pomocniczy-(l-1));
        }
        if (*pomocniczy!=c)
            lpom=l;
        pomocniczy++;
    }
pomocniczy=bufor;
lpom=l;
    while(*pomocniczy!='9')
    {
        if (*pomocniczy==c)
            lpom--;
        if (lpom==0)
        {
        wskaznik=(pomocniczy-(l-1));
        return (pomocniczy-(l-1));
        }
        if (*pomocniczy!=c)
            lpom=l;
        pomocniczy++;
    }
printf("\nFind_Block: wrong input data\n");
exit(0);
}

bool Set_Block(char* b, long l, char c)
{
//printf("\n\n%c\n\n%li\n\n", c, l);
b=Assign_Block(l);
if (!b)
{
printf("\nSet_Block: wrong input data\n");
exit(0);
}
wskaznik=b;
    if (c<'A' || c>'Z')
    {
        if(c<'a' || c>'z')
        {
        printf("\nSet_Block: wrong input data\n");
        exit(0);
        }
        else
            c-=('a'-'A');
    }

    for (; l>0; l--, b++)
        (*b)=c;

return 1;
}

bool Release_Block(char* b, long l, char c)
{
if (l<=0)
{
printf("\nRelease_Block: wrong input data\n");
exit(0);
}

b=Find_Block(c, l);

if (!b)
{
printf("\nRelease_Block: wrong input data\n");
exit(0);
}

wskaznik=b;
for (; l>0; l--, b++)
    (*b)=0;
return 1;
}

char* Relocate()
{
char* pomocniczy=bufor;
char* puste=0;
bool czy_zostalo=1;
    while((*pomocniczy)!='9')
    {
        puste=pomocniczy;
            while (*puste==0)
            {
            czy_zostalo=0;
                while ((*pomocniczy)!='9')
                {
                if(*pomocniczy!=0)
                    czy_zostalo=1;
                *pomocniczy=*(pomocniczy+1);
                pomocniczy++;
                }
            *(pomocniczy-1)=0;
            pomocniczy=puste;
            if (!czy_zostalo)
                break;
            }
        pomocniczy++;
        if (!czy_zostalo)
            break;
    }


pomocniczy=bufor;
while((*pomocniczy) && (*pomocniczy++)!='9');
if(*pomocniczy=='9')
    return NULL;
return pomocniczy;
}

bool Process_Request()
{
scanf("%d", &rozmiar);
Clear_Buffer(bufor);
/*for (int i=0; i<rozmiar; i++)
        printf("%c", bufor[i]);*/
int a=0, b=0, c=0;
bool dobrze=1;
c=scanf("%d", &a);
b=getchar();
    while(b!=EOF && c!=EOF)
    {
        if(a==0)
        {
        printf("\nProcess_Request: zero length blocks not allowed\n");
        exit(0);
        }

        else if(a<0)
        {
        a*=-1;
        dobrze=Release_Block(wskaznik, a, b);
            if(!dobrze)
                return 0;
        }

        else
        {
        dobrze=Set_Block(wskaznik, a, b);
            if(!dobrze)
                return 0;
        }
    c=scanf("%d", &a);
    b=getchar();
    while(isspace(b))
        b=getchar();

    /*for (int i=0; i<rozmiar; i++)
    {if (bufor[i])
        printf("%c", bufor[i]);
    else
        printf("-");
    }
    printf("\n");*/
    }
Output_Buffer_State();
return 1;
}

void Output_Buffer_State()
{
char *pomocniczy=bufor;
int licznik=0;
char znak;
znak=*pomocniczy;
pomocniczy++;
licznik++;
    while(*pomocniczy!='9')
    {
    //printf(" %c ", *pomocniczy);
    if (*pomocniczy==znak)
        licznik++;
    else
    {
    if (*(pomocniczy-1))
        printf("%d%c ", licznik, *(pomocniczy-1));
    else
        printf("%d%c ", licznik, '*');
    if(*pomocniczy!='9')
        licznik=1;
    }
    znak=*pomocniczy;
    pomocniczy++;
    }
    if(znak)
        printf("%d%c ", licznik, znak);
    else
        printf("%d%c ", licznik, '*');
}