"""
This file contains the essential tests that your functions in `simplex.py` must pass. 
You can run this file to check that your code is working correctly, and to get feedback on any errors. 
"""

import simplex
import simplex_generation
import numpy as np
import pytest
import inspect
import os
import itertools

# Define some standard tableaus and bases that we will use for testing.

# The tableau for the optimal portfolio

tableau_op = np.array([
    [1   , 1   , 1, 0, 0, 10],
    [1   , 0   , 0, 1, 0, 7 ],
    [0   , 1   , 0, 0, 1, 5 ],
    [0.02, 0.03, 0, 0, 0, 0 ]
])
basis_op = np.array([2, 3, 4])
pivot_op_ss = (1, 0)
pivot_op_ls = (2, 1)
pivot_op_lc = (2, 1)

# A larger tableau 

tableau_big = np.array([
        [ 0.93685371,  0.24529965,  0.91566762,  0.05794614,
          0.41770668,  0.36103308,  0.43817328,  0.72815797,  1.        ,
          0.        ,  0.        ,  0.        ,  0.        , 0.71216599],
        [ 0.46258504,  0.4309533 ,  0.03737471,  0.5988908 ,
          0.59668892,  0.28488038,  0.41908488,  0.56289125,  0.        ,
          1.        ,  0.        ,  0.        ,  0.        , 0.67723093],
        [ 0.50438403,  0.43308728,  0.6261691 ,  0.84054068,
          0.67698027,  0.72761735,  0.37016184,  0.3011547 ,  0.        ,
          0.        ,  1.        ,  0.        ,  0.        , 0.43036773],
        [ 0.91542146,  0.70124546,  0.26554441,  0.45877908,
          0.09731031,  0.66812684,  0.24087872,  0.21926235,  0.        ,
          0.        ,  0.        ,  1.        ,  0.        , 0.60865022],
        [ 0.63325907,  0.93061055,  0.04982956,  0.06692785,
          0.20593886,  0.62103973,  0.9741131 ,  0.38035238,  0.        ,
          0.        ,  0.        ,  0.        ,  1.        , 0.15181008],
        [ 0.46539895,  0.21998826,  0.3369545 ,  0.24399055,
          0.65203634,  0.69648645,  0.81364481,  0.3588273 ,  0.        ,
          0.        ,  0.        ,  0.        ,  0.        , 0.        ]
        
    ])
basis_big = np.array([8, 9, 10, 11, 12])
pivot_big_ss = (4, 0)
pivot_big_ls = (4, 7)
pivot_big_lc = (2, 4)

# A tableau with one negative reduced cost only
# Comes from the optimal portfolio problem, penultimate step.
# However, RHS modified so that two rows are possible,
# to check the tie-breaking rule is working correctly.

tableau_neg = np.array([
    [0, 1, 1, -1, 0, 3],
    [1, 0, 0, 1, 0, 2],
    [0, 0, -1, 1, 1, 2],
    [0, 0, -0.03, 0.01, 0, -0.23]
])
basis_neg = np.array([2, 0, 4])
pivot_neg_ss = (1, 3)
pivot_neg_ls = (2, 3)
pivot_neg_lc = (1, 3)

# Documentation check function.

def doccheck(fn, validate):
    """
    Checks the docstring. 
    Returns
    0 if none,
    1 for exists but noteable violations of numpydoc standard
    2 otherwise

    Parameters
    ----------
    fn : function
        The function whose docstring is to be checked
    validate : function
        The numpydoc.validate function to validate the docstring

    Returns
    -------
    score : integer
        The score for the docstring
    explanation : string
        The explanation for the score
    validation : dict
        The full validation result from numpydoc.validate
    """
    noteable_errors = ['PR01', 'PR02', 'PR03', 'PR04', 'PR07', 'RT01', 'RT03', 'SS01']
    fn_docstring = 2
    filename = f"tmp{np.random.randint(10000)}"
    with open(f"{filename}.py", mode="w") as f:
        f.write(inspect.getsource(fn))
    validation = validate(f"{filename}.{fn.__name__}")
    error_keys = [k for k, v in validation['errors']]
    explanation = ""
    if 'GL08' in error_keys:
        fn_docstring = 0
        explanation = "There is no docstring."
    elif [ x for x in noteable_errors if x in error_keys]:
        if len(validation['docstring']) == 0:
            fn_docstring = 0
            explanation += "Docstring is empty.\n"
        else:
            fn_docstring = 1
        for k, v in [(k, v) for (k, v) in validation['errors'] if k in noteable_errors]:
            explanation += v + "\n"
            
    os.remove(f"{filename}.py")
    return fn_docstring, explanation, validation

## Largest subscript tests

