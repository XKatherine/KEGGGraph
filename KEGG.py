import sys
import pandas as pd
import graphviz
from hola.hola import hola
from hola.hola import HolaConfig
from hola.ortho import Compass
import hola.gmlparse as gmlparse

class Node:
    def __init__(self, idx, label, shape, x, y, w, h, label_anchor):
        self.id = idx
        self.label = label
        self.shape = shape
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label_anchor = label_anchor
        
    def to_gml(self):
        node_id = "\t" + "\t" + "id " + str(self.id) + "\n"
        node_label = "\t" + "\t" + "label " + '\"' + self.label + '\"' + "\n"
        node_x = "\t" + "\t" + "\t" + "x " + str(self.x) + "\n"
        node_y = "\t" + "\t" + "\t" + "y " + str(self.y) + "\n"
        node_w = "\t" + "\t" + "\t" + "w " + str(self.w) + "\n"
        node_h = "\t" + "\t" + "\t" + "h " + str(self.h) + "\n"
        node_shape =  "\t" + "\t" + "\t" + "type " + '\"' + self.shape + '\"' + "\n"
        node_anchor = "\t" + "\t" + "\t" + "anchor " + '\"' + self.label_anchor + '\"' + "\n"
        node_graphics = "\t" + "\t" + "graphics [" + "\n" \
                        + node_x + node_y + node_w + node_h + node_shape \
                        + "\t" + "\t" + "]" + "\n"
        node_label_graphics = "\t" + "\t" + "LabelGraphics [" + "\n" \
                                + "\t" + "\t" + "\t" + 'type \"text\"' + "\n" \
                                + "\t" + "\t" + "\t" +  'text ' + '\"' + self.label + '\"' + "\n" \
                                + node_anchor \
                                + "\t" + "\t" + "]" + "\n"
        gml = "\t" + "node [" + "\n" \
                + node_id + node_label + node_graphics + node_label_graphics \
                + "\t" + "]" + "\n"
        return gml
        
    def __str__(self):
        return "Node "+str(self.id)+": "+self.label

class Edge:
    def __init__(self, source, target, direction, source_arrow, target_arrow, style):
        self.source = source
        self.target = target
        self.direction = direction
        self.source_arrow = source_arrow
        self.target_arrow = target_arrow
        self.style = style
        
    def to_gml(self):
        edge_source = "\t" + "\t" + "source " + str(self.source) + "\n"
        edge_target = "\t" + "\t" + "target " + str(self.target) + "\n"
        edge_arrow = "last" if self.direction == 0 else "both"
        edge_graphics = "\t" + "\t" + "graphics [" + "\n" \
                        + "\t" + "\t" + "\t" + 'type \"quadCurve\"' + "\n" \
                        + "\t" + "\t" + "\t" + "style " + '\"' + self.style + '\"' + "\n" \
                        + "\t" + "\t" + "\t" + "arrow " + '\"' + edge_arrow + '\"' + "\n" \
                        + "\t" + "\t" + "\t" + "sourceArrow " + '\"' + self.source_arrow + '\"' + "\n" \
                        + "\t" + "\t" + "\t" + "targetArrow " + '\"' + self.target_arrow + '\"' + "\n" \
                        + "\t" + "\t" + "]" + "\n"
        gml = "\t" + "edge [" + "\n" \
                + edge_source + edge_target + edge_graphics \
                + "\t" + "]" + "\n"
        return gml
        
    def __str__(self):
        return "Node: "+str(self.source)+" - "+"Node: "+str(self.target)

