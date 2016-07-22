#!/usr/bin/env python
import ROOT, CATTools.CatAnalyzer.CMS_lumi, json, os, getopt, sys
from CATTools.CatAnalyzer.histoHelper import *
from ROOT import TLorentzVector
#import DYestimation
ROOT.gROOT.SetBatch(True)

rfile = ROOT.TFile("histo_higgs.root")

ltname = ["/nom","/mu_u","/mu_d","/jes_u","/jes_d","/jer_u","/jer_d"]
lh=[]
for i in range(len(ltname)):
  h=rfile.Get(ltname[i])
  h.SetMarkerColor(1+i)
  h.SetFillColor(0)
  lh.append(copy.deepcopy(h))
rfile.Close()
c=ROOT.TCanvas("c","c",800,600)
leg=ROOT.TLegend(0.7,0.7,0.9,0.9)
c.cd()
lh[0].Draw("hist")
leg.AddEntry(lh[0],ltname[0],"l")    
lh[1].Draw("hist same")        
leg.AddEntry(lh[1],ltname[1],"l")    
lh[2].Draw("hist same")        
leg.AddEntry(lh[2],ltname[2],"l")    
leg.Draw("same")
c.SetLogy()
c.SaveAs("se_test_nohiggs.png")


