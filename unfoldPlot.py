import argparse	
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath, gROOT
import ratios
from setTDRStyle import setTDRStyle
gROOT.SetBatch(True)
from helpers import *
from defs import getPlot, Backgrounds, Backgrounds2016, Backgrounds2018, Signals, Signals2016, Signals2016ADD, SignalsADD, Signals2018ADD, Signals2018, Data, Data2016, Data2018, path, plotList, zScale, zScale2016, zScale2018
import math
import os
from copy import copy


def plotDataMC(datahist,mchist,usedata, label1, label2,name,filename):
	

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	if usedata==True:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
                ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
                setTDRStyle()
                plotPad.UseCurrentStyle()
                ratioPad.UseCurrentStyle()
                plotPad.Draw("hist")
                ratioPad.Draw("hist")
                plotPad.cd()
        else:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
                setTDRStyle()
                plotPad.UseCurrentStyle()
                plotPad.Draw()
                plotPad.cd()	
	colors = createMyColors()		
	
	legend = TLegend(0.55, 0.6, 0.925, 0.925)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	legend.SetTextFont(42)
	legendEta = TLegend(0.45, 0.75, 0.925, 0.925)
	legendEta.SetFillStyle(0)
	legendEta.SetBorderSize(0)
	legendEta.SetTextFont(42)
	legendEta.SetNColumns(2)
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.06)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.045)
	latexCMSExtra.SetNDC(True)	
	legendHists = []
	legendHistData = ROOT.TH1F()
	category = ROOT.TLatex()
	category.SetNDC(True)
	category.SetTextSize(0.04)
	if usedata==True:	
		legend.AddEntry(legendHistData,label1,"pe")	
		legendEta.AddEntry(legendHistData,label1,"pe")	

	#process.label = process.label.replace("#mu^{+}#mu^{-}","e^{+^{*}}e^{-}")
	temphist = ROOT.TH1F()
	temphist.SetFillColor(3)
	legendHists.append(temphist.Clone)
	legend.AddEntry(temphist,label2,"f")
	#legendEta.AddEntry(temphist,process.label,"f")
	
	# Modify plot pad information	
	nEvents=-1

	ROOT.gStyle.SetOptStat(0)
	
	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.045)
	intlumi.SetNDC(True)
	intlumi2 = ROOT.TLatex()
	intlumi2.SetTextAlign(12)
	intlumi2.SetTextSize(0.07)
	intlumi2.SetNDC(True)
	scalelabel = ROOT.TLatex()
	scalelabel.SetTextAlign(12)
	scalelabel.SetTextSize(0.03)
	scalelabel.SetNDC(True)
	metDiffLabel = ROOT.TLatex()
	metDiffLabel.SetTextAlign(12)
	metDiffLabel.SetTextSize(0.03)
	metDiffLabel.SetNDC(True)
	chi2Label = ROOT.TLatex()
	chi2Label.SetTextAlign(12)
	chi2Label.SetTextSize(0.03)
	chi2Label.SetNDC(True)
	hCanvas.SetLogy()


	# Luminosity information	
	plotPad.cd()
	plotPad.SetLogy(0)
	plotPad.SetLogy()
	if usedata==True:
		yMax = datahist.GetBinContent(datahist.GetMaximumBin())*1000
		yMin = 0.00000001
		xMax = datahist.GetXaxis().GetXmax()
		xMin = datahist.GetXaxis().GetXmin()
	else:	
		yMax = mchist.GetBinContent(datahist.GetMaximumBin())
		yMin = 0.00000001
		xMax = mchist.GetXaxis().GetXmax()
		xMin = mchist.GetXaxis().GetXmin()	
		yMax = yMax*10000

	plotPad.DrawFrame(xMin,yMin,xMax,yMax,"; GeV ;fb/GeV")
	
	# Draw signal information
	
	# Draw background from stack
	mchist.SetFillColor(3)
	mchist.Draw("samehist")		

	# Draw data
	datahist.SetMinimum(0.0001)
	if usedata==True:
		datahist.SetMarkerStyle(8)
		datahist.Draw("samepehist")	

	# Draw legend
	legend.Draw()
	plotPad.SetLogx()
	latex.DrawLatex(0.95,0.96,"13 TeV")
	yLabelPos = 0.85
	cmsExtra = "Preliminary"
	if not usedata==True:
		cmsExtra = "#splitline{Preliminary}{Simulation}"
		yLabelPos = 0.82	
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	category.DrawLatex(0.3,0.7,name)
	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	#~ print datahist.Integral()
	if usedata==True:
		try:
			ratioPad.cd()
			ratioPad.SetLogx()
		except AttributeError:
			print ("Plot fails. Look up in errs/failedPlots.txt")
			outFile =open("errs/failedPlots.txt","a")
			outFile.write('%s\n'%plot.filename%("_"+run.label+"_"+dilepton))
			outFile.close()
			#plot.cuts=baseCut
			return 1
		ratioGraphs =  ratios.RatioGraph(datahist,mchist, xMin=xMin, xMax=xMax,title="After/Before-1",yMin=-1.0,yMax=1.0,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=10000000000000,labelSize=0.125,pull=True)
		ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
					

	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	if usedata==True:

		ratioPad.RedrawAxis()
	if not os.path.exists("plots"):
		os.makedirs("plots")	
	hCanvas.Print("plots/%s.pdf"%filename)

					

						
