"""Simple classes to test introspection functions"""

class A(): pass
class B(A): pass
class C(B): pass
class D(): pass
class E(D): pass
class F(E): pass
class G(C, F): pass
class H(): pass
class J(G, H, D): pass

class Super:
    class_level_variable = "Who can see me?"

    def hello(self):
        self.data = 'More'

class Sub(Super):
    def hola(self):
        self.data2 = 'Cowbell'
