import numpy as np
seqA = 'AAAGTCGTCGTCGTCGTCGTC'
seqB = 'ATAGTCGTCGTCGTCGTCGTC'

def get_intersect(a1, a2, b1, b2):
    """ 
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)

def hamming(s1,s2):
    result=0
    if len(s1)!=len(s2):
        print("String are not equal")
    else:
        for x,(i,j) in enumerate(zip(s1,s2)):
            if i!=j:
                #print(f'char not math{i,j}in {x}')
                result+=1
    return result

def computeSimilarity(templateStrand, testStrand, readingFrame = 3, matches = 2, ):
    i = 0
    res = []
    while (i < len(testStrand)):
        #print( (str)(testStrand)[i:(i+3)])
        j = 0
        while (j < len(templateStrand)):
            #print( (str)(templateStrand)[i:(i+3)])
            if(hamming((str)(templateStrand)[j:(j+3)],(str)(testStrand)[i:(i+3)]) <= (readingFrame-matches)):
                res.append(((int)(i/readingFrame),(int)(j/readingFrame)))
            j+= readingFrame
        i+=readingFrame
    return res

def graphIntersections (seq):
    ints = []
    for i in range(0,len(seq)):
        #print(seq[i])
        intersections = 0
        for j in range(0,len(seq)):
            if(seq[j][0]!=seq[i][0]):
                x = get_intersect([0,seq[i][0]],[1,seq[i][1]],[0,seq[j][0]],[1,seq[j][1]])[0]
                if (x > 0.0 and x < 1.0):
                    intersections +=1
        ints.append(intersections)
    return ints

def computeAccuracy(seq):
    result = 0
    for i in range (0, len(seq)):
        if(seq[i]==0):
            result+=1
    return result

def pruneTree (tree, intersections):
    maxError = 0
    errorArea = -1
    for i in range(0, len(intersections)):
        if (intersections[i] > maxError):
            maxError = intersections[i]
            errorArea = i
    currentAccuracy = computeAccuracy(intersections)
    print("current accuracy = ", currentAccuracy)
    print("max error = ", maxError)

    if(maxError > 0):
        newTree = tree[:]
        newTree.pop(errorArea)
        print("Worst node is ", errorArea)
        print("new tree = ", newTree)
        newIntersections = graphIntersections(newTree)
        newError = computeAccuracy(newIntersections)
        pruneTree(newTree,newIntersections)
    else:
        return(tree, intersections)
    

seq = computeSimilarity(seqA,seqB)
print(seq)
print(graphIntersections(seq))
print(pruneTree(seq,graphIntersections(seq)))