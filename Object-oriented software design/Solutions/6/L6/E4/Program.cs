// https://stackoverflow.com/questions/2637817/system-linq-expressions-expressionvisitor-is-inaccessible-due-to-its-protection

using System.Linq.Expressions;

namespace E4 {
	internal class Program {
		public static void Main(string[] args) {
			PrintExpressionVisitor visitor = new PrintExpressionVisitor();
			
			UnaryExpression u = UnaryExpression.ArrayLength(ConstantExpression.Constant(new[] {1, 2, 3, 4, 5}));
			visitor.Visit(u);

			ParameterExpression p = ParameterExpression.Parameter(typeof(int), "number");
			visitor.Visit(p);
		}
	}
}