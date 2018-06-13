using System.IO;
using System.Net;

namespace Local_Factory {
	class FtpDownloader {
		private string UserName { get; set; }
		private string Password { get; set; }
		
		private string Address { get; set; }

		internal FtpDownloader(string userName, string password, string address) {
			UserName = userName;
			Password = password;
			Address = address;
		}

		internal void DownloadToFile(string filename) {
			FtpWebRequest request = (FtpWebRequest) WebRequest.Create(Address);
			request.Method = WebRequestMethods.Ftp.DownloadFile;
			request.Credentials = new NetworkCredential(UserName, Password);

			FtpWebResponse response = (FtpWebResponse) request.GetResponse();
			Stream responseStream = response.GetResponseStream();

			using (Stream file = File.Create(filename))
				responseStream.CopyTo(file);
			
			response.Close();
		}
	}

	class HttpDownloader {
		private string Address { get; set; }

		internal HttpDownloader(string address) {
			Address = address;
		}

		internal void DownloadToFile(string filename) {
			using (WebClient client = new WebClient())
				client.DownloadFile(Address, filename);
		}
	}
}