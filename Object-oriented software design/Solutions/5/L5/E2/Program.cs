using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace E2 {
	internal class Program {
		public static void Main(string[] args) {
			string filename = "C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\5\\L5\\E2\\file.txt";

			FileStream output = new FileStream(filename, FileMode.Create);
			CaesarStream encrypt = new CaesarStream(output, 50);
			string s = "some content";
			encrypt.Write(Encoding.ASCII.GetBytes(s), 0, s.Length);
			output.Close();

			FileStream input = new FileStream(filename, FileMode.Open);
			CaesarStream decrypt = new CaesarStream(input, -50);
			byte[] bytes = new byte[s.Length];
			decrypt.Read(bytes, 0, s.Length);

			Console.WriteLine(Encoding.ASCII.GetString(bytes));
		}
	}
}