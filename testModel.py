from model.modello import Model

myModel = Model()

print(myModel.buildGraph("Colorado", 1999))
max, num, list = (myModel.getConnesse())


lista, num = (myModel.getBestPath())
for l in lista:
    print(f"{l}")

print(num)