f=ROOT.TFile.Open("RooUnfold/ClosureTest.root")
genBB_17_mu=f.Get("genBB2017_mu")
recBB_17_mu=f.Get("recBB2017_mu")
unfoldBB_17_mu=f.Get("BB2017mu_invert")
genBE_17_mu=f.Get("genBE2017_mu")
recBE_17_mu=f.Get("recBE2017_mu")
unfoldBE_17_mu=f.Get("BE2017mu_invert")
genBB_16_mu=f.Get("genBB2016_mu")
recBB_16_mu=f.Get("recBB2016_mu")
unfoldBB_16_mu=f.Get("BB2016mu_invert")
genBE_16_mu=f.Get("genBE2016_mu")
recBE_16_mu=f.Get("recBE2016_mu")
unfoldBE_16_mu=f.Get("BE2016mu_invert")
genBB_18_mu=f.Get("genBB2018_mu")
recBB_18_mu=f.Get("recBB2018_mu")
unfoldBB_18_mu=f.Get("BB2018mu_invert")
genBE_18_mu=f.Get("genBE2018_mu")
recBE_18_mu=f.Get("recBE2018_mu")
unfoldBE_18_mu=f.Get("BE2018mu_invert")
genBB_17_e=f.Get("genBB2017_e")
recBB_17_e=f.Get("recBB2017_e")
unfoldBB_17_e=f.Get("BB2017el_invert")
genBE_17_e=f.Get("genBE2017_e")
recBE_17_e=f.Get("recBE2017_e")
unfoldBE_17_e=f.Get("BE2017el_invert")
genBB_16_e=f.Get("genBB2016_e")
recBB_16_e=f.Get("recBB2016_e")
unfoldBB_16_e=f.Get("BB2016el_invert")
genBE_16_e=f.Get("genBE2016_e")
recBE_16_e=f.Get("recBE2016_e")
unfoldBE_16_e=f.Get("BE2016el_invert")
genBB_18_e=f.Get("genBB2018_e")
recBB_18_e=f.Get("recBB2018_e")
unfoldBB_18_e=f.Get("BB2018el_invert")
genBE_18_e=f.Get("genBE2018_e")
recBE_18_e=f.Get("recBE2018_e")
unfoldBE_18_e=f.Get("BE2018el_invert")




