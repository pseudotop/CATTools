import os
import ROOT,copy
ROOT.gROOT.SetBatch(True)

def hist_maker(name, title, bin_set, x_name, y_name, tr, br, cut):
    hist = ROOT.TH1F(name, title, bin_set[0], bin_set[1], bin_set[2])
    #hist.GetXaxis().SetTitle(x_name)
    #hist.GetYaxis().SetTitle(y_name)
    #hist.SetLineColor(color)
    #hist.Sumw2()
    hist.SetStats(0)
    tr.Project(name, br, cut)
    return hist
def text_maker(size, align, x, y, text):
    t = ROOT.TLatex()
    #t.SetTextFont(42)
    t.SetTextSize(size)
    t.SetTextAlign(align)
    t.DrawLatexNDC(x, y, text)

datalumi = 225.6
currentdir = os.getcwd()
saveddir = '/PLOTS'
if not os.path.isdir(currentdir+saveddir):
    os.mkdir(currentdir+saveddir)
import sys
print sys.argv
resultdir = sys.argv[1]
filelist1 = os.listdir(resultdir)
filelist2 = []
for i in filelist1:
    filelist2.append(i.split(".")[0])
filenames = [0,0,0,0,0,0,0,0,0]

date = "20151013"
#date = ''
for i in filelist2:#replace 'filelist2' replace to 'filelist1'
    if (('DYJets' in i) and ( date in i)):filenames[0]=i
    if (('TTJets' in i) and ( date in i)):filenames[1]=i
    if (('WZ' in i) and ( date in i)):filenames[2]=i
    if (('WW' in i) and ( date in i)):filenames[3]=i
    if (('ZZ' in i) and ( date in i)):filenames[4]=i
    if (('GluGlu' in i) and ( date in i)):filenames[5]=i
    if (('VBF' in i) and ( date in i)):filenames[6]=i
    if (('Double' in i) and ( date in i)):filenames[7]=i
    if (('Single' in i) and ( date in i)):filenames[8]=i
    
'''
mcfilelist = {'mc_DYJets_merged':6025.2 ,
              'mc_TTJets_mad_merged':831.8,
              'mc_ZZ_merged':31.8,
              'mc_WW_merged':65.9,
              'mc_WZ_merged':118.7}
rdfilelist = [#'DoubleMuon',
              'data_MuonEG_merged']
'''
mcfilelist = {filenames[0]:6025.2,
              filenames[1]:831.8,
              filenames[2]:118.7,
              filenames[3]:65.9,
              filenames[4]:31.8,
              filenames[5]:1,
              filenames[6]:1
             }
rdfilelist = [
              #filenames[7],
              filenames[8]
             ]
mcfilelist_order = sorted(mcfilelist.keys(), key=lambda key_value: key_value[0])
print mcfilelist
re_mcfilelist = [filenames[4],filenames[3],filenames[2],filenames[1],filenames[0],filenames[5],filenames[6]]
## Jet Category cut
jet0_tight = "(jetcat_f_hier == 1)"
jet0_loose = "(jetcat_f_hier == 2)"
jet1_tight = "(jetcat_f_hier == 3)"
jet1_loose = "(jetcat_f_hier == 4)"
jet2_vbf = "(jetcat_f_hier == 5 || jetcat_f_hier == 7)"
jet2_ggf = "(jetcat_f_hier == 6)"
jet2_loose = "(jetcat_f_hier == 8)"

jetcat = ["0jet_tight","0jet_loose","1jet_tight","1jet_loose","2jet_VBF_tight","2jet_ggF_tight","2jet_loose"]
jetcat_cut = [jet0_tight, jet0_loose, jet1_tight, jet1_loose, jet2_vbf, jet2_ggf, jet2_loose]

##jetcat, in case 0,1jet
BB = "(jetcat_GC == 2)"
BO = "(jetcat_GC == 11)"
BE = "(jetcat_GC == 101)"
OO = "(jetcat_GC == 20)"
OE = "(jetcat_GC == 110)"
EE = "(jetcat_GC == 200)"

jetcat_GC = ["BB","BO","BE","OO","OE","EE"]
jetcat_GC_cut = [BB,BO,BE,OO,OE,EE]

## initial cut
init_cuts = ["(step == 3 && isTight)","(step == 3 && isMedium)","(step == 4 && isTight)","(step == 4 && isMedium)"]
whatiscut = ["_tight3","_medium3","_tight4","_medium4"]

## style
from ROOT import kPink,kOrange,kSpring,kCyan,kAzure,kMagenta
cols = [kPink,kOrange,kSpring,kCyan,kAzure-3,kMagenta,kOrange-3,kAzure-6]

