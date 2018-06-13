using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace E4 {
	public class TagBuilder {
		private string TagName { get; set; }
		public bool IsIndented { get; set; }
		public int Indentation { get; set; }
		private string IndentationString { get; set; }
		private TagBuilder Parent { get; set; }
		private StringBuilder Body { get; set; }
		private Dictionary<string, string> Attributes { get; set; }

		public TagBuilder() {
			Body = new StringBuilder();
			Attributes = new Dictionary<string, string>();
		}

		public TagBuilder(string tagName, TagBuilder parent) {
			Body = new StringBuilder();
			Attributes = new Dictionary<string, string>();

			TagName = tagName;
			Parent = parent;

			IsIndented = parent.IsIndented;
			if (IsIndented) {
				Indentation = parent.Indentation;
				IndentationString = string.Concat(Enumerable.Repeat(" ", Indentation));
			}
		}

		public TagBuilder AddContent(string content) {
			Body.Append(content);
			return this;
		}

		public TagBuilder AddContentFormat(string format, params object[] args) {
			Body.AppendFormat(format, args);
			return this;
		}

		public TagBuilder StartTag(string tagName) {
			return new TagBuilder(tagName, this);
		}

		public TagBuilder EndTag() {
			Parent.AddContent(ToString());
			if (IsIndented)
				Parent.AddContent(Environment.NewLine);
			return Parent;
		}

		public TagBuilder AddAttribute(string name, string value) {
			Attributes.Add(name, value);
			return this;
		}

		public override string ToString() {
			StringBuilder tag = new StringBuilder();
			
			// preamble
			if (!string.IsNullOrEmpty(TagName))
				tag.AppendFormat("<{0}", TagName);

			if (Attributes.Count > 0) {
				tag.Append(" ");
				tag.Append(string.Join(" ",
					Attributes.Select(kvp => string.Format("{0}='{1}'",
						kvp.Key, kvp.Value)).ToArray()));
			}

			// body / ending
			if (Body.Length > 0) {
				if (!string.IsNullOrEmpty(TagName) || Attributes.Count > 0) {
					tag.Append(">");
					if (IsIndented) {
						foreach (string line in Body.ToString().Split(new string[] {Environment.NewLine}, StringSplitOptions.None))
							if (!string.IsNullOrEmpty(line))
								tag.Append(Environment.NewLine + IndentationString + line);
						tag.Append(Environment.NewLine);
					}
					else
						tag.Append(Body.ToString());						
				}
				else
					tag.Append(Body.ToString());
				if (!string.IsNullOrEmpty(TagName))
					tag.AppendFormat("</{0}>", TagName);
			}
			else if (!string.IsNullOrEmpty(TagName))
				tag.Append("/>");

			return tag.ToString();
		}
	}
}