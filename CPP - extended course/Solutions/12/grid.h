
#ifndef GRID_INCLUDED
#define GRID_INCLUDED 1
/*
#include <SFML/Window.hpp>
#include <SFML/OpenGL.hpp>*/
#include <initializer_list>
#include <iostream>
#include <vector>
#include "figure.h"

#include <cstring>
#include <climits>

class grid
{
    struct cell {
        bool s0; // Current state.
        bool s1; // Next state.

        cell( )
        : s0( false ),
        s1( false ) {}
    };

    unsigned int xsize;
    unsigned int ysize;
    cell* c;

public:
    // Points in the grid are indexed in the computer graphics way,
    // not in the matrix way.

    // Points are indexed in the computer graphics way, not in
    // the matrix way.
    //
    //  (0,ysize-1)   .....     (xsize-1,ysize-1)
    //      .                          .
    //      .                          .
    //    (0,0)       .....        (xsize-1,0)


    struct wrongchar
    {
        char c;                 // Character that we didn't like.
        unsigned int x;         // Its position.
        unsigned int y;


        wrongchar( char c, unsigned int x, unsigned int y )
        : c{c}, x{x}, y{y}
        { }
    };

    inline bool isonchar( char c ) { return c == 'X' || c == '#' ||
    c == 'O' || c == '0'; }

    inline bool isoffchar( char c ) { return c == '.'; }


    grid( unsigned int xsize, unsigned int ysize )
    : xsize( xsize ),
    ysize( ysize ),
    c( new cell [xsize * ysize] )
    { }

    grid(const grid& g) : xsize{g.xsize}, ysize{g.ysize}, c{new cell[xsize * ysize]} {
        for (size_t i = 0; i < ysize && i != UINT_MAX; i++)
            for (size_t j = 0; j < xsize && j != UINT_MAX; j++)
                c[i * xsize + j] = g.c[i * xsize + j];
    }

    grid( grid&& g) : xsize{g.xsize}, ysize{g.ysize}, c{std::move(g.c)} { }

    void operator =(const grid& g) {
        *this = grid(g);
    }

    void operator =(grid&& g) {
        xsize = g.xsize;
        ysize = g.ysize;
        std::swap(c, g.c);
    }

    ~grid( ) {
        delete c;
    }

    cell* operator [] ( unsigned int x ) { return c + x * ysize; }

    const cell* operator [] ( unsigned int x ) const { return c + x * ysize; }

    void plot( ) const;

#if 0
     void plot( ) const {
    	for (size_t j = 0; j < ysize; j++) {
    		for (size_t i = 0; i < xsize; i++) {
    			if ((*this)[i][j].s0)
    			   std::cout << '#';
    		    else
    		       std::cout << ' ';
    		}
    		std::cout << "\n";
    	}
       std::cout << "\n\n\n";
    }
#endif



    void clear( ) {
        for (size_t i = 0; i < ysize && i != UINT_MAX; i++)
            for (size_t j = 0; j < xsize && j != UINT_MAX; j++)
                c[i * xsize + j] = cell();
    }

    void addfigure(unsigned int x, unsigned int y, std::initializer_list< const char* > p) {
        for (auto i = p.begin(); i != p.end(); i++, y++) {
            size_t tempX = x;

            for (size_t j = 0; j < strlen(*i); j++, tempX++) {
                c[y * xsize + tempX].s0 = isonchar((*i)[j]);
            }
        }
    }

    void addfigure(unsigned int x, unsigned int y, const figure& f) {
        for (auto i = f.repr.begin(); i != f.repr.end(); i++, y++) {
            size_t tempX = x;

            for (size_t j = 0; (*i)[j] != 0; j++, tempX++) {
                c[y * xsize + tempX].s0 = isonchar((*i)[j]);
            }
        }
    }

    int countLivingNeighbours(size_t x, size_t y) {
        int res = 0;

        for (int i = -1; i < 2; i++)
            for (int j = -1; j < 2; j++)
                if (y + i >= 0 && y + i < ysize && x + j >= 0 && x + j < xsize)
                	res += c[(y + i) * xsize + x + j].s0;

        return res - c[y * xsize + x].s0;
    }

    void nextgeneration() {
        for (size_t i = 0; i < ysize && i != UINT_MAX; i++) {
            for (size_t j = 0; j < xsize && j != UINT_MAX; j++) {
                int neighbours = countLivingNeighbours(j, i);
                c[i * xsize + j].s1 = neighbours == 3 || c[i * xsize + j].s0 && neighbours == 2;
            }
        }

        for (size_t i = 0; i < ysize && i != UINT_MAX; i++)
            for (size_t j = 0; j < xsize && j != UINT_MAX; j++)
                c[i * xsize + j].s0 = c[i * xsize + j].s1;
    }

    friend std::ostream& operator << ( std::ostream& stream, const grid& g );
};

std::ostream& operator <<(std::ostream& stream, const grid& g);

std::ostream& operator <<(std::ostream& stream, const grid::wrongchar& w);

#endif
