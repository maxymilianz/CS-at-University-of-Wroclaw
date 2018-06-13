using System;
using Unity;

namespace E1 {
	internal class Program {
		private static void CompositionRoot() {
			UnityContainer container = new UnityContainer();
			LocalFactory.ORMProvider = () => container.Resolve<ORM>();
		}

		private static void InsertParent(ORM orm) {
			Parent parent = new Parent();
			orm.InsertParent(parent);
			Console.WriteLine("Inserted parent with id = " + parent.Id + ".");
		}

		private static void InsertChild(ORM orm) {
			Console.WriteLine("Enter parents id:");
			int parentId = int.Parse(Console.ReadLine());
			Child child = new Child(orm.ParentFromId(parentId));
			orm.InsertChild(child);
			Console.WriteLine("Inserted child with id = " + child.Id + ".");
		}

		private static void CheckParent(ORM orm) {
			Console.WriteLine("Enter childs id:");
			int id = int.Parse(Console.ReadLine());
			Console.WriteLine("Parents id = " + orm.ChildFromId(id).parent.Id);
		}

		public static void Main(string[] args) {
			CompositionRoot();

			LocalFactory factory = new LocalFactory();
			ORM orm = factory.CreateORM();

			Console.WriteLine("How many operations do you want to perform?");
			int operationsCount = int.Parse(Console.ReadLine());

			for (int i = 0; i < operationsCount; i++) {
				Console.WriteLine("Do you want to insert parent (ip), insert child (ic) or check childs parent (cp)?");
				string choice = Console.ReadLine();

				switch (choice) {
					case "ip":
						InsertParent(orm);
						break;
					case "ic":
						InsertChild(orm);
						break;
					case "cp":
						CheckParent(orm);
						break;
				}
			}
		}
	}

	public class Parent {
		private static int LastId = 0;
		public int Id { get; }

		public Parent() {
			Id = NextId();
		}

		public Parent(int id) {
			Id = id;
		}

		private static int NextId() {
			return LastId++;
		}
	}

	public class Child {
		private static int LastId = 0;
		public int Id { get; }
		public Parent parent { get; }

		public Child(Parent parent) {
			Id = NextId();
			this.parent = parent;
		}

		public Child(int id, Parent parent) {
			Id = id;
			this.parent = parent;
		}

		private static int NextId() {
			return LastId++;
		}
	}
}