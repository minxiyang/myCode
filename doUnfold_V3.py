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
import root_numpy
import math
from unfoldPlot import plotMC
from unfoldDataPlot import plotData
from defs import Backgrounds, Backgrounds2016, Backgrounds2018, zScale, zScale2016, zScale2018, fileNamesEle, fileNames, crossSections

def getErrors(default, others, keys):
        dfarr=root_numpy.hist2array(default)
        errs={}
        for other, key in zip(others,keys):
                if type(other)==list:
                        err1=root_numpy.hist2array(other[0])-dfarr
                        err1=abs(err1)
                        err2=root_numpy.hist2array(other[1])-dfarr
                        err2=abs(err2)
                        err=numpy.maximum(err1,err2)
                        errs[key]=err
                else:
                        err=root_numpy.hist2array(other)-dfarr
                        err=abs(err)
                        errs[key]=err
        return errs

def average(hist):
        for i in range(hist.GetNbinsX()+2):
                val=hist.GetBinContent(i)
                err=hist.GetBinError(i)
                wid=hist.GetBinWidth(i)
                val=val/wid
                err=err/wid
                if i==hist.GetNbinsX()+1:
                        print wid
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
def closureTest(hreco,handle):
        hist1=handle.doUnfold(hreco)
        hist2=handle.doUnfold(hreco,regdiff=0.001)
        average(hist1)
        average(hist2)
        return [hist1,hist2]
def reBin1D(hist):
        bng1=[200,300,400,500,690,900,1250,1610, 2000, 3000]
        bng1=numpy.asarray(bng1,dtype=numpy.float64)
        bng=[200,300,400,500,690,900,1250,1610, 2000, 3000, 4000]
        bng=numpy.asarray(bng,dtype=numpy.float64)
        name=hist.GetName()
        hist1=hist.Rebin(len(bng)-1,name,bng)
        hist1.SetBinContent(len(bng)+1,0)
        hist1.SetBinError(len(bng)+1,0)
        hist2=hist1.Rebin(len(bng1)-1,name,bng1)
        return hist2
def reBinfin(hist):
        bng1=([j for j in range(200, 600, 20)]+ [j for j in range(600, 900, 30) ]+[j for j in range(900, 1250,50)]+[j for j in range(1250, 1610, 60) ] +[j for j in range(1610, 3000, 85) ])
        bng1=numpy.asarray(bng1,dtype=numpy.float64)
        hist.Sumw2()
        name=hist.GetName()
        hist1=hist.Rebin(len(bng1)-1,name,bng1)
        return hist1

def reBin2D(hist):
        bng1=[200,300,400,500,690,900,1250,1610, 2000, 3000]
        bng1=numpy.asarray(bng1,dtype=numpy.float64)
        bng=[200,300,400,500,690,900,1250,1610, 2000, 3000, 4000]
        bng=numpy.asarray(bng,dtype=numpy.float64)
        name=hist.GetName()
        title=hist.GetTitle()
        tmp=ROOT.TH2F(name,title,len(bng1)-1,bng1,len(bng1)-1,bng1)
        for i in range(hist.GetNbinsX()+1):
                for j in range(hist.GetNbinsY()+1):
                        print i
                        if i==9 or i==10:
                                k=9
                        elif i==11 or 1==12:
                                k=10
                        else:
                                k=i
                        if j==10 or j==9:
                                l=9
                                print l
                        elif j==11 or j==12:
                                l=10
                        else:
                                l=j
                        val1=hist.GetBinContent(i,j)
                        val2=tmp.GetBinContent(k,l)
                        tmp.SetBinContent(k,l,val1+val2)
        return tmp

def norm(hist):
        bng1=[200,300,400,500,690,900,1250,1610, 2000, 3000]
        bng1=numpy.asarray(bng1,dtype=numpy.float64)
        name=hist.GetName()
        title=hist.GetTitle()
        hist1=ROOT.TH2F(name,title,len(bng1)-1,bng1,len(bng1)-1,bng1)
        for i in range(hist.GetNbinsX()+2):
                norm=0
                for j in range(hist.GetNbinsX()+2):
                        norm+=hist.GetBinContent(j,i)
                for j in range(hist.GetNbinsX()+2):
                        val=hist.GetBinContent(j,i)
                        if norm !=0 and val !=0:
                                hist1.SetBinContent(j,i,val/norm)
                        else:
                                hist1.SetBinContent(j,i,0)
        return hist1

