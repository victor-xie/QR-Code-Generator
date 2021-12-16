import z256

def divide_terms(coefficient1, power1, coefficient2, power2):
    """
    Computes the quotient of two terms.

    The degree of the first term, power1, must be greater than or
    equal to the degree of the second term, power2.

    Inputs:
        - coefficient1: a Z_256 number representing the coefficient of the first polynomial term
        - power1: an integer representing the power of the first term.
        - coefficient2: a Z_256 number representing the coefficient of the second polynomial term
        - power2: an integer representing the power of the second term.

    Returns: an instance of a Polynomial that is the resulting
    term.
    """
    new_coeff = z256.div(coefficient1, coefficient2)
    new_pow = power1 - power2

    # Represent our answer as a Polynomial
    divided = Polynomial()
    divided = divided.add_term(new_coeff, new_pow)
    return divided

class Polynomial:
    """
    A class used to abstract methods on a polynomial in the finite
    field Z_256 (including numbers from 0 through 255).

    Since 256 is not prime, but is rather of the form p^n = 2^8, this
    representation uses special arithmetic via the z256 module so as to
    preserve multiplicative inverses (division) inside this field.
    """

    def __init__(self, terms=None):
        """
        Creates a new Polynomial object.  If a dictionary of terms is provided,
        they will be the terms of the polynomial,
        otherwise the polynomial will be the 0 polynomial.

        inputs:
            - terms: a dictionary of terms mapping powers to coefficients or None
              (None indicates that all coefficients are 0)
        """
        if terms != None:
            self._terms = dict(terms)
        else:
            self._terms = {}

    def __str__(self):
        """
        Returns: a string representation of the polynomial, containing the
        class name and all of the terms.
        """
        # Create a string of the form "ax^n + bx^n-1 + ... + c" by
        # creating a string representation of each term, and inserting
        # " + " in between each
        term_strings = []

        # Add the highest powers first
        powers = list(self._terms.keys())
        powers.sort(reverse=True)
        for power in powers:
            coefficient = self._terms[power]
            # Don't print out terms with a zero coefficient
            if coefficient != 0:
                # Don't print "x^0"; that just means it's a constant
                if power == 0:
                    term_strings.append("%d" % coefficient)
                else:
                    term_strings.append("%d*x^%d" % (coefficient, power))

        terms_str = " + ".join(term_strings)
        if terms_str == "":
            terms_str = "0"
        return "Polynomial: %s" % terms_str

    def __eq__(self, other_polynomial):
        """
        Check if another polynomial is equvalent

        inputs:
            - other_polynomial: a Polynomial object

        Returns a boolean: True if other_polynomial contains
        the same terms as self, False otherwise.
        """
        # Make sure that other_polynomial is a Polynomial
        if not isinstance(other_polynomial, Polynomial):
            return False

        # Get the terms of the other_polynomial
        terms = other_polynomial.get_terms()

        # Check that all terms in other_polynomial appear in self
        for power, coefficient in terms.items():
            if coefficient != 0:
                if power not in self._terms:
                    return False
                if self._terms[power] != coefficient:
                    return False

        # Check that all terms in self appear in other_polynomial
        for power, coefficient in self._terms.items():
            if coefficient != 0:
                if power not in terms:
                    return False
                if terms[power] != coefficient:
                    return False

        return True

    def __ne__(self, other_polynomial):
        """
        Check if another polynomial is NOT equivalent

        inputs:
            - other_polynomial: a Polynomial object

        Return a boolean: False if other_polynomial contains the same terms
        as self, True otherwise.
        """
        return not self.__eq__(other_polynomial)

    def get_terms(self):
        """
        Returns: a dictionary of terms, mapping powers to coefficients.
        This dictionary is a completely new object and is not a reference
        to any internal structures.
        """
        terms = dict(self._terms)
        return terms

    def get_degree(self):
        """
        Returns: the maximum power over all terms in this polynomial.
        """
        # Since we don't clean zero-coefficient powers out of our dictionary,
        # we need a trickier get_degree function, to take into account that
        # some coefficients could be zero.
        highest_power = 0
        for power in self._terms:
            if (power > highest_power) and (self._terms[power] != 0):
                highest_power = power

        return highest_power


    def get_coefficient(self, power):
        """
        Determines the coefficient of x^(power) in this polynomial.
        If there is no coefficient of x^(power), this method
        returns 0.

        inputs:
            - power: an integer representing a polynomial power

        Returns: a Z_256 number that is the coefficient or 0 if there
                 is no term of the given power
        """
        if power in self._terms:
            return self._terms[power]
        else:
            return 0

    def add_term(self, coefficient, power):
        """
        Add one term to this polynomial.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the sum of adding this polynomial
        to (coefficient) * x^(power) using Z_256 arithmetic to add
        coefficients, if necessary.
        """
        #Get the existening polynomial's coefficient at the additional term's [pwer
        poly_coef = self.get_coefficient(power)
        #Add the two coefficients in z256
        new_coef = z256.add(poly_coef, coefficient)
        #Get the dictionary mapping of the original polynomials' powers to coefficients
        poly_map = self.get_terms()
        #Update the coefficient of the corresponding power
        poly_map[power] = new_coef
        #Use this updated mapping to create the updated polynomial
        added = Polynomial(poly_map)
        return added

    def subtract_term(self, coefficient, power):
        """
        Subtract one term from this polynomial.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the difference of this polynomial
        and (coefficient) * x^(power) using Z_256 arithmetic to subtract
        coefficients, if necessary.
        """
        #Addition and subtraction produce the same result in z256
        #Get the existening polynomial's coefficient at the additional term's [pwer
        poly_coef = self.get_coefficient(power)
        #Add the two coefficients in z256
        new_coef = z256.add(poly_coef, coefficient)
        #Get the dictionary mapping of the original polynomials' powers to coefficients
        poly_map = self.get_terms()
        #Update the coefficient of the corresponding power
        poly_map[power] = new_coef
        #Use this updated mapping to create the updated polynomial
        subtracted = Polynomial(poly_map)
        return subtracted

    def multiply_by_term(self, coefficient, power):
        """
        Multiply this polynomial by one term.

        inputs:
            - coefficient: a Z_256 number representing the coefficient of the term
            - power: an integer representing the power of the term

        Returns: a new Polynomial that is the product of multiplying
        this polynomial by (coefficient) * x^(power).
        """
        # Must update every power and coefficient
        #Get the dictionary mapping of the original polynomials' powers to coefficients
        poly_map = self.get_terms()
        #Create a new mapping to store the updated polynomial
        multiplied_poly_map = {}
        #Iterate through the keys and update the powers and coefficients
        for poly_power in poly_map:
            updated_coef = z256.mul(poly_map[poly_power], coefficient)
            updated_power = poly_power + power
            multiplied_poly_map[updated_power] = updated_coef
        #Create new polynomial using updated mapping
        multiplied = Polynomial(multiplied_poly_map)

        return multiplied
    
    def add_polynomial(self, other_polynomial):
        """
        Compute the sum of the current polynomial other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the sum of both polynomials.
        """
        #Create a copy of the original polynomial
        added = Polynomial(self.get_terms())
        #Iterate through every key-value pair in other_polynomial and use the add_term() method
        other_poly_map = other_polynomial.get_terms()
        for other_power in other_poly_map:
            other_coef = other_poly_map[other_power]
            added = added.add_term(other_coef, other_power)
            
        return added

    def subtract_polynomial(self, other_polynomial):
        """
        Compute the difference of the current polynomial and other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the difference of both polynomials.
        """
        #Create a copy of the original polynomial
        subtracted = Polynomial(self.get_terms())
        #Iterate through every key-value pair in other_polynomial and use the add_term() method
        other_poly_map = other_polynomial.get_terms()
        for other_power in other_poly_map:
            other_coef = other_poly_map[other_power]
            subtracted = subtracted.add_term(other_coef, other_power)
            
        return subtracted

    def multiply_by_polynomial(self, other_polynomial):
        """
        Compute the product of the current polynomial and other_polynomial.

        inputs:
            - other_polynomial: a Polynomial object

        Returns: a new Polynomial that is the product of both polynomials.
        """
        #Create a copy of the original polynomial
        multiplied_out = Polynomial()
        #Store the power-coefficient mapping of other_polynomial
        other_poly_map = other_polynomial.get_terms()
        #Iterate through the powers of other_polynomial
        for other_power in other_poly_map:
            #Access the corresponding coefficient
            other_coef = other_poly_map[other_power]
            #Perform multiply_by_term() using the other_polynomial term and the original polynomial
            term_multiplied = self.multiply_by_term(other_coef, other_power)
            #Add the result of this term multiplication to multiplied out using add_polynomial()
            multiplied_out = multiplied_out.add_polynomial(term_multiplied)
        return multiplied_out

    def remainder(self, denominator):
        """
        Compute a new Polynomial that is the remainder after dividing this
        polynomial by denominator.

        Note: does *not* return the quotient; only the remainder!

        inputs:
            - denominator: a Polynomial object

        Returns: a new polynomial that is the remainder
        """
        #Itialize remainder
        remainder = Polynomial()
        #Create a copy of the numerator polynomial
        numerator = Polynomial(self.get_terms())
        #Get the degree and leading coefficient of the numerator
        numerator_degree = numerator.get_degree()
        numerator_lead_coef = numerator.get_coefficient(numerator_degree)
        #Get the degree and leading coefficient of the denominator
        denominator_degree = denominator.get_degree()
        denominator_lead_coef = denominator.get_coefficient(denominator_degree)
        #Continue dividing so long as the numerator's degree 
        #is greater than or equal to the denominator's degree
        while numerator_degree >= denominator_degree and numerator_degree >= 0:
            #Get the polynomial you have to multiply the divisor by
            multiply_by = divide_terms(numerator_lead_coef, numerator_degree, 
                                       denominator_lead_coef, denominator_degree)
            #Get the increased divisor
            increased_divisor = denominator.multiply_by_polynomial(multiply_by)

            #Subtract the increased divisor from the numerator
            numerator = numerator.subtract_polynomial(increased_divisor)
            if numerator.__eq__(Polynomial({0:0})):
                break
       
            #Update the numerator values
            numerator_degree = numerator.get_degree()
            numerator_lead_coef = numerator.get_coefficient(numerator_degree)

        #What's left in the numerator is the remainder
        remainder = numerator
        return remainder

