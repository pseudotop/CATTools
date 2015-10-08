import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.register('dataset', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "dataset: 0  default")
options.parseArguments()
process = cms.Process("h2muAnalyzer")

if options.dataset == 0:
    savename ="h2mu.root"
    datadir1 = '/xrootd/store/group/CAT/SingleMuon/v7-4-2_Run2015D-PromptReco-v3/150930_225445/0000/'
    datadir2 = '/xrootd/store/group/CAT/SingleMuon/v7-4-2_Run2015D-PromptReco-v3/150930_225445/0000/'

if options.dataset == 1:
    savename ="SingleMuon.root"
    datadir1 = '/xrootd/store/group/CAT/SingleMuon/v7-4-2_Run2015C-PromptReco-v1/150928_133011/0000/'
    datadir2 = '/xrootd/store/group/CAT/SingleMuon/v7-4-2_Run2015D-PromptReco-v3/150930_225445/0000/'
if options.dataset == 2:
    savename ="DoubleMuon.root"
    datadir1 = '/xrootd/store/group/CAT/DoubleMuon/v7-4-2_Run2015C-PromptReco-v1/150928_133225/0000/'
    datadir2 = '/xrootd/store/group/CAT/DoubleMuon/v7-4-2_Run2015D-PromptReco-v3/150928_133626/0000/'
    

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
import os
for f in os.listdir(datadir1):
    if '.root' in f:
        process.source.fileNames.append("file:"+datadir1+f)
for f in os.listdir(datadir2):
    if '.root' in f:
        process.source.fileNames.append("file:"+datadir2+f)
print process.source.fileNames
#runOnMC=True
### for run data
#lumiFile = 'Cert_246908-255031_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
lumiFile = 'Cert_246908-256869_13TeV_PromptReco_Collisions15_25ns_JSON.txt'
#for i in process.source.fileNames:
#    if 'Run2015' in i:
#        runOnMC=False

if options.dataset:
    from FWCore.PythonUtilities.LumiList import LumiList
    lumiList = LumiList(os.environ["CMSSW_BASE"]+'/src/CATTools/CatProducer/prod/LumiMask/'+lumiFile)
    process.source.lumisToProcess = lumiList.getVLuminosityBlockRange()
    print process.source.lumisToProcess
        
process.h2mu = cms.EDAnalyzer("h2muAnalyzer",
    vertices = cms.InputTag("catVertex"),
    muons = cms.InputTag("catMuons"),
    electrons = cms.InputTag("catElectrons"),
    jets = cms.InputTag("catJets"),
    mets = cms.InputTag("catMETs"),
    mcLabel = cms.InputTag("prunedGenParticles"),
    triggerBits = cms.InputTag("TriggerResults","","HLT"),
    triggerObjects = cms.InputTag("catTrigger"),
    #triggerObjects = cms.InputTag("selectedPatTrigger"),
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(savename)
)

process.p = cms.Path(process.h2mu)
process.MessageLogger.cerr.FwkReport.reportEvery = 50000


