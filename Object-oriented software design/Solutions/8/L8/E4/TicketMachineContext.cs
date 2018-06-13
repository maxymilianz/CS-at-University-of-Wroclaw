namespace E4 {
	public class TicketMachineContext {
		public IState State { get; set; }

		public TicketMachineContext() {
			State = new TicketSelection();
		}

		public void Handle(string input) {
			State.Handle(this, input);
		}
	}
}