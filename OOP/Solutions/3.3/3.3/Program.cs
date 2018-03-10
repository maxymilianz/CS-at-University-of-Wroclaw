using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using TNTNamespace;

namespace _3._3 {
    class Program {

        static void Main(string[] args) {
            TimeNTon[] tnts = new TimeNTon[5];

            for (int i = 0; i < 5; i++) {
                tnts[i] = TimeNTon.instance();
                Console.WriteLine(tnts[i].getId());
            }
        }
    }
}
