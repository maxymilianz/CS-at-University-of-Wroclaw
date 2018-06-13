using System;
using System.Collections.Generic;

namespace E2 {
	public class Program {
		public static void Main(string[] args) {
			string v0 = "v0", v1 = "v1", v2 = "v2";
			Context context = new Context(new Dictionary<string, bool> {
				{v0, true},
				{v1, false},
				{v2, true}
			});

			BinaryExpression.op and = (b, b1) => b && b1;
			BinaryExpression.op or = (b, b1) => b || b1;

			UnaryExpression.op not = b => !b;

			AbstractExpression expression = new BinaryExpression(new BinaryExpression(new Variable(v0), new ConstExpression(false), or),
				new BinaryExpression(new UnaryExpression(new Variable(v1), not), new Variable(v2), and), or);
			Console.WriteLine(expression.Interpret(context));
		}
	}
}