#test = Polynomial({0:1})
#print(test)
#test_new = test.remainder(Polynomial({0:14}))
#print(test_new)
             

def create_message_polynomial(message, num_correction_bytes):
    """
    Creates the appropriate Polynomial to represent the
    given message. Relies on the number of error correction
    bytes (k). The message polynomial is of the form
    message[i]*x^(n+k-i-1) for each number/byte in the message.

    Inputs:
        - message: a list of integers (each between 0-255) representing data
        - num_correction_bytes: an integer representing the number of
          error correction bytes to use

    Returns: a Polynomial with the appropriate terms to represent the
    message with the specified level of error correction.
    """
    #Get n, the number of message bytes
    message_polynomial = Polynomial()
    num_message_bytes = len(message)
    for idx in range(num_message_bytes):
        m_coefficient = message[idx]
        m_power = num_message_bytes + num_correction_bytes - idx - 1
        message_polynomial = message_polynomial.add_term(m_coefficient, m_power)
    return message_polynomial

def create_generator_polynomial(num_correction_bytes):
    """
    Generates a static generator Polynomial for error
    correction, which is the product of (x-2^i) for all i in the
    set {0, 1, ..., num_correction_bytes - 1}.

    Inputs:
        - num_correction_bytes: desired number of error correction bytes.
                                In the formula, this is represented as k.

    Returns: generator Polynomial for generating Reed-Solomon encoding data.
    """
    generator_polynomial = Polynomial({0:1})
    #Iterate from 0 to k-1, updating the generator polynomial
    #variable by multiplying in the most recent polynomial term
    for idx in range(num_correction_bytes):
        #Calculates the 2^i constant in z256
        converted_constant = (z256.power(2, idx)) % 256
        #Gets the term that will be multiplied into generator_polynomial
        term_multiplier = Polynomial({1:1, 0:converted_constant})
        #Multiply term into generator_polynomial
        generator_polynomial = generator_polynomial.multiply_by_polynomial(term_multiplier)

    return generator_polynomial

def reed_solomon_correction(encoded_data, num_correction_bytes):
    """
    Corrects the encoded data using Reed-Solomon error correction

    Inputs:
        - encoded_data: a list of integers (each between 0-255)
                        representing an encoded QR message.
        - num_correction_bytes: desired number of error correction bytes.

    Returns: a polynomial that represents the Reed-Solomon error
    correction code for the input data.
    """
    #Get the message and generator polynomials
    message_polynomial = create_message_polynomial(encoded_data, num_correction_bytes)
    generator_polynomial = create_generator_polynomial(num_correction_bytes)
    
    remainder = message_polynomial.remainder(generator_polynomial)
    return remainder
