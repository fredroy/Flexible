import Sofa

def vonMises2d(e):
	return max(0,e[0]*e[0] + e[1]*e[1] - e[0]*e[1] + 3.0*e[2]*e[2])**(0.5)

class ColorMap(Sofa.PythonScriptController):

	def createGraph(self,node):
		path = '@../../..'

		self.strain=node.getObject('E')			
		self.gpSampler=node.getParents()[0].getObject('sampler')			

		self.mynode = node.createChild('ColorMapping')
		self.mynode.createObject('TriangleSetTopologyContainer' )
  		self.mynode.createObject('TriangleSetTopologyModifier' )
  		self.mynode.createObject('Quad2TriangleTopologicalMapping' )
		self.disp =self.mynode.createObject('DataDisplay')
		self.mynode.createObject('ColorMap',colorScheme='Blue to Red')
		self.mynode.createObject('IdentityMapping',input=path, output='@.')
		return 0

	def onEndAnimationStep(self,dt):
		S = self.strain.findData('force').value
		vol= self.gpSampler.findData('volume').value
		L = (len(S)/2)*[0]
		for index, item in enumerate(S):
			val = vonMises2d(item) / (vol[index][0] * 4.0)
        		L[2*(index/4)] += val
        		L[2*(index/4)+1] += val
		self.disp.findData('cellData').value= str(L).replace('[', '').replace("]", '').replace(",", ' ')
		return 0

