using System;
using System.Collections.Generic;
using System.Data.SQLite;
using System.Xml;

namespace E3 {
	public class DataAccessHandler {
		private IDataAccessStrategy Strategy { get; set; }

		public DataAccessHandler(IDataAccessStrategy strategy) {
			Strategy = strategy;
		}

		public void Execute() {
			Strategy.ConnectToData();
			Strategy.LoadData();
			Strategy.ProcessData();
			Strategy.CloseConnection();
		}
	}

	public interface IDataAccessStrategy {
		void ConnectToData();

		void LoadData();

		void ProcessData();

		void CloseConnection();
	}
	
	public class DbHandler : IDataAccessStrategy {
		private SQLiteConnection Connection { get; set; }
		private SQLiteDataReader Reader { get; set; }

		public void ConnectToData() {
			Connection = new SQLiteConnection(
				"Data Source=C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\8\\L8\\E2\\db.sqlite; Version=3;");
			Connection.Open();
		}

		public void LoadData() {
			SQLiteCommand command = new SQLiteCommand("select * from mytable", Connection);
			Reader = command.ExecuteReader();
		}

		public void ProcessData() {
			int sum = 0;
			
			while (Reader.Read())
				sum += (int) Reader["mycolumn"];
			
			Console.WriteLine("Sum of mycolumn: " + sum + '.');
		}

		public void CloseConnection() {
			Connection.Close();
		}
	}

	public class XmlHandler : IDataAccessStrategy {
		private XmlDocument Document { get; set; }

		public XmlHandler() {
			Document = new XmlDocument();
		}

		public void ConnectToData() {
			Document.Load(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E2\osinfo.xml");
		}

		public void LoadData() { }

		public void ProcessData() {
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

		public void CloseConnection() { }
	}
}