def test_ls_op1():
    """
    Optimal portfolio tableau, Largest subscript rule: check for expected pivot.
    """
    t = np.copy(tableau_op)
    assert simplex.find_pivot_largest_subscript(t) == pivot_op_ls

def test_ls_op2():
    """
    Optimal portfolio tableau, Largest subscript rule, but permute rows and columns: check for expected pivot.
    """
    expected_r = pivot_op_ls[0]
    expected_s = pivot_op_ls[1]
    for rows in itertools.permutations(range(tableau_op.shape[0]-1)):
        for cols in [list(range(tableau_op.shape[1]-1)),]: # Note this does not re-order the columns
            tableau = tableau_op.copy()
            for i_r, r in enumerate(rows):
                tableau[r, -1] = tableau_op[i_r+1, -1]
                for i_c, c in enumerate(cols):
                    tableau[r, c] = tableau_op[i_r, i_c]
                    tableau[-1, c] = tableau_op[-1, i_c]
            new_r = rows[expected_r]
            new_s = cols[expected_s]
            result = simplex.find_pivot_largest_subscript(tableau)
            assert result == (new_r, new_s), f"The expected result for\\n{tableau}\\nis {(new_r, new_s)}, but the function gives {result}."

def test_ls_big1():
    """
    Big tableau, Largest subscript rule: check for expected pivot.
    """
    t = np.copy(tableau_big)
    assert simplex.find_pivot_largest_subscript(t) == pivot_big_ls

def test_ls_big2():
    """
    Big tableau, Largest subscript rule, but permute rows and columns: check for expected pivot.
    """
    expected_r = pivot_big_ls[0]
    expected_s = pivot_big_ls[1]
    for rows in itertools.permutations(range(tableau_big.shape[0]-1)):
        for cols in [list(range(tableau_big.shape[1]-1)),]: # Note this does not re-order the columns
            tableau = tableau_big.copy()
            for i_r, r in enumerate(rows):
                tableau[r, -1] = tableau_big[i_r+1, -1]
                for i_c, c in enumerate(cols):
                    tableau[r, c] = tableau_big[i_r, i_c]
                    tableau[-1, c] = tableau_big[-1, i_c]
            new_r = rows[expected_r]
            new_s = cols[expected_s]
            result = simplex.find_pivot_largest_subscript(tableau)
            assert result == (new_r, new_s), f"The expected result for\\n{tableau}\\nis {(new_r, new_s)}, but the function gives {result}."

def test_ls_neg1():
    """
    Negative tableau, Largest subscript rule: check for expected pivot.
    """
    t = np.copy(tableau_neg)
    assert simplex.find_pivot_largest_subscript(t) == pivot_neg_ls

def test_ls_neg2():
    """
    Negative tableau, Largest subscript rule, but permute rows and columns: check for expected pivot.
    """
    expected_r = pivot_neg_ls[0]
    expected_s = pivot_neg_ls[1]
    for rows in itertools.permutations(range(tableau_neg.shape[0]-1)):
        for cols in [list(range(tableau_neg.shape[1]-1)),]: # Note this does not re-order the columns
            tableau = tableau_neg.copy()
            for i_r, r in enumerate(rows):
                tableau[r, -1] = tableau_neg[i_r+1, -1]
                for i_c, c in enumerate(cols):
                    tableau[r, c] = tableau_neg[i_r, i_c]
                    tableau[-1, c] = tableau_neg[-1, i_c]
            new_r = rows[expected_r]
            new_s = cols[expected_s]
            result = simplex.find_pivot_largest_subscript(tableau)
            assert result == (new_r, new_s), f"The expected result for\\n{tableau}\\nis {(new_r, new_s)}, but the function gives {result}."


def test_ls_vs_bland1():
    """
    Now we check that both pivoting rules, used within the simplex method, 
    give the same result on the larger tableau.
    """
    t = np.copy(tableau_big)
    b = np.copy(basis_big)
    result_bland = simplex_generation.simplex(t, b, simplex.find_pivot_bland)
    result_ls = simplex_generation.simplex(t, b, simplex.find_pivot_largest_subscript)
    assert result_bland['result'] == result_ls['result']
    assert np.allclose(result_bland['objective'], result_ls['objective'])
    # Checking solution and basis is painful, but this combined with the above should be sufficient.
    # This cannot be tested generically - with degenerate solutions the basis may differ - but in this case should match.
    assert np.allclose(np.sort(result_bland['solution']), np.sort(result_ls['solution']))


