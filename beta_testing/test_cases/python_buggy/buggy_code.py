#!/usr/bin/env python3
"""
Buggy Python Code - Test Case for Code City 2.0
Contains intentional bugs for testing bug detection
"""

# Import statements
def calculate_sum(a, b):
    """Calculate sum of two numbers - missing return statement"""
    result = a + b  # Unused variable
    
# Syntax error - missing colon
def check_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

# Line too long - exceeds 120 characters
this_is_a_very_long_line_that_exceeds_the_recommended_120_character_limit_and_should_be_flagged_by_the_code_city_bug_detection_system_as_a_style_violation_that_needs_to_be_fixed_for_better_code_readability_and_maintenance

# Trailing whitespace issue
variable_with_trailing_whitespace = 42

# Unused function
def unused_function():
    """This function is never called"""
    print("I'm never used!")

# Main function
def main():
    # This should work fine
    print("Testing Code City bug detection...")
    
    # Call function with syntax error (will cause runtime error)
    try:
        result = check_even(10)
        print(f"10 is even: {result}")
    except:
        print("Error in check_even function!")
    
    # Call function that doesn't return anything
    calculate_sum(5, 3)
    
    # Variable that's never used
    never_used_variable = "I serve no purpose"
    
    # Long line that should be flagged
    another_very_long_line_that_exceeds_the_recommended_120_character_limit_and_will_be_detected_by_code_city_as_a_potential_readability_issue_that_should_be_addressed_in_code_review

if __name__ == "__main__":
    main()