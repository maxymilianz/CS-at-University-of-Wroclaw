using NUnit.Framework;

namespace E4 {
	[TestFixture]
	public class Tests {
		[Test]
		public void ParentChildIndentTest() {
			TagBuilder parent = new TagBuilder();
			parent.IsIndented = true;
			parent.Indentation = 4;
			TagBuilder child = new TagBuilder("sample-tag", parent);
			Assert.AreEqual(parent.IsIndented, child.IsIndented);
			Assert.AreEqual(parent.Indentation, child.Indentation);
		}

		[Test]
		public void IndentTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").AddContent("body0").EndTag();
			Assert.AreEqual(builder.ToString(), System.IO.File.ReadAllText(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\4\L4\E4\IndentTestResult.txt"));
		}

		[Test]
		public void NestedIndentTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").StartTag("tag1").AddContent("body1").EndTag().AddContent("body0").EndTag();
			Assert.AreEqual(builder.ToString(), System.IO.File.ReadAllText(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\4\L4\E4\NestedIndentTestResult.txt"));
		}

		[Test]
		public void ManyTagsIndentTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").AddContent("body0").EndTag().StartTag("tag1").AddContent("body1").EndTag();
			Assert.AreEqual(builder.ToString(), System.IO.File.ReadAllText(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\4\L4\E4\ManyTagsIndentTestResult.txt"));
		}

		[Test]
		public void ManyTagsNestedIndentTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").StartTag("tag2").AddContent("body2").EndTag().AddContent("body0").EndTag().StartTag("tag1").AddContent("body1").EndTag();
			Assert.AreEqual(builder.ToString(), System.IO.File.ReadAllText(@"C:\Users\Maksymilian Zawartko\Documents\Dokumenty\studia\lato 17-18\POO\4\L4\E4\ManyTagsNestedIndentTestResult.txt"));
		}
	}
}