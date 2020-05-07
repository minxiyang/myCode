from ROOT import RooUnfold
from ROOT import RooUnfoldResponse
from ROOT import RooUnfoldInvert
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
from ROOT import RooUnfoldTUnfold
import ROOT
import numpy
from ROOT import TUnfoldDensity
from unfoldHandle import unfoldHandle
from setTDRStyle import setTDRStyle
#import TUnfoldIterativeEM


def average(hist):
	for i in range(hist.GetNbinsX()+2):
		val=hist.GetBinContent(i)
		err=hist.GetBinError(i)
		wid=hist.GetBinWidth(i)
		val=val/wid
		err=err/wid
		hist.SetBinContent(i,val)
		hist.SetBinError(i,err)
def reAverage(hist):
        for i in range(hist.GetNbinsX()+2):
                val=hist.GetBinContent(i)
                err=hist.GetBinError(i)
                wid=hist.GetBinWidth(i)
                val=val*wid
                err=err*wid
                hist.SetBinContent(i,val)
                hist.SetBinError(i,err)

def rebin(hist1,hist2):
	for i in range(15):
        	for j in range(15):
                	if i<3:
                        	k=0
                	elif i>12:
                        	k=10
			else:
				k=i-3
                	if j<3:
                        	l=0
			elif j>12:
				l=10
                	else:
                        	l=j-3
			val1=hist1.GetBinContent(i,j)
                	val2=hist2.GetBinContent(k,l)
                	hist2.SetBinContent(k,l,val1+val2)
def Norm2D(hist1, hist2):
	for i in range(hist1.GetNbinsX()+2):
        	norm=0
        	for j in range(hist1.GetNbinsX()+2):
                	norm+=hist1.GetBinContent(j,i)
        	for j in range(hist1.GetNbinsX()+2):
                	val=hist1.GetBinContent(j,i)
                	if norm !=0 and val !=0:
                        	hist2.SetBinContent(j,i,val/norm)
                	else:
                        	hist2.SetBinContent(j,i,0)

lumi_el = [35.9*1000,41.529*1000,59.97*1000]
lumi_mu = [36.3*1000,42.135*1000,61.608*1000]
zScale_el_bb=[0.902374,0.949371,0.950691]
zScale_el_be=[0.874569,0.938017,0.953648]
zScale_mu=[1.0282,1.0062,0.9727]

f1=ROOT.TFile.Open("ResponseMatrix_e.root")
f2=ROOT.TFile.Open("ResponseMatrix_mu.root")
f3=ROOT.TFile.Open("unfoldingData.root")
f4=ROOT.TFile.Open("unfoldingMC.root")

genBB2018_e=f1.Get("genBB2018_e")
recBB2018_e=f1.Get("recBB2018_e")
reMBB2018_e=f1.Get("reM2018BB_e")
genBE2018_e=f1.Get("genBE2018_e")
recBE2018_e=f1.Get("recBE2018_e")
reMBE2018_e=f1.Get("reM2018BE_e")
genBB2017_e=f1.Get("genBB2017_e")
recBB2017_e=f1.Get("recBB2017_e")
reMBB2017_e=f1.Get("reM2017BB_e")
genBE2017_e=f1.Get("genBE2017_e")
recBE2017_e=f1.Get("recBE2017_e")
reMBE2017_e=f1.Get("reM2017BE_e")
genBB2016_e=f1.Get("genBB2016_e")
recBB2016_e=f1.Get("recBB2016_e")
reMBB2016_e=f1.Get("reM2016BB_e")
genBE2016_e=f1.Get("genBE2016_e")
recBE2016_e=f1.Get("recBE2016_e")
reMBE2016_e=f1.Get("reM2016BE_e")

genBB2018_mu=f2.Get("genBB2018_mu")
recBB2018_mu=f2.Get("recBB2018_mu")
reMBB2018_mu=f2.Get("reM2018BB_mu")
genBE2018_mu=f2.Get("genBE2018_mu")
recBE2018_mu=f2.Get("recBE2018_mu")
reMBE2018_mu=f2.Get("reM2018BE_mu")
reMBE2018n_mu=f2.Get("reM2018BEn_mu")
genBB2017_mu=f2.Get("genBB2017_mu")
recBB2017_mu=f2.Get("recBB2017_mu")
reMBB2017_mu=f2.Get("reM2017BB_mu")
genBE2017_mu=f2.Get("genBE2017_mu")
recBE2017_mu=f2.Get("recBE2017_mu")
reMBE2017_mu=f2.Get("reM2017BE_mu")
genBB2016_mu=f2.Get("genBB2016_mu")
recBB2016_mu=f2.Get("recBB2016_mu")
reMBB2016_mu=f2.Get("reM2016BB_mu")
genBE2016_mu=f2.Get("genBE2016_mu")
recBE2016_mu=f2.Get("recBE2016_mu")
reMBE2016_mu=f2.Get("reM2016BE_mu")

