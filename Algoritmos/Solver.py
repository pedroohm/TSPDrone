import heapq
from random import randint

class Solver(object):
    def __init__(self, truckMatrix, droneMatrix, nodes, st, sr, endurance):
        self.__truckMatrix = truckMatrix
        self.__droneMatrix = droneMatrix
        self.__nodes = nodes
        self.__time = 0
        self.__st = st
        self.__sr = sr
        self.__endurance = endurance
        self.__solution = []
        self.__droneDeliveries = []
        self.__droneSolution = []
        self.__truckSolution = []
        self.__representation = []

    # Funções auxiliares
    def printSolution(self):
        print("Time: ", self.__time)
        print(len(self.__solution))
        print(self.__solution)

    def getTotalTime(self):
        return self.__time

    def getTime(self, _from, _to):
        return float(self.__truckMatrix[self.__solution[_from]][self.__solution[_to]])

    def getDroneTime(self, i, j, k):
        return float(self.__droneMatrix[self.__solution[i]][self.__solution[j]]) + float(self.__droneMatrix[self.__solution[j]][self.__solution[k]]) 

    def calcDist(self):
        self.__time = 0;
        for i in range(len(self.__solution) - 1):
            # print(self.__solution[i], " - ", self.__solution[i+1], " | ",self.__truckMatrix[self.__solution[i]][self.__solution[i + 1]]);
            self.__time += float(self.__truckMatrix[self.__solution[i]][self.__solution[i + 1]])

    def calculateTime(self):
        time = 0
        truckTime = 0
        droneAvailable = True
        for i in range(1, len(self.__solution)):
            if self.__representation[i] == 1 and droneAvailable:
                droneAvailable = False
                droneDelivery = self.__solution[i]
                droneLaunch = self.__solution[i - 1]
                time += float(self.__truckMatrix[i - 1][i]) if (truckTime == 0)  else truckTime
                truckTime = 0
            else:
                truckTime += float(self.__truckMatrix[self.__solution[i - 1]][self.__solution[i]]) 
            if self.__representation[i] == 0 and ~droneAvailable:
                droneRecover = self.__solution[i]
                droneAvailable = True
                droneTime = float(self.__droneMatrix[droneLaunch][droneDelivery]) + float(self.__droneMatrix[droneDelivery][droneRecover]) + self.__st + self.__sr
                time += max(droneTime, truckTime)
                truckTime = 0
        self.__time = time

    def closestPoints(self, num_points):
        pq = []
        lastInsert = self.__solution[-1]
        size = len(self.__nodes) - 1
        for j in range(size):
            if j not in self.__solution and j != lastInsert:
                heapq.heappush(pq, (self.__truckMatrix[lastInsert][j], j))
        closest = heapq.nsmallest(num_points, pq)
        return closest

    def adjustTimeSwap(self, i, j):
        self.__time = self.__time - self.getTime(i-1,i) - self.getTime(i, i+1) - self.getTime(j,j+1)
        self.__time = self.__time + self.getTime(i-1,j) + self.getTime(j, i+1) + self.getTime(i, j+1)
        if(i != j - 1):
            self.__time = self.__time - self.getTime(j-1,j)
            self.__time = self.__time + self.getTime(j-1,i)
        print("TESTE:" , self.__time)

    # Heurísitca do vizinho mais próximo com escolhas aleatórias. Utilizar m = 1 para a versão tradicional.
    def HVMP(self, m):
        self.__solution.append(0) # Adiciona o depósito a solução.
        count = 1
        while(count < len(self.__nodes) - 1):
            closest = self.closestPoints(m); # Recupera os m pontos mais próximos
            m1 = min(len(closest), m) # Trata a questão de não existir m pontos que não estão na solução
            index = randint(0, m1 - 1) # Define o indice do ponto que será inserido
            lastInsert = self.__solution[-1] # Recupera o último ponto a ser inserido
            # print(self.__solution[-1], " - ", closest[index][1], " | ",closest[index][0]);
            self.__solution.append(closest[index][1]) # Adiciona na solução
            self.__time += float(closest[index][0]) # Acrescenta a distância
            count += 1
        lastInsert = self.__solution[-1]
        self.__solution.append(len(self.__nodes) - 1) # Adiciona o depósito, para fechar o ciclo
        self.__time += float(self.__truckMatrix[lastInsert][0])
        self.__time = round(self.__time,2)
        print(len(self.__solution))
        print(self.__solution)
        # print(self.__time)
        # self.calcDist()
        # print(self.__time)

    def localSearchSwap(self):
        better = True
        while better:
            better = False
            lessTime = self.__time
            lessSol = self.__solution.copy()
            for i in range(1,len(self.__solution) - 2):
                for j in range(i + 1, len(self.__solution) - 2):
                    self.__solution[i], self.__solution[j] = self.__solution[j] , self.__solution[i]
                    self.calcDist()
                    if(self.__time < lessTime):
                        better = True
                        lessTime = self.__time
                        lessSol = self.__solution.copy()
                    else:
                        self.__solution[i], self.__solution[j] = self.__solution[j] , self.__solution[i]
                        self.calcDist()
            self.__time = lessTime
            self.__solution = lessSol

    def localSearchInsertion(self):
        better = True
        while better:
            better = False
            lessTime = self.__time
            lessSol = self.__solution.copy()
            for i in range(1, len(self.__solution) - 1):
                for j in range(1, len(self.__solution) - 1):
                    sol = self.__solution.copy()
                    valueToInsert = self.__solution[i]
                    self.__solution.pop(i)
                    self.__solution.insert(j, valueToInsert)
                    self.calcDist()
                    if(self.__time < lessTime):
                        better = True
                        lessTime = self.__time
                        lessSol = self.__solution.copy()
                    self.__solution = sol
            self.__time = lessTime
            self.__solution = lessSol

    def localSearch2OPT(self):
        better = True
        while better:
            better = False
            lessTime = self.__time
            lessSol = self.__solution.copy()
            for i in range(1,len(self.__solution)-1):
                for j in range(len(self.__solution) - 2, -1, -1):
                    if j > i:
                        sol = self.__solution.copy()
                        self.__solution[i:j+1] = reversed(self.__solution[i:j+1])
                        self.calcDist()
                        if(self.__time < lessTime):
                            better = True
                            lessTime = self.__time
                            lessSol = self.__solution.copy()
                        self.__solution = sol
                    else:
                        break
            self.__time = lessTime
            self.__solution = lessSol

    def RVND(self):
        localSearchs = randomizeLocalSearchs()
        k = 1
        while k <= 3:
            oldTime = self.__time
            chosenLS = localSearchs.pop()
            if chosenLS == 1:
                self.localSearchSwap()
            elif chosenLS == 2:
                self.localSearchInsertion()
            elif chosenLS == 3:
                self.localSearch2OPT()
            if(self.__time < oldTime):
                k = 1
                localSearchs = randomizeLocalSearchs()
            else:
                k+=1

    def getDroneDeliveries(self):
        droneDeliveries = []
        for droneNode in self.__nodes:
            if droneNode[3] == 1:
                for departureNode in self.__nodes:
                    if departureNode == self.__nodes[-1]:
                        break
                    for arriveNode in self.__nodes:
                        departureIndex = self.__solution.index(departureNode[0])
                        arriveIndex = self.__solution.index(arriveNode[0])
                        if departureNode != droneNode and arriveNode != droneNode and departureIndex < arriveIndex:
                            # print(f"Departure: {departureNode} | Arrival: {arriveNode} | Drone: {droneNode}")
                            # print(len(self.__droneMatrix))
                            timeSpend = float(self.__droneMatrix[departureNode[0]][droneNode[0]]) + float(self.__droneMatrix[droneNode[0]][arriveNode[0]]) + self.__sr + self.__st
                            if timeSpend <= self.__endurance:
                                droneDeliveries.append((departureNode[0], droneNode[0], arriveNode[0]))
        self.__droneDeliveries = droneDeliveries


    def split1(self):
        self.getDroneDeliveries()

        arcs = []
        T = []
        # print(self.__solution)
        for i in range(len(self.__solution) - 1):
            arcs.append((self.__solution[i], self.__solution[i+1], self.getTime(i,i+1)))

        # print(arcs)


        for i in range(len(self.__solution) - 2):
            for k in range(len(self.__solution) - 1):
                if(k >= i + 2):
                    minValue = -1
                    minIndex = -1
                    for j in range(len(self.__solution)):
                        if(i < j and j < k):
                            if (i,j,k) in self.__droneDeliveries:
                                time = max(self.getTime(i,k), self.getDroneTime(i,j,k)) + self.__sr + self.__st 
                                if minValue == -1 or time < minValue:
                                    minValue = time
                                    minIndex = j
                    if minValue != -1  and minIndex != - 1:
                        arcs.append((self.__solution[i],self.__solution[k],minValue))
                        minDroneDelivery = (self.__solution[i], self.__solution[minIndex], self.__solution[k], minValue)
                        if minDroneDelivery not in T:
                            T.append(minDroneDelivery)
        # print(T)
        V = []
        P = []  
        V = [2147483647 for i in range(len(self.__solution) )]
        P = [2147483647 for i in range(len(self.__solution) )] 
        V[0] = 0
        P[0] = 0
        for i in self.__solution:
            if i != 0:  # 
                for arc in arcs:
                    if arc[1] == i: #
                        if V[i] > V[arc[0]] + arc[2]:
                            V[arc[1]] =  V[arc[0]] + arc[2]
                            P[arc[1]] = arc[0]
        
        return P, V, T

    def getDroneNode(self, T , launch, recover):
        for droneDelivery in T:
            if droneDelivery[0] == launch and droneDelivery[2] == recover:
                return droneDelivery[1]
    
    def isLaunchNode(self, currentNode, droneSolution):
        for droneDelivery in droneSolution:
            if droneDelivery[0] == currentNode:
                return (True, droneDelivery)
        return (False, 0)

    def split2(self):
        P, V , T =  self.split1()
        j = self.__solution[-1]
        i = 2147483647
        s = []
        s.append(j)
        # print(P)
        while i != 0:
            i = P[j]
            # print(i)
            s.append(i)
            j = i

        s.reverse()
        # print(self.__solution)
        # print(s)
        # print(T)
        droneSolution = []
        truckSolution = []

        for i in range(len(s) - 1):
            iIndex = self.__solution.index(s[i])
            i1Index = self.__solution.index(s[i + 1])
            if iIndex + 1 != i1Index:
                droneNode = self.getDroneNode(T, s[i], s[i + 1])
                droneSolution.append((s[i], droneNode, s[i + 1]))

        currentNode = 0
        while currentNode != self.__solution[-1]:
            print(currentNode)
            aux = self.isLaunchNode(currentNode, droneSolution)
            if aux[0]:
                launchIndex = self.__solution.index(aux[1][0])
                recoverIndex = self.__solution.index(aux[1][2])
                for i in range(launchIndex,recoverIndex):
                    if(self.__solution[i] != aux[1][1]):
                        truckSolution.append(self.__solution[i])
                currentNode = aux[1][2]
            else:
                truckSolution.append(currentNode)
                currentNode = self.__solution[self.__solution.index(currentNode) + 1]
        truckSolution.append(currentNode)
        

        print(truckSolution)
        print(droneSolution)
        self.__truckSolution = truckSolution
        self.__droneSolution = droneSolution
        print(f'Truck Nodes: {len(truckSolution)} | Drone Nodes: {len(droneSolution)} | TSP Solution: {len(self.__solution)}')

    def createRepresentation(self):
        representation = [0 for i in range(len(self.__solution) )] 
        for delivery in self.__droneSolution:
            tspDroneLaunchIndex = self.__solution.index(delivery[0])
            tspDroneDeliveredIndex = self.__solution.index(delivery[1])
            tspDroneRecoverIndex = self.__solution.index(delivery[2])
            self.__solution.pop(tspDroneDeliveredIndex)
            tspDroneLaunchIndex += 1 
            self.__solution.insert(tspDroneLaunchIndex, delivery[1])
            while(tspDroneLaunchIndex != tspDroneRecoverIndex):
                representation[tspDroneLaunchIndex] = 1
                tspDroneLaunchIndex += 1
        self.__representation = representation
    

def randomizeLocalSearchs():
    localSearchs = []
    availableValues = [1, 2, 3]
    while len(availableValues) != 0:
        newInsert = randint(0, len(availableValues) - 1)
        localSearchs.append(availableValues.pop(newInsert))

    return localSearchs