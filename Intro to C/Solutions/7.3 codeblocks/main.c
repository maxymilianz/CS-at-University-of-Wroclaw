#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

char map[101][101];
char maphelp[101][101];
int n, m, p, l;
char sequence[101];
bool used[101][101][101][4];
bool usedhelp[101][101][4];

enum
{
lewo=0,
gora=1,
dol=2,
prawo=3
};

void CopyUsed(int first, int second)
{
for (int i=0; i<101; i++)
    for (int j=0; j<101; j++)
        for (int p=0; p<4; p++)
            used[second][i][j][p]=used[first][i][j][p];
}

void CheckForDifferencesAndReplace(int wheren, int wherem)
{
for (int i=0; i<4; i++)
{
    if (used[wheren][wherem][i] == 1 && usedhelp[wheren][wherem][i] == 0)
    {
    used[0][wheren][wherem][i]=0;
    }
}
}

void NotUsed()
{
for (int f=0; f<101; f++)
for (int i=0; i<101; i++)
    for (int j=0; j<101; j++)
        for (int p=0; p<4; p++)
        {
        used[f][i][j][p]=0;
        }
}

void WriteToMap()
{
    for (int i=0; i<n; i++)
        for (int j=0; j<=m; j++)
        {
        scanf("%c", &map[i][j]);
        maphelp[i][j]=map[i][j];
        }
}

void GetSequence()
{
int i;
    for (i=0; i<l; i++)
        scanf("%c", &sequence[i]);
}

void Comparison()
{
for (int i=0; i<n; i++)
    for (int j=0; j<=m; j++)
        if (maphelp[i][j] == '.' && map[i][j] == '#')
            map[i][j]='.';
}

void CheckForPositions(int where, int wheren, int wherem, int ruchy, int dimersion)
{
//printf("Usedlewo %d wherem %d wheren %d\n", used[wheren][wherem][lewo], wherem, wheren);
    if (wheren < 0 || wherem < 0)
        return;

    if (wheren >= n || wherem >= m)
        return;

    if (map[wheren][wherem] == '#')
        return;


    /*if (where==l)
    {
    printf("Where l %d %d\n\n", wheren, wherem);
    }

    if (ruchy==p)
    {
    printf("Ruchy p %d %d\n\n", wheren, wherem);
    }*/


    if (where == l && ruchy == p)
    {
    map[wheren][wherem]='X';
    return;
    }

    if (sequence[where] == 'L')
    {
        if (used[dimersion][wheren][wherem][lewo] == 1)
            return;
        else
        {
        used[dimersion][wheren][wherem][lewo]=1;
        CheckForPositions(where+1, wheren, wherem-1, ruchy+1, dimersion);
        }
    }

    else if (sequence[where] == 'P')
    {
        if (used[dimersion][wheren][wherem][prawo] == 1)
            return;
        else
        {
        used[dimersion][wheren][wherem][prawo]=1;
        CheckForPositions(where+1, wheren, wherem+1, ruchy+1, dimersion);
        }
    }

    else if (sequence[where] == 'G')
    {
        if (used[dimersion][wheren][wherem][gora] == 1)
            return;
        else
        {
        used[dimersion][wheren][wherem][gora]=1;
        CheckForPositions(where+1, wheren-1, wherem, ruchy+1, dimersion);
        }
    }

    else if (sequence[where] == 'D')
    {
        if (used[dimersion][wheren][wherem][dol] == 1)
            return;
        else
        {
        used[dimersion][wheren][wherem][dol]=1;
        CheckForPositions(where+1, wheren+1, wherem, ruchy+1, dimersion);
        }
    }
    else if (sequence[where] == 'S')
        CheckForPositions(where+1, wheren, wherem, ruchy, dimersion);

    else if (sequence[where] == '?')
{

    CheckForPositions(where+1, wheren, wherem, ruchy, dimersion); //postoj
    //CheckForDifferencesAndReplace(wheren, wherem);
        if (used[dimersion][wheren][wherem][lewo] == 0)
        {
        used[dimersion][wheren][wherem][lewo]=1;
        CopyUsed(dimersion, dimersion+1);

        CheckForPositions(where+1, wheren, wherem-1, ruchy+1, dimersion+1); //lewo
        }
   //CheckForDifferencesAndReplace(wheren, wherem);
        if (used[dimersion][wheren][wherem][prawo] == 0)
        {
        used[dimersion][wheren][wherem][prawo]=1;
        CopyUsed(dimersion, dimersion+1);
        CheckForPositions(where+1, wheren, wherem+1, ruchy+1, dimersion+1); //prawo
        }
    //CheckForDifferencesAndReplace(wheren, wherem);

        if(used[dimersion][wheren][wherem][gora] == 0)
        {
        used[dimersion][wheren][wherem][gora]=1;
        CopyUsed(dimersion, dimersion+1);
        CheckForPositions(where+1, wheren-1, wherem, ruchy+1, dimersion+1); //gora
        }
    //CheckForDifferencesAndReplace(wheren, wherem);
        if (used[dimersion][wheren][wherem][dol] == 0)
        {
        used[dimersion][wheren][wherem][dol]=1;
        CopyUsed(dimersion, dimersion+1);
        CheckForPositions(where+1, wheren+1, wherem, ruchy+1, dimersion+1); //dol
        }
    }
}

void PrintArray()
{
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<=m; j++)
            printf("%c", map[i][j]);
    }
    printf("\n");
}

void CheckFromAllPositions()
{
    for (int i=0; i<n; i++)
        for (int j=0; j<m; j++)
        {
        CheckForPositions(0, i, j, 0, 0);
        NotUsed();
        //printf("Mapa dla i=%d oraz j=%d:\n", i, j);
        //PrintArray();
        }
}

void FunctionCreatedOnlyToReplaceMain()
{
scanf("%d%d", &m, &n);
getchar();
WriteToMap();
scanf("%d%d", &p, &l);
getchar();
//PrintArray();
GetSequence();
CheckFromAllPositions();
PrintArray();

}




int main()
{
FunctionCreatedOnlyToReplaceMain();
}
