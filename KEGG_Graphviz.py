from KEGG import *

if __name__ == "__main__":
    pathway = sys.argv[1]
    G = KEGGGraph(pathway)
    G.graphviz_view()
