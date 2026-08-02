# cpy Compiler for RISC-V

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![RISC-V](https://img.shields.io/badge/Target-RISC--V-283198?style=flat&logo=riscv&logoColor=white)
![University](https://img.shields.io/badge/University%20of%20Ioannina-Compilers%20Course-005baa?style=flat)

A full compiler for **cpy**, a minimal educational programming language, translating `.cpy` source code directly into working **RISC-V assembly**. Built from scratch in Python using classical syntax-directed translation — lexical analysis, recursive-descent parsing with intermediate code generation, symbol table/scope management, and final code generation.

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

The compiler follows a classical **syntax-directed translation** design rather than a separate parse-then-generate model — intermediate code is emitted directly as the parser recognizes each construct:

1. **Lexical Analysis** — tokenizes raw `.cpy` source into keywords, identifiers, numbers, operators, and delimiters
2. **Syntax Analysis + Intermediate Code Generation** — a recursive-descent parser validates cpy's grammar and simultaneously emits intermediate code as quadruples (`op, arg1, arg2, result`), using **backpatching** to resolve jump targets for `if` / `elif` / `else` / `while`, including short-circuit evaluation of `and` / `or`
3. **Symbol Table & Scope Management** — tracks nested function scopes, variable offsets, and stack-frame layout, supporting recursion and parameter passing
4. **Final Code Generation** — translates the quadruple sequence into real RISC-V assembly instructions

Running the compiler produces three output files: the symbol table (`.sym`), the intermediate quadruple code (`.int`), and the final RISC-V assembly (`.asm`).

## cpy Syntax Notes

cpy uses distinctive delimiters rather than standard braces:
- Blocks are wrapped in `#{ ... #}` (functions, `if`, `while` bodies)
- Variable declarations use `#int`
- The program entry point is defined with `#def main: ... #}`
- Comments are wrapped in `##...##`

## Usage

```bash
python cpy_language_compiler.py test.cpy
```

This compiles `test.cpy` and generates three output files in the same directory:
- `test.cpy.sym` — the symbol table
- `test.cpy.int` — intermediate code (quadruples)
- `test.cpy.asm` — the final RISC-V assembly, ready to run on a RISC-V simulator (e.g., RARS or Spike)

## Example

`test.cpy` is included in this repo as a working example program — check it out to see cpy syntax in action, and run it through the compiler to see the generated assembly output.

## Tech Stack

`Python` `RISC-V Assembly` `Compiler Design` `Syntax-Directed Translation` `Backpatching` `Symbol Table Management` `Lexical Analysis` `Recursive-Descent Parsing`

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
