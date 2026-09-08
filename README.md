# operations_research_project

A Python program for solving transportation problems using the North-West Corner, Balas-Hammer, and Stepping-Stone methods, while calculating transportation costs and studying algorithm complexity.

## Description

The transportation problem is an optimization problem that aims to determine how goods can be transported from suppliers to customers while satisfying supply and demand constraints and minimizing the total transportation cost.

This project implements several methods for solving transportation problems:

* **North-West Corner method** for building an initial transportation proposal.
* **Balas-Hammer method** for building an initial transportation proposal.
* **Stepping-Stone method with potentials** for optimizing the initial proposal.
* **Complexity analysis** through the generation of random transportation problems and calculation of their execution costs.

The program uses transportation tables containing suppliers, customers, supply, demand, and transportation costs.

The program can use predefined transportation problems or generate random problems of a chosen size for complexity studies.

## Getting Started

### Dependencies

To run the project, you need:

* **Python 3.10 or later**
* A terminal or command prompt
* A Python development environment such as **Visual Studio Code**, **PyCharm**, or **IDLE** (optional)

The project only uses Python modules included in the project and does not require external libraries.

The project is designed to run on common operating systems such as Windows, Linux, and macOS, provided that Python is correctly installed.

### Installing

Clone the project:

```bash
git clone https://github.com/hezaqqq/operations_research_project.git
```

Then navigate to the project directory:

```bash
cd operations_research_project
```

Make sure that the Python files and the `tables` directory are located in the correct project directory.

### Executing program

Run the main program using Python:

```bash
python main.py
```

Once the program starts, you will be asked what type of transportation problem you want to use.

1. Select **1** to use one of the predefined problems.

2. Enter a problem number between **1 and 12**.

3. Select the initial algorithm:

   * **1. North-West**
   * **2. Balas-Hammer**

4. The program displays the initial transportation proposal and its total transportation cost.

5. The **Stepping-Stone method with potentials** is then used to optimize the transportation proposal.

Alternatively, select **2** when choosing the problem type to generate a random transportation problem for a complexity study.

The program will ask for the size of the transportation table and generate the corresponding problem automatically.

At the end of the calculation, you can choose whether to solve another transportation problem.

## Help

### The program does not start

Make sure that Python is correctly installed and accessible from the terminal.

You can check your Python installation with:

```bash
python --version
```

If your system uses `python3`, try:

```bash
python3 --version
```

### The program cannot find a transportation table

Make sure that the `tables` directory exists and contains the required files.

For predefined problems, the program expects files such as:

```text
tables/tab_1.txt
tables/tab_2.txt
```

up to:

```text
tables/tab_12.txt
```

If you generate a random problem, the program creates:

```text
tables/tab_complexity.txt
```

### Testing individual algorithms

The different algorithms can be tested individually by importing their functions into `main.py` or another Python file.

For example:

```python
from north_west import north_west
from balas_hammer import bh
from stepping_stone import stepping_stone
```

You can then call the desired function directly with a transportation problem.
