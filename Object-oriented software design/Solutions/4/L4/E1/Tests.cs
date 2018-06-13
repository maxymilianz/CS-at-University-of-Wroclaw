using System.Threading;
using NUnit.Framework;

namespace E1 {
	[TestFixture]
	public class ProcessSingletonTests {
		[Test]
		public void UniquenessTest() {
			ProcessSingleton s0 = ProcessSingleton.GetInstance();
			ProcessSingleton s1 = ProcessSingleton.GetInstance();
			Assert.AreSame(s0, s1);
		}
	}

	[TestFixture]
	public class ThreadSingletonTests {
		private ThreadSingleton S0 { get; set; }
		private ThreadSingleton S1 { get; set; }

		[Test]
		public void SameThreadUniquenessTest() {
			ThreadSingleton s0 = ThreadSingleton.GetInstance();
			ThreadSingleton s1 = ThreadSingleton.GetInstance();
			Assert.AreSame(s0, s1);
		}
		
		[Test]
		public void DifferentThreadsTest() {
			AssignS0();
			Thread t1 = new Thread(AssignS1);
			t1.Start();
			t1.Join();
			Assert.AreNotSame(S0, S1);
		}

		private void AssignS0() {
			S0 = ThreadSingleton.GetInstance();
		}

		private void AssignS1() {
			S1 = ThreadSingleton.GetInstance();
		}
	}

	[TestFixture]
	public class FiveSSingletonTests {
		[Test]
		public void FiveSUniquenessTest() {
			FiveSSingleton s0 = FiveSSingleton.GetInstance();
			FiveSSingleton s1 = FiveSSingleton.GetInstance();
			Assert.AreSame(s0, s1);
		}

		[Test]
		public void AfterFiveSTest() {
			FiveSSingleton s0 = FiveSSingleton.GetInstance();
			Thread.Sleep(5000);
			FiveSSingleton s1 = FiveSSingleton.GetInstance();
			Assert.AreNotSame(s0, s1);
		}
	}
}