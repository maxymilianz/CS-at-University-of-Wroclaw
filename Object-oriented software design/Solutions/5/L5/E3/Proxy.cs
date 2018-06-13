using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace E3 {
	public class Plane {
		private static int Counter = 0;
		
		private readonly int Id;

		public Plane() {
			Id = Counter;
			Counter++;
		}

		public string ToString() {
			return Id.ToString();
		}
	}

	public abstract class AbstractAirport {
		public static AbstractAirport Instance() {
			throw new NotImplementedException();
		}

		public abstract Plane AcquirePlane();

		public abstract void ReleasePlane(Plane plane);
	}

	public class Airport : AbstractAirport {
		// I could alternatively have many pools in one airport and use a Hashtable to find a pool for a plane (e.g. cargo and passenger planes)

		public static readonly string CapacityExceededEx = "Airport capacity exceeded.";
		public static readonly string PlaneNotFromThisAirportEx = "Plane not from this airport.";

		private HashSet<Plane> AvailablePlanes { get; set; }
		private HashSet<Plane> BusyPlanes { get; set; }
		public int Capacity { get; private set; }

		private Airport() {
			AvailablePlanes = new HashSet<Plane>();
			BusyPlanes = new HashSet<Plane>();
			Capacity = 4;
		}

		public static Airport Instance() {
			return new Airport();
		}

		public override Plane AcquirePlane() {
			if (AvailablePlanes.Any()) {
				Plane plane = AvailablePlanes.First();
				AvailablePlanes.Remove(plane);
				BusyPlanes.Add(plane);
				return plane;
			}

			if (BusyPlanes.Count < Capacity) {
				Plane plane = new Plane();
				BusyPlanes.Add(plane);
				return plane;
			}

			throw new Exception(CapacityExceededEx);
		}

		public override void ReleasePlane(Plane plane) {
			if (BusyPlanes.Contains(plane)) {
				BusyPlanes.Remove(plane);
				AvailablePlanes.Add(plane);
			}
			else
				throw new Exception(PlaneNotFromThisAirportEx);
		}
	}

	public class HoursProxyAirport : AbstractAirport {
		private Airport airport { get; set; }

		private TimeSpan Start { get; set; }
		private TimeSpan End { get; set; }

		private HoursProxyAirport(TimeSpan start, TimeSpan end) {
			airport = Airport.Instance();
			Start = start;
			End = end;
		}

		public static AbstractAirport Instance() {
			return new HoursProxyAirport(new TimeSpan(8, 0, 0), new TimeSpan(22, 0, 0));
		}

		public override Plane AcquirePlane() {
			TimeSpan now = DateTime.Now.TimeOfDay;
//			TimeSpan now = new TimeSpan(6, 12, 18);
//			TimeSpan now = new TimeSpan(23, 24, 25);

			if (now >= Start && now <= End)
				return airport.AcquirePlane();
			else
				throw new Exception("You cannot use airport at this time.");
		}

		public override void ReleasePlane(Plane plane) {
			TimeSpan now = DateTime.Now.TimeOfDay;
//			TimeSpan now = new TimeSpan(6, 12, 18);
//			TimeSpan now = new TimeSpan(23, 24, 25);

			if (now >= Start && now <= End)
				airport.ReleasePlane(plane);
			else
				throw new Exception("You cannot use airport at this time.");
		}
	}

	public class LoggingProxyAirport : AbstractAirport {
		private Airport airport { get; set; }

		private string Filename { get; set; }

		private LoggingProxyAirport(string filename) {
			airport = Airport.Instance();
			Filename = filename;
		}

		public static AbstractAirport Instance() {
			return new LoggingProxyAirport("C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\5\\L5\\E3\\log.txt");
		}

		public override Plane AcquirePlane() {
			using (StreamWriter file = new StreamWriter(Filename, true)) {
				file.Write("AcquirePlane method call at " + DateTime.Now + ". ");
				Plane plane = airport.AcquirePlane();
				file.Write("Call finished. '" + plane + " " + plane.ToString() + "' returned.\n");
				return plane;
			}
		}

		public override void ReleasePlane(Plane plane) {
			using (StreamWriter file = new StreamWriter(Filename, true)) {
				file.Write("ReleasePlane method call at " + DateTime.Now + " with '" + plane + " " + plane.ToString() + "' argument. ");
				airport.ReleasePlane(plane);
				file.Write("Call finished.\n");
			}
		}
	}
}