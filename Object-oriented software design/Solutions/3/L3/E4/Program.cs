using System;
using System.Collections.Generic;

namespace E4 {
	public abstract class Figure {
		public abstract double Area();
	}

	public class Rectangle : Figure {
		private int w, h;

		public Rectangle(int w, int h) {
			this.w = w;
			this.h = h;
		}

		public override double Area() {
			return w * h;
		}

		public int W {
			get { return w; }
			set { w = value; }
		}

		public int H {
			get { return h; }
			set { h = value; }
		}
	}

	public class Square : Figure {
		private int a;

		public Square(int a) {
			this.a = a;
		}

		public override double Area() {
			return a * a;
		}

		public int A {
			get { return a; }
			set { a = value; }
		}
	}
	
	internal class Program {
		public static void Main(string[] args) {
			Rectangle rectangle = new Rectangle(19, 97);
			Console.WriteLine(rectangle.Area());

			Square square = new Square(1997);
			Console.WriteLine(square.Area());
		}
	}
}