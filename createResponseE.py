import ROOT
import os
import numpy
import subprocess
import root_numpy
import math
import copy
from readCrab import getBkg
from crossSection import DYCrossSection

path="/depot/cms/users/minxi/crab"
pathList=getBkg(path,"electrons")
ROOT.gStyle.SetOptStat(0)

#print pathList
pathList2016={}
pathList2017={}
pathList2018={}
eventNum2016={"50to120":2498789,"120to200":100000,"200to400":99200,"200to400":100000,"400to800":100000,"800to1400":100000,"1400to2300":100000,"2300to3500":100000,"3500to4500":100000,"4500to6000":100000,"6000toInf":100000}
eventNum2017={"50to120":2965146,"120to200":100000,"200to400":100000,"200to400":100000,"400to800":100000,"800to1400":100000,"1400to2300":100000,"2300to3500":100000,"3500to4500":100000,"4500to6000":100000,"6000toInf":100000}
eventNum2018={"50to120":2940000,"120to200":100000,"200to400":100000,"200to400":100000,"400to800":100000,"800to1400":100000,"1400to2300":100000,"2300to3500":100000,"3500to4500":100000,"4500to6000":100000,"6000toInf":98000}
for path in pathList:
        if path.find("2016")!=-1 and path.find("Inclusive")==-1:
                for key in DYCrossSection.keys():
                        if path.find(key)!=-1:
                                pathList2016[path]= DYCrossSection[key]
        elif path.find("2018")!=-1 and path.find("Inclusive")==-1:
                for key in DYCrossSection.keys():
                        if path.find(key)!=-1:
                                pathList2018[path]= DYCrossSection[key]
        elif path.find("Inclusive")==-1:
                for key in DYCrossSection.keys():
                        if path.find(key)!=-1:
				pathList2017[path]= DYCrossSection[key]

