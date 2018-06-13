using System;
using System.Collections.Generic;

namespace E7 {
	public class ReportComposer {
		private Report report;

		public ReportComposer(Report report) {
			this.report = report;
		}

		public string getData() {
			return report.getData();
		}
	}
	
	public class Report {
		private string data;

		public Report(string data) {
			this.data = data;
		}

		public void formatDocument() {
			// some implementation
		}

		public string getData() {
			return data;
		}
	}
	
	public class ReportPrinter {
		public ReportPrinter() {
			// some initialization
		}

		public void printReport(ReportComposer composer) {
			Console.WriteLine(composer.getData());
		}
	}
	
	internal class Program {
		public static void Main(string[] args) { }
	}
}