import unittest

from core.cartao import Cartao


class CartaoTest(unittest.TestCase):
    def testacertos(self):
        cartao_a = Cartao((1, 2, 3, 4, 7))
        cartao_b = Cartao([4, 5, 6, 7])
        cartao_c = Cartao([])

        self.assertEqual(len(cartao_a.conferir(cartao_b)), 2)
        self.assertEqual(len(cartao_b.conferir(cartao_a)), 2)

        self.assertEqual(len(cartao_c.conferir(cartao_a)), 0)
        self.assertEqual(len(cartao_c.conferir(cartao_b)), 0)
        self.assertEqual(len(cartao_c.conferir(cartao_c)), 0)

    def testStr(self):
        cartao = Cartao((0, 1, 2, 3, 4, 7))

        self.assertEqual(str(cartao), "00 - 01 - 02 - 03 - 04 - 07")
        self.assertEqual(cartao.to_string(';'), "00;01;02;03;04;07")


    def testEqual(self):
        cartao_a = Cartao((1, 2, 3, 4, 7))
        cartao_b = Cartao((2, 1, 7, 3, 4))

        self.assertEqual(cartao_a, cartao_b)

if __name__ == "__main__":
    unittest.main()
