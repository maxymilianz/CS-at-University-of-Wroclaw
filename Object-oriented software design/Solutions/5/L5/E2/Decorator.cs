using System;
using System.IO;

namespace E2 {
	public class CaesarStream : Stream {
		private bool _canRead;
		private bool _canSeek;
		private bool _canWrite;
		private long _length;

		private Stream stream { get; set; }
		private int Shift { get; set; }

		public CaesarStream(Stream stream, int shift) {
			this.stream = stream;
			Shift = shift;

			_canRead = stream.CanRead;
			_canSeek = stream.CanSeek;
			_canWrite = stream.CanWrite;
			_length = stream.Length;
		}

		public override void Flush() {
			stream.Flush();
		}

		public override long Seek(long offset, SeekOrigin origin) {
			return stream.Seek(offset, origin);
		}

		public override void SetLength(long value) {
			stream.SetLength(value);
		}

		private byte Shifted(byte b) {
			return (byte) (b + Shift);
		}

		public override int Read(byte[] buffer, int offset, int count) {
			int ret = stream.Read(buffer, offset, count);

			for (int i = offset; i < offset + count; i++)
				buffer[i] = Shifted(buffer[i]);

			return ret;
		}

		public override void Write(byte[] buffer, int offset, int count) {
			for (int i = offset; i < offset + count; i++)
				stream.WriteByte(Shifted(buffer[i]));
		}

		public override bool CanRead {
			get { return _canRead; }
		}

		public override bool CanSeek {
			get { return _canSeek; }
		}

		public override bool CanWrite {
			get { return _canWrite; }
		}

		public override long Length {
			get { return _length; }
		}

		public override long Position { get; set; }
	}
}