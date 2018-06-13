using System;
using System.Collections.Generic;
using System.Linq;

namespace E3 {
	internal class Program {
		public static void Main(string[] args) {
			HashSet<object> test = new HashSet<object>();
			test.Add(1);
			Console.WriteLine(test.First());
		}
	}
}