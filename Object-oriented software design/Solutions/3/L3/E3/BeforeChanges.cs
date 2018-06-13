using System;

namespace E3BeforeChanges {
	public class TaxCalculator {
		public Decimal CalculateTax(Decimal Price) {
			return Price * new decimal(0.22);
		}
	}

	public class Item {
		public Item(double price) {
			this.price = new decimal(price);
		}
		
		private Decimal price;
		
		public Decimal Price {
			get { return price; }
		}

		private string name;

		public string Name {
			get { return name; }
		}
	}

	public class CashRegister {
		public TaxCalculator taxCalc = new TaxCalculator();

		public Decimal CalculatePrice(Item[] Items) {
			Decimal _price = 0;

			foreach (Item item in Items) {
				_price += item.Price + taxCalc.CalculateTax(item.Price);
			}

			return _price;
		}

		public string PrintBill(Item[] Items) {
			foreach (var item in Items)
				Console.WriteLine("towar {0} : cena {1} + podatek {2}",
					item.Name, item.Price, taxCalc.CalculateTax(item.Price));

			return "";
		}
	}
}