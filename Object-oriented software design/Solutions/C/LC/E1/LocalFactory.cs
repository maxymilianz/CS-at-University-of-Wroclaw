using System;

namespace E1 {
	public class LocalFactory {
		public static Func<ORM> ORMProvider { get; set; }

		public ORM CreateORM() {
			if (ORMProvider == null)
				throw new Exception("No ORM provider");

			return ORMProvider();
		}
	}
}