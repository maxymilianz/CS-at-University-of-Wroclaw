namespace Local_Factory {
	public interface IFileCommand {
		void Execute(string filename);
	}

	public class FtpDownload : IFileCommand {
		private FtpDownloader Downloader { get; set; }

		internal FtpDownload(string userName, string password, string address) {
			Downloader = new FtpDownloader(userName, password, address);
		}

		public void Execute(string filename) {
			Downloader.DownloadToFile(filename);
		}
	}

	public class HttpDownload : IFileCommand {
		private HttpDownloader Downloader { get; set; }

		internal HttpDownload(string address) {
			Downloader = new HttpDownloader(address);
		}

		public void Execute(string filename) {
			Downloader.DownloadToFile(filename);
		}
	}
}