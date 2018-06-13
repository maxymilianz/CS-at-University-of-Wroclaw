using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;

namespace E5 {
	public abstract class PersonLoader {
		public abstract List<Person> GetPersons();
	}

	public class SerializationPersonLoader : PersonLoader {
		private IFormatter Formatter { get; set; }
		private string Filename { get; set; }

		public SerializationPersonLoader(string filename) {
			Formatter = new BinaryFormatter();
			Filename = filename;
		}

		public override List<Person> GetPersons() {
			Stream stream = new FileStream(Filename, FileMode.Open, FileAccess.Read, FileShare.Read);
			List<Person> list = (List<Person>) Formatter.Deserialize(stream);
			stream.Close();
			return list;
		}
	}
	
	public abstract class AbstractNotifyPersonRegistry {
		private PersonLoader Loader { get; set; }
		public List<Person> Persons { get; private set; }

		public AbstractNotifyPersonRegistry(PersonLoader loader) {
			Loader = loader;
		}

		public void LoadPersons() {
			Persons = Loader.GetPersons();
		}

		public abstract void NotifyPersons();
	}

	public class PrintNotifyPersonRegistry : AbstractNotifyPersonRegistry {
		public PrintNotifyPersonRegistry(PersonLoader loader) : base(loader) {
			LoadPersons();
		}

		public override void NotifyPersons() {
			foreach (Person person in Persons)
				Console.WriteLine(person.ToString());
		}
	}
}