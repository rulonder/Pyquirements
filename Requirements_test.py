import Requirements
import unittest

class TestRequirementNode(unittest.TestCase):
#    def setUp(self):
#        self.seq = range(10)
    def test_new_node(self):
        # make sure the shuffled sequence does not lose any elements
        Idname = "idNodeTest"
        content= {1:2,"2":3}
        new = Requirements.node(Idname,content)

        self.assertEqual(new.Id, Idname)
        self.assertEqual(new.Content, content)
        # Pointing and pointed arrays is empty
        self.assertEqual(new.Pointing, [])   
        self.assertEqual(new.Pointed,  [])
    def test_addPointing(self):
        Ids = "idNodeTest"
        content= {1:2,"2":3}        
        new = Requirements.node(Ids,content)
        new.addPointing(2)
        self.assertEqual(new.Pointing, [2])        
        new.addPointing("test")
        self.assertEqual(new.Pointing, [2,"test"]) 
        new.addPointing(2)
        self.assertEqual(new.Pointing, [2,"test"]) 
    def test_addPointed(self):
        Ids = "idNodeTest"
        content= {1:2,"2":3}        
        new = Requirements.node(Ids,content)
        new.addPointed(2)
        self.assertEqual(new.Pointed, [2])        
        new.addPointed("test")
        self.assertEqual(new.Pointed, [2,"test"]) 
        new.addPointed(2)
        self.assertEqual(new.Pointed, [2,"test"]) 
    def test_removePointed(self):
        Ids = "idNodeTest"
        content= {1:2,"2":3}        
        new = Requirements.node(Ids,content)
        new.addPointed(2)
        self.assertEqual(new.Pointed, [2])        
        new.removePointed("test")
        # Remove non existing node shall not do anything
        self.assertEqual(new.Pointed, [2]) 
        new.addPointed("test")
        new.removePointed(2)
        self.assertEqual(new.Pointed, ["test"])         
    def test_removePointing(self):
        Ids = "idNodeTest"
        content= {1:2,"2":3}        
        new = Requirements.node(Ids,content)
        new.addPointing(2)
        self.assertEqual(new.Pointing, [2])        
        new.removePointing("test")
        # Remove non existing node shall not do anything
        self.assertEqual(new.Pointing, [2]) 
        new.addPointing("test")
        new.removePointing(2)
        self.assertEqual(new.Pointing, ["test"])         
    def test_Parents(self):
        Ids = "idNodeTest"
        content= {1:2,"2":3}        
        new = Requirements.node(Ids,content)
        new.addParent(2)
        self.assertEqual(new.Parents, [2])        
        new.removeParent("test")
        # Remove non existing node shall not do anything
        self.assertEqual(new.Parents, [2]) 
        new.addParent("test")
        new.removeParent(2)
        self.assertEqual(new.Parents, ["test"])     
    def test_Childs(self):
        Ids = "idNodeTest"
        content= {1:2,"2":3}        
        new = Requirements.node(Ids,content)
        new.addChild(2)
        self.assertEqual(new.Childs, [2])        
        new.removeChild("test")
        # Remove non existing node shall not do anything
        self.assertEqual(new.Childs, [2]) 
        new.addChild("test")
        new.removeChild(2)
        self.assertEqual(new.Childs, ["test"])              
    def test_string(self):
        # make sure the shuffled sequence does not lose any elements
        Idname = "idNodeTest"
        content= {1:2,"2":3}

        new = Requirements.node(Idname,content)
        self.assertEqual(new.getDir(), "idNodeTest") 
        self.assertEqual(new.writeNode(), 'idNodeTest [1="2" 2="3" ];')                
        new.addParent(2)
        self.assertEqual(new.getDir(), "2:idNodeTest") 
        self.assertEqual(new.writeNode(), "") 