class KEGGGraph:
    def __init__(self, pathway):
        xls = pd.ExcelFile(pathway)
        df_node = pd.read_excel(xls, 'Node')
        df_edge = pd.read_excel(xls, 'Edge')
        
        V = []
        for idx, row in df_node.iterrows():
            if row['Type'] == "map":
                s = len(row['Label'])
                width = int(s/4.5*30)
                n = Node(row['Node_ID'], row['Label'], "roundrectangle", 0, 0, width, 30, "c")
            elif row['Type'] == "module":
                n = Node(row['Node_ID'], row['Label'], "circle", 0, 0, 10, 10, "s")
            else:
                s = len(row['Label'])
                width = int(s/7*50)
                n = Node(row['Node_ID'], row['Label'], "rectangle", 0, 0, width, 20, "c")
            V.append(n)
        
        E = []
        for idx, row in df_edge.iterrows():
            if pd.isnull(row['Label_ID']) is True:
                if row['IS_Double'] == 1:
                    if row['Type'] == "empty_dash":
                        e = Edge(row['Source_Node_ID'], row['Target_Node_ID'], 1, "white_delta", "white_delta", "dashed")
                        E.append(e)
                    else:
                        e = Edge(row['Source_Node_ID'], row['Target_Node_ID'], 1, "delta", "delta", "line")
                        E.append(e)
                else:
                    if row['Type'] == "empty_dash":
                        e = Edge(row['Source_Node_ID'], row['Target_Node_ID'], 1, "none", "white_delta", "dashed")
                        E.append(e)
                    else:
                        e = Edge(row['Source_Node_ID'], row['Target_Node_ID'], 1, "none", "delta", "line")
                        E.append(e)
            else:
                if row['IS_Double'] == 1:
                    e1 = Edge(int(row['Label_ID']), row['Source_Node_ID'], 0, "none", "delta", "line")
                    e2 = Edge(int(row['Label_ID']), row['Target_Node_ID'], 0, "none", "delta", "line")
                    E.append(e1)
                    E.append(e2)
                else:
                    e1 = Edge(int(row['Label_ID']), row['Source_Node_ID'], 1, "none", "none", "line")
                    e2 = Edge(int(row['Label_ID']), row['Target_Node_ID'], 0, "none", "delta", "line")
                    E.append(e1)
                    E.append(e2)
                    
        self.V = V
        self.E = E
        
    def to_gml(self):
        nodes = ""
        for v in self.V:
            nodes += v.to_gml()
        edges = ""
        for e in self.E:
            edges += e.to_gml()
        gml = "graph [" + "\n" \
                + "\t" + "directed 1" + "\n" \
                + nodes + edges \
                + "]"
        return gml
        
    def to_hola_gml(self):
        gml = self.to_gml()
        G_hola = gmlparse.buildGraph(gml)
        hola(G_hola)
    
        for idx, n in G_hola.nodes.items():
            n.label = G.V[idx].label
            n.label_anchor = G.V[idx].label_anchor
        edges = [0 for i in range(len(G.E))]
        for idx, e in enumerate(G.E):
            edge = str(e.source) + " --> " + str(e.target)
            edges[idx] = edge
        for idx, n in G_hola.edges.items():
            index = edges.index(idx)
            n.style = G.E[index].style
            n.arrow = "last" if G.E[index].direction == 0 else "both"
            n.source_arrow = G.E[index].source_arrow
            n.target_arrow = G.E[index].target_arrow
            gml_out = G_hola.writeGML()
        return gml_out
    
    def save_gml(self):
        gml_file = self.to_hola_gml()
        sys.stdout.write(gml_file)
    
    def to_graphviz(self):
        d = graphviz.Digraph()
        for v in self.V:
            if v.shape == 'circle':
                d.node(str(v.id), xlabel = v.label, shape = 'point', style = 'filled', fillcolor = 'white', fixedsize = 'true', width = '0.1')
            elif v.shape == 'rectangle':
                d.node(str(v.id), label = v.label, shape = 'rectangle')
            elif v.shape == 'roundrectangle':
                d.node(str(v.id), label = v.label, shape = 'box', style = 'rounded')

        for e in self.E:
            if e.direction == 1:
                if e.target_arrow == 'white_delta':
                    d.edge(str(e.source), str(e.target), dir='both', arrowhead='empty', arrowtail='empty', style='dashed')
                elif e.target_arrow == 'delta':
                    d.edge(str(e.source), str(e.target), dir='both', arrowhead='normal', arrowtail='normal')
                elif e.target_arrow == 'none':
                    d.edge(str(e.source), str(e.target), dir='none')
            else:
                if e.target_arrow == 'white_delta':
                    d.edge(str(e.source), str(e.target), dir='forward', arrowhead='empty', style='dashed')
                elif e.target_arrow == 'delta':
                    d.edge(str(e.source), str(e.target), dir='forward', arrowhead='normal')
        d.graph_attr.update({'splines' : 'ortho'})
        d.graph_attr.update({'rankdir': 'LR'})
        d.engine = 'fdp'
        return d
        
    def graphviz_view(self):
        d = self.to_graphviz()
        d.format = 'png'
        d.view('output.png')
        d.render()

    def __str__(self):
        string = ""
        for v in self.V:
            string += str(v)+'\n'
        for e in self.E:
            string += str(e)+'\n'
        return string

#if __name__ == "__main__":
#    pathway = sys.argv[1]
#    G = KEGGGraph(pathway)
#
#    G.graphviz_view()
