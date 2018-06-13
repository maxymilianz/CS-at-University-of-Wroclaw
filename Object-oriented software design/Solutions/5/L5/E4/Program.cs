using System;
using System.Collections;
using System.Collections.Generic;

namespace E4 {
	internal class Program {
		static int IntComparer(int x, int y) {
			return x.CompareTo(y);
		}

		public static void Main(string[] args) {
			ArrayList l = new ArrayList{2, 1, 4, 8, 15, 34, 12, 3, 22, 18};
			l.Sort(new MyComparer<int>(IntComparer));

			foreach (int n in l)
				Console.WriteLine(n);
		}
	}
}