class TestNodesContainer(unittest.TestCase):
    def setUp(self):
        self.container = Requirements.nodesContainer()
    def test_loadNodes(self):
        dummyContent="Dummy"
        for Id in range(100):
            self.container.addNode(Id,dummyContent)
        self.assertEqual(len(self.container.getNodesArray()), 100)  

    def test_loadRelations(self):
        # node 0 pitns nobody, node pints node 0, node 2 point node 0 and 1 .....
        for fromId in range(100):
            for toID in range(fromId):
                self.container.addRelation(fromId,toID)

        self.assertEqual(self.container.getNode(50).Pointing, map(str,range(50)))               
        self.assertEqual(self.container.getNode(0).Pointed, map(str,range(1,100)))
    
    def test_removeRelation(self):
        for fromId in range(100):
            for toID in range(fromId):
                self.container.addRelation(fromId,toID)        
        self.container.removeRelation(50,0)        
        self.assertEqual(self.container.getNode(50).Pointing, map(str,range(1,50)))  
        final = range(1,100)
        final.remove(50)             
        self.assertEqual(self.container.getNode(0).Pointed, map(str,final) )

    def test_parentship(self):
        parent = 2
        for fromId in range(100):
            self.container.addParentship(fromId,parent)             
        self.assertEqual(self.container.getNode(2).Childs,map(str,range(100)))  

    def test_nodesfiltering(self):
        dummyContent="Dummy"
        for Id in range(100):
            self.container.addNode(Id,dummyContent)        
        subset = self.container.getSetOfNodes("^11$")
        self.assertEqual(subset, ["11"])        
  

class TestRelationsParser(unittest.TestCase):
    def setUp(self):
        pass
    def test_parseline(self):
        # make sure the shuffled sequence does not lose any elements
        filename = ""
        Relations = Requirements.relationsParser(filename)

        Relations.parseLine(" hola -> adios      ")

        self.assertEqual(Relations.relations , [["hola","adios"]])

        Relations.parseLine(" hola <- adios ")
        Relations.parseLine("")
        self.assertEqual(Relations.relations , [["hola","adios"]])

        Relations.parseLine(" a->b  ")

        self.assertEqual(Relations.relations , [["hola","adios"],["a","b"]])
    def test_parseFile(self):
        filename = "links.txt"
        Relations = Requirements.relationsParser(filename)

        Relations.parseFile()

        self.assertEqual(Relations.relations , [["hola","adios"],["a","b"]])
    def test_loadCOnatiner(self):
        filename = "links.txt"
        Relations = Requirements.relationsParser(filename)
        Relations.parseFile()    

        container = Requirements.nodesContainer()

        Relations.loadNodeContainer(container)
        Nodes = container.getNodesArray()    

        self.assertEqual(Nodes , ["a","adios","b","hola"])  


class TestNodesParser(unittest.TestCase):
    def setUp(self):
        pass
    def test_parseline(self):
        # make sure the shuffled sequence does not lose any elements
        filename = ""
        Relations = Requirements.nodesParser(filename)

        Relations.parseLine(" # UR-20 : TO do something fine   ")

        self.assertEqual(Relations.Nodes , {"UR-20":"TO do something fine"})

        Relations.parseLine(" hola <- adios ")
        Relations.parseLine("")
        self.assertEqual(Relations.Nodes , {"UR-20":"TO do something fine"})


    def test_parseFile(self):
        filename = "nodes.txt"
        Relations = Requirements.nodesParser(filename)

        Relations.parseFile()
        self.assertEqual(Relations.Nodes , {"UR-10" : "Hello", "UR-20" : "TO do something fine"})

    def test_loadCOnatiner(self):
        pass


class TestdotGenerator(unittest.TestCase):
    def setUp(self):
        filenameNodes = "nodes_1.txt"
        filenameLinks = "links_1.txt"
        Nodes     = Requirements.nodesParser(filenameNodes)  
        Nodes.parseFile()      
        Relations = Requirements.relationsParser(filenameLinks)
        Relations.parseFile()

        self.container = Requirements.nodesContainer()
        Nodes.loadNodeContainer(self.container)
        Relations.loadNodeContainer(self.container)


    def test_load_File(self):
        # make sure the shuffled sequence does not lose any elements
        filename= "out.dot"
        dot = Requirements.dotGenerator(self.container, filename)
        dot.loadFile()


class TestTableGenerator(unittest.TestCase):
    def setUp(self):
        filenameNodes = "nodes_1.txt"
        filenameLinks = "links_1.txt"
        Nodes     = Requirements.nodesParser(filenameNodes)  
        Nodes.parseFile()      
        Relations = Requirements.relationsParser(filenameLinks)
        Relations.parseFile()

        self.container = Requirements.nodesContainer()
        Nodes.loadNodeContainer(self.container)
        Relations.loadNodeContainer(self.container)


    def test_load_File(self):
        # make sure the shuffled sequence does not lose any elements
        filename= "out.html"
        dot = Requirements.tableGenerator(self.container, filename)
        dot.loadFile()
        
if __name__ == '__main__':
    unittest.main(verbosity=1)