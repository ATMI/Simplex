# Linear program solver

<!-- ABOUT THE PROJECT -->
## About The Project
Simplex method implementation to solve linear programming problems

### Built With

* [Python](https://www.python.org/)

<!-- GETTING STARTED -->
## Running the code
open terminal and run the following commands:

    pip install -r requirements.txt
    python main.py

### Further reading
* [Simplex method](https://en.wikipedia.org/wiki/Simplex_algorithm)


<!-- USAGE EXAMPLES -->
## Usage
Input format:
The input contains:
* Maximize or minimize
* The approximation accuracy.
* A vector of coefficients of objective function - C.
* A matrix of coefficients of constraint function - A.
* A vector of right-hand side numbers - b.

Input Example:

    Maximize, 0.01
    #Objective function:
    1, 3
    #Matrix:
    1, 1
    -1, 1
    #Vector b:
    2, 4

Output format
The output contains:
* The string ”The method is not applicable!”
or
* A vector of decision variables - x
* Maximum (minimum) value of the objective function.

Output of the Example:
    
    # todo 
