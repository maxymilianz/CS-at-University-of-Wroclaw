using System;
using System.Collections.Generic;
using System.IO;

namespace E1 {
	public abstract class ILogger {
		public virtual void ApplyParameters(string parameters) { }

		public abstract void Log(string message);
	}

	public class NoneLogger : ILogger {
		public override void Log(string message) { }
	}

	public class ConsoleLogger : ILogger {
		public override void Log(string message) {
			Console.WriteLine("Logging at " + DateTime.Now + ":");
			Console.WriteLine(message);
		}
	}

	public class FileLogger : ILogger {
		private string Filename { get; set; }

		public override void ApplyParameters(string filename) {
			Filename = filename;
		}

		public override void Log(string message) {
			using (StreamWriter file = new StreamWriter(Filename, true)) {
				file.WriteLine("Logging at " + DateTime.Now + ":");
				file.WriteLine(message);
				file.WriteLine();
			}
		}
	}

	public enum LogType {
		None,
		Console,
		File
	}

	public class LoggerFactory {
		private static LoggerFactory _instance;

		public static LoggerFactory Instance {
			get {
				_instance = _instance ?? new LoggerFactory();
				return _instance;
			}
		}

		public static readonly Dictionary<LogType, Type> TypeToClass = new Dictionary<LogType, Type> {
			{LogType.None, typeof(NoneLogger)},
			{LogType.Console, typeof(ConsoleLogger)},
			{LogType.File, typeof(FileLogger)}
		};

		public ILogger GetLogger(LogType logType, string parameters = null) {
			ILogger logger = (ILogger) Activator.CreateInstance(TypeToClass[logType]);
			logger.ApplyParameters(parameters);
			return logger;
		}
	}
}