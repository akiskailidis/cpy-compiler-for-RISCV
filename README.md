# cpy Compiler for RISC-V

This project implements a full compiler for the educational programming language **cpy**, developed as part of the course "Μεταφραστές" at the University of Ioannina.

The compiler is implemented in Python and translates `.cpy` source code into RISC-V assembly. It is structured into four compilation phases, covering all key steps of a modern compiler pipeline.

---

## 📚 University Info

- **University**: University of Ioannina  
- **Department**: Computer Engineering and Informatics  
- **Course**: Μεταφραστές  
- **Instructor**: Γ. Μανής  
- **Semester**: Spring 2024  


---

## Language Overview – cpy

The `cpy` language is a minimal, integer-only, structured programming language designed for compiler construction exercises. It includes:

- **Data types**: Only 16-bit signed integers (–32767 to 32767)
- **Control flow**: `if`, `elif`, `else`, `while`
- **Functions**: With support for nesting, recursion, and parameter passing
- **I/O**: `input()`, `print()`
- **Global variables**: Managed via the `global` keyword
- **Return statements**

### Limitations:
- No support for arrays, strings, floating-point types, or `for` loops
- Only integer expressions and variables



