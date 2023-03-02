def mitad(x):
    return x/2

def suma(x,y):
    return x+y

def promedio(x,y):
    return mitad(suma(x,y))

def mostrar_promedio(x,y):
    print("El promedio es: "+str(promedio(x,y)))

def mayor_menor(x,y,z):
    menor = x
    if y<menor:
        menor = y
    if z<menor:
        menor = z
    
    mayor = x
    if y>mayor:
        mayor = y
    if z>mayor:
        mayor = z
    
    return mayor, menor

mostrar_promedio(2,3)

x = mitad(2)
print(x)

print(suma(3,4))

v1, v2 = mayor_menor(7,9,2)
print("Mayor menor:",v1, v2)

lista_ejemplo = ["Hola", 123, True, [1.72, 'J']]
print(lista_ejemplo)
lista_ejemplo = lista_ejemplo+[32]
print(lista_ejemplo)
print(lista_ejemplo[3][1])