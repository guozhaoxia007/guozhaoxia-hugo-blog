class A():
    def a(self):
        print 'aaa'

class B(A):
    def b(self):
        print 'bbb'

class C(B):
    def c(self):
        print 'ccc'


ci = C()
ci.c()
ci.b()
ci.a()
