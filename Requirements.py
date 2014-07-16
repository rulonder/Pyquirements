import os
import re

class node():
    """docstring for node"""
    def __init__(self, Id, Content):
        self.Id = Id
        self.Content = Content
        self.Pointing = []
        self.Pointed = []
        self.Childs = []
        self.Parents = []
    def addPointing(self, pointingId):
        if self.Pointing.count(pointingId) == 0:        
            self.Pointing.append(pointingId)
    def addPointed(self, pointedId):
        if self.Pointed.count(pointedId) == 0:        
            self.Pointed.append(pointedId)
    def removePointed(self, pointedId):
        if self.Pointed.count(pointedId) > 0:
            self.Pointed.remove(pointedId)
    def removePointing(self, pointingId):
        if self.Pointing.count(pointingId) > 0:
            self.Pointing.remove(pointingId)
    def addParent(self, ParentsId):
        if self.Parents.count(ParentsId) == 0:        
            self.Parents.append(ParentsId)            
    def removeParent(self, ParentsId):
        if self.Parents.count(ParentsId) > 0:
            self.Parents.remove(ParentsId)  
    def addChild(self, ChildsId):
        if self.Childs.count(ChildsId) == 0:        
            self.Childs.append(ChildsId)            
    def removeChild(self, ChildsId):
        if self.Childs.count(ChildsId) > 0:
            self.Childs.remove(ChildsId)
    def getlabel(self):
        labelStr=""
        if "label" in self.Content.keys():
            labelStr=self.Content["label"]
        else:
            labelStr = self.Id
        return labelStr            
    def getDir(self):
        IdStr=self.Id
        if len(self.Parents)>0:
            IdStr=str(self.Parents[0])+":"+IdStr
        return IdStr
    def writeNode(self,container=None):
        nodeStr= ""
        # only write if is a parent
        if len(self.Parents)== 0:
            nodeStr= self.Id+" ["
            for key in self.Content.keys():
                nodeStr+= str(key)+'="'+str(self.Content[key])
                # add childs as in UML
                if key == "label":
                    for child in self.Childs:
                        nodeStr+= "|<" + container.getNode(child).Id + ">" + container.getNode(child).getlabel() 
                # finish label
                nodeStr+= '" '    
            if len(self.Childs) > 0:
                nodeStr+="shape=record "
            nodeStr+="];"
        return nodeStr



# this class is in charge of handling the nodes relationships in order to be consistence
class nodesContainer():
    """docstring for nodesContainer"""
    def __init__(self):
        self.Nodes = {}
    def addNode(self,Id,Content):
        # if node already exists override Content but leave relations
        Id = str(Id)
        if Id in self.Nodes:
            self.Nodes[Id].Content = Content
        else:
            self.Nodes[Id] = node(Id,Content)
    def removeNode(self, Id):
        Id = str(Id)
        if Id in self.Nodes:
            for node in self.Nodes[Id].Pointing :
                self.removeRelation(Id, node)
            for node in self.Nodes[Id].Pointed :
                self.removeRelation(node, Id) 
            del self.Nodes[Id]               
    def addRelation(self,pointingID,pointedId):
        # if not present add empty node
        pointingID = str(pointingID)
        pointedId  = str(pointedId ) 
        if pointingID not in self.Nodes:
            self.addNode(pointingID,{"label":pointingID})
        if pointedId not in self.Nodes:
            self.addNode(pointedId,{"label":pointedId})            
        self.Nodes[pointingID].addPointing(pointedId)         
        self.Nodes[pointedId].addPointed(pointingID)     
    def removeRelation(self,pointingID,pointedId):
        pointingID = str(pointingID)
        pointedId  = str(pointedId )         
        if pointingID in self.Nodes:
            if pointedId in self.Nodes:      
                self.Nodes[pointingID].removePointing(pointedId)         
                self.Nodes[pointedId].removePointed(pointingID) 
    def getNode(self,Id):
        return self.Nodes[str(Id)]          
    def getNodesArray(self):
        return sorted(self.Nodes.keys())  
    def addParentship(self,ChildId,ParentId):
        # if not present add empty node
        ChildId = str(ChildId)
        ParentId  = str(ParentId ) 
        if ChildId not in self.Nodes:
            self.addNode(ChildId,{"label":ChildId})
        if ParentId not in self.Nodes:
            self.addNode(ParentId,{"label":ParentId})            
        self.Nodes[ChildId].addParent(ParentId)         
        self.Nodes[ParentId].addChild(ChildId)           
    def removeParentship(self,ChildId,ParentId):
        ChildId = str(ChildId)
        ParentId  = str(ParentId )         
        if ChildId in self.Nodes:
            if ParentId in self.Nodes:      
                self.Nodes[ChildId].removeParent(ParentId)         
                self.Nodes[ParentId].removeChild(ChildId) 
    def getSetOfNodes(self,regexp):
        regular = re.compile(regexp)
        nodes = self.getNodesArray()
        def filterFunction (x) : return regular.search(x)
        return filter(filterFunction, nodes)

