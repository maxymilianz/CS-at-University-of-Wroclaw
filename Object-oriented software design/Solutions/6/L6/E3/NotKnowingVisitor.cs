using System.Collections.Generic;

namespace E3 {
	public abstract class AbstractTree {
		public abstract void Accept(AbstractVisitor abstractVisitor);
	}

	public class Leaf : AbstractTree {
		public override void Accept(AbstractVisitor visitor) {
			visitor.VisitLeaf(this);
		}
	}

	public class Node : AbstractTree {
		public AbstractTree Left { get; private set; }
		public AbstractTree Right { get; private set; }

		public Node(AbstractTree left, AbstractTree right) {
			Left = left;
			Right = right;
		}

		public override void Accept(AbstractVisitor visitor) {
			visitor.VisitNode(this);

			if (Left != null)
				Left.Accept(visitor);
			if (Right != null)
				Right.Accept(visitor);
		}
	}

	public abstract class AbstractVisitor {
		public abstract void VisitLeaf(Leaf tree);

		public abstract void VisitNode(Node tree);
	}

	public class DepthVisitor : AbstractVisitor {
		private Dictionary<AbstractTree, int> TreeToDepth { get; set; }
		public int Depth { get; private set; }

		public DepthVisitor() {
			TreeToDepth = new Dictionary<AbstractTree, int>();
			Depth = 0;
		}
		
		public override void VisitLeaf(Leaf tree) {
			if (TreeToDepth[tree] > Depth)
				Depth = TreeToDepth[tree];
		}

		public override void VisitNode(Node tree) {
			if (!TreeToDepth.ContainsKey(tree))
				TreeToDepth[tree] = 0;

			if (tree.Left != null)
				TreeToDepth[tree.Left] = TreeToDepth[tree] + 1;
			if (tree.Right != null)
				TreeToDepth[tree.Right] = TreeToDepth[tree] + 1;
		}
	}
}