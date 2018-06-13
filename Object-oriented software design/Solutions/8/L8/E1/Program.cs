using System;
using System.Collections.Concurrent;
using System.Threading;

namespace E1 {
	class Program {
		private static ConcurrentQueue<IFileCommand> Queue = new ConcurrentQueue<IFileCommand>();

		static void Main(string[] args) {
			// something happened to my ftp account
//			FtpDownload ftpDownload = new FtpDownload("2711182_rajmund", "568923bbb", "ftp://f20-preview.runhosting.com/test.txt");
//			ftpDownload.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\test.txt");

			IFileCommand httpDownload = new HttpDownload("http://www.ii.uni.wroc.pl/~wzychla/ra2H2I/OOPCourse2018.pdf");
			httpDownload.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\wyklad.pdf");

			IFileCommand random = new CreateRandom(16);
			random.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\random.txt");

			IFileCommand copy = new Copy(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\random.txt");
			copy.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\copy.txt");


			Thread invoker = new Thread(new ThreadStart(AddToQueue));
			Thread handler0 = new Thread(new ThreadStart(GetFromQueue));
			Thread handler1 = new Thread(new ThreadStart(GetFromQueue));
			
			invoker.Start();
			handler0.Start();
			handler1.Start();
		}

		private static void AddToQueue() {
			IFileCommand httpDownload = new HttpDownload("http://www.ii.uni.wroc.pl/~wzychla/ra2H2I/OOPCourse2018.pdf");
			httpDownload.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\wyklad.pdf");

			IFileCommand randomCommand = new CreateRandom(16);
			randomCommand.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\random.txt");

			IFileCommand copy = new Copy(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\random.txt");
			copy.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\copy.txt");

			Random random = new Random();
			
			while (true) {
				int r = random.Next();

				if (r % 3 == 0) {
					Queue.Enqueue(httpDownload);
//					Console.WriteLine("Enqueuing httpDownload");
				}
				else if (r % 3 == 1) {
					Queue.Enqueue(randomCommand);
//					Console.WriteLine("Enqueuing randomCommand");
				}
				else if (r % 3 == 2) {
					Queue.Enqueue(copy);
//					Console.WriteLine("Enqueuing copy");
				}
			}
		}

		private static void GetFromQueue() {
			while (true) {
				try {
					IFileCommand command;
					Queue.TryDequeue(out command);
					command.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\8\L8\E1\from_queue.txt");
					Console.WriteLine("Executing " + command);
				}
				catch (Exception e) {
//					Console.WriteLine("Queue is empty");
				}
			}
		}
	}
}