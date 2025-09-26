import unittest

def calculate_adoption_fee(age):
    """
    Calculate adoption fee based on pet age.
    - Pets 2 years or younger: $100
    - Adult pets (3+ years): $50
    - Invalid age (negative): "Invalid age"
    """
    if age < 0:
        return "Invalid age"
    elif age <= 2:
        return 100
    else:
        return 50

class TestCalculateAdoptionFee(unittest.TestCase):
    
    def test_calculate_adoption_fee(self):
        """Test the calculate_adoption_fee function with various scenarios"""
        
        # Test Case 1: Valid young pet age returns correct fee (100 for younger pets)
        result1 = calculate_adoption_fee(1)
        self.assertEqual(result1, 100, "1-year-old pet should have adoption fee of 100")
        
        # Additional young pet tests
        self.assertEqual(calculate_adoption_fee(0), 100, "0-year-old pet should have adoption fee of 100")
        self.assertEqual(calculate_adoption_fee(2), 100, "2-year-old pet should have adoption fee of 100")
        
        # Test Case 2: Adult pet returns correct fee (50 for adults)
        result2 = calculate_adoption_fee(3)
        self.assertEqual(result2, 50, "3-year-old pet should have adoption fee of 50")
        
        # Additional adult pet tests
        self.assertEqual(calculate_adoption_fee(5), 50, "5-year-old pet should have adoption fee of 50")
        self.assertEqual(calculate_adoption_fee(10), 50, "10-year-old pet should have adoption fee of 50")
        
        # Test Case 3: Invalid pet age returns "Invalid age"
        result3 = calculate_adoption_fee(-1)
        self.assertEqual(result3, "Invalid age", "Negative age should return 'Invalid age'")
        
        # Additional invalid age tests
        self.assertEqual(calculate_adoption_fee(-5), "Invalid age", "Negative age should return 'Invalid age'")

if __name__ == '__main__':
    unittest.main()
