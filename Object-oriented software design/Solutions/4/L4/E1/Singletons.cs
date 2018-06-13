using System;
using System.Collections;
using System.Threading;

namespace E1 {
	public class ProcessSingleton {
		private static ProcessSingleton Singleton { get; set; }

		private ProcessSingleton() {
			
		}

		public static ProcessSingleton GetInstance() {
			Singleton = Singleton ?? new ProcessSingleton();
			return Singleton;
		}
	}

	public class ThreadSingleton {
		private static readonly Hashtable ThreadIdToInstance = new Hashtable();

		private ThreadSingleton() {
			
		}

		public static ThreadSingleton GetInstance() {
			int threadId = Thread.CurrentThread.ManagedThreadId;
			ThreadIdToInstance[threadId] = ThreadIdToInstance[threadId] ?? new ThreadSingleton();
			return (ThreadSingleton) ThreadIdToInstance[threadId];
		}
	}

	public class FiveSSingleton {
		private static FiveSSingleton Singleton { get; set; }
		private static DateTime CreationTime = DateTime.Now;

		private FiveSSingleton() {
			
		}

		public static FiveSSingleton GetInstance() {
			if (CreationTime.AddSeconds(5).CompareTo(DateTime.Now) < 0) {
				Singleton = new FiveSSingleton();
				CreationTime = DateTime.Now;
			}
			return Singleton;
		}
	}
}