class fileParser(object):
    """This object is in  charge of parsing a file , 
        is to be inherit to customize the line parsinfg methods"""
    def __init__(self, filename):
        self.file = filename
        self.loaded = False
    def loadFile(self):
        f = open(self.file)
        g = f.read()
        self.data = g.split("\n")
        self.loaded = True
    def parseFile(self):
        if not self.loaded:
            self.loadFile()
        for line in self.data:
            if self.lineParseCriteria(line):
                self.parseLine(line)
    def lineParseCriteria(self,line):
        return False
    def parseLine(self, line):
        pass
    def __str__(self):
        return "This is the parsing of %s \n Loaded status %l" % (self.file, self.loaded)        
        
# This class reads the files with nodes relations and loads them in the desired container
class relationsParser(fileParser):
    """docstring for relationsParser"""
    def __init__(self, filename):
        fileParser.__init__(self,filename)
        self.relations=[]
        self.parentships =[]
    def lineParseCriteria(self,line):
        return not (line.strip() == '' or line.strip()[0] =='#')
    def parseLine(self, line):
        position = line.find("->")
        if position >= 0:
            fromId = line[0:position].strip()
            toId   = line[position+2:].strip()
            # check parent - child
            position = toId.find(":")
            if position >= 0: 
                parentID = toId[0:position].strip()
                toId   = toId[position+1:].strip()   
                self.parentships.append([toId.strip(), parentID.strip()])                  
            self.relations.append([fromId.strip(), toId.strip()])
    def loadNodeContainer(self, nodeContainer):
        for relation in self.relations:
            nodeContainer.addRelation(relation[0],relation[1])
        for parentship in self.parentships:
            nodeContainer.addParentship(parentship[0],parentship[1])

class nodesParser(fileParser):
    """docstring for nodesParser"""
    def __init__(self, filename):
        fileParser.__init__(self,filename)
        self.Nodes={}  
        self.Relations=[]
    def lineParseCriteria(self,line):
        return (len(line.strip())>1 and line.strip()[0] =='#')
    def parseLine(self, line):
        line = line.strip()
        position = line.find(":")
        if position >= 0:
            Id            = line[1:position].strip()
            Description   = line[position+2:].strip()
            self.Nodes[Id]= Description
    def loadNodeContainer(self, nodeContainer):
        for node in self.Nodes.keys():
            nodeContainer.addNode(node,{"label":self.Nodes[node]})

class dotGenerator():
    def __init__(self, container, fileName):
        self.container = container
        self.fileName  = fileName
        self.name      = ""
    def loadFile(self):
        f = open(self.fileName,"w")
        f.write("""
        digraph g {
        graph [
        ranksep = 4.0;  
        rankdir = "LR"
        ];
        node [
        fontsize = "16"
        shape = "box"
        ];
        edge [
        ];
        \n
        """)
        for node in self.container.Nodes.keys():
            NodeObj = self.container.getNode(node)
            f.write(NodeObj.writeNode(self.container) +"\n")
            idString =NodeObj.getDir()
            # for reverse change to for pointed in NodeObj.Pointed:
            for pointed in NodeObj.Pointed:
                toObj = self.container.getNode(pointed)
                f.write(idString+" -> "+ toObj.getDir() +"; \n" )
        
        #f.write(self.Groupnodes(['SR','UR']))

        f.write("""
        }
        """)
        f.close()
        os.system("dot "+self.fileName+" -Tpng -o outfile.png")
    def Groupnodes(self,regulars):
        string =""
        for regular in regulars:
            group = self.container.getSetOfNodes(regular)
            if group:
                string += "{ \n rank=same; \n  "
                dummy = reduce(joinNodes,group)
                string += dummy + ' [style="invis"] ; \n };\n'
        return string

class tableGenerator():
    def __init__(self, container, fileName):
        self.container = container
        self.fileName  = fileName
        self.name      = ""
    def loadFile(self):
        f = open(self.fileName,"w")
        f.write("""
           <table>
            <tr>
              <th>User Requirements</th>
              <th>Software Requirements</th>
            </tr>
        """)

        for node in self.container.getSetOfNodes("UR"):
            f.write(self.writeElements(node))
        

        f.write("""
           </table>
        """)
        f.close()

    def writeElements(self,node):
        string ="            <tr>\n"
        NodeObj = self.container.getNode(node)
        string += "              <td>"+ NodeObj.getDir() +"</td>\n              <td>"
        for element in NodeObj.Pointing:
            string += self.container.getNode(element).getDir()+ "<br>"
        string +="</td>\n            </tr>\n"            
        return string

def joinNodes(x,y):
    return x+" -> "+y

class HTMLcontainerParser():
    """docstring for HTMLcontainerParser"""
    def __init__(self, container, filename):
        self.html = ""
        self.container = container
        self.filename = filename
                                