datamubb2018=f3.Get("datamubb2018")
datamube2018=f3.Get("datamube2018")
datamubb2017=f3.Get("datamubb2017")
datamube2017=f3.Get("datamube2017")
datamubb2016=f3.Get("datamubb2016")
datamube2016=f3.Get("datamube2016")
dataebb2018=f3.Get("dataebb2018")
dataebe2018=f3.Get("dataebe2018")
dataebb2017=f3.Get("dataebb2017")
dataebe2017=f3.Get("dataebe2017")
dataebb2016=f3.Get("dataebb2016")
dataebe2016=f3.Get("dataebe2016")

bkgmubb2018=f4.Get("bkgmubb2018")
bkgmube2018=f4.Get("bkgmube2018")
bkgmubb2017=f4.Get("bkgmubb2017")
bkgmube2017=f4.Get("bkgmube2017")
bkgmubb2016=f4.Get("bkgmubb2016")
bkgmube2016=f4.Get("bkgmube2016")
bkgebb2018=f4.Get("bkgebb2018")
bkgebe2018=f4.Get("bkgebe2018")
bkgebb2017=f4.Get("bkgebb2017")
bkgebe2017=f4.Get("bkgebe2017")
bkgebb2016=f4.Get("bkgebb2016")
bkgebe2016=f4.Get("bkgebe2016")


handle2016_bb_el=unfoldHandle(genBB2016_e,recBB2016_e,reMBB2016_e,"BB2016el")
print "2016 BB electrons condtion number is %f" %handle2016_bb_el.getConditionN()
handle2016_be_el=unfoldHandle(genBE2016_e,recBE2016_e,reMBE2016_e,"BE2016el")
print "2016 BE electrons condtion number is %f" %handle2016_be_el.getConditionN()
handle2017_bb_el=unfoldHandle(genBB2017_e,recBB2017_e,reMBB2017_e,"BB2017el")
print "2017 BB electrons condtion number is %f" %handle2017_bb_el.getConditionN()
handle2017_be_el=unfoldHandle(genBE2017_e,recBE2017_e,reMBE2017_e,"BE2017el")
print "2017 BE electrons condtion number is %f" %handle2017_be_el.getConditionN()
handle2018_bb_el=unfoldHandle(genBB2018_e,recBB2018_e,reMBB2018_e,"BB2018el")
print "2018 BB electrons condtion number is %f" %handle2018_bb_el.getConditionN()
handle2018_be_el=unfoldHandle(genBE2018_e,recBE2018_e,reMBE2018_e,"BE2018el")
print "2018 BE electrons condtion number is %f" %handle2018_be_el.getConditionN()
handle2016_bb_mu=unfoldHandle(genBB2016_mu,recBB2016_mu,reMBB2016_mu,"BB2016mu")
print "2016 BB muons condtion number is %f" %handle2016_bb_mu.getConditionN()
handle2016_be_mu=unfoldHandle(genBE2016_mu,recBE2016_mu,reMBE2016_mu,"BE2016mu")
print "2016 BE muons condtion number is %f" %handle2016_be_mu.getConditionN()
handle2017_bb_mu=unfoldHandle(genBB2017_mu,recBB2017_mu,reMBB2017_mu,"BB2017mu")
print "2017 BB muons condtion number is %f" %handle2017_bb_mu.getConditionN()
handle2017_be_mu=unfoldHandle(genBE2017_mu,recBE2017_mu,reMBE2017_mu,"BE2017mu")
print "2017 BE muons condtion number is %f" %handle2017_be_mu.getConditionN()
handle2018_bb_mu=unfoldHandle(genBB2018_mu,recBB2018_mu,reMBB2018_mu,"BB2018mu")
print "2018 BB muons condtion number is %f" %handle2018_bb_mu.getConditionN()
handle2018_be_mu=unfoldHandle(genBE2018_mu,recBE2018_mu,reMBE2018_mu,"BE2018mu")
print "2018 BE muons condtion number is %f" %handle2018_be_mu.getConditionN()


