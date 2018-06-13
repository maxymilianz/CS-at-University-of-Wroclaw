using System;
using NUnit.Framework;

namespace E3 {
	[TestFixture]
	public class Tests {
		[Test]
		public void AcquireTest() {
			Airport airport = Airport.Instance();
			Plane plane = airport.AcquirePlane();
			Assert.NotNull(plane);
		}

		[Test]
		public void UniquenessTest() {
			Airport airport = Airport.Instance();
			Plane plane0 = airport.AcquirePlane();
			Plane plane1 = airport.AcquirePlane();
			Assert.AreNotSame(plane0, plane1);
		}

		[Test]
		public void ReleaseTest() {
			Assert.DoesNotThrow(AcquireReleaseManyTimes);
		}

		[Test]
		public void CapacityTest() {
			Exception exception = Assert.Throws<Exception>(AcquireManyTimes);
			Assert.That(exception.Message, Is.EqualTo(Airport.CapacityExceededEx));
		}

		[Test]
		public void PlaneNotFromAirportTest() {
			Exception exception = Assert.Throws<Exception>(Release);
			Assert.That(exception.Message, Is.EqualTo(Airport.PlaneNotFromThisAirportEx));
		}

		private void Release() {
			Airport airport = Airport.Instance();
			Plane plane = new Plane();
			airport.ReleasePlane(plane);
		}

		private void AcquireReleaseManyTimes() {
			Airport airport = Airport.Instance();

			for (int i = 0; i < airport.Capacity + 1; i++) {
				Plane plane = airport.AcquirePlane();
				airport.ReleasePlane(plane);
			}
		}

		private void AcquireManyTimes() {
			Airport airport = Airport.Instance();

			for (int i = 0; i < airport.Capacity + 1; i++)
				airport.AcquirePlane();
		}
	}
}