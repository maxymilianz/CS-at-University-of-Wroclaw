using System;

namespace Local_Factory {
	class Program {
		private static void CompositionRoot() {
			SimpleContainer container = new SimpleContainer();
			FtpDownload ftpDownload = new FtpDownload("2711182_rajmund", "568923bbb", "ftp://f20-preview.runhosting.com/test.txt");
			HttpDownload httpDownload = new HttpDownload("http://www.ii.uni.wroc.pl/~wzychla/ra2H2I/OOPCourse2018.pdf");

			container.RegisterInstance(ftpDownload);
			container.RegisterInstance(httpDownload);

			LocalFactory.FtpDownloadProvider = () => container.Resolve<FtpDownload>();
			LocalFactory.HttpDownloadProvider = () => container.Resolve<HttpDownload>();
		}

		static void Main(string[] args) {
			CompositionRoot();

			LocalFactory factory = new LocalFactory();
			factory.CreateHttpDownload()
				.Execute(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\B\LB\Local Factory\wyklad.pdf");
		}
	}
}