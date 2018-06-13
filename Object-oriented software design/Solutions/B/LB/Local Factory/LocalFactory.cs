using System;

namespace Local_Factory {
	public class LocalFactory {
		public static Func<FtpDownload> FtpDownloadProvider { get; set; }
		public static Func<HttpDownload> HttpDownloadProvider { get; set; }

		public FtpDownload CreateFtpDownload() {
			if (FtpDownloadProvider == null)
				throw new Exception("No FtpDownload provider");
			
			return FtpDownloadProvider();
		}

		public HttpDownload CreateHttpDownload() {
			if (HttpDownloadProvider == null)
				throw new Exception("No HttpDownload provider");
			
			return HttpDownloadProvider();
		}
	}
}