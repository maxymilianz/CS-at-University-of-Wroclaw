using System;
using System.Collections.Generic;

namespace E2 {
	public class Context {
		private Dictionary<string, bool> Values { get; set; }

		public Context() { }

		public Context(Dictionary<string, bool> values) {
			Values = values;
		}

		public bool GetValue(string variableName) {
			try {
				return Values[variableName];
			}
			catch (KeyNotFoundException) {
				throw new Exception("No value for \"" + variableName + "\".");
			}
		}

		public void SetValue(string variableName, bool value) {
			Values[variableName] = value;
		}
	}

	public abstract class AbstractExpression {
		public abstract bool Interpret(Context context);
	}

	public class Variable : AbstractExpression {
		private string Name { get; set; }

		public Variable(string name) {
			Name = name;
		}
		
		public override bool Interpret(Context context) {
			return context.GetValue(Name);
		}
	}
	
	public class ConstExpression : AbstractExpression {
		private bool Value { get; set; }

		public ConstExpression(bool value) {
			Value = value;
		}
		
		public override bool Interpret(Context context) {
			return Value;
		}
	}

	public class BinaryExpression : AbstractExpression {
		private AbstractExpression Left { get; set; }
		private AbstractExpression Right { get; set; }
		private Delegate Operator { get; set; }

		public delegate bool op(bool v0, bool v1);

		public BinaryExpression(AbstractExpression left, AbstractExpression right, Delegate op) {
			Left = left;
			Right = right;
			Operator = op;
		}

		public override bool Interpret(Context context) {
			return (bool) Operator.DynamicInvoke(Left.Interpret(context), Right.Interpret(context));
		}
	}

	public class UnaryExpression : AbstractExpression {
		private AbstractExpression Expression { get; set; }
		private Delegate Operator { get; set; }

		public delegate bool op(bool v);

		public UnaryExpression(AbstractExpression expression, Delegate op) {
			Expression = expression;
			Operator = op;
		}

		public override bool Interpret(Context context) {
			return (bool) Operator.DynamicInvoke(Expression.Interpret(context));
		}
	}
}