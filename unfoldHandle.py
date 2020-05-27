from ROOT import RooUnfold
from ROOT import RooUnfoldResponse
from ROOT import RooUnfoldInvert
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
from ROOT import RooUnfoldTUnfold
import ROOT
import numpy
from ROOT import gROOT

class unfoldHandle(object):
	def __init__(self,genHist,recHist,hist2d,name):
		self.genHist=genHist.Clone()
		self.recHist=recHist.Clone()
		self.hist2d=hist2d.Clone()
		self.response=RooUnfoldResponse(recHist,genHist,hist2d,"response matrix","response matrix")
		self.response.UseOverflow()
		self.name=name
		hx=self.hist2d.ProjectionX()
		hy=self.hist2d.ProjectionY()
		vaild=0.0001
		test1=0
		test2=0
		for i in range(hx.GetNbinsX()+2):
			if recHist.GetBinContent(i)!=0:
				val=abs(hx.GetBinContent(i)/recHist.GetBinContent(i)-1)
			else:
				val=0
			if val>test1:
				test1=val	
		for i in range(hx.GetNbinsX()+2):
                        if genHist.GetBinContent(i)!=0:
                                val=abs(hy.GetBinContent(i)/genHist.GetBinContent(i)-1)
                        else:
                                val=0
                        if val>test2:
                                test2=val
		if test1<vaild and test2<vaild:
			print "response matrix is correct"
		else:
			print "response matrix is wrong"
			print test1
			print test2
	def getConditionN(self):
		m=self.response.Mresponse()
		SVD=ROOT.TDecompSVD(m)
		return SVD.Condition()
	def doUnfold(self,data,back=0,regdiff=0,iteration=0):
		self.data=data.Clone()
		if back!=0:
			self.data.Sumw2()
			back.Sumw2()
			self.data.Add(back,-1.)
			self.back=back.Clone()
			for i in range(self.data.GetNbinsX()+2):
				if self.data.GetBinContent(i)<0:
					self.data.SetBinContent(i,0)
		if regdiff!=0:
			Unfold=RooUnfoldBayes(self.response,self.data,1,False,self.name+"_reg",self.name+"_reg")
			h2=self.data.Clone()
        		for i in range(9999):
                		h1=Unfold.Hreco().Clone()
                		vaild=0
                		val=0
                		for j in range(1,h2.GetNbinsX()+1):
                        		if h2.GetBinContent(j)>0:
                                		val=h1.GetBinContent(j)/h2.GetBinContent(j)
                                		val=abs(val-1)
                        			if vaild<val:
                                			vaild=val
				print vaild
                		if vaild<regdiff:
                        		print "%d times iteration" %i
					self.UnfoldedData=h1
					return h1
				else:
					h2=h1.Clone()
                        		Unfold.Reset()
                        		Unfold=RooUnfoldBayes(self.response,self.data,i+2,False,self.name+"_reg",self.name+"_reg")
		elif iteration !=0:
			s="iter_%d"%iteration
			Unfold=RooUnfoldBayes(self.response,self.data,iteration,False,self.name+s,self.name+s)
			h1=Unfold.Hreco().Clone()
			return h1
		else:
			Unfold=RooUnfoldInvert(self.response,self.data,self.name+"_invert",self.name+"_invert")
			Unfold.SetMeasured(self.data)
			self.Unfold=Unfold
			h1=Unfold.Hreco().Clone()
			self.UnfoldedData=h1
			return h1

