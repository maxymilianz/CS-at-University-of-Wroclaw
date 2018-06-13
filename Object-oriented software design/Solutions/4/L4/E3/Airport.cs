using System;
using System.Collections.Generic;
using System.Linq;

namespace E3 {
	public class Plane {
		
	}
	
	public class Airport {
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
		
		public Plane AcquirePlane() {
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

		public void ReleasePlane(Plane plane) {
			if (BusyPlanes.Contains(plane)) {
				BusyPlanes.Remove(plane);
				AvailablePlanes.Add(plane);
			}
			else
				throw new Exception(PlaneNotFromThisAirportEx);
		}
	}
}