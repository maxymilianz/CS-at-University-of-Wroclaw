namespace E3 {
	class Program {
		static void Main(string[] args) {
			new DataAccessHandler(new DbHandler()).Execute();
			new DataAccessHandler(new XmlHandler()).Execute();
		}
	}
}