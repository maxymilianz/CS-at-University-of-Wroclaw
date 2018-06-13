using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;

namespace E5 {
	[Serializable]
	public class Person {
		private static int Counter = 0;
		
		private int Id { get; set; }

		public Person() {
			Id = Counter;
			Counter++;
		}

		public string ToString() {
			return Id.ToString();
		}
	}

	public class Serializator {
		private IFormatter Formatter { get; set; }
		private string Filename { get; set; }

		public Serializator(string filename) {
			Formatter = new BinaryFormatter();
			Filename = filename;
		}
		
		public void Serialize(List<Person> persons) {
			Stream stream = new FileStream(Filename, FileMode.Create, FileAccess.Write, FileShare.Write);
			Formatter.Serialize(stream, persons);
			stream.Close();
		}
	}
}