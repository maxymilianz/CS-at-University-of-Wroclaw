namespace E1 {
	internal class Program {
		public static void Main(string[] args) {
			LoggerFactory factory = LoggerFactory.Instance;

			ILogger none = factory.GetLogger(LogType.None);
			none.Log("Nothing should happen.");

			ILogger console = factory.GetLogger(LogType.Console);
			console.Log("This is written in console.");

			ILogger file = factory.GetLogger(LogType.File,
				@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\6\L6\E1\log.txt");
			file.Log("This is logged in file.");
		}
	}
}