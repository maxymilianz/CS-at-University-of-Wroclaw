#include "grid.h"

std::ostream& operator <<(std::ostream& stream, const grid& g) {
    for (size_t i = 0; i < g.ysize; i++) {
        for (size_t j = 0; j < g.xsize; j++)
            stream << g[i][j].s0 << ' ';

        stream << '\n';
    }

    return stream;
}


  void grid::plot( ) const {
    	for( int  j = 0; j < ysize; j++) {
    		for (int  i = 0; i < xsize; i++) {
    			if ((*this)[i][j].s0) {
    				i -= xsize / 2;
    				j -= ysize / 2;

    				glBegin(GL_POLYGON);
    				glVertex3f( i, j, 0);
    				glVertex3f( i + 1, j, 0);
    				glVertex3f( i + 1, j + 1, 0);
    				glVertex3f( i, j + 1, 0);
    				glEnd();
    				
    				i += xsize / 2;
    				j += ysize / 2;
    			}
    		}
    	}
    	
    	glFlush();
    }




std::ostream& operator <<(std::ostream& stream, const grid::wrongchar& w) {
    stream << w.c << " (" << w.x << ", " << w.y << ")\n";

    return stream;
}
