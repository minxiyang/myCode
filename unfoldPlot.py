import argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath, gROOT, TGaxis
import ratios
from setTDRStyle import setTDRStyle
gROOT.SetBatch(True)
from helpers import *
from defs import getPlot, Backgrounds, Backgrounds2016, Backgrounds2018, Signals, Signals2016, Signals2016ADD, Data, Data2016, Data2018, path, plotList, zScale, zScale2016, zScale2018
import math
import os
from copy import copy
import numpy as np
import root_numpy
from copy import deepcopy



def plot(hist, inhist, name):
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
        ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
        setTDRStyle()
        plotPad.UseCurrentStyle()
        ratioPad.UseCurrentStyle()
        plotPad.Draw()
        ratioPad.Draw()
        plotPad.cd()
	colors = createMyColors()
	legend = TLegend(0.55, 0.75, 0.925, 0.925)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	legend.SetTextFont(42)
	legend.AddEntry(hist,"Data","pe")
        legend.AddEntry(inhist,"MC","l")
	ROOT.gStyle.SetOptStat(0)
	xMin = 200
        xMax = 3490
        yMin = 1e-3
        yMax = 1e4
	vh = plotPad.DrawFrame(xMin,yMin,xMax,yMax,"; %s ; %s" %("m(l^{+}l^{-}) [GeV]","Events / GeV"))
	vh.GetXaxis().SetMoreLogLabels()
	hist.SetLineColor(ROOT.kBlue-3)
        inhist.SetLineColor(ROOT.kRed-3)
        hist.SetMarkerStyle(6)
        inhist.SetMarkerStyle(6)
        hist.SetFillStyle(0)
        inhist.SetFillStyle(0)
	hist.Draw("same histe ")
	inhist.Draw("same histe ")
	legend.Draw()
	yLabelPos = 0.95
	dataLabel = "Full Run 2 %s" %name
	latexCMS = ROOT.TLatex()
        latexCMS.SetTextFont(61)
        latexCMS.SetTextSize(0.06)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        latexCMSExtra.SetTextFont(52)
        latexCMSExtra.SetTextSize(0.045)
        latexCMSExtra.SetNDC(True)
	latexCMSExtra.DrawLatex(0.29,0.69,"%s"%(dataLabel))
	ROOT.gPad.RedrawAxis()
        plotPad.RedrawAxis()
	plotPad.SetLogy()
        plotPad.SetLogx()
	hCanvas.Update()
	val=inhist.GetBinContent(13)
	print val
	ratioGraphs = ROOT.TGraphAsymmErrors(hist.GetSize()-2)
	ratioPad.cd()
	ratioPad.SetLogx()
	for i in range(1, hist.GetSize()-1):
		xval = hist.GetBinCenter(i)
                if hist.GetBinContent(i) == 0: continue
                if hist.GetBinContent(i) == 0: continue
                yval = hist.GetBinContent(i)*1.0/inhist.GetBinContent(i)
                ratioGraphs.SetPoint(i, xval, yval)
	nBinsX = 20
	nBinsY = 10
	hAxis = ROOT.TH2F("hAxis", "", nBinsX, xMin, xMax, nBinsY, 0.5, 2.5)
	hAxis.Draw("AXIS")
	hAxis.GetYaxis().SetNdivisions(408)
        hAxis.SetTitleOffset(0.4, "Y")
        hAxis.SetTitleSize(0.09, "Y")
        hAxis.SetTitleSize(0.06, "X")
        #hAxis.SetYTitle("R_{#mu#mu/ee}")
        hAxis.SetXTitle("m(l^{+}l^{-}) [GeV]")
        hAxis.GetXaxis().SetLabelSize(0.048)
        hAxis.GetYaxis().SetLabelSize(0.048)
        hAxis.GetXaxis().SetMoreLogLabels()
        oneLine = ROOT.TLine(xMin, 1.0, xMax, 1.0)
        oneLine.SetLineStyle(2)
        oneLine.Draw()
        ratioGraphs.SetFillColor(ROOT.kBlue-3)
        ratioGraphs.SetMarkerColor(ROOT.kBlue-3)
        ratioGraphs.GetXaxis().SetLabelSize(0.0)
        ratioGraphs.SetFillStyle(3002)
        ratioGraphs.Draw("same p")
	#ratioData.SetMarkerColor(ROOT.kViolet)
        #ratioData.Draw("same p")
	rlegend = TLegend(0.2, 0.65, 0.5, 0.925)
        rlegend.SetFillStyle(0)
        rlegend.SetBorderSize(1)
        rlegend.SetTextFont(42)
        rlegend.AddEntry(ratioGraphs, "data/mc in MC inclusive", "l")
        rlegend.Draw("same")
	ratioPad.Update()
	ROOT.gPad.RedrawAxis()
        plotPad.RedrawAxis()
	hCanvas.Print("lepFlavor/%s.pdf" %name)

	

f1=ROOT.TFile.Open("RooUnfold/unfoldSample.root")

invertBB=f1.Get("UnfoldedBB")
invertBE=f1.Get("UnfoldedBE")
bayesBB=f1.Get("bayesBB")
bayesBE=f1.Get("bayesBE")
invertBBMC=f1.Get("UnfoldedBB_mc")
invertBEMC=f1.Get("UnfoldedBE_mc")
bayesBBMC=f1.Get("bayesBBMC")
bayesBEMC=f1.Get("bayesBEMC")
hmuBE=f1.Get("hist_f26f74ed27824519bcad66a6f539b3e5")
hmuBB=f1.Get("hist_1405a58d67164a8bb28859df616bad3c")
hmuBEMC=f1.Get("hist_bab6670dc2a946a7af6bdfbc761f87c5")
hmuBBMC=f1.Get("hist_35313753f6e34206bd2294885ac1096f")
plot(hmuBB,hmuBBMC,"BB")
plot(hmuBE,hmuBEMC,"BE")
plot(invertBB,invertBBMC,"invert_BB")
plot(invertBE,invertBEMC,"invert_BE")
plot(bayesBB,bayesBBMC,"bayes_BB")
plot(bayesBE,bayesBEMC,"_bayesBE")