plotDataMC(unfoldBB_17_mu,genBB_17_mu,True,"Unfolded","Gen mass","2017 BB Dimuon","gen_closure_BB_17_mu" )
plotDataMC(unfoldBB_17_mu,genBB_17_mu,True,"Unfolded","Reco mass","2017 BB Dimuon","rec_closure_BB_17_mu" )
plotDataMC(unfoldBE_17_mu,genBE_17_mu,True,"Unfolded","Gen mass","2017 BE Dimuon","gen_closure_BE_17_mu" )
plotDataMC(unfoldBE_17_mu,genBE_17_mu,True,"Unfolded","Reco mass","2017 BE Dimuon","rec_closure_BE_17_mu" )


plotDataMC(unfoldBB_17_e,genBB_17_e,True,"Unfolded","Gen mass","2017 BB Dielectron","gen_closure_BB_17_el" )
plotDataMC(unfoldBB_17_e,genBB_17_e,True,"Unfolded","Reco mass","2017 BB Dielectron","rec_closure_BB_17_el" )
plotDataMC(unfoldBE_17_e,genBE_17_e,True,"Unfolded","Gen mass","2017 BE Dielectron","gen_closure_BE_17_el" )
plotDataMC(unfoldBE_17_e,genBE_17_e,True,"Unfolded","Reco mass","2017 BE Dielectron","rec_closure_BE_17_el" )

plotDataMC(unfoldBB_16_mu,genBB_16_mu,True,"Unfolded","Gen mass","2016 BB Dimuon","gen_closure_BB_16_mu" )
plotDataMC(unfoldBB_16_mu,genBB_16_mu,True,"Unfolded","Reco mass","2016 BB Dimuon","rec_closure_BB_16_mu" )
plotDataMC(unfoldBE_16_mu,genBE_16_mu,True,"Unfolded","Gen mass","2016 BE Dimuon","gen_closure_BE_16_mu" )
plotDataMC(unfoldBE_16_mu,genBE_16_mu,True,"Unfolded","Reco mass","2016 BE Dimuon","rec_closure_BE_16_mu" )


plotDataMC(unfoldBB_16_e,genBB_16_e,True,"Unfolded","Gen mass","2016 BB Dielectron","gen_closure_BB_16_el" )
plotDataMC(unfoldBB_16_e,genBB_16_e,True,"Unfolded","Reco mass","2016 BB Dielectron","rec_closure_BB_16_el" )
plotDataMC(unfoldBE_16_e,genBE_16_e,True,"Unfolded","Gen mass","2016 BE Dielectron","gen_closure_BE_16_el" )
plotDataMC(unfoldBE_16_e,genBE_16_e,True,"Unfolded","Reco mass","2016 BE Dielectron","rec_closure_BE_16_el" )

plotDataMC(unfoldBB_18_mu,genBB_18_mu,True,"Unfolded","Gen mass","2018 BB Dimuon","gen_closure_BB_18_mu" )
plotDataMC(unfoldBB_18_mu,genBB_18_mu,True,"Unfolded","Reco mass","2018 BB Dimuon","rec_closure_BB_18_mu" )
plotDataMC(unfoldBE_18_mu,genBE_18_mu,True,"Unfolded","Gen mass","2018 BE Dimuon","gen_closure_BE_18_mu" )
plotDataMC(unfoldBE_18_mu,genBE_18_mu,True,"Unfolded","Reco mass","2018 BE Dimuon","rec_closure_BE_18_mu" )


plotDataMC(unfoldBB_18_e,genBB_18_e,True,"Unfolded","Gen mass","2018 BB Dielectron","gen_closure_BB_18_el" )
plotDataMC(unfoldBB_18_e,genBB_18_e,True,"Unfolded","Reco mass","2018 BB Dielectron","rec_closure_BB_18_el" )
plotDataMC(unfoldBE_18_e,genBE_18_e,True,"Unfolded","Gen mass","2018 BE Dielectron","gen_closure_BE_18_el" )
plotDataMC(unfoldBE_18_e,genBE_18_e,True,"Unfolded","Reco mass","2018 BE Dielectron","rec_closure_BE_18_el" )


