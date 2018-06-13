using System;
using System.Collections.Generic;

namespace E4 {
	internal class Program {
		public static void Main(string[] args) {
		}

		private static void ManyTagsNestedIndentTestTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").StartTag("tag2").AddContent("body2").EndTag().AddContent("body0").EndTag().StartTag("tag1").AddContent("body1").EndTag();
			Console.WriteLine(builder.ToString());
		}

		private static void ManyTagsIndentTestTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").AddContent("body0").EndTag().StartTag("tag1").AddContent("body1").EndTag();
			Console.WriteLine(builder.ToString());
		}

		private static void NestedIndentTestTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").StartTag("tag1").AddContent("body1").EndTag().AddContent("body0").EndTag();
			Console.WriteLine(builder.ToString());
		}

		private static void IndentTestTest() {
			TagBuilder builder = new TagBuilder();
			builder.IsIndented = true;
			builder.Indentation = 4;
			builder.StartTag("tag0").AddContent("body0").EndTag();
			Console.WriteLine(builder.ToString());
		}

		private static void ExampleFromList() {
			TagBuilder tag = new TagBuilder();
			tag.IsIndented = true;
			tag.Indentation = 4;
			tag.StartTag( "parent" )
				.AddAttribute( "parentproperty1", "true" )
				.AddAttribute( "parentproperty2", "5" )
				.StartTag( "child1")
				.AddAttribute( "childproperty1", "c" )
				.AddContent( "childbody" )
				.EndTag()
				.StartTag( "child2" )
				.AddAttribute( "childproperty2", "c" )
				.AddContent( "childbody" )
				.EndTag()
				.EndTag()
				.StartTag( "script" )
				.AddContent( "$.scriptbody();")
				.EndTag();
			Console.WriteLine(tag.ToString());
		}
	}
}