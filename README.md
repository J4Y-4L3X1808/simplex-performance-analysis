# Simplex Algorithm Performance Analysis (Python)

## Overview
This project implements and compares different Simplex algorithms in Python, analysing their computational performance using data.

The goal is to arrive at a conclusion as to which is most efficient using data and complexities.

---

## Implemented Algorithms
- Bland's Rule
- Largest Subscript Rule
- Largest Chnage Rule

---

## Methodology
A benchmarking framework (provided as part of the module) was used to generate timing data for each algorithm.

My contributions were:
- Implementing pivot rule functions in Python

The benchmarking system handled problem generation and execution timing.

---

## Analysis
- Execution times were analysed across multiple test cases
- Performance differences between simplex variants were evaluated
- A complexity analysis was included in a separate LaTeX report (`report.pdf`)

---

## Files
`simplex_given.py` was provided as part of the coureswork as a framework

`simplex.py` is my finished python

`simplex_generation` and `simplex_test` were given and used to record the timings in an excel file
`analysis.xlsx` contains the genetrated timings, and my analysis of them
`report.pdf ` is the latex write up

---

## How to Run
python simplex.py
