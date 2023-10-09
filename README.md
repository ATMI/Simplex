# Linear program solver

<!-- ABOUT THE PROJECT -->
## About The Project
Simplex method implementation to solve linear programming problems

### Built With

* [Python](https://www.python.org/)

<!-- GETTING STARTED -->
## Requirements
To install dependencies you may use pip.

open terminal and run the following command:

    pip install -r requirements.txt

<!-- USAGE EXAMPLES -->
## QuickStart
Input format:
The input file (input.txt) contains:
* A vector of coefficients of objective function - C.
* A matrix of coefficients of constraint function - A.
* A vector of right-hand side numbers - b.

Input Example:

    #Objective function:
    1 3
    #Matrix:
    1 1
    -1 1
    #Vector b:
    2 4

Running the code:

    python main.py -p max

The output contains:

* The string ”The method is not applicable!”
or
* A vector of decision variables - x
* Maximum (minimum) value of the objective function.

Output of the Example:
    
    A vector of decision variables: [0. 2.]
    Optimal value: [6.]

## Options

Help -h: show available commands. 

Problem -p: specify type of the problem min or max (default: max)

Input -i: specify input file (default: input.txt)

Accuracy -a: specify approximation accuracy (default: 0.001)

Log -l: set logging to true (default: false)

### Further reading
* [Simplex method](https://en.wikipedia.org/wiki/Simplex_algorithm)