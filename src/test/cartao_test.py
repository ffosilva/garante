import unittest
from model.cartao import Cartao


class CartaoTest(unittest.TestCase):
    def testConferir(self):
        cartao_a = Cartao((1, 2, 3, 4, 7))
        cartao_b = Cartao([4, 5, 6, 7])
        cartao_c = Cartao([])

        self.assertEqual(cartao_a.conferir(cartao_b), 2)
        self.assertEqual(cartao_b.conferir(cartao_a), 2)

        self.assertEqual(cartao_c.conferir(cartao_a), 0)
        self.assertEqual(cartao_c.conferir(cartao_b), 0)
        self.assertEqual(cartao_c.conferir(cartao_c), 0)
    
    def testStr(self):
        cartao = Cartao((0, 1, 2, 3, 4, 7))
        cartao_str = str(cartao)
        print(cartao_str)



if __name__ == "__main__":
    unittest.main()
