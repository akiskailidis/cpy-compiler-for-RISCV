# cpy Compiler for RISC-V

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![RISC-V](https://img.shields.io/badge/Target-RISC--V-283198?style=flat&logo=riscv&logoColor=white)
![University](https://img.shields.io/badge/University%20of%20Ioannina-Compilers%20Course-005baa?style=flat)

A full compiler for **cpy**, a minimal educational programming language, translating `.cpy` source code directly into working **RISC-V assembly**. Built from scratch in Python — covering lexical analysis, parsing, semantic analysis, and code generation.

Developed for the course *Μεταφραστές* (Compilers) at the University of Ioannina.

---

## Overview

cpy is a small, structured, integer-only language designed for compiler-construction exercises. This project implements a complete compiler pipeline for it — not just a parser or interpreter, but a compiler that emits real, runnable RISC-V assembly instructions.

## Language Features (cpy)

- **Data type**: 16-bit signed integers (–32767 to 32767)
- **Control flow**: `if`, `elif`, `else`, `while`
- **Functions**: nesting, recursion, and parameter passing
- **I/O**: `input()`, `print()`
- **Global variables** via the `global` keyword
- **Return statements**

**Not supported (by design):** arrays, strings, floating-point types, `for` loops — kept out to focus the exercise on core compiler construction concepts.

## Compilation Pipeline

The compiler is structured into four phases, covering the key stages of a standard compiler pipeline:

1. **Lexical Analysis** — tokenizes raw `.cpy` source into a stream of recognized symbols
2. **Syntax Analysis** — parses tokens into an abstract syntax tree (AST), enforcing cpy's grammar
3. **Semantic Analysis** — checks scoping, variable declarations, and function usage for correctness
4. **Code Generation** — walks the AST and emits RISC-V assembly instructions

## Usage

```bash
python3 cpy_language_compiler.py test.cpy
```

This compiles `test.cpy` and outputs the corresponding RISC-V assembly, ready to run on a RISC-V simulator (e.g., RARS or Spike).

## Example

`test.cpy` is included in this repo as a working example program — check it out to see cpy syntax in action, and run it through the compiler to see the generated assembly output.

## Tech Stack

`Python` `RISC-V Assembly` `Compiler Design` `Lexical Analysis` `Parsing` `Code Generation`

---

### Course Info

- **University**: University of Ioannina
- **Department**: Computer Engineering and Informatics
- **Course**: Μεταφραστές (Compilers)
- **Instructor**: Γ. Μανής
- **Semester**: Spring 2024

---

### Contact

[![Email](https://img.shields.io/badge/Email-akiskailidis1%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:akiskailidis1@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Kyrillos%20Kailidis-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kyrillos-kailidis-9ba034370/)
[![GitHub](https://img.shields.io/badge/GitHub-akiskailidis-181717?style=flat&logo=github&logoColor=white)](https://github.com/akiskailidis)
