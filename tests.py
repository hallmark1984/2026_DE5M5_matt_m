import unittest
from docker_demo.calculator import Calculator


#calc = Calculator(num1=8,num2=2, matrix_1=[1,1], matrix_2=[1,1])
class TestOperations(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator(
            num1=8,
            num2=2,
            matrix_1=[1, 1],
            matrix_2=[1, 1]
        )

    def test_sum(self):
        self.assertEqual(self.calculator.get_sum(),10,'The sum was not 10')

    def test_subtract_1(self):
        self.assertEqual(self.calculator.get_subtract_a(),6,'The return was not 6')

    def test_subtract_2(self):
        self.assertEqual(self.calculator.get_subtract_b(),-6,'The return was not -6')

    #def test_divide(self):      
    #    self.assertEqual(self.calculator.get_quotient_a(),0.25,'The return was not 0.25')

    #def test_cross_product(self):
    #    self.assertEqual(self.calculator.get_cross_product(),[29,60],'The return was not 0.25')



if __name__ == '__main__':
    unittest.main()