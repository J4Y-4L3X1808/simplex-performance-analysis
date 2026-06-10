"""
Computing coursework file: to be completed.
"""

import numpy as np
import simplex_generation

"""
This variable must be updated to your student ID number. 
It is used to create a unique spreadsheet for you, and to link the spreadsheet to your code. 
The spreadsheet will be created in the same location as this file.
"""
student_id = 36800252

## Settings

"""
When you have completed your code, set `run_timings` to `True` so that an Excel workbook is created.
"""

run_timings = True

"""
If you want to create a spreadsheet before you have completed the code, 
set `time_largest_subscript` and `time_largest_change` to `False`. 
You can set just one to `False` if you do not yet want to include that result.
"""

time_largest_subscript = True
time_largest_change = True


## Code for Bland's rule

"""
This code is provided as an example. It works correctly, is fully documented, and will be used later."""

def find_pivot_bland(tableau):
    """
    Using Bland's rule and the minimum ratio test, find the pivot entry in the tableau.
    
    Parameters
    ----------
    tableau : array
        The simplex method tableau in basic form
    
    Returns
    -------
    r, s : integer
        Row and column indexes of the pivot

    Notes
    -----
    Assumes that there is a negative reduced cost that we can pivot on.
    """
    M, N = tableau.shape
    m = M-1  # Number of constraints
    n = N-1  # Number of variables
    # Bland's rule: find first negative reduced cost
    s = 0
    while tableau[-1, s] <= 0:
        s = s + 1
    # Minimum ratio test plus Bland's rule:
    # find the (first) row i minimizing b_i / a_{is}, a_{is} > 0
    r = -1
    theta_star = np.inf
    for i in range(m):
        if tableau[i, s] > 0:
            if tableau[i, -1] / tableau[i, s] < theta_star:
                r = i
                theta_star = tableau[i, -1] / tableau[i, s]
    return r, s



## Code for largest subscript case

"""
This is the first function you must complete.

It needs to return the `(row, column)` indexes `(r, s)` on which the Simplex method will pivot.
 
It needs to be fully and correctly documented.
"""

def find_pivot_largest_subscript(tableau):
    """
    Using Largest Subscript Rule and the minimum ratio test, find the pivot entry in the tableau.
    
    Parameters
    ----------
    tableau : array
        The simplex method tableau in basic form
    
    Returns
    -------
    final_r, final_s : integer
        Row and column indexes of the pivot

    Notes
    -----
    Assumes that there is a positive reduced cost that we can pivot on.
    """
    
    m = len(tableau[0]) - 2         #columns minus the RHS
    n = len(tableau) - 1            #rows

    k = m
    while tableau[n][k] <= 0:      #checks through each column of the reduced costs, from right to left, to see if they're positive
        k -= 1
    final_s = k

    theta_star = np.inf
    for i in reversed(range(n)): #goes through each row of the optimal column from largest to smallest to find the one with the smallest ratio
        if tableau[i][final_s] > 0:
            ratio = tableau[i][-1] / tableau[i][final_s]
            if ratio < theta_star:
                theta_star = ratio 
                r = i   
    final_r = r

    return final_r, final_s



## Code for largest change case

"""
This is the second function you must complete.

It needs to return the `(row, column)` indexes `(r, s)` on which the Simplex method will pivot.
 
It needs to be fully and correctly documented.
"""

def find_pivot_largest_change(tableau):
    """
    Using Largest Change Rule and the minimum ratio test, find the pivot entry in the tableau.
    
    Parameters
    ----------
    tableau : array
        The simplex method tableau in basic form
    
    Returns
    -------
    final_r, final_s : integer
        Row and column indexes of the pivot

    Notes
    -----
    Assumes that there is a positive reduced cost that we can pivot on.
    """

    m = len(tableau[0]) - 2
    n = len(tableau) - 1
    change = -np.inf
    final_r = None
    final_s = None

    for s in range(m):
        theta_star = np.inf
        r = None
        if tableau[-1][s] > 0:

            for i in range(n): #goes through each row of the optimal column from largest to smallest to find the one with the smallest ratio
                if tableau[i][s] > 0:
                    ratio = tableau[i][-1] / tableau[i][s]
                    if ratio < theta_star:
                        theta_star = ratio  
                        r = i
        
            if theta_star == np.inf:
                continue
            if r is None:
                continue

            new_change = tableau[-1][s] * theta_star

            if new_change > change:
                final_s = s
                change = new_change
                final_r = r

    if final_r is None or final_s is None:
        return -1, -1

    return final_r, final_s
    


## Code to create the spreadsheet

"""
When you want to create the timings, the following line will do so. 
You need to have modified the "Settings" section above appropriately.

If your code is working you should see the progress bar moving. 
The full case should complete in about a minute if the code is very efficient, 
and within less than 3 minutes even if inefficient. 
The generation code starts with small cases which complete quickly: 
the last few steps will take the longest time. 

If this step freezes for much longer it likely indicates a problem with your code above.
"""

if __name__ == "__main__":
    if run_timings:
        success = simplex_generation.run_times(student_id,
                                            find_pivot_bland, 
                                            find_pivot_largest_subscript,
                                            find_pivot_largest_change,
                                            time_largest_subscript,
                                            time_largest_change)