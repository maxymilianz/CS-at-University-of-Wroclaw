using System;
using System.Collections.Generic;
using System.Linq;

namespace E3AfterChanges {
	public abstract class AbstractTaxCalculator {
		public abstract Decimal CalculateTax(Decimal price);
	}
	
	public class TaxCalculator : AbstractTaxCalculator {
		public override Decimal CalculateTax(Decimal price) {
			return price * new decimal(.22);
		}
	}

	public class DifferentTaxCalculator : AbstractTaxCalculator {
		public override Decimal CalculateTax(Decimal price) {
			return price * new decimal(.84);
		}
	}

	public class Item {
		public Item(int id, double price) {
			this.id = id;
			this.price = new decimal(price);
			this.name = id.ToString();
		}

		private int id;

		public int Id {
			get { return id; }
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
		public Decimal CalculatePrice(Tuple<Item, AbstractTaxCalculator>[] itemsAndTaxes) {
			Decimal price = 0;

			foreach (Tuple<Item, AbstractTaxCalculator> itemAndTax in itemsAndTaxes) {
				price += itemAndTax.Item1.Price + itemAndTax.Item2.CalculateTax(itemAndTax.Item1.Price);
			}

			return price;
		}

		public string PrintBill(Tuple<Item, AbstractTaxCalculator>[] itemsAndTaxes, Func<Item, object> key) {
			List<Tuple<Item, AbstractTaxCalculator>> list = itemsAndTaxes.OrderBy(itemAndTax => key(itemAndTax.Item1)).ToList();
			
			foreach (var itemAndTax in list)
				Console.WriteLine("towar {0} : cena {1} + podatek {2}",
					itemAndTax.Item1.Name, itemAndTax.Item1.Price, itemAndTax.Item2.CalculateTax(itemAndTax.Item1.Price));

			return "";
		}
	}
}