def test_ls_vs_bland2():
    """
    Finally we check that both pivoting rules, using the simplex method, 
    give the same result for every permutation of the optimal portfolio problem.
    """
    for rows in itertools.permutations(range(tableau_op.shape[0]-1)):
        for cols in itertools.permutations(range(tableau_op.shape[1]-1)):
            tableau = tableau_op.copy()
            basis = basis_op.copy()
            for i_c, c in enumerate(cols):
                for i_b, b in enumerate(basis_op):
                    if b == c:
                        basis[i_b] = i_c
            result_bland = simplex_generation.simplex(tableau.copy(), basis.copy(), simplex.find_pivot_bland)
            result_ls = simplex_generation.simplex(tableau.copy(), basis.copy(), simplex.find_pivot_largest_subscript)
            assert result_bland['result'] == result_ls['result']
            assert np.allclose(result_bland['objective'], result_ls['objective'])
            # Checking solution and basis is painful, but this combined with the above should be sufficient.
            assert np.allclose(np.sort(result_bland['solution']), np.sort(result_ls['solution']))



# We now check function documentation.

def test_docstring_ls1():
    numpydoc = pytest.importorskip("numpydoc", reason="numpydoc is required to run this test, but it is not installed.")
    from numpydoc import validate
    score, explanation, errors = doccheck(simplex.find_pivot_largest_subscript, validate.validate)
    assert score > 0, f"find_pivot_largest_subscript docstring has the following issues:\n{explanation}"

def test_docstring_ls2():
    numpydoc = pytest.importorskip("numpydoc", reason="numpydoc is required to run this test, but it is not installed.")
    from numpydoc import validate
    score, explanation, errors = doccheck(simplex.find_pivot_largest_subscript, validate.validate)
    assert score == 2, f"find_pivot_largest_subscript docstring has the following issues:\n{explanation}"

## Largest change tests

def test_lc_op1():
    """
    Optimal portfolio tableau, Largest change rule: check for expected pivot.
    """
    t = np.copy(tableau_op)
    assert simplex.find_pivot_largest_change(t) == pivot_op_lc

def test_lc_big1():
    """
    Big tableau, Largest change rule: check for expected pivot.
    """
    t = np.copy(tableau_big)
    assert simplex.find_pivot_largest_change(t) == pivot_big_lc

def test_lc_neg1():
    """
    Negative tableau, Largest change rule: check for expected pivot.
    """
    t = np.copy(tableau_neg)
    assert simplex.find_pivot_largest_change(t) == pivot_neg_lc


def test_lc_vs_bland1():
    """
    Now we check that both pivoting rules, used within the simplex method, 
    give the same result on the larger tableau.
    """
    t = np.copy(tableau_big)
    b = np.copy(basis_big)
    result_bland = simplex_generation.simplex(t, b, simplex.find_pivot_bland)
    result_lc = simplex_generation.simplex(t, b, simplex.find_pivot_largest_change)
    assert result_bland['result'] == result_lc['result']
    assert np.allclose(result_bland['objective'], result_lc['objective'])
    # Checking solution and basis is painful, but this combined with the above should be sufficient.
    # This cannot be tested generically - with degenerate solutions the basis may differ - but in this case should match.
    assert np.allclose(np.sort(result_bland['solution']), np.sort(result_lc['solution']))


def test_lc_vs_bland2():
    """
    Finally we check that both pivoting rules, using the simplex method, 
    give the same result for every permutation of the optimal portfolio problem.
    """
    for rows in itertools.permutations(range(tableau_op.shape[0]-1)):
        for cols in itertools.permutations(range(tableau_op.shape[1]-1)):
            tableau = tableau_op.copy()
            basis = basis_op.copy()
            for i_c, c in enumerate(cols):
                for i_b, b in enumerate(basis_op):
                    if b == c:
                        basis[i_b] = i_c
            result_bland = simplex_generation.simplex(tableau.copy(), basis.copy(), simplex.find_pivot_bland)
            result_lc = simplex_generation.simplex(tableau.copy(), basis.copy(), simplex.find_pivot_largest_change)
            assert result_bland['result'] == result_lc['result']
            assert np.allclose(result_bland['objective'], result_lc['objective'])
            # Checking solution and basis is painful, but this combined with the above should be sufficient.
            assert np.allclose(np.sort(result_bland['solution']), np.sort(result_lc['solution']))


# We now check function documentation.

def test_docstring_lc1():
    numpydoc = pytest.importorskip("numpydoc", reason="numpydoc is required to run this test, but it is not installed.")
    from numpydoc import validate
    score, explanation, errors = doccheck(simplex.find_pivot_largest_change, validate.validate)
    assert score > 0, f"find_pivot_largest_change docstring has the following issues:\n{explanation}"

def test_docstring_lc2():
    numpydoc = pytest.importorskip("numpydoc", reason="numpydoc is required to run this test, but it is not installed.")
    from numpydoc import validate
    score, explanation, errors = doccheck(simplex.find_pivot_largest_change, validate.validate)
    assert score == 2, f"find_pivot_largest_change docstring has the following issues:\n{explanation}"


if __name__ == "__main__":
    pytest.main(["-q", "test_simplex.py"])