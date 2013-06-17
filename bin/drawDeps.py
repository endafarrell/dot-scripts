#!/usr/bin/python
import pprint
import sys

# A script to help visaulaise dependencies. This example was drawn up using a
# complex Java suite of applications which are built using a Maven reactor
# build. There are good tools for drawing dependency trees for maven, but when
# the dependencies reach down into sub-modules, the tools simply draw the
# dependencies for the particular project. There *is* one plugin for maven
# (http://mvnplugins.fusesource.org/maven/1.10/maven-graph-plugin/) but for
# large projects it can result in difficult to read diagrams. Hence this.


#################################################################################
# Left depends on right.
# This is from where the dependencies are taken and are generated as follows:
# 1/ mvn dependency:tree -DoutputType=dot -Dincludes=com.you.X,com.you.A \
#        -DoutputFile=dependency.digraph    
#    This generates a reactor module by module dependency in digraph format.
#    Note that it creates compile, test and provided dependencies which later we
#    are going to "suppress"/flatten - you may wish to pay more attention here.
# 2/ find ./ -name dependency.digraph -exec grep '" -> "' {} \;
#    This gathers together all the digraphs and gives the dependencies. 
# 3/ cut -c2-
#    This left-aligns the data
# 4/ At this stage you may wish to do a few more things such as:
#    - remove your current build-number (esp if you have a SNAPSHOT build)
#    - shorten your "com.you.X" and/or "com.you.A" to "c.y.X" and/or "c.y.A"
#    - suppress/flatten ":compile" and/or ":test"

# find ./ -name dependency.digraph -exec grep '" -> "' {} \; | cut -c2- | \
#    sed 's/:2.24.0-SNAPSHOT:compile//g' | sed 's/:2.24.0-SNAPSHOT//g' | \
#    sed # 's/:jar:test"/:jar"/g' | sed 's/com.x.nose/c.n.n/g' | \
#    sed 's/com.x.buss/c.n.b/g' > left.depends-on.right


file = open("left.depends-on.right")
lines = file.readlines()
file.close()

modules = set()
deps = set()

for line in lines:
  line = line.rstrip(" ;\n")
  (left, right) = line.split(" -> ")
  if left not in modules:
    modules.add(left)
  if right not in modules:
    modules.add(right)
  if (left, right) not in deps:
    deps.add( (left, right) )

modules = frozenset(modules)
deps = frozenset(deps)

def nextOrder(modules, deps, ordered, unordered, fileName):
  order = set()
  for module in unordered:
    isOrd = True
    for (left, right) in deps:
      if module == left:
        if right not in ordered:
          # It's not already ordered, so this is not this order
          isOrd = False
    if isOrd:
      order.add(module)

  file = open(fileName,"w")
  pprint.pprint(order, file, 2, 70)
  file.close()

  ordered = ordered | order # Union
  unordered = modules - ordered # difference
  return ordered, unordered

# Writes the "generation" file for the supplied args.
# A file is in "this generation" if it only appears in the "left" side of the
# dependencies. For generations other than the first, if a module appears on the
# right, the corresponding left should be in the already-generation-ed list.
def nextGeneration(modules, deps, gened, ungened, fileName):
  gen = set()
  for module in ungened:
    isGen = True
    for (left, right) in deps:
      if module == right:
        if left not in gened:
          isGen = False
    if isGen:
      gen.add(module)

  file = open(fileName,"w")
  pprint.pprint(gen, file, 2, 70)
  file.close()

  gened = gened | gen # union
  ungen = modules - gened # difference
  return gened, ungen, gen


ordered = set()
unordered = modules
orderIndex = 1
while len(unordered) > 0:
  (ordered, unordered) = \
      nextOrder(modules, deps, ordered, unordered, "order-%02d" % orderIndex)
  orderIndex = orderIndex + 1

gened = set()
ungened = modules
structuredDeps = dict()
genIndex = 1
while len(ungened) > 0:
  filename = "gen-%02d" % genIndex
  (gened, ungened, thisGen) = \
      nextGeneration(modules, deps, gened, ungened, filename)
  structuredDeps[filename] = sorted(thisGen)
  genIndex = genIndex + 1

#pprint.pprint(structuredDeps, sys.stdout, 2, 70)

genAlpha = []
for gen in sorted(structuredDeps.keys()):
  genAlpha.extend(structuredDeps[gen])
  genAlpha.append("x")
#pprint.pprint(genAlpha, sys.stdout, 2, 70)


file = open("dependencies-by-generation.csv", "w")
# Header row
file.write( "row.depends-on.col," )
for mod in genAlpha:
  file.write( "%s," % mod )
file.write("\n")

# Data row
for row in genAlpha:
  file.write( "%s," % row )
  csvRow = []
  for col in genAlpha:
    csvRow.append(".")
    for (left, right) in deps:
      if left == row:
        try: 
          csvCol = genAlpha.index(right)
          csvRow[csvCol] = "Y"
        except:
          pass
  file.write( ",".join(csvRow) )
  file.write( "\n" )
file.close()

mods = sorted(modules)
file = open("dependencies-by-module.csv", "w")
# Header row
file.write( "row.depends-on.col," )
for mod in mods:
  file.write( "%s," % mod )
file.write("\n")

# Data row
for row in mods:
  file.write( "%s," % row )
  csvRow = []
  for col in mods:
    csvRow.append(".")
    for (left, right) in deps:
      if left == row:
        try: 
          csvCol = mods.index(right)
          csvRow[csvCol] = "Y"
        except:
          pass
  file.write( ",".join(csvRow) )
  file.write( "\n" )
file.close()

