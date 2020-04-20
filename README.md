# KEGGGraph

Graph Visualization Tool for KEGG Pathway Maps

## Build Steps

1. Clone the [HOLA](https://github.com/skieffer/hola) repository into a directory of your choice, `HOLADIR`
2. Go to HOLADIR, and clone the KEGGGraph repository into it.
3. Follow the instructions at the [HOLA](https://github.com/skieffer/hola) to build Hola.

## Using KEGGGraph

1. Use Graphviz to generate graph. Output stores in `output.png` :

   ```
   $ ./KEGG_Graphviz [xlsx file pathway]
   ```

2. Use Hola to generate graph.

   ```
   $ ./KEGG_Hola [xlsx file pathway] > [Output file]
   ```