def printM(res,cond,flavor,category,uncert="none"):
        reM=norm(res)
        latexCMS = ROOT.TLatex()
        latexCMS.SetTextSize(0.06)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        yLabelPos = 0.8
        latexCMSExtra.SetTextSize(0.045)
        latexCMSExtra.SetNDC(True)
        cmsExtra = "Preliminary"
        latex=ROOT.TLatex()
        latex.SetNDC(True)
        latex.SetTextSize(0.025)
        #setTDRStyle()
        c=ROOT.TCanvas("c","c",900,800)
        c.SetLogy()
        c.SetLogx()
        ROOT.gStyle.SetPadRightMargin(0.2)
        reM.SetTitle("response matrix for %s %s"%(flavor,category))
        reM.GetXaxis().SetTitle("Reconstructed M[GeV]")
        reM.GetYaxis().SetTitle("Generated M[GeV]")
        reM.GetZaxis().SetRangeUser(1e-3,1)
        reM.Draw("COLZ")
        latex.DrawLatex(0.5,0.3,"%s %s"%(flavor,category))
        latex.DrawLatex(0.4,0.2,"condition number = %f"%cond)
        latexCMS.DrawLatex(0.15,0.84,"CMS")
        latexCMSExtra.DrawLatex(0.15,yLabelPos,"%s"%(cmsExtra))
        #c.Update()
        name="reM_v1/"+flavor+"_"+category+"_"+uncert+".pdf"
        c.Print(name)
def scale(hist1,hist2):
        lowLimit=hist1.FindBin(200)
        upLimit=hist1.FindBin(400)
        sFac1=hist1.Integral(lowLimit,upLimit)
        sFac2=hist2.Integral(lowLimit,upLimit)
        print(sFac2)
        print sFac1/sFac2
        return sFac1/sFac2
