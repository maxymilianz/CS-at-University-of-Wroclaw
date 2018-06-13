using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Xml;

namespace E2 {
	public abstract class AbstractDataAccessHandler {
		public void Execute() {
			ConnectToData();
			LoadData();
			ProcessData();
			CloseConnection();
		}

		public abstract void ConnectToData();

		public abstract void LoadData();

		public abstract void ProcessData();

		public abstract void CloseConnection();
	}

	public class DbHandler : AbstractDataAccessHandler {
		private SQLiteConnection Connection { get; set; }
		private SQLiteDataReader Reader { get; set; }

		public override void ConnectToData() {
			Connection = new SQLiteConnection(
				"Data Source=C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\8\\L8\\E2\\db.sqlite; Version=3;");
			Connection.Open();
		}

		public override void LoadData() {
			SQLiteCommand command = new SQLiteCommand("select * from mytable", Connection);
			Reader = command.ExecuteReader();
		}

		public override void ProcessData() {
			int sum = 0;
			
			while (Reader.Read())
				sum += (int) Reader["mycolumn"];
			
			Console.WriteLine("Sum of mycolumn: " + sum + '.');
		}

		public override void CloseConnection() {
			Connection.Close();
		}
	}

	public class XmlHandler : AbstractDataAccessHandler {
		private XmlDocument Document { get; set; }

		public XmlHandler() {
			Document = new XmlDocument();
		}

		public override void ConnectToData() {
			Document.Load(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E2\osinfo.xml");
		}

		public override void LoadData() { }

		public override void ProcessData() {
			int maxLen = 0;
			Queue<XmlNode> queue = new Queue<XmlNode>();

			foreach (XmlNode node in Document.ChildNodes)
				queue.Enqueue(node);

			while (queue.Count > 0) {
				XmlNode node = queue.Dequeue();
				int len = node.Name.Length;
				if (len > maxLen)
					maxLen = len;
				foreach (XmlNode child in node.ChildNodes)
					queue.Enqueue(child);
			}

			Console.WriteLine("Longest nodes name is " + maxLen + " chars long.");
		}

		public override void CloseConnection() { }
	}
}