def list_depth(l,d):
    if type(l) == list:
        return max(map(lambda m: list_depth(m,d+1),l))
    else:
        return d

def typecode(x):
    """
    If x a number, output, n
    If list of depth 1, output l,
    If list of depth > 1, output L,
    Otherwise output ? for unknown.
    """
    if type(x) == int or type(x) == float:
        return 'n'
    if type(x) == list:
        if list_depth(x,0) > 1:
            return 'L'
        else:
            return 'l'
    return '?'

def prepend(x,y):
    """
    prepend y to x. Returns y. This is like inserting a new head of a list and
    then returning the head.
    """
    y.next = x
    return y

def append(x,y):
    """
    append y to x. Returns y. This is like adding a new tail on to the end of a
    list and then returning the tail.
    """
    x.next = y
    return y

def pop(x):
    """
    Returns the value popped and the next value after x so that this can be
    assigned to x
    """
    return (x,x.next)

def is_true(x):
    """
    For now this is just Python's bool rules.
    """
    return bool(x)
            
