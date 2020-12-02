#Readme/Installation and Usage

Running this program requires Python, which can be downloaded here:
https://www.python.org/downloads/

It is recommended that you install Python version 3.8.2, but as a minimum, you need Python 3.6 or newer, as this is a dependency for CuPy, the CUDA library for Python. CuPy has a few dependencies that are required in order to install it. Find an installation guide here:
https://docs.cupy.dev/en/latest/install.html

You will most likely find running Python programs and managing packages is easier with an installation of Anaconda. A guide to installing it can be found here:
https://docs.anaconda.com/anaconda/user-guide/getting-started/

The programs in our project require several additional Python modules, which must also be installed on your computer prior to running them. To install them via the command line, type the following commands:

pip install pygame
pip install numpy
pip install cupy

Depending on your Python installation, you may alternatively be able to enter:

pip3 install pygame
pip3 install numpy
pip3 install cupy

Once you have successfully installed these modules, you should be able to run the programs now. If you are using Anaconda, you can open them up and run them with Anaconda. Otherwise, in your command line, navigate to the project directory, and type into the command line:

Serial program:

python sudoku.py

Parallel program:

python sudoku_para.py

Depending on your installation of Python (I believe this is the case for Python 3.9.0), you may need to enter the following instead:

Serial program:

python3 sudoku.py

Parallel program:

python3 sudoku_para.py

When in doubt, if one syntax doesn't work, try the other.

The serial program provides the user two options, and will print a message to the console prompting them to choose which mode they would like. At this point, the user can enter 1 for the GUI mode, which opens a window with a GUI to display the puzzle and solution time. Alternatively, they can enter 2 to view it in CLI mode, which will not open up a window, but will instead display everything in the console.

Note that each program runs using the initial sudoku configurations programmed into the main functions in the files, including the grid size and any initial filled-in values. If necessary, you may go into the main method and create a sudoku configuration.

and modify the "sudoku" variable, and the parameters in the solve_sudoku method call to match the parameters that your puzzle has. Please note that the grid must remain in the correct format (ie a 2D array) and should be a configuration that is "sudoku-ish" (the overall grid should be square in shape, block_width should be sqrt(grid_width), values should not exceed grid width or be less than 0, etc.). Doing otherwise may cause the program to not run properly. Also note that initial grid sizes larger than 25x25 (for example 36x36) may require more memory than some GPUs have available and may take a long time to solve in either case.

Due to the nondeterminism involved in Algorithm X, the program is not guaranteed to get the exact same results on each run.
