#include <iostream>
#include <cmath>

const double PI = 3.14159265358979323846;

struct surf
{
    virtual double area( ) const = 0;

    virtual double circumference( ) const = 0;

    virtual surf* clone( ) const & = 0;

    virtual surf* clone( ) && = 0;

    virtual void print( std::ostream& ) const = 0;

    virtual ~surf( ) = default;
};

struct rectangle : public surf
{
    double x1, y1;
    double x2, y2;

    rectangle(double x1, double y1, double x2, double y2) : x1{x1}, y1{y1}, x2{x2}, y2{y2} { }

    double area( ) const override {
        return std::abs((x1 - x2) * (y1 - y2));
    }

    double circumference( ) const override {
        return 2 * (std::abs(x1 - x2) + std::abs(y1 - y2));
    }

    rectangle* clone( ) const & override {
        return new rectangle{*this};
    }

    rectangle* clone( ) && override {
        return new rectangle{std::move(*this)};
    }

    void print(std::ostream& out) const override {
        out << "(" << x1 << ", " << y1 << ")" << ", (" << x2 << ", " << y2 << ")\n";
    }
};

struct triangle : public surf
{
    double x1, y1; // Positions of corners.
    double x2, y2;
    double x3, y3;

    triangle(double x1, double y1, double x2, double y2, double x3, double y3) : x1{x1}, y1{y1}, x2{x2}, y2{y2}, x3{x3}, y3{y3} { }

    double area( ) const override {
        double halfCircuit = circumference() / 2;
        return sqrt(halfCircuit * (halfCircuit - sideLength(x1, y1, x2, y2)) * (halfCircuit - sideLength(x3, y3, x2, y2)) * (halfCircuit - sideLength(x1, y1, x3, y3)));
    }

    double sideLength(double x1, double y1, double x2, double y2) const {
        return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
    }

    double circumference( ) const override {
        return sideLength(x1, y1, x2, y2) + sideLength(x3, y3, x2, y2) + sideLength(x1, y1, x3, y3);
    }

    triangle* clone( ) const & override {
        return new triangle{*this};
    }

    triangle* clone( ) && override {
        return new triangle{std::move(*this)};
    }

    void print(std::ostream& out) const override {
        out << "(" << x1 << ", " << y1 << ")" << ", (" << x2 << ", " << y2 << ")" << ", (" << x3 << ", " << y3 << ")\n";
    }
};

struct circle : public surf
{
    double x; // Position of center.
    double y;
    double radius;

    circle(double x, double y, double r) : x{x}, y{y}, radius{r} { }

    double area( ) const override {
        return PI * radius * radius;
    }

    double circumference( ) const override {
        return 2 * PI * radius;
    }

    circle* clone( ) const & override {
        return new circle{*this};
    }

    circle* clone( ) && override {
        return new circle{std::move(*this)};
    }

    void print(std::ostream& out) const override {
        out << "(" << x << ", " << y << "), " << radius << "\n";
    }
};

struct surface
{
    surf* ref;

    surface( const surface& s ) : ref{s.ref -> clone()} { }

    surface( surface&& s ) : ref{std::move(*s.ref).clone()} { }

    surface( const surf& s ) : ref{s.clone()} { }

    surface( surf&& s ) : ref{std::move(s).clone()} { }

    void operator = ( const surface& s ) {
        *this = surface(s);
    }

    void operator = ( surface&& s ) {
        std::swap(ref, s.ref);
    }

    void operator = ( const surf& s ) {
        if (&s != ref) {
            delete ref;
            ref = s.clone();
        }
    }

    void operator = ( surf&& s ) {
        if (&s != ref) {
            delete ref;
            ref = std::move(s).clone();
        }
    }

    ~surface( )
    {
        delete ref;
    }

    const surf& getsurf( ) const { return *ref; }
    // There is no non-const access, because
    // changing would be dangerous.
};

std::ostream & operator <<(std::ostream &out, const surface &s) {
    s.ref -> print(out);
    return out;
}