class unfoldedResult:
	def __init__(self,year,flavor,category):
		f=ROOT.TFile.Open("dataCollection.root")
		name=flavor+"_"+year+"_"+category+"_response_combine"
		reMraw=f.Get(name)
		reM=reBin2D(reMraw)
		self.response=reM
		handle=unfoldHandle(reM.ProjectionY(),reM.ProjectionX(),reM,"response"+category+"_"+flavor+"_"+year)
		printM(reM, handle.getConditionN(),"di"+flavor,year+category)
		dataName=flavor+"_"+year+"_"+category+"_data"
		dataRaw=f.Get(dataName)
		data=reBin1D(dataRaw)
		reAverage(data)
		self.data=data
		bkgName=flavor+"_"+year+"_"+category+"_bkg"
		bkgRaw=f.Get(bkgName)
		bkg=reBin1D(bkgRaw)
		reAverage(bkg)
		self.bkg=bkg
		self.unfoldedData=handle.doUnfold(data,bkg)
		Mcov=handle.Unfold.Ereco(2)
		print type(Mcov)
		Hcov=ROOT.TH2D(Mcov)
		self.Hcov=Hcov
		c=ROOT.TCanvas("c","c",800,800)
		c.SetLogx()
		c.SetLogy()
		self.Hcov.Draw("COLZ")
		c.Print("reM_v1/cov_"+year+"_"+flavor+"_"+category+"_"+".pdf")
		name=flavor+"_"+year+"_"+category+"_response_combine_scaleUp"
                reMraw_Up=f.Get(name)
                reM_Up=reBin2D(reMraw_Up)
                handle_Up=unfoldHandle(reM_Up.ProjectionY(),reM_Up.ProjectionX(),reM_Up,"response"+category+"Up"+"_"+flavor+"_"+year)
		self.dataUp=handle_Up.doUnfold(self.data,self.bkg)	
                printM(reM_Up, handle_Up.getConditionN(),"di"+flavor,year+category,"scaleUp")
		name=flavor+"_"+year+"_"+category+"_response_combine_scaleDown"
                reMraw_Down=f.Get(name)
                reM_Down=reBin2D(reMraw_Down)
                handle_Down=unfoldHandle(reM_Down.ProjectionY(),reM_Down.ProjectionX(),reM_Down,"response"+category+"Down"+"_"+flavor+"_"+year)
                self.dataDown=handle_Down.doUnfold(self.data,self.bkg)
                printM(reM_Down, handle_Down.getConditionN(),"di"+flavor,year+category,"scaleDown")
		name=flavor+"_"+year+"_"+category+"_response_combine_kFac"
                reMraw_kFac=f.Get(name)
                reM_kFac=reBin2D(reMraw_kFac)
                handle_kFac=unfoldHandle(reM_kFac.ProjectionY(),reM_kFac.ProjectionX(),reM_kFac,"response"+category+"kFac"+"_"+flavor+"_"+year)
		self.data_kFac=handle_kFac.doUnfold(self.data,self.bkg)
                printM(reM_kFac, handle_kFac.getConditionN(),"di"+flavor,year+category,"kFac")
		if flavor=="muon":
			name=flavor+"_"+year+"_"+category+"_response_combine_resolution"
			reMraw_smear=f.Get(name)
			reM_smear=reBin2D(reMraw_smear)
			handle_smear=unfoldHandle(reM_smear.ProjectionY(),reM_smear.ProjectionX(),reM_smear,"response"+category+"smear"+"_"+flavor+"_"+year)
			self.dataSmear=handle_smear.doUnfold(self.data,self.bkg)
			average(self.dataSmear)
		average(self.data)
		average(self.unfoldedData)
		average(self.bkg)
		average(self.dataUp)
		average(self.dataDown)
		average(self.data_kFac)
		self.data.Add(self.bkg,-1)
		if flavor=="muon":
			uncertainties=getErrors(self.unfoldedData,[[self.dataUp,self.dataDown],self.dataSmear],["scale","smear"])
		else:
			uncertainties=getErrors(self.unfoldedData,[[self.dataUp,self.dataDown]],["scale"])	
		self.dataUncertainties=uncertainties
		name=flavor+"_"+year+"_"+category+"_"+"recoMass_"+"combine"
		recoMassRaw=f.Get(name)
		recoMass=reBin1D(recoMassRaw)
		name=flavor+"_"+year+"_"+category+"_"+"recoMass_"+"combine_"+"kFac"
                recoMassRaw_kFac=f.Get(name)
		name=flavor+"_"+year+"_"+category+"_"+"genMass_combine"
		genMassRaw=f.Get(name)
		genMass=reBin1D(genMassRaw)
                recoMass_kFac=reBin1D(recoMassRaw_kFac)
		unfoldedRecoMass=handle.doUnfold(recoMass)
		average(recoMass)
		average(genMass)
		average(unfoldedRecoMass)
		average(recoMass_kFac)
		lumi={}
		lumi["electron"]={"2016":35.9*1000,"2017":41.529*1000,"2018":59.97*1000}
		lumi["muon"]={"2016":36.3*1000,"2017":42.135*1000,"2018":61.608*1000}
		zFac={}
		zFac["muon"]={}
		zFac["muon"]["bb"]={"2016":zScale2016["muons"],"2017":zScale["muons"],"2018":zScale2018["muons"]}
		zFac["muon"]["be"]={"2016":zScale2016["muons"],"2017":zScale["muons"],"2018":zScale2018["muons"]}
		zFac["electron"]={}
		zFac["electron"]["bb"]={"2016":zScale2016["electrons"][1],"2017":zScale["electrons"][1],"2018":zScale2018["electrons"][1]}
		zFac["electron"]["be"]={"2016":zScale2016["electrons"][2],"2017":zScale["electrons"][2],"2018":zScale2018["electrons"][2]}
		recoMass.Scale(lumi[flavor][year]*zFac[flavor][category][year])
		genMass.Scale(lumi[flavor][year]*zFac[flavor][category][year])
		unfoldedRecoMass.Scale(lumi[flavor][year]*zFac[flavor][category][year])
		recoMass_kFac.Scale(lumi[flavor][year]*zFac[flavor][category][year])
		if flavor=="muon":
                        name=flavor+"_"+year+"_"+category+"_"+"genMass_"+"combine_ID"
                        genMassRawID=f.Get(name)
                        genMassfinID=reBinfin(genMassRawID)
			genMassfin=reBinfin(genMassRaw)
                        average(genMassfinID)
			average(genMassfin)
			genMassfin.Scale(lumi[flavor][year]*zFac[flavor][category][year])
			genMassfinID.Scale(lumi[flavor][year]*zFac[flavor][category][year])
			mcErr=getErrors(genMassfin,[genMassfinID],["ID"])
                else:
			genMassfin=reBinfin(genMassRaw)
			name=flavor+"_"+year+"_"+category+"_"+"genMass_"+"combine_pileUp"
			genMassRawPU=f.Get(name)
			genMassfinPU=reBinfin(genMassRawPU)
			name=flavor+"_"+year+"_"+category+"_"+"genMass_"+"combine_pileDown"
                        genMassRawPD=f.Get(name)
                        genMassfinPD=reBinfin(genMassRawPD)
			name=flavor+"_"+year+"_"+category+"_"+"genMass_"+"combine_prefireUp"
                        genMassRawPreU=f.Get(name)
                        genMassfinPreU=reBinfin(genMassRawPreU)
                        name=flavor+"_"+year+"_"+category+"_"+"genMass_"+"combine_prefireDown"
                        genMassRawPreD=f.Get(name)
                        genMassfinPreD=reBinfin(genMassRawPreD)
			average(genMassfin)
			average(genMassfinPU)
			average(genMassfinPD)
			average(genMassfinPreU)
			average(genMassfinPreD)
			mcErr=getErrors(genMassfin,[[genMassfinPU,genMassfinPD],[genMassfinPreU,genMassfinPreD]],["PU","prefire"])
		self.mcUncertainties=mcErr
		self.recoMass=recoMass
		self.genMass=genMass
		self.genMassfin=genMassfin
		self.unfoldedRecoMass=unfoldedRecoMass
		self.recoMass_kFac=recoMass_kFac
		name=flavor+"_"+year+"_"+category+"_response_Other"
                reMraw_other=f.Get(name)
                reM_other=reBin2D(reMraw_other)
                handle_other=unfoldHandle(reM_other.ProjectionY(),reM_other.ProjectionX(),reM_other,"responseOther"+category+"_"+flavor+"_"+year)
                printM(reM_other, handle_other.getConditionN(),"di"+flavor,year+category,"Other")
		name=flavor+"_"+year+"_"+category+"_response_DrellYan"
                reMraw_DY=f.Get(name)
                reM_DY=reBin2D(reMraw_DY)
                handle_DY=unfoldHandle(reM_DY.ProjectionY(),reM_DY.ProjectionX(),reM_DY,"responseDY"+category+"_"+flavor+"_"+year)
		printM(reM_DY, handle_DY.getConditionN(),"di"+flavor,year+category,"DY")
		plotMC(self.recoMass,self.recoMass_kFac,True,"kFac/w","kFac/o",category+" di"+flavor,"reM_v1/kFac_reco_"+flavor+"_"+category+"_"+year,"kFac")
		plotMC(self.unfoldedRecoMass,self.recoMass,True,"unfolded","Reconstructed",category+" di"+flavor,"reM_v1/closure_reco_"+flavor+"_"+category+"_"+year,"unfolded/reco")
		plotMC(self.unfoldedRecoMass,self.genMass,True,"unfolded","Generated",category+" di"+flavor,"reM_v1/closure_gen_"+flavor+"_"+category+"_"+year,"unfolded/gen")
		plotData(self.unfoldedData,self.data_kFac,True,"kFac/w","kFac/o",category+" di"+flavor,"reM_v1/kFac_data_"+flavor+"_"+category+"_"+year,"w/o kFac ratio")
		plotData(self.unfoldedData,self.data,True,"unfolded","original",category+" di"+flavor,"reM_v1/ratio_data_"+flavor+"_"+category+"_"+year,"after/before")

