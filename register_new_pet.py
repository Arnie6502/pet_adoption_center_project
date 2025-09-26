import unittest
import warnings
from pet_adoption_center import register_new_pet

class TestRegisterNewPet(unittest.TestCase):
    
    def test_register_new_pet_success(self):
        """Test Case 1: Test that a new pet is successfully added to the adoption list."""
        adoption_list = []
        new_pet = {'name': 'Buddy', 'species': 'Dog', 'age': 3}
        
        result = register_new_pet(new_pet, adoption_list)
        
        self.assertEqual(len(result), 1)
        self.assertIn(new_pet, result)
    def test_register_duplicate_pet_warning(self):
        """Test Case 2: Test that a warning is raised when attempting to add a pet with a duplicate name (name-based duplication only)."""
        adoption_list = [{'name': 'Max', 'species': 'Cat', 'age': 2}]
        duplicate_pet = {'name': 'Max', 'species': 'Dog', 'age': 5}  # Same name, different species and age
        duplicate_pet = {'name': 'Max', 'species': 'Dog', 'age': 5}  # Same name
        
        with self.assertWarns(UserWarning):
            result = register_new_pet(duplicate_pet, adoption_list)
            # Should still have only one pet (original)
            self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()
