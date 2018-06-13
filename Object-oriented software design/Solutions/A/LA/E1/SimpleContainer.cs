using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Reflection;
using NUnit.Compatibility;

namespace E1 {
	[AttributeUsage(AttributeTargets.Constructor)]
	public class DependencyConstructorAttribute : Attribute { }

	public class SimpleContainer {
		public const string UnregisteredTypeException = "Attempt to resolve an unregistered type.";
		public const string WrongValueException = "Wrong value in Solutions dictionary.";
		public const string ResolveCycleException = "Dependency cycle detected.";

		private Dictionary<Type, object> Solutions { get; set; }
		private HashSet<Type> Singletons { get; set; }

		public SimpleContainer() {
			Solutions = new Dictionary<Type, object>();
			Singletons = new HashSet<Type>();
		}

		public void RegisterType<T>(bool singleton) where T : class {
			if (singleton)
				Singletons.Add(typeof(T));
			else if (Singletons.Contains(typeof(T)))
				Singletons.Remove(typeof(T));

			Solutions[typeof(T)] = typeof(T);
		}

		public void RegisterType<From, To>(bool singleton) where To : From {
			if (singleton)
				Singletons.Add(typeof(From));
			else if (Singletons.Contains(typeof(From)))
				Singletons.Remove(typeof(From));

			Solutions[typeof(From)] = typeof(To);
		}

		public void RegisterInstance<T>(T instance) {
			Solutions[typeof(T)] = instance;
		}

		private object ResolveFromConstructor(ConstructorInfo constructor, ImmutableHashSet<Type> resolvedTypes) {
			return constructor.Invoke(constructor.GetParameters().Select(parameter => {
				Type type = parameter.ParameterType;
				return Resolve(type, resolvedTypes);
			}).ToArray());
		}

		private object ResolveType(Type type, ImmutableHashSet<Type> resolvedTypes) {
			ConstructorInfo[] constructors = type.GetConstructors();
			IEnumerable<ConstructorInfo> dependencyConstructors =
				constructors.Where(constructor => constructor.GetCustomAttribute<DependencyConstructorAttribute>() != null);

			try {
				return ResolveFromConstructor(dependencyConstructors.Single(), resolvedTypes);
			}
			catch (InvalidOperationException e) {
				// there is > 1 DependencyConstructor
				return ResolveFromConstructor(constructors.OrderByDescending(constructor => constructor.GetParameters().Length).First(),
					resolvedTypes);
			}
		}

		private object Resolve(Type type, ImmutableHashSet<Type> resolvedTypes) {
			if (resolvedTypes.Contains(type))
				throw new Exception(ResolveCycleException);

			if (!Solutions.ContainsKey(type))
				throw new Exception(UnregisteredTypeException);

			object solution = Solutions[type];

			if (type.IsCastableFrom(solution.GetType()))
				return solution;
			if (solution is Type) {
				object instance = ResolveType((Type) solution, resolvedTypes.Add(type));
				if (Singletons.Contains(type))
					Solutions[type] = instance;
				return instance;
			}

			throw new Exception(WrongValueException);
		}

		public T Resolve<T>() {
			return (T) Resolve(typeof(T), new HashSet<Type>().ToImmutableHashSet());
		}
	}
}