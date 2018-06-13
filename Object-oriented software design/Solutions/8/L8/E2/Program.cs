namespace E2 {
	class Program {
		static void Main(string[] args) {
			new DbHandler().Execute();
			new XmlHandler().Execute();
		}
	}
}