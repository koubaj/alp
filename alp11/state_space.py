class State:
    def __init__(self, listMaxVolume, listActualVolume):
        self.listMaxVolume = listMaxVolume
        self.listActualVolume = listActualVolume
        self.action = None

    def expand(self):
        result = []
        for i in range(len(self.listActualVolume)):
            #nalit
            tlistActualVolume = self.listActualVolume[:]
            tlistActualVolume[i] = self.listMaxVolume[i]
            s = State(self.listMaxVolume,tlistActualVolume)
            s.action = "Nalit"+str(i)
            result.append(s)

            #vylit
            tlistActualVolume = self.listActualVolume[:]
            tlistActualVolume[i] = 0
            s = State(self.listMaxVolume,tlistActualVolume)
            s.action = "Vylit"+str(i)
            result.append(s)

            #prelit
            for j in range(len(self.listActualVolume)):
                if j != i:
                    tlistActualVolume = self.listActualVolume[:]
                    tlistActualVolume[i] = max(self.listActualVolume[i] - (self.listMaxVolume[j]-self.listActualVolume[j]), 0)
                    tlistActualVolume[j] += self.listActualVolume[i]-tlistActualVolume[i]
                    s = State(self.listMaxVolume,tlistActualVolume)
                    s.action = "Prelit z "+str(i)+" do "+str(j)
                    result.append(s)

        return result

    def signiture(self):
        return tuple(self.listActualVolume)

    def way(self):
        return (self.action, tuple(self.listActualVolume))

def bfs(start,end):
    queue = [start]
    endSigniture = end.signiture()
    isKnown = {start.signiture:start}
    while len(queue) > 0:
        actual = queue.pop(0)
        if actual.signiture() == endSigniture: # when it finds end
            way = []
            looking = actual
            while looking.action != None:
                way.insert(0,looking.way())
                looking = isKnown[looking.signiture()]
            return way

        newStates = actual.expand() #list of states
        for state in newStates:
            if not state.signiture() in isKnown:
                isKnown[state.signiture()] = actual
                queue.append(state)



a = State([5,3,2],[0,0,0])
b = State([5,3,2],[0,1,1])
for i in bfs(a,b):
    print(i)
