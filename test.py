class Test:
  def test(self):
    print("wew")
    
a = Test()

a.test()
a.test = lambda: print("wew!")
a.test()