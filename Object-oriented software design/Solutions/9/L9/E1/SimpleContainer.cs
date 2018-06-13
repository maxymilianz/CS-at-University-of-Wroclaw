using System;
using System.Collections.Generic;

namespace E1 {
	public class SimpleContainer {
		public const string UnregisteredTypeException = "Attempt to resolve an unregistered type.";
		private Dictionary<Type, Func<object>> Actions { get; set; }

		public SimpleContainer() {
			Actions = new Dictionary<Type, Func<object>>();
		}

		public void RegisterType<T>(bool singleton) where T : class {
			if (singleton) {
				T instance = Activator.CreateInstance<T>();
				Actions[typeof(T)] = () => instance;
			}
			else
				Actions[typeof(T)] = () => Activator.CreateInstance<T>();
		}

		public void RegisterType<From, To>(bool singleton) where To : From {
			if (singleton) {
				To instance = Activator.CreateInstance<To>();
				Actions[typeof(From)] = () => instance;
			}
			else
				Actions[typeof(From)] = () => Activator.CreateInstance<To>();
		}

		public void RegisterInstance<T>(T instance) {
			Actions[typeof(T)] = () => instance;
		}

		public T Resolve<T>() {
			if (Actions.ContainsKey(typeof(T)))
				return (T) Actions[typeof(T)]();

			throw new Exception(UnregisteredTypeException);
		}
	}
}