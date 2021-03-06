Rules for writing and uploading code:

1. Use Python 3.5+ (or Matlab for control if desired)
2. Use clear, standard indentation according to PEP conventions
3. When defining a function or class:
	- Write comments about the functionalities at the top of a new definition
	- Define Inputs and Outputs and their types appropriately

	eg.

	def quadratic(x: float) -> float:
    	    """
    	    param x: Value to be raised to the power 2
    	    return: x raised to the power 2
    	    """
    	    return x**2 	# Write additional explanation next to code

4. Separate functions and code chunks into different files as much as possible for an overseeable structure
5. NO HARDCODING! Make everything into variables and save values in other files,
   such as .csv, .txt, .xlsx, .mat and other data file formats. Do NOT save parameter values in a .py file
   which has to be edited manually if a value changes, as this is a perfect spot for bugs to show up.
6. Write unit tests after finishing a block of code. Use the unittest module for this.
7. When pushing code to the remote repository, push into your section's branch. Merges
   must be approved by info systems chief. 
8. Do not couple modules (eg. A.py imports from B.py, while B.py also imports from A.py)

Look at example.py for a proper python file layout