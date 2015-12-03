#!/usr/bin/env python

import ROOT,os,sys,copy,json
ROOT.gROOT.SetBatch(True)


cmssw = os.environ['CMSSW_BASE']

outDir = "plot"
exe = "h2muDraw.py"
if not os.path.isdir(outDir):os.mkdir(outDir)
abspathOut = os.path.abspath("./")
abspathExe = "%s/%s"%(abspathOut,exe)

try:
    info_json = json.load(open("%s/info.json" % outDir))
    isdatajson = os.path.isfile("%s/src/CATTools/CatAnalyzer/data/dataset.json" % os.environ['CMSSW_BASE'])
except:
    info_json = None
    isdatajson = None

if (info_json==None) or (isdatajson==None):
    print """
    !! WARNNING !!

    1. before you run, dataset.json file in "data" folder is required
    2. please try to run "set_config.py" file which makes json file at first.
    and then you can run this file.
    """
    sys.exit(2)

sh_s = """#!/bin/bash
workD=%s
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $workD
eval `scramv1 runtime -sh`
cd -
%s
"""

jds_s = """
executable = %s
universe = vanilla
getenv = True

dir= %s/plot
num= %s
fname= %s

error = $(dir)/error_$(num)
log = $(dir)/log_$(num)

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = %s
transfer_output_files = $(fname).png
transfer_output_remaps = "$(fname).png = $(dir)/$(fname).png"

queue
""" 
for i,info in enumerate(info_json):
    plotvar,f_name,cut,binning,x_name,y_name = info['plotvar'],info['f_name'],info['cut'],info['binning'],info['x_name'],info['y_name']
    if plotvar == 'll_m':
        args = "-c \'%s\' -b %s -p %s -x \'%s\' -y \'%s\' -f \'%s\'-d"%(cut,binning,plotvar,x_name,y_name,f_name)
    else:
        args = "-c \'%s\' -b %s -p %s -x \'%s\' -y \'%s\' -f \'%s\'"%(cut,binning,plotvar,x_name,y_name,f_name)
    
    if not i<1:continue
    name_sh, name_jds = "%s/tmp_%s.sh"%(outDir,i),"%s/tmp_%s.jds"%(outDir,i)
    f_sh = sh_s%(cmssw,abspathExe+" "+args)
    tmp_f_sh = open(name_sh,"w")
    tmp_f_sh.write(f_sh)
    tmp_f_sh.close()
    f_jds = jds_s%("tmp_%s.sh"%i,abspathOut,i,f_name,abspathExe)
    tmp_f_jds = open(name_jds,"w")
    tmp_f_jds.write(f_jds)
    tmp_f_jds.close()
    os.system("chmod 755 %s"%name_jds)
    os.system("chmod 755 %s"%name_sh)
    os.system("condor_submit %s"%(name_jds))
    #os.system("rm -f tmp.jds")
    #os.system("rm -f tmp.sh")
    print "%d/%d"%(i,len(info_json))
    #os.system("mv -t %s %s %s"%(outDir,name_sh,name_jds))
#print ("./h2muDraw.py -c \"%s\" -b %s -p %s -x %s -y %s -f %s/%s&"%(cut,binning,plotvar,x_name,y_name,outDir,f_name))
