

a = [(1,2,3), ("a","b","c"), ("d","e","f"), ("g","h","i")]
rows = iter(a)
print (*next(rows))
print (*next(rows))
print (*next(rows))
print (*next(rows))

print (list((1, 2,3)))