handle2016_be_el.response.Print()
handle2016_be_mu.response.Print()
bng=[200,300,400,500,690,900,1250,1610, 2000, 4000]
bng=numpy.asarray(bng,dtype=numpy.float64)
reMBB2018_mu_rebin=ROOT.TH2D("rebinMBB2018_mu","rebinMBB2018_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBE2018_mu_rebin=ROOT.TH2D("rebinMBE2018_mu","rebinMBE2018_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBB2017_mu_rebin=ROOT.TH2D("rebinMBB2017_mu","rebinMBB2017_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBE2017_mu_rebin=ROOT.TH2D("rebinMBE2017_mu","rebinMBE2017_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBB2016_mu_rebin=ROOT.TH2D("rebinMBB2016_mu","rebinMBB2016_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBE2016_mu_rebin=ROOT.TH2D("rebinMBE2016_mu","rebinMBE2016_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBB2018_e_rebin=ROOT.TH2D("rebinMBB2018_el","rebinMBB2018_el",len(bng)-1,bng,len(bng)-1,bng)
reMBE2018_e_rebin=ROOT.TH2D("rebinMBE2018_el","rebinMBE2018_el",len(bng)-1,bng,len(bng)-1,bng)
reMBB2017_e_rebin=ROOT.TH2D("rebinMBB2017_el","rebinMBB2017_el",len(bng)-1,bng,len(bng)-1,bng)
reMBE2017_e_rebin=ROOT.TH2D("rebinMBE2017_el","rebinMBE2017_el",len(bng)-1,bng,len(bng)-1,bng)
reMBB2016_e_rebin=ROOT.TH2D("rebinMBB2016_el","rebinMBB2016_el",len(bng)-1,bng,len(bng)-1,bng)
reMBE2016_e_rebin=ROOT.TH2D("rebinMBE2016_el","rebinMBE2016_el",len(bng)-1,bng,len(bng)-1,bng)
reMBB2018n_mu_rebin=ROOT.TH2D("rebinMBB2018n_mu","rebinMBB2018_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBE2018n_mu_rebin=ROOT.TH2D("rebinMBE2018n_mu","rebinMBE2018_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBB2017n_mu_rebin=ROOT.TH2D("rebinMBB2017n_mu","rebinMBB2017_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBE2017n_mu_rebin=ROOT.TH2D("rebinMBE2017n_mu","rebinMBE2017_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBB2016n_mu_rebin=ROOT.TH2D("rebinMBB2016n_mu","rebinMBB2016_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBE2016n_mu_rebin=ROOT.TH2D("rebinMBE2016n_mu","rebinMBE2016_mu",len(bng)-1,bng,len(bng)-1,bng)
reMBB2018n_e_rebin=ROOT.TH2D("rebinMBB2018n_el","rebinMBB2018_el",len(bng)-1,bng,len(bng)-1,bng)
reMBE2018n_e_rebin=ROOT.TH2D("rebinMBE2018n_el","rebinMBE2018_el",len(bng)-1,bng,len(bng)-1,bng)
reMBB2017n_e_rebin=ROOT.TH2D("rebinMBB2017n_el","rebinMBB2017_el",len(bng)-1,bng,len(bng)-1,bng)
reMBE2017n_e_rebin=ROOT.TH2D("rebinMBE2017n_el","rebinMBE2017_el",len(bng)-1,bng,len(bng)-1,bng)
reMBB2016n_e_rebin=ROOT.TH2D("rebinMBB2016n_el","rebinMBB2016_el",len(bng)-1,bng,len(bng)-1,bng)
reMBE2016n_e_rebin=ROOT.TH2D("rebinMBE2016n_el","rebinMBE2016_el",len(bng)-1,bng,len(bng)-1,bng)
f5=ROOT.TFile.Open("ResponseMatrix_e_V2.root")
f6=ROOT.TFile.Open("ResponseMatrix_mu_V2.root")

reMBB2018_e_v2=f5.Get("reM2018BB_e")
reMBE2018_e_v2=f5.Get("reM2018BE_e")
reMBB2017_e_v2=f5.Get("reM2017BB_e")
reMBE2017_e_v2=f5.Get("reM2017BE_e")
reMBB2016_e_v2=f5.Get("reM2016BB_e")
reMBE2016_e_v2=f5.Get("reM2016BE_e")

reMBB2018_mu_v2=f6.Get("reM2018BB_mu")
reMBE2018_mu_v2=f6.Get("reM2018BE_mu")
reMBB2017_mu_v2=f6.Get("reM2017BB_mu")
reMBE2017_mu_v2=f6.Get("reM2017BE_mu")
reMBB2016_mu_v2=f6.Get("reM2016BB_mu")
reMBE2016_mu_v2=f6.Get("reM2016BE_mu")

rebin(reMBB2018_mu_v2,reMBB2018_mu_rebin)
handleBB2018Mu=unfoldHandle(reMBB2018_mu_rebin.ProjectionY(),reMBB2018_mu_rebin.ProjectionX(),reMBB2018_mu_rebin,"cropBB2018Mu")
print "crop 2018 BB muons condtion number is %f" %handleBB2018Mu.getConditionN()

rebin(reMBE2018_mu_v2,reMBE2018_mu_rebin)
handleBE2018Mu=unfoldHandle(reMBE2018_mu_rebin.ProjectionY(),reMBE2018_mu_rebin.ProjectionX(),reMBE2018_mu_rebin,"cropBE2018Mu")
print "crop 2018 BE muons condtion number is %f" %handleBE2018Mu.getConditionN()

rebin(reMBB2017_mu_v2,reMBB2017_mu_rebin)
handleBB2017Mu=unfoldHandle(reMBB2017_mu_rebin.ProjectionY(),reMBB2017_mu_rebin.ProjectionX(),reMBB2017_mu_rebin,"cropBB2017Mu")
print "crop 2017 BB muons condtion number is %f" %handleBB2017Mu.getConditionN()

rebin(reMBE2017_mu_v2,reMBE2017_mu_rebin)
handleBE2017Mu=unfoldHandle(reMBE2017_mu_rebin.ProjectionY(),reMBE2017_mu_rebin.ProjectionX(),reMBE2017_mu_rebin,"cropBE2017Mu")
print "crop 2017 BE muons condtion number is %f" %handleBE2017Mu.getConditionN()

rebin(reMBB2016_mu_v2,reMBB2016_mu_rebin)
handleBB2016Mu=unfoldHandle(reMBB2016_mu_rebin.ProjectionY(),reMBB2016_mu_rebin.ProjectionX(),reMBB2016_mu_rebin,"cropBB2016Mu")
print "crop 2016 BB muons condtion number is %f" %handleBB2016Mu.getConditionN()

rebin(reMBE2016_mu_v2,reMBE2016_mu_rebin)
handleBE2016Mu=unfoldHandle(reMBE2016_mu_rebin.ProjectionY(),reMBE2016_mu_rebin.ProjectionX(),reMBE2016_mu_rebin,"cropBE2016Mu")
print "crop 2016 BE muons condtion number is %f" %handleBE2016Mu.getConditionN()

rebin(reMBB2018_e_v2,reMBB2018_e_rebin)
handleBB2018E=unfoldHandle(reMBB2018_e_rebin.ProjectionY(),reMBB2018_e_rebin.ProjectionX(),reMBB2018_e_rebin,"cropBB2018E")
print "crop 2018 BB electrons condtion number is %f" %handleBB2018E.getConditionN()

rebin(reMBE2018_e_v2,reMBE2018_e_rebin)
handleBE2018E=unfoldHandle(reMBE2018_e_rebin.ProjectionY(),reMBE2018_e_rebin.ProjectionX(),reMBE2018_e_rebin,"cropBE2018E")
print "crop 2018 BE electrons condtion number is %f" %handleBE2018E.getConditionN()

rebin(reMBB2017_e_v2,reMBB2017_e_rebin)
handleBB2017E=unfoldHandle(reMBB2017_e_rebin.ProjectionY(),reMBB2017_e_rebin.ProjectionX(),reMBB2017_e_rebin,"cropBB2017E")
print "crop 2017 BB electrons condtion number is %f" %handleBB2017E.getConditionN()

rebin(reMBE2017_e_v2,reMBE2017_e_rebin)
handleBE2017E=unfoldHandle(reMBE2017_e_rebin.ProjectionY(),reMBE2017_e_rebin.ProjectionX(),reMBE2017_e_rebin,"cropBE2017E")
print "crop 2017 BE electrons condtion number is %f" %handleBE2017E.getConditionN()

rebin(reMBB2016_e_v2,reMBB2016_e_rebin)
handleBB2016E=unfoldHandle(reMBB2016_e_rebin.ProjectionY(),reMBB2016_e_rebin.ProjectionX(),reMBB2016_e_rebin,"cropBB2016E")
print "crop 2016 BB electrons condtion number is %f" %handleBB2016E.getConditionN()

rebin(reMBE2016_e_v2,reMBE2016_e_rebin)
handleBE2016E=unfoldHandle(reMBE2016_e_rebin.ProjectionY(),reMBE2016_e_rebin.ProjectionX(),reMBE2016_e_rebin,"cropBE2016E")
print "crop 2016 BE electrons condtion number is %f" %handleBE2016E.getConditionN()

#f1.Close()
#f2.Close()
#f3.Close()
#f4.Close()
#f5.Close()
#f6.Close()
ROOT.gStyle.SetOptStat(0)
latex=ROOT.TLatex()
latex.SetNDC(True)
latex.SetTextSize(0.025)

c1=ROOT.TCanvas("c1","c1",800,800)
c1.SetLogy()
c1.SetLogx()
setTDRStyle()
Norm2D(reMBB2018_mu_rebin,reMBB2018n_mu_rebin)
reMBB2018n_mu_rebin.SetTitle("2018 BB for Dimuon")
reMBB2018n_mu_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBB2018n_mu_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBB2018n_mu_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBB2018n_mu_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2018 BB for dimuon")
latex.DrawLatex(0.5,0.2,"condition number = 1.579")
c1.Update()
c1.Print("plot/response_matrix_2018BB_mu_V3.pdf")

c2=ROOT.TCanvas("c2","c2",800,800)
c2.SetLogy()
c2.SetLogx()
setTDRStyle()
Norm2D(reMBE2018_mu_rebin,reMBE2018n_mu_rebin)
reMBE2018n_mu_rebin.SetTitle("2018 BE for dimuon")
reMBE2018n_mu_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBE2018n_mu_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBE2018n_mu_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBE2018n_mu_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2018 BE for dimuon")
latex.DrawLatex(0.5,0.2,"condition number = 1.817")
c2.Update()
c2.Print("plot/response_matrix_2018BE_mu_V3.pdf")

c3=ROOT.TCanvas("c3","c3",800,800)
c3.SetLogy()
c3.SetLogx()
setTDRStyle()
Norm2D(reMBB2017_mu_rebin,reMBB2017n_mu_rebin)
reMBB2017n_mu_rebin.SetTitle("2017 BB for dimuon")
reMBB2017n_mu_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBB2017n_mu_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBB2017n_mu_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBB2017n_mu_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2017 BB for dimuon")
latex.DrawLatex(0.5,0.2,"condition number = 1.588")
c3.Update()
c3.Print("plot/response_matrix_2017BB_mu_V3.pdf")

c4=ROOT.TCanvas("c4","c4",800,800)
c4.SetLogy()
c4.SetLogx()
setTDRStyle()
Norm2D(reMBE2017_mu_rebin,reMBE2017n_mu_rebin)
reMBE2017n_mu_rebin.SetTitle("2017 BE for Dimuon")
reMBE2017n_mu_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBE2017n_mu_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBE2017n_mu_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBE2017n_mu_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2017 BE for dimuon")
latex.DrawLatex(0.5,0.2,"condition number = 1.807")
c4.Update()
c4.Print("plot/response_matrix_2017BE_mu_V3.pdf")

c5=ROOT.TCanvas("c5","c5",800,800)
c5.SetLogy()
c5.SetLogx()
setTDRStyle()
Norm2D(reMBB2016_mu_rebin,reMBB2016n_mu_rebin)
reMBB2016n_mu_rebin.SetTitle("2016 BB for Dimuon")
reMBB2016n_mu_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBB2016n_mu_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBB2016n_mu_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBB2016n_mu_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2016 BB for dimuon")
latex.DrawLatex(0.5,0.2,"condition number = 1.644")
c5.Update()
c5.Print("plot/response_matrix_2016BB_mu_V3.pdf")

c6=ROOT.TCanvas("c6","c6",800,800)
c6.SetLogy()
c6.SetLogx()
setTDRStyle()
Norm2D(reMBE2016_mu_rebin,reMBE2016n_mu_rebin)
reMBE2016n_mu_rebin.SetTitle("2016 BE for Dimuon")
reMBE2016n_mu_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBE2016n_mu_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBE2016n_mu_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBE2016n_mu_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2016 BE for dimuon")
latex.DrawLatex(0.5,0.2,"condition number = 1.929")
c6.Update()
c6.Print("plot/response_matrix_2016BE_mu_V3.pdf")

c7=ROOT.TCanvas("c7","c7",800,800)
c7.SetLogy()
c7.SetLogx()
setTDRStyle()
Norm2D(reMBB2018_e_rebin,reMBB2018n_e_rebin)
reMBB2018n_e_rebin.SetTitle("2018 BB for Dielectron")
reMBB2018n_e_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBB2018n_e_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBB2018n_e_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBB2018n_e_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2018 BB for dielectron")
latex.DrawLatex(0.5,0.2,"condition number = 1.120")
c7.Update()
c7.Print("plot/response_matrix_2018BB_e_V3.pdf")

c8=ROOT.TCanvas("c8","c8",800,800)
c8.SetLogy()
c8.SetLogx()
setTDRStyle()
Norm2D(reMBE2018_e_rebin,reMBE2018n_e_rebin)
reMBE2018n_e_rebin.SetTitle("2018 BE for Dielectron")
reMBE2018n_e_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBE2018n_e_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBE2018n_e_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBE2018n_e_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2018 BE for dielectron")
latex.DrawLatex(0.5,0.2,"condition number = 1.237")
c8.Update()
c8.Print("plot/response_matrix_2018BE_e_V3.pdf")

c9=ROOT.TCanvas("c9","c9",800,800)
c9.SetLogy()
c9.SetLogx()
setTDRStyle()
Norm2D(reMBB2017_e_rebin,reMBB2017n_e_rebin)
reMBB2017n_e_rebin.SetTitle("2017 BB for Dielectron")
reMBB2017n_e_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBB2017n_e_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBB2017n_e_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBB2017n_e_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2017 BB for dielectron")
latex.DrawLatex(0.5,0.2,"condition number = 1.198")
c9.Update()
c9.Print("plot/response_matrix_2017BB_e_V3.pdf")

c10=ROOT.TCanvas("c10","c10",800,800)
c10.SetLogy()
c10.SetLogx()
setTDRStyle()
Norm2D(reMBE2017_e_rebin,reMBE2017n_e_rebin)
reMBE2017n_e_rebin.SetTitle("2017 BE for Dielectron")
reMBE2017n_e_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBE2017n_e_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBE2017n_e_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBE2017n_e_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2017 BE for dielectron")
latex.DrawLatex(0.5,0.2,"condition number = 1.252")
c10.Update()
c10.Print("plot/response_matrix_2017BE_e_V3.pdf")

c11=ROOT.TCanvas("c11","c11",800,800)
c11.SetLogy()
c11.SetLogx()
setTDRStyle()
Norm2D(reMBB2016_e_rebin,reMBB2016n_e_rebin)
reMBB2016n_e_rebin.SetTitle("2016 BB for Dielectron")
reMBB2016n_e_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBB2016n_e_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBB2016n_e_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBB2016n_e_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2016 BB for dielectron")
latex.DrawLatex(0.5,0.2,"condition number = 1.303")
c11.Update()
c11.Print("plot/response_matrix_2016BB_e_V3.pdf")

c12=ROOT.TCanvas("c12","c12",800,800)
c12.SetLogy()
c12.SetLogx()
setTDRStyle()
Norm2D(reMBE2016_e_rebin,reMBE2016n_e_rebin)
reMBE2016n_e_rebin.SetTitle("2016 BE for Dielectron")
reMBE2016n_e_rebin.GetXaxis().SetTitle("Reconstructed M[GeV]")
reMBE2016n_e_rebin.GetYaxis().SetTitle("Generated M[GeV]")
reMBE2016n_e_rebin.GetZaxis().SetRangeUser(1e-3,1)
reMBE2016n_e_rebin.Draw("COLZ")
latex.DrawLatex(0.7,0.4,"2016 BE for dielectron")
latex.DrawLatex(0.5,0.2,"condition number = 1.270")
c12.Update()
c12.Print("plot/response_matrix_2016BE_e_V3.pdf")

f7=ROOT.TFile("responseMatrices.root","RECREATE")
reMBB2018_mu_rebin.Write()
reMBE2018_mu_rebin.Write()
reMBB2017_mu_rebin.Write()
reMBE2017_mu_rebin.Write()
reMBB2016_mu_rebin.Write()
reMBE2016_mu_rebin.Write()
reMBB2018_e_rebin.Write()
reMBE2018_e_rebin.Write()
reMBB2017_e_rebin.Write()
reMBE2017_e_rebin.Write()
reMBB2016_e_rebin.Write()
reMBE2016_e_rebin.Write()