ROOT.TH1.AddDirectory(0)
ROOT.TH2.AddDirectory(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadRightMargin(0.2)
setTDRStyle()
result2016_mu_bb=unfoldedResult("2016","muon","bb")
result2016_mu_be=unfoldedResult("2016","muon","be")
result2016_el_bb=unfoldedResult("2016","electron","bb")
result2016_el_be=unfoldedResult("2016","electron","be")
result2017_mu_bb=unfoldedResult("2017","muon","bb")
result2017_mu_be=unfoldedResult("2017","muon","be")
result2017_el_bb=unfoldedResult("2017","electron","bb")
result2017_el_be=unfoldedResult("2017","electron","be")
result2018_mu_bb=unfoldedResult("2018","muon","bb")
result2018_mu_be=unfoldedResult("2018","muon","be")
result2018_el_bb=unfoldedResult("2018","electron","bb")
result2018_el_be=unfoldedResult("2018","electron","be")

unfoldedData_mu_bb=result2016_mu_bb.unfoldedData.Clone()
unfoldedData_mu_bb.Add(result2017_mu_bb.unfoldedData.Clone())
unfoldedData_mu_bb.Add(result2018_mu_bb.unfoldedData.Clone())
Err2_mu_bb=result2016_mu_bb.dataUncertainties["scale"]**2+(result2017_mu_bb.dataUncertainties["scale"]+result2018_mu_bb.dataUncertainties["scale"])**2+result2016_mu_bb.dataUncertainties["smear"]**2+result2017_mu_bb.dataUncertainties["smear"]**2+result2018_mu_bb.dataUncertainties["smear"]**2
for i in range(1,unfoldedData_mu_bb.GetNbinsX()+1):
	err=unfoldedData_mu_bb.GetBinError(i)**2+Err2_mu_bb[i-1]
	err=math.sqrt(err)
	unfoldedData_mu_bb.SetBinError(i,err)
unfoldedData_mu_be=result2016_mu_be.unfoldedData.Clone()
unfoldedData_mu_be.Add(result2017_mu_be.unfoldedData.Clone())
unfoldedData_mu_be.Add(result2018_mu_be.unfoldedData.Clone())
Err2_mu_be=result2016_mu_be.dataUncertainties["scale"]**2+(result2017_mu_be.dataUncertainties["scale"]+result2018_mu_be.dataUncertainties["scale"])**2+result2016_mu_be.dataUncertainties["smear"]**2+result2017_mu_be.dataUncertainties["smear"]**2+result2018_mu_be.dataUncertainties["smear"]**2
for i in range(1,unfoldedData_mu_bb.GetNbinsX()+1):
        err=unfoldedData_mu_be.GetBinError(i)**2+Err2_mu_be[i-1]
        err=math.sqrt(err)
        unfoldedData_mu_be.SetBinError(i,err)

unfoldedData_el_bb=result2016_el_bb.unfoldedData.Clone()
unfoldedData_el_bb.Add(result2017_el_bb.unfoldedData.Clone())
unfoldedData_el_bb.Add(result2018_el_bb.unfoldedData.Clone())
Err2_el_bb=result2016_el_bb.dataUncertainties["scale"]**2+result2017_el_bb.dataUncertainties["scale"]**2+result2018_el_bb.dataUncertainties["scale"]**2
for i in range(1,unfoldedData_mu_bb.GetNbinsX()+1):
        err=unfoldedData_el_bb.GetBinError(i)**2+Err2_el_bb[i-1]
        err=math.sqrt(err)
        unfoldedData_el_bb.SetBinError(i,err)
unfoldedData_el_be=result2016_el_be.unfoldedData.Clone()
unfoldedData_el_be.Add(result2017_el_be.unfoldedData.Clone())
unfoldedData_el_be.Add(result2018_el_be.unfoldedData.Clone())
Err2_el_be=result2016_el_be.dataUncertainties["scale"]**2+result2017_el_be.dataUncertainties["scale"]**2+result2018_el_be.dataUncertainties["scale"]**2
for i in range(1,unfoldedData_el_be.GetNbinsX()+1):
        err=unfoldedData_el_be.GetBinError(i)**2+Err2_el_be[i-1]
        err=math.sqrt(err)
        unfoldedData_el_be.SetBinError(i,err)

genMassfin_mu_bb=result2016_mu_bb.genMassfin.Clone()
genMassfin_mu_bb.Add(result2017_mu_bb.genMassfin.Clone())
genMassfin_mu_bb.Add(result2018_mu_bb.genMassfin.Clone())
genErr2_mu_bb=result2016_mu_bb.mcUncertainties["ID"]**2+(result2017_mu_bb.mcUncertainties["ID"]+result2018_mu_bb.mcUncertainties["ID"])**2
for i in range(1,genMassfin_mu_bb.GetNbinsX()+1):
        err=genMassfin_mu_bb.GetBinError(i)**2+genErr2_mu_bb[i-1]
        err=math.sqrt(err)
        genMassfin_mu_bb.SetBinError(i,err)
genMassfin_mu_be=result2016_mu_be.genMassfin.Clone()
genMassfin_mu_be.Add(result2017_mu_be.genMassfin.Clone())
genMassfin_mu_be.Add(result2018_mu_be.genMassfin.Clone())
genErr2_mu_be=result2016_mu_be.mcUncertainties["ID"]**2+result2017_mu_be.mcUncertainties["ID"]**2+result2018_mu_be.mcUncertainties["ID"]**2
for i in range(1,genMassfin_mu_be.GetNbinsX()+1):
        err=genMassfin_mu_be.GetBinError(i)**2+genErr2_mu_be[i-1]
        err=math.sqrt(err)
        genMassfin_mu_be.SetBinError(i,err)
genMassfin_el_bb=result2016_el_bb.genMassfin.Clone()
genMassfin_el_bb.Add(result2017_el_bb.genMassfin.Clone())
genMassfin_el_bb.Add(result2018_el_bb.genMassfin.Clone())
genErr2_el_bb=(result2016_el_bb.mcUncertainties["PU"]+result2017_mu_bb.mcUncertainties["ID"]+result2018_mu_bb.mcUncertainties["ID"])**2+result2016_el_bb.mcUncertainties["prefire"]**2+result2017_el_bb.mcUncertainties["prefire"]**2+result2018_el_bb.mcUncertainties["prefire"]**2
for i in range(1,genMassfin_el_bb.GetNbinsX()+1):
        err=genMassfin_el_bb.GetBinError(i)**2+genErr2_el_bb[i-1]
        err=math.sqrt(err)
        genMassfin_el_bb.SetBinError(i,err)
genMassfin_el_be=result2016_el_be.genMassfin.Clone()
genMassfin_el_be.Add(result2017_el_be.genMassfin.Clone())
genMassfin_el_be.Add(result2018_el_be.genMassfin.Clone())
genErr2_el_be=(result2016_el_be.mcUncertainties["PU"]+result2017_mu_be.mcUncertainties["ID"]+result2018_mu_be.mcUncertainties["ID"])**2+result2016_el_be.mcUncertainties["prefire"]**2+result2017_el_be.mcUncertainties["prefire"]**2+result2018_el_be.mcUncertainties["prefire"]**2
for i in range(1,genMassfin_el_be.GetNbinsX()+1):
        err=genMassfin_el_be.GetBinError(i)**2+genErr2_el_be[i-1]
        err=math.sqrt(err)
        genMassfin_el_be.SetBinError(i,err)

plotData(unfoldedData_mu_be,unfoldedData_el_be,True,"#mu#mu","ee","BE","reM_v1/Unscaled_be","R_{#mu#mu/ee}")
plotData(unfoldedData_mu_bb,unfoldedData_el_bb,True,"#mu#mu","ee","BB","reM_v1/Unscaled_bb","R_{#mu#mu/ee}")

#scaling function

bng=[200,300,400,500,690,900,1250,1610, 2000, 3000]
bng=numpy.asarray(bng,dtype=numpy.float64)
finBng=([j for j in range(200, 600, 20)]+ [j for j in range(600, 900, 30) ]+[j for j in range(900, 1250,50)]+[j for j in range(1250, 1610, 60) ] +[j for j in range(1610, 3000, 85) ])
finBng=numpy.asarray(finBng,dtype=numpy.float64)
h_ratioMCbb=ROOT.TH1F("ratioMCbb","flavor ratio from MC BB",len(finBng)-1,finBng)
h_ratioDatabb=ROOT.TH1F("ratioDatabb","flavor ratio from data BB",len(bng)-1,bng)
h_ratioMCbe=ROOT.TH1F("ratioMCbe","flavor ratio from MC BE",len(finBng)-1,finBng)
h_ratioDatabe=ROOT.TH1F("ratioDatabe","flavor ratio from data BE",len(bng)-1,bng)
func=ROOT.TF1("func","[0]+[1]*log(x)+[2]*x^2",200,3000)
genMassfin_el_bb.Sumw2()
genMassfin_mu_bb.Sumw2()
genMassfin_el_be.Sumw2()
genMassfin_mu_be.Sumw2()
unfoldedData_mu_bb.Sumw2()
unfoldedData_mu_be.Sumw2()
unfoldedData_el_bb.Sumw2()
unfoldedData_el_be.Sumw2()

h_ratioMCbb.Divide(genMassfin_mu_bb,genMassfin_el_bb)
#h_ratioDatabb.Divide(unfoldedData_mu_bb,unfoldedData_el_bb)
h_ratioMCbb.Fit(func,"","",200,3000)
h_ratioMCbb.GetXaxis().SetTitle("m[GeV]")
h_ratioMCbb.GetYaxis().SetTitle("R_{mumu/ee}")
c1=ROOT.TCanvas("c1","c1",800,800)
c1.SetLogx()
h_ratioMCbb.Draw("hist")
func.Draw("same")
c1.Print("reM_v1/fit_to_mc_bb.pdf")
Fac=scale(unfoldedData_el_bb,unfoldedData_mu_bb)
unfoldedData_mu_bb.Scale(Fac)
h_ratioDatabb.Divide(unfoldedData_mu_bb,unfoldedData_el_bb)
h_ratioDatabb.Sumw2()
ParErr0=func.GetParError(0)
ParErr1=func.GetParError(1)
ParErr2=func.GetParError(2)
for i in range(1,h_ratioDatabb.GetNbinsX()+1):
        xval=h_ratioDatabb.GetBinCenter(i)
        fval=func.Eval(xval)
        fErr=math.sqrt(ParErr0**2+(ParErr1*math.log(xval))**2+(ParErr2*xval**2)**2)
        err=h_ratioDatabb.GetBinError(i)
        val=h_ratioDatabb.GetBinContent(i)
        rErr=math.sqrt((fErr/fval)**2+(err/val)**2)
        h_ratioDatabb.SetBinContent(i,val/fval)
        h_ratioDatabb.SetBinError(i,rErr*val/fval)
c2=ROOT.TCanvas("c2","c2",800,800)
c2.SetLogx()
h_ratioDatabb.GetXaxis().SetTitle("m[GeV]")
h_ratioDatabb.GetYaxis().SetTitle("R_{mumu/ee}")
h_ratioDatabb.Draw("l")
c2.Print("reM_v1/ratioPlot_bb.pdf")

h_ratioMCbe.Divide(genMassfin_mu_be,genMassfin_el_be)
#h_ratioDatabb.Divide(unfoldedData_mu_bb,unfoldedData_el_bb)
h_ratioMCbe.Fit(func,"","",200,3000)
h_ratioMCbe.GetXaxis().SetTitle("m[GeV]")
h_ratioMCbe.GetYaxis().SetTitle("R_{mumu/ee}")
c3=ROOT.TCanvas("c3","c3",800,800)
c3.SetLogx()
h_ratioMCbe.Draw()
func.Draw("same")
c3.Print("reM_v1/fit_to_mc_be.pdf")

Fac=scale(unfoldedData_el_be,unfoldedData_mu_be)
unfoldedData_mu_be.Scale(Fac)
h_ratioDatabe.Divide(unfoldedData_mu_be,unfoldedData_el_be)
h_ratioDatabe.Sumw2()
ParErr0=func.GetParError(0)
ParErr1=func.GetParError(1)
ParErr2=func.GetParError(2)
for i in range(1,h_ratioDatabe.GetNbinsX()+1):
        xval=h_ratioDatabe.GetBinCenter(i)
        fval=func.Eval(xval)
        fErr=math.sqrt(ParErr0**2+(ParErr1*math.log(xval))**2+(ParErr2*xval**2)**2)
        err=h_ratioDatabe.GetBinError(i)
        val=h_ratioDatabe.GetBinContent(i)
        rErr=math.sqrt((fErr/fval)**2+(err/val)**2)
        h_ratioDatabe.SetBinContent(i,val/fval)
        h_ratioDatabe.SetBinError(i,rErr*val/fval)
c4=ROOT.TCanvas("c4","c4",800,800)
c4.SetLogx()
h_ratioDatabe.GetXaxis().SetTitle("m[GeV]")
h_ratioDatabe.GetYaxis().SetTitle("R_{mumu/ee}")
h_ratioDatabe.Draw("l")
c4.Print("reM_v1/ratioPlot_be.pdf")

