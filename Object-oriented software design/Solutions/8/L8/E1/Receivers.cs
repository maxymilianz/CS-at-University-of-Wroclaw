using System;
using System.IO;
using System.Net;

namespace E1 {
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

	class RandomFileGenerator {
		private int Size { get; set; }		// size of file in bits

		internal RandomFileGenerator(int size) {
			Size = size;
		}

		internal void Generate(string filename) {
			using (StreamWriter file = new StreamWriter(filename)) {
				Random random = new Random();

				for (int i = 0; i < Size; i++)
					file.Write((char) (random.Next() % (char.MaxValue / 2)));
			}
		}
	}

	class FileCopier {
		private string Source { get; set; }

		internal FileCopier(string source) {
			Source = source;
		}

		internal void Copy(string filename) {
			try {
				File.Copy(Source, filename);
			}
			catch (IOException e) {
				File.Delete(filename);
				File.Copy(Source, filename);
			}
		}
	}
}