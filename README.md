#Econometrics Regressions
#By: Christopher Li

# Files:
regress.py - has all of the regression functions in class data  
pipeline.py - runs the files for the problem set  
helper.py - contains a few helper functions  
montecarlo - contains the montecarlo simulations  
parse.py - parses csv files  
requirements.txt - holds the necessary installations  
READ.md - this file  
csv/ - contains all csv  
venv/ - contains the virtual environment  
problem sets/ - contains the pdfs for problem sets with STATA problems  

# Requirements
The "venv" virtual environment does not support any directories in the working directory to have a blank space in them. Either the file must be place in a working directory with no spaces, or you could skip the first command below and globally install the modules.

# Implementation

To run the code, run these commands in the home directory:

source venv/bin/activate  
pip install -r requirements.txt  
python  
>> execfile('pipeline.py')
