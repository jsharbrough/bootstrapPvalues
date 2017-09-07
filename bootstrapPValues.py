def bootstrapPValues(sortedBootstrapFile):
    #Each parameter in Infile must be sorted from smallest to largest and of the same length!
    infile = open(sortedBootstrapFile,'r')
    outfile = open(sortedBootstrapFile[0:-4] + '_pValues.txt','w')
    parameterList = []
    parameterDict = {}
    lineNum = 0
    lineHeader = ''
    for line in infile:
        if lineNum == 0:
            lineHeader = line[0:-1]
            splitLine = lineHeader.split('\t')
            for item in splitLine[1:]:
                parameterList.append(item)
                parameterDict[item] = []
        else:
            splitLine = line.split('\t')
            i = 0
            for value in splitLine[1:]:
                currParam = parameterList[i]
                currParamList = parameterDict[currParam]
                currParamList.append(float(value))
                parameterDict[currParam] = currParamList
                i += 1
        lineNum += 1
    infile.close()
    pValues = {}
    total = 0
    for parameter1 in parameterList:
        total += 1
        for parameter2 in parameterList:
            paramList2 = parameterDict[parameter2]
            paramList1 = parameterDict[parameter1]
            if len(paramList1) < len(paramList2):
                paramList2 = paramList2[0:(len(paramList1))]
            elif len(paramList2) < len(paramList1):
                paramList1 = paramList1[0:(len(paramList2))]
            i = 0
            if paramList1[0] > paramList2[len(paramList2)-1] or paramList1[len(paramList1)-1] < paramList2[0]:
                p = '< 0.0002'
                pValues[(parameter1,parameter2)] = p
            else:
                i = i
                while i < len(paramList1):
                    if paramList1[i] > paramList2[(len(paramList2)-(i+1))] or paramList1[(len(paramList1)-(i+1))] < paramList2[i]:
                        finalNum = i + 1
                        i = len(paramList1)
                    else:
                        finalNum = i + 1
                        i += 1
                pvalue = ((finalNum)*2.0)/len(paramList1)
                pValues[(parameter1,parameter2)] = pvalue
    paramNum = 1
    for parameter1 in parameterList:
        outfile.write(parameter1)
        for parameter2 in parameterList[paramNum:]:
            outfile.write('\t' + str(pValues[(parameter1,parameter2)])) 
        outfile.write('\n')
        paramNum += 1
    outfile.close()
    