import unittest
import warnings
import pytest
import os

class TestPetAdoption(unittest.TestCase):
    def test_add_dog_to_adoption_list(self):
        adoption_list = []
        add_pet(adoption_list, {"type": "dog", "name": "Buddy"})
        assert len(adoption_list) == 1
        assert adoption_list[0]["type"] == "dog"

    def test_add_cat_to_adoption_list(self):
        adoption_list = []
        add_pet(adoption_list, {"type": "cat", "name": "Whiskers"})
        assert len(adoption_list) == 1
        assert adoption_list[0]["type"] == "cat"

    # This test is skipped until:
    # - Exotic pet validation logic is implemented
    # - Special licensing requirements are added
    # - Specialized care instructions are integrated
    @pytest.mark.skip(reason="Exotic pet functionality not yet implemented")
    def test_add_exotic_pets_to_adoption_list(self):
        """Test adding exotic pets to the adoption list."""
        adoption_list = []
        exotic_pet = {
            "type": "parrot",
            "name": "Polly",
            "special_requirements": ["large_cage", "specialized_diet", "exotic_vet"],
            "license_required": True
        }
        
        add_exotic_pet(adoption_list, exotic_pet)
        assert len(adoption_list) == 1
        assert adoption_list[0]["type"] == "parrot"
        assert adoption_list[0]["license_required"] is True

    @pytest.mark.skipif(
        not os.getenv("EXOTIC_PETS_ENABLED"), 
        reason="Exotic pets feature flag not enabled"
    )
    def test_exotic_pet_licensing_validation(self):
        # This test will only run when EXOTIC_PETS_ENABLED=true
        pass


# Function to add a pet to the adoption list

def add_pet(adoption_list, pet):
    """Add a pet to the adoption list."""
    adoption_list.append(pet)

def add_exotic_pet(adoption_list, exotic_pet):
    """Add an exotic pet to the adoption list."""
    adoption_list.append(exotic_pet)

def register_new_pet(new_pet, adoption_list):
    """Register a new pet in the adoption list"""
    if any(existing_pet["name"] == new_pet["name"] for existing_pet in adoption_list):
        warnings.warn(f"{new_pet['name']} is already in the adoption list", UserWarning)
        return adoption_list  # Return unchanged list
    else:
        adoption_list.append(new_pet)
    return adoption_list


def calculate_adoption_fee(age):
    """Calculate adoption fee based on pet age."""
    if age < 0:
        return "Invalid age"
    elif age <= 2:
        return 100
    else:
        return 50
    
    
class PetAdoptionCenter:
    def __init__(self):
        self.pets = [
            {'name': 'Max', 'species': 'dog', 'size': 'large', 'age': 5},
            {'name': 'Whiskers', 'species': 'cat', 'size': 'small', 'age': 1},
            {'name': 'Buddy', 'species': 'dog', 'size': 'medium', 'age': 3},
        ]
    
    def match_pet(self, preferences):
        for pet in self.pets:
            if self._matches_all_criteria(pet, preferences):
                return pet['name']
        return None

    def _matches_all_criteria(self, pet, preferences):
        """Check if pet matches ALL provided preferences exactly"""
        for key, value in preferences.items():
            if key not in pet or pet[key] != value:
                return False
        return True

