#!/usr/bin/env python
# Colin
# Modified by Tae Jeong
# batch mode for cmsRun, March 2009


import os, sys,  imp, re, pprint, string
from optparse import OptionParser

# particle flow specific
from batchmanager import BatchManager
import castortools

# cms specific
import FWCore.ParameterSet.Config as cms
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper

def batchScriptLocal(  remoteDir, index ):
   
   
   script = """#!/bin/bash
echo 'running'
%s run_cfg.py
echo
echo 'sending the job directory back'
""" % prog

   if remoteDir != '':
      script += """
for file in *.root; do
newFileName=`echo $file | sed -r -e 's/\./_%s\./'`
rfcp $file %s/$newFileName 
done
""" % (index, remoteDir)

   return script


class MyBatchManager( BatchManager ):

    # prepare a job
    def PrepareJobUser(self, jobDir, value ):

       process.source = fullSource.clone()

       #prepare the batch script
       scriptFileName = jobDir+'/batchScript.sh'
       scriptFile = open(scriptFileName,'w')

       # are we at CERN or somewhere else? testing the afs path
       cwd = os.getcwd()
       patternCern = re.compile( '^/afs/cern.ch' )

       patternBatch = re.compile( '\w*bsub')
       wantBatch = patternBatch.match( options.batch )
       if wantBatch:
          print "we want to run on the batch with bsub"
          if patternCern.match( cwd ):
             print '@ CERN'
             scriptFile.write( batchScriptCERN( self.remoteOutputDir_,
                                                value) )
       else: 
          print '@ local'
          scriptFile.write( batchScriptLocal( self.remoteOutputDir_,
                                              value) )          
       
       scriptFile.close()
       os.system('chmod +x %s' % scriptFileName)

       #prepare the cfg
       
       # replace the list of fileNames by a chunk of filenames:
       if generator:
          randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
          randSvc.populate()
       else:

          print "grouping : ", grouping
          print "value : ", value
          
          iFileMin = (value)*grouping 
          iFileMax = (value+1)*grouping 
          
          process.source.fileNames = fullSource.fileNames[iFileMin:iFileMax]
          print process.source
          
       cfgFile = open(jobDir+'/run_cfg.py','w')
       cfgFile.write(process.dumpPython())
       cfgFile.close()
       
    def SubmitJob( self, jobDir ):
       os.system( self.options_.batch )


batchManager = MyBatchManager()


file = open('cmsBatch.txt', 'w')
file.write(string.join(sys.argv) + "\n")
file.close()

batchManager.parser_.usage = "%prog [options] <number of input files per job> <your_cfg.py>. Submits a number of jobs taking your_cfg.py as a template. your_cfg.py can either read events from input files, or produce them with a generator. In the later case, the seeds are of course updated for each job.\n\nExample:\tcmsBatch.py 10 fastSimWithParticleFlow_cfg.py -o Out2 -r /castor/cern.ch/user/c/cbern/CMSSW312/SinglePions -b 'bsub -q 1nh < batchScript.sh' "
batchManager.parser_.add_option("-p", "--program", dest="prog",
                                help="program to run on your cfg file",
                                default="cmsRun")
batchManager.parser_.add_option("-b", "--batch", dest="batch",
                                help="batch command. default is: bsub -q cmst3 < batchScript.sh",
                                default="bsub -q cmst3 < batchScript.sh")

(options,args) = batchManager.parser_.parse_args()
batchManager.ParseOptions()

prog = options.prog

if len(args)!=2:
   batchManager.parser_.print_help()
   sys.exit(1)

grouping = int(args[0])
nJobs = grouping
cfgFileName = args[1]
# queue = options.queue

# load cfg script
handle = open(cfgFileName, 'r')
cfo = imp.load_source("pycfg", cfgFileName, handle)
process = cfo.process
handle.close()

# keep track of the original source
fullSource = process.source.clone()



generator = False

try:
   process.source.fileNames
except:
   print 'No input file. This is a generator process.'
   generator = True
   listOfValues = range( 0, nJobs)
else:
   print "Number of files in the source:",len(process.source.fileNames), ":"
   pprint.pprint(process.source.fileNames)
   
   nFiles = len(process.source.fileNames)
   nJobs = nFiles / grouping
   if (nJobs!=0 and (nFiles % grouping) > 0) or nJobs==0:
      nJobs = nJobs + 1
      
   print "number of jobs to be created: ", nJobs

   listOfValues = range( 0, nJobs)

batchManager.PrepareJobs( listOfValues )



batchManager.SubmitJobs()



