using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;

namespace E5 {
	public abstract class PersonNotifier {
		public List<Person> Persons { get; set; }

		public abstract void NotifyPersons();
	}

	public class PrintPersonNotifier : PersonNotifier {
		public override void NotifyPersons() {
			foreach (Person person in Persons)
				Console.WriteLine(person.ToString());
		}
	}
	
	public abstract class AbstractLoadPersonRegistry {
		protected PersonNotifier Notifier { get; set; }
		public List<Person> Persons { get; protected set; }

		public AbstractLoadPersonRegistry(PersonNotifier notifier) {
			Notifier = notifier;
		}

		public abstract void LoadPersons();

		public void NotifyPersons() {
			Notifier.NotifyPersons();
		}
	}

	public class SerializationLoadPersonRegistry : AbstractLoadPersonRegistry {
		private IFormatter Formatter { get; set; }
		private string Filename { get; set; }

		public SerializationLoadPersonRegistry(PersonNotifier notifier, string filename) : base(notifier) {
			Formatter = new BinaryFormatter();
			Filename = filename;
			LoadPersons();
			Notifier.Persons = Persons;
		}

		public override void LoadPersons() {
			Stream stream = new FileStream(Filename, FileMode.Open, FileAccess.Read, FileShare.Read);
			Persons = (List<Person>) Formatter.Deserialize(stream);
			stream.Close();
		}
	}
}