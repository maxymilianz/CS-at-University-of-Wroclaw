#include <stdio.h>
#include <stdlib.h>
int x,y,p,l;
char*ruchy;
char**tab1,**tab2,**tab3,**tab4;
char** input_data(void)
{
	scanf("%d %d",&x,&y);
	getchar();
	char **tab;
	tab=(char** )malloc(sizeof(char*)*y);
	for (int i =0;i<y;i++)
	{
			tab[i]=(char*)malloc(sizeof(char)*x);
	}
	for(int i =0; i<y;i++)
	{
		for(int j=0;j<x;j++)
		{
			scanf("%c",&tab[i][j]);
		}
		getchar();
	}

	scanf("%d %d",&p,&l);
	getchar();
	ruchy=(char*)malloc(sizeof(char)*l);
	for(int i=0;i<l;i++)
	{
		scanf("%c",&ruchy[i]);
	}
	return tab;
}

char** make_controlling_tab(void)
{
    char** tab=(char** )malloc(sizeof(char*)*y);
	for (int i =0;i<y;i++)
	{
			tab[i]=(char*)malloc(sizeof(char)*x);
	}
	for(int i =0; i<y;i++)
	{
		for(int j=0;j<x;j++)
		{
			 tab[i][j]='0';
		}

	}
	return tab;
}
void clear(char**tab)
{
    for(int i=0; i<y;i++)
	{
		for(int j=0;j<x;j++)
		{
			 tab[i][j]='0';
		}

	}
}
void print_data(char** tab)
{
    for(int i=0;i<y;i++)
    {
        for(int j=0;j<x;j++)
        {
            printf("%c",tab[i][j]);
        }
        printf("\n");
    }
}

int if_empty(int y1,int x1,char**tab)
{
	if(x1>=0 && x1<x &&  y1>=0 && y1<y && tab[y1][x1]!='#') return 1;
	else return 0;
}

void check (int y, int x,int i,int p1,char**tab)
{
		if (i==l && p1==p) {tab[y][x]='X'; return ;}
		char c=ruchy[i];

		switch (c)
		{
			case 'G':
			{
				if(if_empty(y-1,x,tab) && tab1[y][x]!='G') {tab1[y][x]='G'; check(y-1,x,i+1,p1+1,tab);}
				break;
			}
			case 'D':
			{
				if(if_empty(y+1,x,tab)&& tab2[y][x]!='D') {tab2[y][x]='D'; check(y+1,x,i+1,p1+1,tab);}
				break;
			}
			case 'P':
			{
				if(if_empty(y,x+1,tab)&& tab3[y][x]!='P') {tab3[y][x]='P'; check(y,x+1,i+1,p1+1,tab);}
				break;
			}
			case 'L':
			{
				if(if_empty(y,x-1,tab)&& tab4[y][x]!='L') {tab4[y][x]='L'; check(y,x-1,i+1,p1+1,tab);}
				break;
			}
			case 'S':
			{
				check(y,x,i+1,p1,tab);
				break;
			}
			case '?':
			{


				if(if_empty(y-1,x,tab)&& tab1[y][x]!='G')  {tab1[y][x]='G';check(y-1,x,i+1,p1+1,tab);}

				if(if_empty(y+1,x,tab)&& tab2[y][x]!='D')  {tab2[y][x]='D';check(y+1,x,i+1,p1+1,tab);}

				if(if_empty(y,x+1,tab)&& tab3[y][x]!='P')  {tab3[y][x]='P';check(y,x+1,i+1,p1+1,tab);}

				if(if_empty(y,x-1,tab)&& tab4[y][x]!='L')  {tab4[y][x]='L';check(y,x-1,i+1,p1+1,tab);}
                check(y,x,i+1,p1,tab);
				break;
			}
			default:
            break;
		}
		 tab1[y][x]='0';
		 tab2[y][x]='0';
		 tab3[y][x]='0';
		 tab4[y][x]='0';
}
int main()
{
   char**tab=input_data();
   tab1=make_controlling_tab();
   tab2=make_controlling_tab();
   tab3=make_controlling_tab();
   tab4=make_controlling_tab();
   for(int i=0;i<y;i++)
    {
        for(int j=0;j<x;j++)
       {
        if(tab[i][j]!='#') {
            check(i,j,0,0,tab);}


        }

   }

  print_data(tab);
  for(int i=0;i<y;i++)
  {
      free(tab[i]);
  }
  free(tab);
  return 0;
}
