using System;
using System.Collections.Generic;

namespace E3 {
	internal class Program {
		public static void Main(string[] args) {
			AbstractAirport airport = HoursProxyAirport.Instance();
			Plane plane = airport.AcquirePlane();
			airport.ReleasePlane(plane);

			airport = LoggingProxyAirport.Instance();
			plane = airport.AcquirePlane();
			airport.ReleasePlane(plane);
		}
	}
}