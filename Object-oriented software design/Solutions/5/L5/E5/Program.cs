using System;
using System.Collections.Generic;

namespace E5 {
	internal class Program {
		public static void Main(string[] args) {
			List<Person> persons = new List<Person>{new Person(), new Person(), new Person()};
			string filename = "C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\5\\L5\\E5\\persons.bin";
			Serializator s = new Serializator(filename);
			s.Serialize(persons);

			AbstractNotifyPersonRegistry registry = new PrintNotifyPersonRegistry(new SerializationPersonLoader(filename));
			registry.NotifyPersons();

			AbstractLoadPersonRegistry registry1 = new SerializationLoadPersonRegistry(new PrintPersonNotifier(), filename);
			registry1.NotifyPersons();
		}
	}
}