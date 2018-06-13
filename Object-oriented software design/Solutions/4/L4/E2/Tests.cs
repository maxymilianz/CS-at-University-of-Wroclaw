using System;
using NUnit.Framework;

namespace E2 {
	[TestFixture]
	public class Tests {
		[Test]
		public void NoWorkerTest() {
			ShapeFactory factory = new ShapeFactory();
			Exception exception = Assert.Throws<Exception>(() => factory.CreateShape("Non-existing shape"));
			Assert.That(exception.Message, Is.EqualTo(ShapeFactory.NoWorkerEx));
		}

		[Test]
		public void SquareTest() {
			ShapeFactory factory = new ShapeFactory();
			factory.RegisterWorker(new SquareFactoryWorker());
			IShape square = factory.CreateShape("Square", 1);
			Assert.IsInstanceOf(typeof(Square), square);
		}

		[Test]
		public void RectangleTest() {
			ShapeFactory factory = new ShapeFactory();
			factory.RegisterWorker(new RectangleFactoryWorker());
			IShape rectangle = factory.CreateShape("Rectangle", 2, 3);
			Assert.IsInstanceOf(typeof(Rectangle), rectangle);
		}

		[Test]
		public void NotEnoughArgsSquareTest() {
			ShapeFactory factory = new ShapeFactory();
			factory.RegisterWorker(new SquareFactoryWorker());
			Exception exception = Assert.Throws<Exception>(() => factory.CreateShape("Square"));
			Assert.That(exception.Message, Is.EqualTo(SquareFactoryWorker.NotEnoughParamsEx));
		}

		[Test]
		public void NotEnoughArgsRectangleTest() {
			ShapeFactory factory = new ShapeFactory();
			factory.RegisterWorker(new RectangleFactoryWorker());
			Exception exception = Assert.Throws<Exception>(() => factory.CreateShape("Rectangle", 4));
			Assert.That(exception.Message, Is.EqualTo(RectangleFactoryWorker.NotEnoughParamsEx));
		}
	}
}