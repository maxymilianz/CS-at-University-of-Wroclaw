using System;

namespace LB {
	public delegate SimpleContainer ContainerProviderDelegate();
	
	public class ServiceLocator {
		private static ContainerProviderDelegate ContainerProvider { get; set; }
		private static ServiceLocator Instance;
		
		public static ServiceLocator Current {
			get {
				Instance = Instance ?? new ServiceLocator();
				return Instance;
			}
		}

		public static void SetContainerProvider(ContainerProviderDelegate containerProvider) {
			ContainerProvider = containerProvider;
		}

		public T GetInstance<T>() {
			if (typeof(T) == typeof(SimpleContainer))
					return (T) (object) ContainerProvider();

			return ContainerProvider().Resolve<T>();
		}
	}
}