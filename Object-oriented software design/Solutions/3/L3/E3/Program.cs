using System;
using System.Collections.Generic;
using E3AfterChanges;

namespace E3 {
	internal class Program {
		public static void Main(string[] args) {
			Decimal d = new decimal(21), e = new decimal(37);
			Console.WriteLine(d * e);

			Func<Item, object> key = item => item.Price;
			TaxCalculator calculator = new TaxCalculator();
			Tuple<Item, AbstractTaxCalculator>[] itemsAndTaxes = {
				new Tuple<Item, AbstractTaxCalculator>(new Item(2, 21.0), calculator),
				new Tuple<Item, AbstractTaxCalculator>(new Item(3, 14.0), calculator),
				new Tuple<Item, AbstractTaxCalculator>(new Item(1, 125.0), calculator)
			};
			CashRegister register = new CashRegister();
			Console.WriteLine(register.CalculatePrice(itemsAndTaxes));
			DifferentTaxCalculator calculator1 = new DifferentTaxCalculator();
			Tuple<Item, AbstractTaxCalculator>[] itemsAndTaxes1 = {
				new Tuple<Item, AbstractTaxCalculator>(new Item(2, 21.0), calculator1),
				new Tuple<Item, AbstractTaxCalculator>(new Item(3, 14.0), calculator1),
				new Tuple<Item, AbstractTaxCalculator>(new Item(1, 125.0), calculator1)
			};
			Console.WriteLine(register.CalculatePrice(itemsAndTaxes1));
			register.PrintBill(itemsAndTaxes, key);
			Func<Item, object> key1 = item => item.Id;
			register.PrintBill(itemsAndTaxes, key1);

			E3BeforeChanges.Item[] beforeItems = {
				new E3BeforeChanges.Item(21),
				new E3BeforeChanges.Item(14),
				new E3BeforeChanges.Item(125)
			};
			E3BeforeChanges.CashRegister beforeRegister = new E3BeforeChanges.CashRegister();
			Console.WriteLine(beforeRegister.CalculatePrice(beforeItems));
			beforeRegister.PrintBill(beforeItems);
		}
	}
}