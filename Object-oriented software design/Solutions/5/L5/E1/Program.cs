using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Mime;

namespace E1 {
	internal class Program {
		public static void Main(string[] args) {
			SmtpFacade facade = new SmtpFacade("smtp.gmail.com", 587, "longsawick@gmail.com", "568923bbb");
			facade.Send("longsawick@gmail.com", "com.liamtoh@gmail.com", "subj",
				"body is what She has perfect *_* as everything else",
				new FileStream(
					"C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\5\\L5\\E1\\attachment.txt",
					FileMode.Open), MediaTypeNames.Text.Plain);
		}
	}
}