import Requirements

def loadNodes2Container(file,container):
	Nodes     = Requirements.nodesParser(file)  
	Nodes.parseFile() 
	Nodes.loadNodeContainer(container) 	

def loadRelations2Container(file,container):
	Nodes     = Requirements.relationsParser(file)  
	Nodes.parseFile() 
	Nodes.loadNodeContainer(container) 	

filenameSoft = "closeap\\CloseapSoft.req"
filenameCode = "closeap\\CloseapCode.req"
filenameUser = "closeap\\CloseapUser.req"

container = Requirements.nodesContainer()


loadNodes2Container(filenameSoft,container)
loadNodes2Container(filenameCode,container)
#loadNodes2Container(filenameUser,container)


loadRelations2Container(filenameSoft,container)
loadRelations2Container(filenameCode,container)
#loadRelations2Container(filenameUser,container)

# make sure the shuffled sequence does not lose any elements
filename= "closeap\\out.html"
dot = Requirements.tableGenerator(container, filename)
dot.loadFile()

filename= "closeap\\out.dot"
dot = Requirements.dotGenerator(container, filename)
dot.loadFile()


