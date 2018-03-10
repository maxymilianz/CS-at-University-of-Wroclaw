
#include <stdio.h>
#include <stdlib.h>
int **tab;
int n;
char c;
void get_input(void)

{
	for (int i=0 ;i<7;i++)
	{
		if(i==3) scanf("%d",&n);
		else getchar ();
	}

	int **tab=(int**)malloc(sizeof(int*)*n);

	for (int i=0;i<n;i++)
	{
		tab[i]=malloc(sizeof(int)*n);
	}

	for (int i=0;i<n;i++)
	{
		for (int j=0;j<n;j++)
		{
			tab[i][j]=(int)getchar()-(int)'0';
		}
		getchar();
	}


}


int main ()

{
	get_input();
	printf("%d%c",n,c);

	for (int i=0;i<n;i++)
	{
		for (int j=0;j<n;j++)
		{
			printf("%d",tab[i][j]);
		}
		printf("\n");
	}
}
