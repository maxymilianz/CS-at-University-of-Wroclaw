
using System;
using System.Collections;

namespace E2 {
	public interface IShape {
		
	}

	public class Square : IShape {
		public int A { get; private set; }
		
		public Square(int a) {
			A = a;
		}
	}

	public class Rectangle : IShape {
		public int A { get; private set; }
		public int B { get; private set; }

		public Rectangle(int a, int b) {
			A = a;
			B = b;
		}
	}

	public interface IShapeFactoryWorker {
		string GetShapeName();

		IShape CreateShape(params object[] parameters);
	}

	public class SquareFactoryWorker : IShapeFactoryWorker {
		public static readonly string NotEnoughParamsEx = "Not enough parameters to create a Square.";

		public string GetShapeName() {
			return "Square";
		}

		public IShape CreateShape(params object[] parameters) {
			if (parameters.Length > 0)
				return new Square((int) parameters[0]);
			throw new Exception(NotEnoughParamsEx);
		}
	}

	public class RectangleFactoryWorker : IShapeFactoryWorker {
		public static readonly string NotEnoughParamsEx = "Not enough parameters to create a Rectangle.";
		
		public string GetShapeName() {
			return "Rectangle";
		}

		public IShape CreateShape(params object[] parameters) {
			if (parameters.Length > 1)
				return new Rectangle((int) parameters[0], (int) parameters[1]);
			throw new Exception(NotEnoughParamsEx);
		}
	}
	
	public class ShapeFactory {
		public static readonly string NoWorkerEx = "No worker for this shape.";
		
		private Hashtable ShapeToWorker { get; set; }

		public ShapeFactory() {
			ShapeToWorker = new Hashtable();
		}
		
		public void RegisterWorker(IShapeFactoryWorker worker) {
			ShapeToWorker[worker.GetShapeName()] = worker;
		}

		public IShape CreateShape(string shapeName, params object[] parameters) {
			if (ShapeToWorker.ContainsKey(shapeName))
				return ((IShapeFactoryWorker) ShapeToWorker[shapeName]).CreateShape(parameters);
			throw new Exception(NoWorkerEx);
		}
	}
}