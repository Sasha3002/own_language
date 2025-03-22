import argparse
import sys
import io
import errors.errors as b
from interpreter.interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(description="Text data processing.")
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to the file to be processed."
    )
    parser.add_argument(
        "-t", "--text",
        type=str,
        help="Text to be processed."
    )
    args = parser.parse_args()


    if not args.file and not args.text:
        print("Error: you need to specify path to file (--file), or string (--text).")
        return



    try:
        if args.file:
            with open(args.file, 'r') as file:
                interpreter = Interpreter(file)
                print(interpreter.run())
        else:
            a = io.StringIO(args.text)
            interpreter = Interpreter(a)
            print(interpreter.run())

    except b.InvalidTokenError as e:
        print(f'Error: Invalid token encountered: {e}')
    except b.ExceedsMaxLengthError as e:
        print(f'Error: Token exceeds maximum allowed length: {e}')
    except b.UndefEscapeChar as e:
        print(f'Error: Undefined escape character: {e}')
    except FileNotFoundError:
        print('Error: File Not Found.')
    except b.InvalidSyntaxError as e: 
        print(f'Error: Invalid Syntax: {e}')
    except b.MainFunctionNotFoundError as e: 
        print(f'Error: Main function not found: {e}')
    except b.RedefinitionError as e: 
        print(f'Error: Redefinition: {e}')
    except b.UndeclaredVariableError as e: 
        print(f'Error: Undeclared variable: {e}')
    except b.UndeclaredFunctionError as e: 
        print(f'Error: Undeclared function: {e}')
    except b.TypeMismatchError as e: 
        print(f'Error: Type mismatch: {e}')
    except b.InvalidNumberOfArgumentsError as e: 
        print(f'Error: Invalid number of arguments: {e}')
    except b.InvalidMethodCallError as e: 
        print(f'Error: Invalid method call: {e}')
    except b.InvalidReturnTypeError as e: 
        print(f'Error: Invalid return type: {e}')
    except b.InvalidTypeError as e: 
        print(f'Error: Invalid type: {e}')
    except b.DivisionByZeroError as e:
        print(f'Error: Division by zero: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')


if __name__ == "__main__":
    #sys.argv = ["main.py", "--text", 'int main() { return @; }']
    sys.argv = ["main.py", "--file", "tests/test_cases/figures.txt"]
    main()
