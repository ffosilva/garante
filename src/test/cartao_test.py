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

    def testClusters(self):
        cartao = Cartao((1, 2, 3, 4, 7))
        assert cartao.num_clusters() == 2

        cartao = Cartao(())
        assert cartao.num_clusters() == 0

        cartao = Cartao((3, 5, 7, 9))
        assert cartao.num_clusters() == 4

        cartao = Cartao((1, 3, 5, 7, 9))
        assert cartao.num_clusters() == 5

        cartao = Cartao((1, 2, 3, 4, 5, 6, 7, 8, 9))
        assert cartao.num_clusters() == 1

    def testMinMax(self):
        cartao = Cartao((1,))
        assert cartao.min() == 1
        assert cartao.max() == 1
        
        cartao = Cartao((2,10,20,30,40))
        assert cartao.min() == 2
        assert cartao.max() == 40

    def testDistancia(self):
        cartao = Cartao((1, 2, 3, 4, 7))
        assert cartao.distancia(1, 2) == 1
        assert cartao.distancia(1, 3) == 2
        assert cartao.distancia(1, 4) == 3
        assert cartao.distancia(1, 5) == 6
        assert cartao.distancia(2, 3) == 1
        assert cartao.distancia(2, 4) == 2
        assert cartao.distancia(2, 5) == 5
        assert cartao.distancia(3, 4) == 1
        assert cartao.distancia(3, 5) == 4
        assert cartao.distancia(4, 5) == 3
        
    def testAdd(self):
        cartao = Cartao(())
        cartao.add(1)
        cartao.add(2)
        cartao.add(3)
        cartao.add(4)
        cartao.add(5)
        cartao.add(6)
        cartao.add(7)
        cartao.add(8)
        cartao.add(9)
        cartao.add(10)
        cartao.add(11)
        cartao.add(12)
        cartao.add(13)
        cartao.add(14)
        cartao.add(15)
        cartao.add(16)
        cartao.add(17)
        cartao.add(18)
        assert len(cartao) == 18
        assert cartao.min() == 1
        assert cartao.max() == 18
        assert cartao.num_clusters() == 1

    def testRemove(self):
        cartao = Cartao((1, 2, 3, 4, 7))
        cartao.remove(2)
        cartao.remove(3)
        cartao.remove(4)
        assert len(cartao) == 2
        assert cartao.min() == 1
        assert cartao.max() == 7
        assert cartao.num_clusters() == 2

if __name__ == "__main__":
    unittest.main()
