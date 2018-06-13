using System.Collections.Generic;
using System.Data.SQLite;

namespace E1 {
	public class ORM {
		private SQLiteConnection Connection { get; set; }

		private Dictionary<int, Parent> IdToParent { get; }
		private Dictionary<int, Child> IdToChild { get; }

		public ORM() {
			Connection = new SQLiteConnection(
				"Data Source=C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\C\\db.sqlite; Version=3;");
			Connection.Open();

			IdToParent = new Dictionary<int, Parent>();
			IdToChild = new Dictionary<int, Child>();
		}

		public void InsertParent(Parent parent) {
			SQLiteCommand command = new SQLiteCommand("insert into Parent (Id) values (" + parent.Id + ");", Connection);
			command.ExecuteNonQuery();
		}

		public void InsertChild(Child child) {
			SQLiteCommand command = new SQLiteCommand(
				"insert into Child (Id, ParentId) values (" + child.Id + ',' + child.parent.Id + ");", Connection);
			command.ExecuteNonQuery();
		}

		public Parent ParentFromId(int id) {
			if (IdToParent.ContainsKey(id))
				return IdToParent[id];

			SQLiteCommand command = new SQLiteCommand("select * from Parent", Connection);
			SQLiteDataReader reader = command.ExecuteReader();
			Parent parent = null;

			while (reader.Read()) {
				int someId = (int) reader["Id"];

				if (someId == id) {
					parent = new Parent(someId);
					break;
				}
			}

			IdToParent[id] = parent;
			return parent;
		}

		public Child ChildFromId(int id) {
			if (IdToChild.ContainsKey(id))
				return IdToChild[id];

			SQLiteCommand command = new SQLiteCommand("select * from Child", Connection);
			SQLiteDataReader reader = command.ExecuteReader();
			Child child = null;

			while (reader.Read()) {
				int someId = (int) reader["Id"];

				if (someId == id) {
					child = new Child(someId, ParentFromId((int) reader["ParentId"]));
					break;
				}
			}

			IdToChild[id] = child;
			return child;
		}
	}
}