bng=[50, 120,150,200,300,400,500,690,900,1250,1610, 2000, 4000, 6070]                               
bng=numpy.asarray(bng,dtype=numpy.float64)
reM2016BB=ROOT.TH2D("reM2016BB_e","Response matrix for 2016 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2016BE=ROOT.TH2D("reM2016BE_e","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2017BB=ROOT.TH2D("reM2017BB_e","Response matrix for 2017 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2017BE=ROOT.TH2D("reM2017BE_e","Response matrix for 2017 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2018BB=ROOT.TH2D("reM2018BB_e","Response matrix for 2018 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2018BE=ROOT.TH2D("reM2018BE_e","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2016BBn=ROOT.TH2D("reM2016BBn_e","Response matrix for 2016 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2016BEn=ROOT.TH2D("reM2016BEn_e","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2017BBn=ROOT.TH2D("reM2017BBn_e","Response matrix for 2017 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2017BEn=ROOT.TH2D("reM2017BEn_e","Response matrix for 2017 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2018BBn=ROOT.TH2D("reM2018BBn_e","Response matrix for 2018 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2018BEn=ROOT.TH2D("reM2018BEn_e","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
genBB2016=ROOT.TH1D("genBB2016_e","MC BB",20000,0,20000)
recBB2016=ROOT.TH1D("recBB2016_e","MC BB",20000,0,20000)
genBE2016=ROOT.TH1D("genBE2016_e","MC BB",20000,0,20000)
recBE2016=ROOT.TH1D("recBE2016_e","MC BE",20000,0,20000)
genBB2017=ROOT.TH1D("genBB2017_e","MC BB",20000,0,20000)
recBB2017=ROOT.TH1D("recBB2017_e","MC BB",20000,0,20000)
genBE2017=ROOT.TH1D("genBE2017_e","MC BB",20000,0,20000)
recBE2017=ROOT.TH1D("recBE2017_e","MC BE",20000,0,20000)
genBB2018=ROOT.TH1D("genBB2018_e","MC BB",20000,0,20000)
recBB2018=ROOT.TH1D("recBB2018_e","MC BB",20000,0,20000)
genBE2018=ROOT.TH1D("genBE2018_e","MC BB",20000,0,20000)
recBE2018=ROOT.TH1D("recBE2018_e","MC BE",20000,0,20000)
#print pathList2018
for path in pathList2018.keys():
	f2018=ROOT.TFile.Open(path)
	num=100000
	for key in eventNum2018.keys():
		if path.find(key)!=-1:
			num=eventNum2018[key]
	temphist=f2018.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_gen_bb")
	temphist.Scale(pathList2018[path]/num)
	genBB2018.Add(temphist,1.)
	temphist=f2018.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_bb")
        temphist.Scale(pathList2018[path]/num)
        recBB2018.Add(temphist,1.)
	temphist=f2018.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_gen_be")
        temphist.Scale(pathList2018[path]/num)
        genBE2018.Add(temphist,1.)
        temphist=f2018.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_be")
        temphist.Scale(pathList2018[path]/num)
        recBE2018.Add(temphist,1.)
	temphist=f2018.Get("ElectronSelectionElectronsAllSignsHistos/DielectronResponse_bb")
        temphist.Scale(pathList2018[path]/num)
	reM2018BB.Add(temphist,1.)
	temphist=f2018.Get("ElectronSelectionElectronsAllSignsHistos/DielectronResponse_be")
        temphist.Scale(pathList2018[path]/num)
        reM2018BE.Add(temphist,1.)

for path in pathList2017.keys():
        f2017=ROOT.TFile.Open(path)
        num=100000
        for key in eventNum2017.keys():
                if path.find(key)!=-1:
                        num=eventNum2017[key]
        temphist=f2017.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_gen_bb")
        temphist.Scale(pathList2017[path]/num)
        genBB2017.Add(temphist,1.)
        temphist=f2017.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_bb")
        temphist.Scale(pathList2017[path]/num)
        recBB2017.Add(temphist,1.)
        temphist=f2017.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_gen_be")
        temphist.Scale(pathList2017[path]/num)
        genBE2017.Add(temphist,1.)
        temphist=f2017.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_be")
        temphist.Scale(pathList2017[path]/num)
        recBE2017.Add(temphist,1.)
        temphist=f2017.Get("ElectronSelectionElectronsAllSignsHistos/DielectronResponse_bb")
        temphist.Scale(pathList2017[path]/num)
        reM2017BB.Add(temphist,1.)
        temphist=f2017.Get("ElectronSelectionElectronsAllSignsHistos/DielectronResponse_be")
        temphist.Scale(pathList2017[path]/num)
        reM2017BE.Add(temphist,1.)

for path in pathList2016.keys():
        f2016=ROOT.TFile.Open(path)
        num=100000
        for key in eventNum2016.keys():
                if path.find(key)!=-1:
                        num=eventNum2016[key]
        temphist=f2016.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_gen_bb")
        temphist.Scale(pathList2016[path]/num)
        genBB2016.Add(temphist,1.)
        temphist=f2016.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_bb")
        temphist.Scale(pathList2016[path]/num)
        recBB2016.Add(temphist,1.)
        temphist=f2016.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_gen_be")
        temphist.Scale(pathList2016[path]/num)
        genBE2016.Add(temphist,1.)
        temphist=f2016.Get("ElectronSelectionElectronsAllSignsHistos/DielectronMass_be")
        temphist.Scale(pathList2016[path]/num)
        recBE2016.Add(temphist,1.)
        temphist=f2016.Get("ElectronSelectionElectronsAllSignsHistos/DielectronResponse_bb")
        temphist.Scale(pathList2016[path]/num)
        reM2016BB.Add(temphist,1.)
        temphist=f2016.Get("ElectronSelectionElectronsAllSignsHistos/DielectronResponse_be")
        temphist.Scale(pathList2016[path]/num)
        reM2016BE.Add(temphist,1.)

genBB2018=genBB2018.Rebin(len(bng)-1,"genBB2018_e",bng)
recBB2018=recBB2018.Rebin(len(bng)-1,"recBB2018_e",bng)
genBE2018=genBE2018.Rebin(len(bng)-1,"genBE2018_e",bng)
recBE2018=recBE2018.Rebin(len(bng)-1,"recBE2018_e",bng)
genBB2017=genBB2017.Rebin(len(bng)-1,"genBB2017_e",bng)
recBB2017=recBB2017.Rebin(len(bng)-1,"recBB2017_e",bng)
genBE2017=genBE2017.Rebin(len(bng)-1,"genBE2017_e",bng)
recBE2017=recBE2017.Rebin(len(bng)-1,"recBE2017_e",bng)
genBB2016=genBB2016.Rebin(len(bng)-1,"genBB2016_e",bng)
recBB2016=recBB2016.Rebin(len(bng)-1,"recBB2016_e",bng)
genBE2016=genBE2016.Rebin(len(bng)-1,"genBE2016_e",bng)
recBE2016=recBE2016.Rebin(len(bng)-1,"recBE2016_e",bng)

c1=ROOT.TCanvas("c1","c1",800,800)
c1.SetLogy()
c1.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
        norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2018BB.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2018BB.GetBinContent(j,i)
                if norm !=0 and val !=0:
                        reM2018BBn.SetBinContent(j,i,val/norm)
                else:
                        reM2018BBn.SetBinContent(j,i,0)
reM2018BBn.GetXaxis().SetTitle("Reco[GeV]")
reM2018BBn.GetYaxis().SetTitle("Gen[GeV]")
reM2018BBn.Draw("COLZ")
c1.Print("plot/response_matrix_2018BB_e.pdf")

c2=ROOT.TCanvas("c2","c2",800,800)
c2.SetLogy()
c2.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
        norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2018BE.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2018BE.GetBinContent(j,i)
                if norm !=0 and val !=0:
                        reM2018BEn.SetBinContent(j,i,val/norm)
                else:
                        reM2018BEn.SetBinContent(j,i,0)
reM2018BEn.GetXaxis().SetTitle("Reco[GeV]")
reM2018BEn.GetYaxis().SetTitle("Gen[GeV]")
reM2018BEn.Draw("COLZ")
c2.Print("plot/response_matrix_2018BE_e.pdf")

c3=ROOT.TCanvas("c3","c3",800,800)
c3.SetLogy()
c3.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
        norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2017BB.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2017BB.GetBinContent(j,i)
                if norm !=0 and val !=0:
                        reM2017BBn.SetBinContent(j,i,val/norm)
                else:
                        reM2017BBn.SetBinContent(j,i,0)
reM2017BBn.GetXaxis().SetTitle("Reco[GeV]")
reM2017BBn.GetYaxis().SetTitle("Gen[GeV]")
reM2017BBn.Draw("COLZ")
c3.Print("plot/response_matrix_2017BB_e.pdf")

c4=ROOT.TCanvas("c4","c4",800,800)
c4.SetLogy()
c4.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
        norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2018BE.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2017BE.GetBinContent(j,i)
                if norm !=0 and val !=0:
                        reM2017BEn.SetBinContent(j,i,val/norm)
		else:
                        reM2017BEn.SetBinContent(j,i,0)
reM2017BEn.GetXaxis().SetTitle("Reco[GeV]")
reM2017BEn.GetYaxis().SetTitle("Gen[GeV]")
reM2017BEn.Draw("COLZ")
c4.Print("plot/response_matrix_2017BE_e.pdf")

c5=ROOT.TCanvas("c5","c5",800,800)
c5.SetLogy()
c5.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
        norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2016BB.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2016BB.GetBinContent(j,i)
                if norm !=0 and val !=0:
                        reM2016BBn.SetBinContent(j,i,val/norm)
                else:
                        reM2016BBn.SetBinContent(j,i,0)
reM2016BBn.GetXaxis().SetTitle("Reco[GeV]")
reM2016BBn.GetYaxis().SetTitle("Gen[GeV]")
reM2016BBn.Draw("COLZ")
c5.Print("plot/response_matrix_2016BB_e.pdf")

c6=ROOT.TCanvas("c6","c6",800,800)
c6.SetLogy()
c6.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
        norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2016BE.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2016BE.GetBinContent(j,i)
                if norm !=0 and val !=0:
			reM2016BEn.SetBinContent(j,i,val/norm)
		else:
                        reM2016BEn.SetBinContent(j,i,0)
reM2016BEn.GetXaxis().SetTitle("Reco[GeV]")
reM2016BEn.GetYaxis().SetTitle("Gen[GeV]")
reM2016BEn.Draw("COLZ")
c6.Print("plot/response_matrix_2016BE_e.pdf")

f=ROOT.TFile("ResponseMatrix_e.root","RECREATE")
reM2016BB.Write()
reM2016BE.Write()
reM2016BBn.Write()
reM2016BEn.Write()
reM2017BB.Write()
reM2017BE.Write()
reM2017BBn.Write()
reM2017BEn.Write()
reM2018BB.Write()
reM2018BE.Write()
reM2018BBn.Write()
reM2018BEn.Write()
genBB2016.Write()
genBE2016.Write()
recBB2016.Write()
recBE2016.Write()
genBB2017.Write()
genBE2017.Write()
recBB2017.Write()
recBE2017.Write()
genBB2018.Write()
genBE2018.Write()
recBB2018.Write()
recBE2018.Write()
f.Close()
	
