class TransversalSection:

    def __init__(self, yVector, zVector):
        self.yVector = yVector
        self.zVector = zVector
        self.area = self.getSectionArea()
        self.yc = self.getYCentroid()
        self.zc = self.getZCentroid()
        self.iy = self.getYInertia()
        self.iz = self.getZInertia()
        self.iyz = self.getProductMomentOfArea()

    def getSectionArea(self):
        area = [0.5*(self.yVector[i] + self.yVector[i+1]) * (-self.zVector[i] + self.zVector[i+1]) for i in range(0, len(self.yVector) - 1)]
        return round(sum(area), 4)

    def getYCentroid(self):
        yCentroid = [-1/6 * (self.zVector[i] - self.zVector[i+1]) * (self.yVector[i+1]**2 + self.yVector[i]**2 + self.yVector[i] * self.yVector[i+1]) for i in range(0, len(self.yVector) - 1)]
        return round((sum(yCentroid)/self.area), 4)

    def getYInertia(self):
        inertiaY = [(1/12 * (self.yVector[i] * self.zVector[i+1] - self.yVector[i+1] * self.zVector[i])*(self.zVector[i]**2 + self.zVector[i] * self.zVector[i+1] + self.zVector[i+1]**2)) for i in range(0, len(self.yVector) - 1)]
        return round((sum(inertiaY) - self.area*self.getZCentroid()**2), 4)

    def getZCentroid(self):
        zCentroid = [1/6 * (self.yVector[i] - self.yVector[i+1]) * (self.zVector[i+1]**2 + self.zVector[i]**2 + self.zVector[i]*self.zVector[i+1]) for i in range(0, len(self.zVector) - 1)]
        return round((sum(zCentroid) / self.area), 4)

    def getZInertia(self):
        inertiaZ = [1/12 * (self.yVector[i] * self.zVector[i+1] - self.yVector[i+1]*self.zVector[i]) * (self.yVector[i]**2 + self.yVector[i] * self.yVector[i+1] + self.yVector[i+1]**2) for i in range(0, len(self.yVector) - 1)]
        return round((sum(inertiaZ) - self.area*self.getYCentroid()**2), 4)

    def getProductMomentOfArea(self):
        productMoment = [1/24*(self.yVector[i] * self.zVector[i+1] - self.yVector[i+1] * self.zVector[i]) * (self.yVector[i] * self.zVector[i+1] + 2 * self.yVector[i] * self.zVector[i] + 2 * self.yVector[i+1] * self.zVector[i+1] + self.yVector[i+1] * self.zVector[i]) for i in range(0, len(self.yVector) - 1)]
        return round((sum(productMoment) - self.area*self.getZCentroid() * self.getYCentroid()), 4)

    def returnAllParameters(self):
        print('\nParâmetros Geométricos -----------------\n')
        print('\tÁrea = ' + str(self.area) + '\n')
        print('\tCentroide: yc = ' + str(self.yc) + ', zc = ' + str(self.zc) + '\n')
        print('\tInércia: Iy = ' + str(self.iy) + ', Iz = ' + str(self.iz) + '\n')
        print('\tProduto de inércia = ' + str(self.iyz))

class Calculator:

    def __init__(self, TransversalSection, Nx, My, Mz):
        self.transversalSection = TransversalSection
        self.Nx = Nx
        self.My = My
        self.Mz = Mz
        self.normalStress = self.getNormalStress()

    def getNormalStress(self):
        yp = [self.transversalSection.yVector[i] - self.transversalSection.yc for i in range(0, len(self.transversalSection.yVector))]
        zp = [self.transversalSection.zVector[i] - self.transversalSection.zc for i in range(0, len(self.transversalSection.zVector))]
        normalStressVector = [round((self.Nx/self.transversalSection.area - (self.transversalSection.iy*self.Mz + self.transversalSection.iyz*self.My)/(self.transversalSection.iz*self.transversalSection.iy - self.transversalSection.iyz**2)*yp[i])+(self.transversalSection.iz*self.My + self.transversalSection.iyz*self.Mz)/(self.transversalSection.iz*self.transversalSection.iy - self.transversalSection.iyz**2)*zp[i], 4) for i in range(0, len(zp))]
        return normalStressVector

    def getMaxAndMinStress(self):
        idMax = []
        idMin = []
        for i in range(0, len(self.normalStress)):
            idMax.append(i) if self.normalStress[i] == max(self.normalStress) else None
            idMin.append(i) if self.normalStress[i] == min(self.normalStress) else None
        return (idMax, idMin)

    def returnAllParameters(self):
        idMax, idMin = self.getMaxAndMinStress()
        print('\nTensão de Flexão Composta -----------------')

        print('\n\tTensão Máxima:\n')
        for i in idMax:
            print('\t\tp(' + str(self.transversalSection.yVector[i]) + ', ' + str(self.transversalSection.zVector[i]) + ') = ' + str(self.normalStress[i]))

        print('\n\tTensão Mínima:\n')
        for i in idMin:
            print('\t\tp(' + str(self.transversalSection.yVector[i]) + ', ' + str(
                self.transversalSection.zVector[i]) + ') = ' + str(self.normalStress[i]))

        print('\n\tTensões nos pontos:\n')
        for i in range(len(self.normalStress)):
            print('\t\tp(' + str(self.transversalSection.yVector[i]) + ', ' + str(self.transversalSection.zVector[i]) + ') = ' + str(self.normalStress[i]) + '\n')



# Entrada de Dados
section = TransversalSection(
    yVector=[0, 10, 10, 25, 25, 0, 0],
    zVector=[0, 0, 15, 15, 20, 20, 0]
)
strain = Calculator(
    TransversalSection=section,
    Nx=0,
    My=-2.1e5,
    Mz=0
)

section.returnAllParameters()
strain.returnAllParameters()

