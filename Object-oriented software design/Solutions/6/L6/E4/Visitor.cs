using System;
using System.Linq;
using System.Linq.Expressions;

namespace E4 {
	public class PrintExpressionVisitor : ExpressionVisitor {
		protected override Expression VisitBinary(BinaryExpression expression) {
			Console.WriteLine("{0} {1} {2}", expression.Left, expression.NodeType, expression.Right);
			return base.VisitBinary(expression);
		}

		protected override Expression VisitLambda<T>(Expression<T> expression) {
			Console.WriteLine("{0} -> {1}", expression.Parameters.Aggregate(string.Empty, (a, e) => a += e), expression.Body);
			return base.VisitLambda<T>(expression);
		}

		protected override Expression VisitUnary(UnaryExpression u) {
			Console.WriteLine("{0} {1}", u.NodeType, u.Operand);
			return base.VisitUnary(u);
		}

		protected override Expression VisitConstant(ConstantExpression c) {
			Console.WriteLine("{0}", c.Value);
			return base.VisitConstant(c);
		}

		protected override Expression VisitParameter(ParameterExpression p) {
			Console.WriteLine("{0} {1}", p.Type, p.Name);
			return base.VisitParameter(p);
		}
	}

//	public class PrintExpressionVisitor1 : System.Linq.Expressions.ExpressionVisitor {		// works when compiled from cmd
//		protected override Expression VisitBinary(BinaryExpression expression) {
//			Console.WriteLine("{0} {1} {2}",
//				expression.Left, expression.NodeType, expression.Right);
//
//			return base.VisitBinary(expression);
//		}
//
//		protected override Expression VisitLambda<T>(Expression<T> expression) {
//			Console.WriteLine("{0} -> {1}",
//				expression.Parameters.Aggregate(string.Empty, (a, e) => a += e),
//				expression.Body);
//
//			return base.VisitLambda<T>(expression);
//		}
//	}
}