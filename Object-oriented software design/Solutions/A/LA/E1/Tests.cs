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

		[Test]
		public void ParametersTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Foo>(false);
			container.RegisterType<Bar>(false);
			Bar bar = container.Resolve<Bar>();
			Assert.NotNull(bar);
			Assert.NotNull(bar.foo);
		}

		[Test]
		public void UnregisteredParameterTypeTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Bar>(false);
			Exception exception = Assert.Throws<Exception>(() => container.Resolve<Bar>());
			Assert.That(exception.Message, Is.EqualTo(SimpleContainer.UnregisteredTypeException));
		}

		[Test]
		public void CycleResolveAndMaxParamsCountTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Qux>(false);
			Exception exception = Assert.Throws<Exception>(() => container.Resolve<Qux>());
			Assert.That(exception.Message, Is.EqualTo(SimpleContainer.ResolveCycleException));
		}

		[Test]
		public void DependencyConstructorTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Baz>(false);
			container.Resolve<Baz>();
		}

		[Test]
		public void ParametersSingletonTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Foo>(false);
			container.RegisterType<Bar>(true);
			Bar bar0 = container.Resolve<Bar>();
			Bar bar1 = container.Resolve<Bar>();
			Assert.AreSame(bar0, bar1);
		}

		[Test]
		public void LastRegistryMattersTest() {
			SimpleContainer container = new SimpleContainer();
			container.RegisterType<Foo>(false);
			container.RegisterType<Foo>(true);
			Foo foo0 = container.Resolve<Foo>();
			Foo foo1 = container.Resolve<Foo>();
			Assert.AreSame(foo0, foo1);

			container.RegisterType<Foo>(false);
			foo0 = container.Resolve<Foo>();
			foo1 = container.Resolve<Foo>();
			Assert.AreNotSame(foo0, foo1);
		}
	}

	public interface IFoo { }

	public class Foo : IFoo { }

	public class Bar {
		public Foo foo { get; private set; }

		public Bar(Foo foo) {
			this.foo = foo;
		}
	}

	public class Qux {
		public Qux() {
			
		}
		
		public Qux(Qux qux) {
			
		}
	}

	public class Baz {
		public int N { get; private set; }
		
		[DependencyConstructor]
		public Baz() {
			N = 0;
		}

		public Baz(int n) {
			N = n;
		}
	}
}