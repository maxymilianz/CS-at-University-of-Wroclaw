using System.IO;
using System.Net;
using System.Net.Mail;
using System.Net.Mime;

namespace E1 {
	public class SmtpFacade {
		private SmtpClient Client { get; set; }
		
		private string Host { get; set; }
		private int Port { get; set; }
		private string UserName { get; set; }
		private string Password { get; set; }

		public SmtpFacade(string host, int port, string userName, string password) {
			Host = host;
			Port = port;
			UserName = userName;
			Password = password;
			
			Client = new SmtpClient(host, port);
			Client.EnableSsl = true;
			Client.Credentials = new NetworkCredential(userName, password);
			Client.DeliveryMethod = SmtpDeliveryMethod.Network;
		}

		public void Send(string from, string to, string subject, string body, Stream attachment,
			string attachmentMimeType) {
			MailMessage message = new MailMessage(from, to, subject, body);
			message.Attachments.Add(new Attachment(attachment, new ContentType(attachmentMimeType)));
			Client.Send(message);
		}
	}
}