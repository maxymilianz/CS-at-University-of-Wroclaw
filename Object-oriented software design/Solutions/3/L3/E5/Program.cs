using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace E5 {
	class Foo : ICollection<int> {
		/*
		 * some collections may be unmodifiable, so Add(int item), Clear(), Remove(int item) and IsReadOnly are useless
		 * and they should be in IModifiableCollection
		 */
		
		IEnumerator IEnumerable.GetEnumerator() {
			return GetEnumerator();
		}

		public IEnumerator<int> GetEnumerator() {
			throw new NotImplementedException();
		}

		public void Add(int item) {
			throw new NotImplementedException();
		}

		public void Clear() {
			throw new NotImplementedException();
		}

		public bool Contains(int item) {
			throw new NotImplementedException();
		}

		public void CopyTo(int[] array, int arrayIndex) {
			throw new NotImplementedException();
		}

		public bool Remove(int item) {
			throw new NotImplementedException();
		}

		public int Count { get; private set; }
		public bool IsReadOnly { get; private set; }
	}

	internal class Program {
		public static void Main(string[] args) {
			
		}
	}
}