consumer1(x:int[])
consumer2(x:int[][])
consumer3(x:int[][][])
 
test()
{
    consumer1(
        { {{}[0]}[0]
        , {}[0]
        , {}[0][0][0]
        })
    consumer2(
        { {{}[0]}[0]
        , {}[0]
        , {}[0][0][0]
        })
    consumer2(
        { { {{}[0]}[0]   }
        , { {}[0]        }
        , { {}[0][0][0]  }
        })
    consumer3(
        { {{}[0]}[0]
        , {}[0]
        , {}[0][0][0]
        })
    consumer3(
        { { {{}[0]}[0]  }
        , { {}[0]       }
        , { {}[0][0][0] }
        })
    consumer3(
        { { { {{}[0]}[0]  } }
        , { { {}[0]       } }
        , { { {}[0][0][0] } }
        })
}

//@PRACOWNIA
//@stop_after typechecker
