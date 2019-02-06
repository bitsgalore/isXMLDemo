#! /usr/bin/env python
#
# Simple demo of XML identification using standard XML parser
#
# Assumption: if contents of file can be parsed by XML parser (i.e. qualifies
# as well-formed XML), format is XML.
# 
# Copyright (C) 2011 Johan van der Knijff, Koninklijke Bibliotheek - National Library of the Netherlands
#	
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# XML parsing code modified from original code by Farhad Fouladi:
#
# http://code.activestate.com/recipes/52256-check-xml-well-formedness/
#

import sys, os, time
import xml.parsers.expat
from glob import glob

def errorExit(msg):
    print ("ERROR (isXMLDemo.py): "+ msg)
    sys.exit()

def getFilesFromTree(rootDir):
    # Recurse into directory tree and return list of all files
    # NOTE: directory names are disabled here!!

    filesList=[]
    for dirname, dirnames, filenames in os.walk(rootDir):
        #Suppress directory names
        for subdirname in dirnames:
            thisDirectory=os.path.join(dirname, subdirname)

        for filename in filenames:
            thisFile=os.path.join(dirname, filename)
            filesList.append(thisFile)
    return filesList

def checkFileInput(fileIn):
    # Check if fileIn is file or directory
    if os.path.isfile(fileIn)==True:
        fileInStatus="isFile"
    elif os.path.isdir(fileIn)==True:
        fileInStatus="isDir"
    else:
        fileInStatus="isNothing"
    return(fileInStatus)

def parseFile(fileObject):
    parser = xml.parsers.expat.ParserCreate()
    parser.ParseFile(fileObject)
                      
def isXML(fileObject):
    # returns 'True' if fileObject is well-formed XML, and 'False' otherwise
    # Only well-formedness is checked (so no validation)
    # Non-parsable (e.g. binary) data will raise an exception in parsefile, which
    # will set the return value of this function to "False"
    
    try:
        parseFile(fileObject)
        # No exception is raised *only* if fileObject contains well-formed XML
        return(True)
    except Exception:
        # Not well-formed XML (could be anything, including binary data)
        return(False)
    
def getCommandLineArguments():
    # Command line arguments to string variable 'argv'
    argv=sys.argv

    # Count number of arguments (remember first argument -  
    # which has index 0 - is the executable/script name!!
    argc=len(argv)

    # Wrong number of arguments: display syntax and exit..
    if argc < 3:
        usage()
        sys.exit()

    # 1st argument: input file
    fileIn=os.path.normpath(argv[1])

    # 2nd argument: output file
    fileOut=os.path.normpath(argv[2])

    return(fileIn, fileOut)

def usage():

    print("""
isXMLDemo.py version 11 July 2011 (JvdK)

Checks file (or collection of files in directory tree) for XML well-formedness

USAGE: isXMLDemo.py <fileIn> <fileOut>

 fileIn         : input file or directory
                    If fileIn is a directory, all files within that 
                    directory and its sub-directories will be analysed
 fileOut        : output file
 
  """)
   
def main():

    # Keep track of start and end time
    startTime = time.time()

    # Get parameters from command line
    inputFile,outputFile=getCommandLineArguments()

    # Check if fileIn is file or directory (and exit if neither)
    inputFileStatus=checkFileInput(inputFile)
    if inputFileStatus=="isNothing":
        msg=inputFile + " does not exist!"
        errorExit(msg)

    # Delete output file if it already exists (reason: we'll be
    # writing in append mode later)
    if checkFileInput(outputFile)=="isFile":
        os.remove(outputFile)

    # Open output file in append mode
    try:
        fOut=open(outputFile,"a")
    except Exception:
        msg=outputFile + " could not be written"
        errorExit(msg)

    # Generate list of files to process
    if inputFileStatus=="isFile":
        myFilesIn=[]
        myFilesIn.append(inputFile)
    else:
        myFilesIn=getFilesFromTree(inputFile)

    numberOfFiles=len(myFilesIn)

    for i in range(0,numberOfFiles):

        outStr="Processing file "+ str(i+1)+ "/"+str(numberOfFiles) + "\r"
        sys.stdout.write(outStr)
        sys.stdout.flush()

        myFileIn=myFilesIn[i]

        try:
            fIn=open(myFileIn, "rb")
      
            # Check for well-formedness. For any non-XML files the result
            # will be "False" 
            isWellFormed=isXML(fIn)
        
            if isWellFormed == True:
                statusString="isXML"
            else:
                statusString="noXML"

        except Exception:
            # Some read error occurred (file doesn't exist, permission denied, etc)
            statusString="readError"

        # Generate output line 
        lineOut='"' + myFileIn + '",' + statusString + '\n'

        # Append output to output file
        fOut.write(lineOut)
    
    fOut.close()

    # How much time did this all take?
    endTime = time.time()
    elapsedTime=endTime-startTime

    try:
        throughput=int(numberOfFiles/elapsedTime)
    except Exception:
        throughput=-9999

    outStr="Processed  " + str(numberOfFiles) + " files in "+ str(elapsedTime) + \
    " seconds \n" + "Average throughput: " + str(throughput) + " files / s \n"
    sys.stdout.write(outStr)
  
main()