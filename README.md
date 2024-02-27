# cosc-4315-set-operations
Homework 1 - Compute set operations on files with words and numbers

Authors: Coby Walters and Jason Pedder

This program performs set operations (union, difference, intersection) on two sets of words stored in text files. It accepts command-line arguments to specify the input files and the operation to perform.

## Prerequisites

- Python 3.x installed on your system.
- Node.js installed on your system.

## Usage

To use the program, follow the instructions below:

**Command Syntax**:

    ```bash
    python3 setops.py set1=[filename];set2=[filename];operation=[difference|union|intersection]
    ```

## Command Line Arguments

- `set1`: Filename of the first set text file.
- `set2`: Filename of the second set text file.
- `operation`: Operation to perform on the sets (`difference`, `union`, or `intersection`).

## File Format

- Input text files should contain sets of words, each word separated by a newline character.
- Output will be written to a text file named `output.txt`.

## Program Flow

1. **Command Parsing**:
    - Parses the command-line arguments to extract `set1`, `set2`, and `operation`.
    - Validates the provided arguments.

2. **File Parsing**:
    - Reads the content of the input files and converts them into sets of words.
    - Performs necessary preprocessing like converting words to lowercase and sorting them.

3. **Set Operations**:
    - Performs the specified set operation (`union`, `difference`, or `intersection`) on the sets of words.
