import Lin

x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
y = [0.0, 12.36, 24.83, 35.91, 48.79, 60.42]

m, b = Lin.fit(x,y)
print (m)
print (b)