os.chdir(resultdir)
for ps,init_cut in enumerate(init_cuts):
    for plot in range(4):
        plotvar = "diMu_m"
        title = plotvar
        tcut = init_cut
        bin_set = [250, 0, 250]
        x_name = "a.u."
        y_name = "M [GeV]"
        '''
        if plot == 1:
          title = plotvar+"_"+jetcat[4]
          tcut = init_cut+"*"+jetcat_cut[4]
        if plot == 2:
          title = plotvar+"_"+jetcat[5]
          tcut = init_cut+"*"+jetcat_cut[5]
        if plot == 3:
          title = plotvar+"_"+jetcat[6]
          tcut = init_cut+"*"+jetcat_cut[6]
        '''
        hs = ROOT.THStack(plotvar,plotvar)
        h_rd = ROOT.TH1F(plotvar, plotvar, bin_set[0], bin_set[1], bin_set[2])
        h_rd.SetMarkerStyle(20)
        h_rd.SetMarkerSize(0.6)
        leg = ROOT.TLegend(0.6,0.6,0.9,0.9)
        leg.AddEntry(h_rd,"Data","p")
        logscale = False
        
        for num,i in enumerate(re_mcfilelist):
            rootfilename = i+".root"
            print rootfilename
            samplename = i.strip().split("_")[0]
            tt = ROOT.TFile(rootfilename)
            tree = tt.h2mu.Get("tree")
            """
            # untill better way to get nentries
            tempdraw = plotvar +" >> temp" +samplename
            tree.Draw(tempdraw)
            temphist = ROOT.gDirectory.Get("temp" +samplename)
            # untill better way to get nentries
            scale = mcfilelist[i]*datalumi / temphist.GetEntries()
            """
            scale = mcfilelist[i]*datalumi / tree.GetEntries()
            print 'lumi = %g '%mcfilelist[i], "scale = %g"%scale
            histo = copy.deepcopy(hist_maker(samplename, title, bin_set, x_name, y_name, tree, plotvar, tcut))
            print num
            histo.SetFillColor(cols[num])
            histo.Scale(scale)
            if histo.GetMaximum()>2000:
                logscale = True
            hs.Add(histo)
            leg.AddEntry(histo,samplename+" : %.1f"%mcfilelist[i],"f")
            tt.Close()
        for i in rdfilelist:
            if not 'Single' in i:
                continue
            rootfilename = i+'.root'
            print rootfilename
            samplename = 'singlemu'
            tt = ROOT.TFile(rootfilename)
            tree = tt.h2mu.Get("tree")
            histo = copy.deepcopy(hist_maker(samplename, title, bin_set, x_name, y_name, tree, plotvar, tcut))
            print histo.GetEntries()
            if histo.GetMaximum()>2000:
                logscale = True
            h_rd.Add(histo)
            tt.Close()
            
        canvas = ROOT.TCanvas(title,title)
        hs.Draw()
        text_maker(0.06, 12, 0.02, 0.95, "#font[32]{CMS Preliminary}")
        text_maker(0.04, 32, 0.98, 0.95, "#font[12]{%.1f pb^{-1}, #sqrt{s}=13 TeV, 25 ns}"%(datalumi))
        text_maker(0.05, 11, 0.14, 0.8,"#font[82]{Dimuon mass}")
        hs.SetTitle()
        hs.GetXaxis().SetTitle('M_{ll} [GeV]')
        hs.GetYaxis().SetTitle('number of entries /1GeV')
        h_rd.Draw("psame")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw("same")
        #if logscale:
        #    canvas.SetLogy()
        hs.SetMinimum(0.1)
        canvas.SetLogy()
        canvas.Update()
        canvas.SaveAs(currentdir+saveddir+"/"+title+whatiscut[ps]+"_%g"%datalumi+".root")
        canvas.SaveAs(currentdir+saveddir+"/"+title+whatiscut[ps]+"_%g"%datalumi+".png")
        canvas.SetLogy(0)
        hs.SetMaximum(6000)
        hs.SetMinimum(0)
        canvas.Update()
        canvas.SaveAs(currentdir+saveddir+"/"+title+whatiscut[ps]+'nolog'+"_%g"%datalumi+".root")
        canvas.SaveAs(currentdir+saveddir+"/"+title+whatiscut[ps]+'nolog'+"_%g"%datalumi+".png")

        del leg
'''
    for jet01 in range(4):
      for gc in range(6):
        title = plotvar+"_"+jetcat[jet01]+"_"+jetcat_GC[gc]
        tcut = init_cut+"*"+jetcat_cut[jet01]+"*"+jetcat_GC_cut[gc]
        hs = ROOT.THStack(plotvar,plotvar)
        h_rd = ROOT.TH1F(plotvar, plotvar, bin_set[0], bin_set[1], bin_set[2])
        h_rd.SetMarkerStyle(20)
        leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
        leg.AddEntry(h_rd,"Data","p")
        logscale=False    

        j=1
        for i in mcfilelist:
            j=j+1
            rootfilename = i+".root"
            print rootfilename
            samplename = i.strip().split("_")[0]
            tt = ROOT.TFile(rootfilename)
            tree = tt.h2mu.Get("tree")
            # untill better way to get nentries
            tempdraw = plotvar +" >> temp" +samplename
            tree.Draw(tempdraw)
            temphist = ROOT.gDirectory.Get("temp" +samplename)
            # untill better way to get nentries
            scale = mcfilelist[i]*datalumi / temphist.GetEntries()
            print mcfilelist[i]
            histo = copy.deepcopy(hist_maker(samplename, title, bin_set, x_name, y_name, tree, plotvar, tcut))
            histo.SetFillColor(j)
            histo.Scale(scale)
            if histo.GetMaximum()>2000:
                logscale = True
            hs.Add(histo)
            leg.AddEntry(histo,samplename,"f")
            tt.Close()

        for i in rdfilelist:
            rootfilename = i+".root"
            print rootfilename
            samplename = i.strip().split("_")[0]
            tt = ROOT.TFile(rootfilename)
            tree = tt.h2mu.Get("tree")
            histo = copy.deepcopy(hist_maker(samplename, title, bin_set, x_name, y_name, tree, plotvar, tcut))
            if histo.GetMaximum()>2000:
                logscale = True
            h_rd.Add(histo)
            tt.Close()        

        canvas = ROOT.TCanvas(title,title)
        hs.Draw()
        h_rd.Draw("psame")
        leg.Draw("same")
        if logscale:
            canvas.SetLogy()
        canvas.SaveAs(currentdir+saveddir+"/"+title+whatiscut[ps]+".root")
        canvas.SaveAs(currentdir+saveddir+"/"+title+whatiscut[ps]+".png")

        del leg
'''
#dilepmass = ROOT.gDirectory.Get("dilepmass")
