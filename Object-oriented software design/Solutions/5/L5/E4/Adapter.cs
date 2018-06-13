using System;
using System.Collections;

namespace E4 {
	public class MyComparer<T> : IComparer {
		private Comparison<T> Comparison { get; set; }
		
		public MyComparer(Comparison<T> comparison) {
			Comparison = comparison;
		}
		
		public int Compare(object x, object y) {
			return Comparison((T) x, (T) y);
		}
	}
}