import numpy as np

class Calculator:
    def __init__(self,num1=1,num2=1, matrix_1=[1,1], matrix_2=[1,1]):
        self.num1 = num1
        self.num2 = num2 
        self.matrix_1 = matrix_1
        self.matrix_2 = matrix_2    

    def get_sum(self):
        return self.num1 + self.num2

    def get_subtract_a(self):
        return self.num1 - self.num2
    def get_subtract_b(self):
        return self.num2 - self.num1

    def get_quotient_a(self):
        if self.num2==0 or self.num1 == 0:
            return 0
        else:
            return self.num2 / self.num1

    def get_quotient_b(self):
        if self.num1==0 or self.num2 == 0:
            return        
        else:
            return self.num1 / self.num2

    def get_product(self):
        return self.num2 * self.num1

    def get_cross_product(self):
        return np.cross(self.matrix_1, self.matrix_2)

    def get_matrix_multiplication(self):  
        return np.dot(self.matrix_1, self.matrix_2)

