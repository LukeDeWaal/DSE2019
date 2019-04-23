Rules for writing and uploading code:

1. Use Python 3.5+ (or Matlab for control)
2. Use clear, standard indentation according to PEP conventions
3. When defining a function or class:
	- Write in comments about the functionalities
	- Define Inputs and Outputs and their types

	eg.

	def quadratic(x: float) -> float:
    	    """
    	    param x: Value to be raised to the power 2
    	    return: x raised to the power 2
    	    """
    	    return x**2 	# Write additional explanation next to code

4. Separate functions and code chunks into different files
5. NO HARDCODING! Make everything into variables and save values in other files,
   such as .csv, .txt, .xlsx, .mat and other data file formats.
6. Write unit tests after finishing a block of code. Use the unittest module for this.
7. When pushing code to the remote repository, push into your section's branch. Merges
   must be approved by info systems chief. 
