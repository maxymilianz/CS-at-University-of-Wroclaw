using System;

namespace E3 {
	internal class Program {
		public static void Main(string[] args) {
			AbstractTree tree =
				new Node(new Node(new Node(new Leaf(), new Leaf()), new Node(new Leaf(), new Node(new Leaf(), new Leaf()))),
					new Node(new Node(new Leaf(), new Leaf()), new Leaf()));
			DepthVisitor depth = new DepthVisitor();
			tree.Accept(depth);
			Console.WriteLine(depth.Depth);
			
			AbstractTree1 tree1 =
				new Node1(new Node1(new Node1(new Leaf1(), new Leaf1()), new Node1(new Leaf1(), new Node1(new Leaf1(), new Leaf1()))),
					new Node1(new Node1(new Leaf1(), new Leaf1()), new Leaf1()));
			DepthVisitor1 depth1 = new DepthVisitor1();
			depth1.Visit(tree1);
			Console.WriteLine(depth1.Depth);
		}
	}
}