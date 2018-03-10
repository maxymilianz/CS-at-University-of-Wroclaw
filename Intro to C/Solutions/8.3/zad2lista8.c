
#include <stdio.h>
#include <stdlib.h>
char tekst [12];
int **tab;
int i=0,c=0,n,xp,yp,xk,yk,if_end=0;


struct node
{
	int pixel;
	struct node * A;
	struct node * B;
	struct node * C;
	struct node * D;
};
/*
void test_tree (struct node* current_node)

{
	if((*current_node).pixel==0) printf("0");
	else if((*current_node).pixel==1) printf("1");
	else
	{
		printf("2");
		test_tree((*current_node).A);
		test_tree((*current_node).B);
		test_tree((*current_node).C);
		test_tree((*current_node).D);
	}

}*/

void make_tree (int x ,int y,int x1,int y1,struct node * current_node)
{
	int z=0,o=0;
	for (int i=y ;i<=y1;i++)
	{
		for (int j=x;j<=x1;j++)
		{
			if (tab[i][j]==0)z++;
			else if(tab[i][j]==1)o++;
		}
	}
	if 		(z==(x1-x+1)*(y1-y+1))
	{
			(*current_node).pixel=0;
			(*current_node).A=NULL;
			(*current_node).B=NULL;
			(*current_node).C=NULL;
			(*current_node).D=NULL;
	}
	else if (o==(x1-x+1)*(y1-y+1))
		{
			(*current_node).pixel=1;
			(*current_node).A=NULL;
			(*current_node).B=NULL;
			(*current_node).C=NULL;
			(*current_node).D=NULL;
		}
	else
	{
		(*current_node).A=(struct node*)malloc(sizeof(struct node));
		(*current_node).B=(struct node*)malloc(sizeof(struct node));
		(*current_node).C=(struct node*)malloc(sizeof(struct node));
		(*current_node).D=(struct node*)malloc(sizeof(struct node));

		(*current_node).pixel=2;
		make_tree(x,y,(x1+x)/2,(y1+y)/2,(*current_node).A);
		make_tree((x1+x)/2+1,y,x1,(y1+y)/2,(*current_node).B);
		make_tree((x1+x)/2+1,(y1+y)/2+1,x1,y1,(*current_node).C);
		make_tree(x,(y1+y)/2+1,(x1+x)/2,y1,(*current_node).D);

	}

}

void get_input(void)
{
	for (int i=0 ;i<7;i++)
	{
		if(i==3) scanf("%d",&n);
		else getchar ();
	}

	tab=(int**)malloc(sizeof(int*)*n);

	for (int i=0;i<n;i++)
	{
		tab[i]=(int*)malloc(sizeof(int)*n);
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

void get_command (void)
{
	char c;
	for (int i=0;i<12;i++)
	{
		if((c=getchar())=='\n' || c==EOF ) {tekst[i]='\0'; break;}
		else tekst[i]=c;
	}
}



struct node *  find_node (struct node * current_node ,int i)
{
	char c;
	if (tekst[i]=='\0') return current_node;
	else if (tekst[i]>='A'&&tekst[i]<='Z') c=tekst[i]+('a'-'A');
	else c=tekst[i];
	switch (c)
	{
		case 'a': { find_node((*current_node).A,i+1);break;}
		case 'b': { find_node((*current_node).B,i+1);break;}
		case 'c': { find_node((*current_node).C,i+1);break;}
		case 'd': { find_node((*current_node).D,i+1);break;}
	}
}

void swap (struct node * current_node )
{
	struct node *a=(*current_node).A;
	struct node *b=(*current_node).B;
	struct node *c=(*current_node).C;
	struct node *d=(*current_node).D;
	(*current_node).A=d;
	(*current_node).B=a;
	(*current_node).C=b;
	(*current_node).D=c;
}

void diversity(struct node * current_node)
{
	if ((*current_node).pixel==0 || (*current_node).pixel==1) i++;
	else
	{
		diversity((*current_node).A);
		diversity((*current_node).B);
		diversity((*current_node).C);
		diversity((*current_node).D);
	}

}



void negation(struct node * current_node)
{
	if ((*current_node).pixel==1) (*current_node).pixel=0;
	else if ((*current_node).pixel==0) (*current_node).pixel=1;
	else
	{
		negation((*current_node).A);
		negation((*current_node).B);
		negation((*current_node).C);
		negation((*current_node).D);
	}
}

void ones(struct node * current_node)
{
	if ((*current_node).pixel==0) (*current_node).pixel=1;
	else if ((*current_node).pixel==1) (*current_node).pixel=1;
	else
	{
		ones((*current_node).A);
		ones((*current_node).B);
		ones((*current_node).C);
		ones((*current_node).D);
	}
}


void zeros(struct node * current_node)
{
	if ((*current_node).pixel==0) (*current_node).pixel=0;
	else if ((*current_node).pixel==1) (*current_node).pixel=0;
	else
	{
		zeros((*current_node).A);
		zeros((*current_node).B);
		zeros((*current_node).C);
		zeros((*current_node).D);
	}
}


int main ()
{
	get_input();
	xp=0; yp=0; xk=n-1; yk=n-1;
	char c;
	struct node r;
	struct node *root=&r;
	make_tree(xp,yp,xk,yk,root);
	while((c=getchar())!='.')
	{
		ungetc(c,stdin);
		get_command();
		struct node * current_node=find_node(root,1);

       // printf("%d",(*current_node).pixel);
		switch(tekst[0])
		{
			case '-':{negation(current_node);break;}
			case '0':{zeros(current_node);break;}
			case '1':{ones(current_node);break;}
		  	case '=':{diversity(current_node) ;printf ("\n%d",i);i=0; break;}
           		case '#':{chess(current_node);printf("\n%d",c);c=0; break; }
			case '*':{swap(current_node);break;}
		}

	}



	return 0;
}
