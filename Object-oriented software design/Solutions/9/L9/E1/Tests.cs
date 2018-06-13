using System;
using NUnit.Framework;

namespace E1 {
	[TestFixture]
	class Tests {
		[Test]
		public void NotRegisteredClassTest() {
			SimpleContainer container = new SimpleContainer();
			Exception exception = Assert.Throws<Exception>(() => container.Resolve<IFoo>());
			Assert.That(exception.Message, Is.EqualTo(SimpleContainer.UnregisteredTypeException));
		}

		[Test]
		public void NotRegisteredInterfaceTest() {
			SimpleContainer container = new SimpleContainer();
			Exception exception = Assert.Throws<Exception>(() => container.Resolve<Foo>());
			Assert.That(exception.Message, Is.EqualTo(SimpleContainer.UnregisteredTypeException));
		}

		[Test]
		public void ClassSingletonTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Foo>(true);
			Foo foo0 = container.Resolve<Foo>();
			Foo foo1 = container.Resolve<Foo>();
			Assert.AreSame(foo0, foo1);
		}

		[Test]
		public void InterfaceSingletonTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<IFoo, Foo>(true);
			IFoo foo0 = container.Resolve<IFoo>();
			IFoo foo1 = container.Resolve<IFoo>();
			Assert.AreSame(foo0, foo1);
			Assert.IsInstanceOf(typeof(Foo), foo0);		// no need to check also for foo1
		}

		[Test]
		public void ClassTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Foo>(false);
			Foo foo0 = container.Resolve<Foo>();
			Foo foo1 = container.Resolve<Foo>();
			Assert.AreNotSame(foo0, foo1);
		}

		[Test]
		public void InterfaceTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<IFoo, Foo>(false);
			IFoo foo0 = container.Resolve<IFoo>();
			IFoo foo1 = container.Resolve<IFoo>();
			Assert.AreNotSame(foo0, foo1);
			Assert.IsInstanceOf(typeof(Foo), foo0);
		}

		[Test]
		public void InstanceTest() {
			IFoo foo = new Foo();
			SimpleContainer container = new SimpleContainer();
			container.RegisterInstance(foo);
			IFoo foo1 = container.Resolve<IFoo>();
			Assert.AreSame(foo, foo1);
		}
	}

	interface IFoo {
		
	}

	class Foo : IFoo {
		
	}
}