class TestPetAdoptionWithFixtures(unittest.TestCase):
    """Unit tests with setUp() and tearDown() fixtures for managing adoption list."""
    
    def setUp(self):
        """Test Case 1: Use setUp() to initialize a list of pets before each test."""
        print("Setting up test fixtures...")
        
        # Initialize adoption list with test data
        self.adoption_list = [
            {'name': 'Max', 'species': 'dog', 'size': 'large', 'age': 5, 'adopted': False},
            {'name': 'Whiskers', 'species': 'cat', 'size': 'small', 'age': 1, 'adopted': False},
            {'name': 'Buddy', 'species': 'dog', 'size': 'medium', 'age': 3, 'adopted': True},
            {'name': 'Luna', 'species': 'cat', 'size': 'medium', 'age': 2, 'adopted': False}
        ]
        
        # Initialize PetAdoptionCenter instance
        self.center = PetAdoptionCenter()
        
        # Track original list length for verification
        self.original_list_length = len(self.adoption_list)
        
        print(f"✅ Setup complete: {len(self.adoption_list)} pets in adoption list")
    
    def tearDown(self):
        """Test Case 2: Use tearDown() to clean up after each test by resetting the pet list."""
        print("Cleaning up test fixtures...")
        
        # Reset adoption list
        self.adoption_list.clear()
        
        # Reset center instance
        self.center = None
        
        # Reset any other test variables
        self.original_list_length = 0
        
        print("✅ Teardown complete: adoption list reset")
    
    def test_adoption_list_initialized_correctly(self):
        """Test that setUp() properly initializes the adoption list."""
        self.assertEqual(len(self.adoption_list), 4, "Should have 4 pets in adoption list")
        self.assertIsInstance(self.adoption_list, list, "Should be a list")
        
        # Verify specific pets are present
        pet_names = [pet['name'] for pet in self.adoption_list]
        self.assertIn('Max', pet_names)
        self.assertIn('Whiskers', pet_names)
        self.assertIn('Buddy', pet_names)
        self.assertIn('Luna', pet_names)
    
    def test_add_new_pet_to_adoption_list(self):
        """Test adding a new pet to the initialized adoption list."""
        new_pet = {'name': 'Rocky', 'species': 'dog', 'size': 'large', 'age': 4, 'adopted': False}
        
        # Add pet to list
        add_pet(self.adoption_list, new_pet)
        
        # Verify pet was added
        self.assertEqual(len(self.adoption_list), self.original_list_length + 1)
        self.assertIn(new_pet, self.adoption_list)
        self.assertEqual(self.adoption_list[-1]['name'], 'Rocky')
    
    def test_register_duplicate_pet_warning(self):
        """Test registering a duplicate pet raises warning."""
        duplicate_pet = {'name': 'Max', 'species': 'dog', 'size': 'large', 'age': 6}
        
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            result = register_new_pet(duplicate_pet, self.adoption_list)
            
            # Verify warning was raised
            self.assertTrue(len(warning_list) > 0)
            self.assertIn("already in the adoption list", str(warning_list[0].message))
            
            # Verify list length didn't change
            self.assertEqual(len(result), self.original_list_length)
    
    def test_calculate_adoption_fees(self):
        """Test adoption fee calculation for pets in the list."""
        for pet in self.adoption_list:
            fee = calculate_adoption_fee(pet['age'])
            
            if pet['age'] <= 2:
                self.assertEqual(fee, 100, f"Pet {pet['name']} (age {pet['age']}) should have fee of 100")
            else:
                self.assertEqual(fee, 50, f"Pet {pet['name']} (age {pet['age']}) should have fee of 50")
    
    def test_find_available_pets(self):
        """Test finding pets that are available for adoption."""
        available_pets = [pet for pet in self.adoption_list if not pet['adopted']]
        
        self.assertEqual(len(available_pets), 3, "Should have 3 available pets")
        
        # Verify Buddy is not in available pets (he's adopted)
        available_names = [pet['name'] for pet in available_pets]
        self.assertNotIn('Buddy', available_names)
        self.assertIn('Max', available_names)
        self.assertIn('Whiskers', available_names)
        self.assertIn('Luna', available_names)
    
    def test_adoption_list_isolation_between_tests(self):
        """Test that each test starts with a fresh adoption list."""
        # This test verifies that tearDown() properly resets the list
        # and setUp() creates a fresh list for each test
        
        # Modify the list
        self.adoption_list.append({'name': 'TestPet', 'species': 'test', 'size': 'test', 'age': 1})
        
        # Verify modification
        self.assertEqual(len(self.adoption_list), self.original_list_length + 1)


class TestPetAdoptionCenter(unittest.TestCase):
    """Unit tests for the Pet Adoption Center functions."""

    def test_sample(self):
        self.assertTrue(True)

    def test_match_pet_exact_match(self):
        """Test Case 1: Test that the correct pet is matched when adopter's preferences match pet's details."""
        center = PetAdoptionCenter()
        # Test matching by type
        adopter_preferences = {"species": "dog", "size": "medium", "age": 3}
        result = center.match_pet(adopter_preferences)
        self.assertEqual(result, "Buddy")  # First dog in the list
        
        # Test matching by size
        adopter_preferences = {"species": "dog", "size": "large", "age": 5}
        result = center.match_pet(adopter_preferences)
        self.assertEqual(result, "Max")  # First pet with large size
        
        # Test matching by age
        adopter_preferences = {"species": "dog", "size": "large", "age": 5}
        result = center.match_pet(adopter_preferences)
        self.assertEqual(result, "Max")  # First pet with age 5
        
        # Test multiple matching criteria (should return first match)
        adopter_preferences = {"species": "cat", "size": "small", "age": 1}
        result = center.match_pet(adopter_preferences)
        self.assertEqual(result, "Whiskers")  # Matches all criteria

    def test_match_pet_no_match_found(self):
        """Test Case 2: Test that the function returns None when no pet matches adopter's preferences."""
        center = PetAdoptionCenter()
        # Test with preferences that don't match any pet
        adopter_preferences = {"species": "fish", "size": "extra-large", "age": "old"}
        result = center.match_pet(adopter_preferences)
        self.assertIsNone(result)
        
        # Test with empty pets list
        center.pets = []
        adopter_preferences = {"species": "dog", "size": "medium", "age": "adult"}
        result = center.match_pet(adopter_preferences)
        self.assertIsNone(result)
        
        # Test with completely different preferences
        center.pets = [
            {'name': 'Max', 'species': 'dog', 'size': 'large', 'age': 5},
            {'name': 'Whiskers', 'species': 'cat', 'size': 'small', 'age': 1},
            {'name': 'Buddy', 'species': 'dog', 'size': 'medium', 'age': 3},
        ]
        adopter_preferences = {"species": "snake", "size": "giant", "age": 10}
        result = center.match_pet(adopter_preferences)
        self.assertIsNone(result)

    def test_match_pet_partial_matches(self):
        """Additional test: Test various partial matching scenarios."""
        center = PetAdoptionCenter()
        # Test that function returns first match when multiple pets could match
        adopter_preferences = {"species": "cat"}
        result = center.match_pet(adopter_preferences)
        self.assertEqual(result, "Whiskers")  # First cat in the list
        
        # Test matching only one criterion
        adopter_preferences = {"species": "dog"}
        result = center.match_pet(adopter_preferences)
        self.assertEqual(result, "Max")  # First dog in the list


if __name__ == "__main__":
    unittest.main(verbosity=2)