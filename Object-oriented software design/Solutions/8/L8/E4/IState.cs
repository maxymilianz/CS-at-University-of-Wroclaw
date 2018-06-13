using System;
using System.Collections.Generic;

namespace E4 {
	public interface IState {
		void Handle(TicketMachineContext context, string input);
	}

	public class TicketSelection : IState {
		private HashSet<string> AvailableTickets { get; set; }

		public TicketSelection() {
			AvailableTickets = new HashSet<string> {"normal", "half-price"};
			Console.WriteLine("Choose ticket. (normal / half-price)");
		}
		
		public void Handle(TicketMachineContext context, string input) {
			if (AvailableTickets.Contains(input))
				context.State = new PaymentSelection();
			else
				context.State = new Failure();
		}
	}

	public class PaymentSelection : IState {
		private Dictionary<string, Type> PaymentMethodToState { get; set; }
			
		public PaymentSelection() {
			PaymentMethodToState = new Dictionary<string, Type>{{"card", typeof(CardPayment)}, {"cash", typeof(CashPayment)}};
			Console.WriteLine("Choose payment method. (card / cash)");
		}
		
		public void Handle(TicketMachineContext context, string input) {
			if (PaymentMethodToState.ContainsKey(input))
				context.State = (IState) Activator.CreateInstance(PaymentMethodToState[input]);
			else
				context.State = new Failure();
		}
	}

	public class CardPayment : IState {
		public CardPayment() {
			Console.WriteLine("Enter card number.");
		}
		
		public void Handle(TicketMachineContext context, string input) {
			if (input.Length == 16)
				context.State = new Success();
			else
				context.State = new Failure();
		}
	}

	public class CashPayment : IState {
		public CashPayment() {
			Console.WriteLine("Enter amount of cash.");
		}
		
		public void Handle(TicketMachineContext context, string input) {
			if (int.Parse(input) > 0)
				context.State = new Success();
			else
				context.State = new Failure();
		}
	}

	public class Success : IState {
		public Success() {
			Console.WriteLine("SUCCESS");
		}
		
		public void Handle(TicketMachineContext context, string input) {
			
		}
	}

	public class Failure : IState {
		public Failure() {
			Console.WriteLine("FAILURE :(");
		}
		
		public void Handle(TicketMachineContext context, string input) {
			
		}
	}
}