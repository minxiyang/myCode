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
from ROOT import TUnfold
def Addhist(histlist):
        tempHist=histlist[0]
        for i in range(1,3):
                tempHist.Add(histlist[i])
        return tempHist
def Addstack(Stacklist):
        tempStack=Stacklist[0]
        for i in range(1,3):
                tempStack.Add(Stacklist[i])
        return tempStack 
def Stacks(processes,lumi,plot,zScale):
        stacks=[]
        for i in range(3):
                stacks.append(TheStack(processes[i],lumi[i],plot,zScale[i]))
        return stacks

datamubb=[]
databb_all=[Process(Data2016, normalized=True),Process(Data, normalized=True),Process(Data2018, normalized=True)]
plot_mu_bb = getPlot("massPlotBB")
plot_mu_be = getPlot("massPlotBE")
lumi_mu = [36.3*1000,42.135*1000,61.608*1000]
zScaleFac_mu = [zScale2016["muons"],zScale["muons"],zScale2018["muons"]]
for i in range(3):
	datamubb.append(databb_all[i].loadHistogram(plot_mu_bb,lumi_mu[i],zScaleFac_mu[i]))
hmuBB=Addhist(datamubb)
#c1=ROOT.TCanvas("c1","c1",800,800)
#c1.SetLogx()
#c1.SetLogy()
hmuBB.SetFillColor(0)
#hmuBB.Draw("hist")
#c1.Print("lepFlavor/unfoldTest.pdf")
datamube=[]
databe_all=[Process(Data2016, normalized=True),Process(Data, normalized=True),Process(Data2018, normalized=True)]
for i in range(3):
        datamube.append(databe_all[i].loadHistogram(plot_mu_be,lumi_mu[i],zScaleFac_mu[i]))
hmuBE=Addhist(datamube)
#c1=ROOT.TCanvas("c1","c1",800,800)
#c1.SetLogx()
#c1.SetLogy()
hmuBE.SetFillColor(0)
#hmuBB.Draw("hist")
#c1.Print("lepFlavor/unfoldTest.pdf")
f=ROOT.TFile("unfoldingData.root","RECREATE")
hmuBE.Write()
hmuBB.Write()
f.Close()
eventCounts_mu_bb = totalNumberOfGeneratedEvents(path,plot_mu_bb.muon)
negWeights_mu_bb = negWeightFractions(path,plot_mu_bb.muon)
processes_mu2016_bb=[Process(getattr(Backgrounds2016,"DrellYan"),eventCounts_mu_bb,negWeights_mu_bb)]
processes_mu2017_bb=[Process(getattr(Backgrounds,"DrellYan"),eventCounts_mu_bb,negWeights_mu_bb)]
processes_mu2018_bb=[Process(getattr(Backgrounds2018,"DrellYan"),eventCounts_mu_bb,negWeights_mu_bb)]
processes_bb=[processes_mu2016_bb,processes_mu2017_bb,processes_mu2018_bb]
stackmu_bb = Stacks(processes_bb,lumi_mu,plot_mu_bb,zScaleFac_mu)
hmuBB_mc=stackmu_bb[0].theHistogram
hmuBB_mc.Add(stackmu_bb[1].theHistogram)
hmuBB_mc.Add(stackmu_bb[2].theHistogram)
eventCounts_mu_be = totalNumberOfGeneratedEvents(path,plot_mu_be.muon)
negWeights_mu_be = negWeightFractions(path,plot_mu_be.muon)
processes_mu2016_be=[Process(getattr(Backgrounds2016,"DrellYan"),eventCounts_mu_be,negWeights_mu_be)]
processes_mu2017_be=[Process(getattr(Backgrounds,"DrellYan"),eventCounts_mu_be,negWeights_mu_be)]
processes_mu2018_be=[Process(getattr(Backgrounds2018,"DrellYan"),eventCounts_mu_be,negWeights_mu_be)]
processes_be=[processes_mu2016_be,processes_mu2017_be,processes_mu2018_be]
stackmu_be = Stacks(processes_be,lumi_mu,plot_mu_be,zScaleFac_mu)
hmuBE_mc=stackmu_be[0].theHistogram
hmuBE_mc.Add(stackmu_be[1].theHistogram)
hmuBE_mc.Add(stackmu_be[2].theHistogram)
f2=ROOT.TFile("unfoldingMC.root","RECREATE")
hmuBE_mc.Write()
hmuBB_mc.Write()
f2.Close()





