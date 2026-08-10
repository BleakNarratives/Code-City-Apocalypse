// Buggy JavaScript Code - Test Case for Code City 2.0
// Contains intentional bugs for testing bug detection

// Console.log left in code (should be flagged)
console.log("Debug message that should be removed");

// Loose equality comparison (should be flagged)
function checkEquality(a, b) {
    if (a == b) {  // Should use ===
        return true;
    }
    return false;
}

// Another loose equality
if (value == null) {  // Should use ===
    console.log("Value is null or undefined");
}

// Function with potential issues
function calculateTotal(items) {
    let sum = 0;
    
    // Debug console.log
    console.log("Calculating total...");
    
    for (let i = 0; i < items.length; i++) {
        sum += items[i].price;
    }
    
    // Another debug statement
    console.log(`Total calculated: ${sum}`);
    
    return sum;
}

// Unused variable
const unusedVariable = "I'm never used";

// Function that could be simplified
function isEven(number) {
    if (number % 2 == 0) {  // Loose equality again
        return true;
    } else {
        return false;
    }
}

// Main function
function main() {
    console.log("Testing JavaScript bug detection...");
    
    // Test equality function
    const result = checkEquality(5, "5"); // This will return true due to loose equality
    console.log(`5 == "5": ${result}`);
    
    // Test calculation
    const prices = [10, 20, 30];
    const total = calculateTotal(prices);
    console.log(`Total: ${total}`);
    
    // Test even function
    const evenResult = isEven(10);
    console.log(`10 is even: ${evenResult}`);
}

// Start the program
main();