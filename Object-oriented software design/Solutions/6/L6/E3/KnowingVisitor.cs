using System;

namespace E3 {
	public abstract class AbstractTree1 { }

	public class Leaf1 : AbstractTree1 { }

	public class Node1 : AbstractTree1 {
		public AbstractTree1 Left { get; private set; }
		public AbstractTree1 Right { get; private set; }

		public Node1(AbstractTree1 left, AbstractTree1 right) {
			Left = left;
			Right = right;
		}
	}

	public abstract class AbstractVisitor1 {
		public void Visit(AbstractTree1 tree) {
			if (tree is Leaf1)
				VisitLeaf((Leaf1) tree);
			else if (tree is Node1)
				VisitNode((Node1) tree);
		}

		public virtual void VisitLeaf(Leaf1 leaf) { }

		public virtual void VisitNode(Node1 node) {
			if (node != null) {
				Visit(node.Left);
				Visit(node.Right);
			}
		}
	}

	public class DepthVisitor1 : AbstractVisitor1 {
		private int CurrentDepth { get; set; }
		public int Depth { get; private set; }

		public DepthVisitor1() {
			CurrentDepth = 0;
			Depth = 0;
		}

		public override void VisitLeaf(Leaf1 leaf) {
			if (CurrentDepth > Depth)
				Depth = CurrentDepth;
		}

		public override void VisitNode(Node1 node) {
			CurrentDepth++;
			base.VisitNode(node);
			CurrentDepth--;
		}
	}
}