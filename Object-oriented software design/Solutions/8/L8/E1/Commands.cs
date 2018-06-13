namespace E1 {
	interface IFileCommand {
		void Execute(string filename);
	}

	class FtpDownload : IFileCommand {
		private FtpDownloader Downloader { get; set; }

		internal FtpDownload(string userName, string password, string address) {
			Downloader = new FtpDownloader(userName, password, address);
		}

		public void Execute(string filename) {
			Downloader.DownloadToFile(filename);
		}
	}

	class HttpDownload : IFileCommand {
		private HttpDownloader Downloader { get; set; }

		internal HttpDownload(string address) {
			Downloader = new HttpDownloader(address);
		}

		public void Execute(string filename) {
			Downloader.DownloadToFile(filename);
		}
	}

	class CreateRandom : IFileCommand {
		private RandomFileGenerator Generator { get; set; }

		internal CreateRandom(int size) {
			Generator = new RandomFileGenerator(size);
		}

		public void Execute(string filename) {
			Generator.Generate(filename);
		}
	}

	class Copy : IFileCommand {
		private FileCopier Copier { get; set; }

		internal Copy(string source) {
			Copier = new FileCopier(source);
		}

		public void Execute(string filename) {
			Copier.Copy(filename);
		}
	}
}