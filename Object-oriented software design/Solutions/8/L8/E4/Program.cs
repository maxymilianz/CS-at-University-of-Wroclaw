using System;

namespace E4 {
	class Program {
		static void Main(string[] args) {
			TicketMachineContext ticketMachine = new TicketMachineContext();
			while (ticketMachine.State.GetType() != typeof(Success) && ticketMachine.State.GetType() != typeof(Failure))
				ticketMachine.Handle(Console.ReadLine());
		}
	}
}