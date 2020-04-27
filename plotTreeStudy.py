import ROOT
import os
import numpy
import subprocess
import root_numpy
import math
import copy
from readCrab import *
from crossSection import DYCrossSection

ROOT.gStyle.SetOptStat(0)
path="/mnt/hadoop/store/user/minxi"
pathList=getBkg(path,"ZToMuMu")
#pathList+=getBkg(path,"DY")
pathList2016={}
pathList2017={}
pathList2018={}
for path in pathList:
	if path.find("2016")!=-1:
		for key in DYCrossSection.keys():
			if path.find(key)!=-1:
				pathList2016[path]= DYCrossSection[key]
	elif path.find("2018")!=-1:
		for key in DYCrossSection.keys():
			if path.find(key)!=-1:
                        	pathList2018[path]= DYCrossSection[key]
	else:
                for key in DYCrossSection.keys():
			if path.find(key)!=-1:
                        	pathList2017[path]= DYCrossSection[key]

bng=[50, 120,150,200,300,400,500,690,900,1250,1610, 2000, 4000, 6070]
bng=numpy.asarray(bng,dtype=numpy.float64)
reM2016BB=ROOT.TH2D("reM2016BB","Response matrix for 2016 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2016BE=ROOT.TH2D("reM2016BE","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2017BB=ROOT.TH2D("reM2017BB","Response matrix for 2017 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2017BE=ROOT.TH2D("reM2017BE","Response matrix for 2017 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2018BB=ROOT.TH2D("reM2018BB","Response matrix for 2018 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2018BE=ROOT.TH2D("reM2018BE","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reMBB=ROOT.TH2D("reMBB","Response matrix for run 2 BB",len(bng)-1,bng,len(bng)-1,bng)
reMBE=ROOT.TH2D("reMBE","Response matrix for run 2 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2016BBn=ROOT.TH2D("reM2016BBn","Response matrix for 2016 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2016BEn=ROOT.TH2D("reM2016BEn","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2017BBn=ROOT.TH2D("reM2017BBn","Response matrix for 2017 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2017BEn=ROOT.TH2D("reM2017BEn","Response matrix for 2017 BE",len(bng)-1,bng,len(bng)-1,bng)
reM2018BBn=ROOT.TH2D("reM2018BBn","Response matrix for 2018 BB",len(bng)-1,bng,len(bng)-1,bng)
reM2018BEn=ROOT.TH2D("reM2018BEn","Response matrix for 2016 BE",len(bng)-1,bng,len(bng)-1,bng)
reMBBn=ROOT.TH2D("reMBBn","Response matrix for run 2 BB",len(bng)-1,bng,len(bng)-1,bng)
reMBEn=ROOT.TH2D("reMBEn","Response matrix for run 2 BE",len(bng)-1,bng,len(bng)-1,bng)
genBB=ROOT.TH1D("genBB","MC BB",len(bng)-1,bng)
recBB=ROOT.TH1D("recBB","MC BB",len(bng)-1,bng)
genBE=ROOT.TH1D("genBE","MC BB",len(bng)-1,bng)
recBE=ROOT.TH1D("recBE","MC BE",len(bng)-1,bng)
#chain=ROOT.TChain("SimpleNtupler")
#genMass2016=mass2016=y2016=pt2016=CS2016=CS_label2016=numpy.ones(0)
#genMass2017=mass2017=y2017=pt2017=CS2017=CS_label2017=numpy.ones(0)
#genMass2018=mass2018=numpy.ones(0)
#eta2016=eta2017=eta2018=[[1,1],[1,1]]
#i=0
#print pathList
print pathList2016
#print pathList2017
#print pathList2018
for path in pathList2016.keys():
	splitPath=path.split("/")
	pathMap="/home/yang1452/myTools/crabFile/"+splitPath[-3]+"/"+splitPath[-2]
	if not os.path.exists(pathMap):
		os.makedirs(pathMap)
	cmd="cp "+path+" "+pathMap
	os.system(cmd)
	pathMap=pathMap+"/"+splitPath[-1]
	f2016=ROOT.TFile.Open(pathMap)
	tree2016=f2016.Get("SimpleNtupler/t")
	mass2016=numpy.concatenate([root_numpy.tree2array(tree2016,"dil_mass"),numpy.ones(0)])
	genMass2016=numpy.concatenate([root_numpy.tree2array(tree2016,"gen_dil_mass"),numpy.ones(0)])
	y2016=root_numpy.tree2array(tree2016,"dil_rap")
	pt2016=root_numpy.tree2array(tree2016,"dil_pt")
	CS2016=root_numpy.tree2array(tree2016,"cos_cs")
	CS_label2016=root_numpy.tree2array(tree2016,"CS_label")
	eta2016=root_numpy.tree2array(tree2016,"lep_eta")
	weight=numpy.repeat(pathList2016[path],len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]))
	reM2016BB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],weight)
	reMBB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],weight)
	reM2016BE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],weight)
	reMBE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],weight)
	genBB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],weight)
	recBB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],weight)
	genBE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],weight)
	recBE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],weight)

for path in pathList2017.keys():
        splitPath=path.split("/")
        pathMap="/home/yang1452/myTools/crabFile/"+splitPath[-3]+"/"+splitPath[-2]
        if not os.path.exists(pathMap):
                os.makedirs(pathMap)
        cmd="cp "+path+" "+pathMap
        os.system(cmd)
        pathMap=pathMap+"/"+splitPath[-1]
        f2017=ROOT.TFile.Open(pathMap)
        tree2017=f2017.Get("SimpleNtupler/t")
        mass2017=numpy.concatenate([root_numpy.tree2array(tree2017,"dil_mass"),numpy.ones(0)])
        genMass2017=numpy.concatenate([root_numpy.tree2array(tree2017,"gen_dil_mass"),numpy.ones(0)])
        y2017=root_numpy.tree2array(tree2017,"dil_rap")
        pt2017=root_numpy.tree2array(tree2017,"dil_pt")
        CS2017=root_numpy.tree2array(tree2017,"cos_cs")
        CS_label2017=root_numpy.tree2array(tree2017,"CS_label")
        eta2017=root_numpy.tree2array(tree2017,"lep_eta")
	weight=numpy.repeat(pathList2017[path],len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]))
        reM2017BB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],weight)
        reMBB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],weight)
        reM2017BE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],weight)
        reMBE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],weight)
        genBB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],weight)
        recBB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],weight)
        genBE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],weight)
        recBE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],weight)

for path in pathList2018.keys():
        splitPath=path.split("/")
        pathMap="/home/yang1452/myTools/crabFile/"+splitPath[-3]+"/"+splitPath[-2]
        if not os.path.exists(pathMap):
                os.makedirs(pathMap)
        cmd="cp "+path+" "+pathMap
        os.system(cmd)
        pathMap=pathMap+"/"+splitPath[-1]
        f2018=ROOT.TFile.Open(pathMap)
        tree2018=f2018.Get("SimpleNtupler/t")
        mass2018=numpy.concatenate([root_numpy.tree2array(tree2018,"dil_mass"),numpy.ones(0)])
        genMass2018=numpy.concatenate([root_numpy.tree2array(tree2018,"gen_dil_mass"),numpy.ones(0)])
        y2018=root_numpy.tree2array(tree2018,"dil_rap")
        pt2018=root_numpy.tree2array(tree2018,"dil_pt")
        CS2018=root_numpy.tree2array(tree2018,"cos_cs")
        CS_label2018=root_numpy.tree2array(tree2018,"CS_label")
        eta2018=root_numpy.tree2array(tree2018,"lep_eta")
	weight=numpy.repeat(pathList2018[path],len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]))
        reM2018BB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],weight)
        reMBB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],weight)
        reM2018BE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],weight)
        reMBE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],weight)
        genBB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],weight)
        recBB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],weight)
        genBE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],weight)
        recBE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],weight)
#reM2016BB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],numpy.ones(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)])))
#reMBB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],numpy.ones(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)])))
#reM2017BB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],numpy.ones(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)])))
#reMBB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],numpy.ones(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)])))
#reM2018BB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],numpy.ones(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)])))
#reMBB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],numpy.ones(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)])))
#reM2016BBn.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],numpy.ones(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)])))
#reMBBn.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],numpy.ones(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)])))
#reM2017BBn.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],numpy.ones(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)])))
#reMBBn.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],numpy.ones(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)])))
#reM2018BBn.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],numpy.ones(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)])))
#reMBBn.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],numpy.ones(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)])))
#genBB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),genMass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],numpy.ones(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)])))
#genBB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),genMass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],numpy.ones(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)])))
#genBB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),genMass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],numpy.ones(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)])))
#recBB.FillN(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)]),mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)],numpy.ones(len(mass2018[(eta2018[:,0]<1.2)&(eta2018[:,1]<1.2)])))
#recBB.FillN(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)]),mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)],numpy.ones(len(mass2017[(eta2017[:,0]<1.2)&(eta2017[:,1]<1.2)])))
#recBB.FillN(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)]),mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)],numpy.ones(len(mass2016[(eta2016[:,0]<1.2)&(eta2016[:,1]<1.2)])))
#reM2016BE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],numpy.ones(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)])))
#reMBE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],numpy.ones(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)])))
#reM2017BE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],numpy.ones(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)])))
#reMBE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],numpy.ones(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]))) 
#reM2018BE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],numpy.ones(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)])))
#reMBE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],numpy.ones(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)])))
#reM2016BEn.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],numpy.ones(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)])))
#reMBEn.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],numpy.ones(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)])))
#reM2017BEn.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],numpy.ones(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)])))
#reMBEn.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],numpy.ones(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)])))
#reM2018BEn.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],numpy.ones(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)])))
#reMBEn.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],numpy.ones(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)])))
#genBE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),genMass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],numpy.ones(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)])))
#genBE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),genMass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],numpy.ones(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)])))
#genBE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),genMass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],numpy.ones(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)])))
#recBE.FillN(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)]),mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)],numpy.ones(len(mass2018[(eta2018[:,0]>1.2)|(eta2018[:,1]>1.2)])))
#recBE.FillN(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)]),mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)],numpy.ones(len(mass2017[(eta2017[:,0]>1.2)|(eta2017[:,1]>1.2)])))
#recBE.FillN(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)]),mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)],numpy.ones(len(mass2016[(eta2016[:,0]>1.2)|(eta2016[:,1]>1.2)])))

c1=ROOT.TCanvas("c1","c1",800,800)
reM2016BBn.GetXaxis().SetTitle("Gen Mass")
reM2016BBn.GetYaxis().SetTitle("Rec Mass")
c1.SetLogy()
c1.SetLogx()
for i in range(reM2016BB.GetNbinsX()+2):
	norm=0
	for j in range(reM2016BB.GetNbinsX()+2):
		norm+=reM2016BB.GetBinContent(j,i)
	for j in range(reM2016BB.GetNbinsX()+2):
		val=reM2016BB.GetBinContent(j,i)
		if norm !=0 and val !=0:
			val=val/norm
		reM2016BBn.SetBinContent(j,i,val)
reM2016BBn.Draw("COLZ")
c1.Print("reM/response_matrix_2016BB.pdf")
c2=ROOT.TCanvas("c2","c2",800,800)
c2.SetLogy()
c2.SetLogx()
for i in range(reM2016BE.GetNbinsX()+2):
	norm=0
        for j in range(reM2016BE.GetNbinsX()+2):
                norm+=reM2016BE.GetBinContent(j,i)
	for j in range(reM2016BE.GetNbinsX()+2):
                val=reM2016BE.GetBinContent(j,i)
		if norm !=0 and val !=0:
                	val=val/norm
                reM2016BEn.SetBinContent(j,i,val)
reM2016BEn.GetYaxis().SetTitle("Gen Mass")
reM2016BEn.GetXaxis().SetTitle("Rec Mass")
reM2016BEn.Draw("COLZ")
c2.Print("reM/response_matrix_2016BE.pdf")

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
                	val=val/norm
                reM2017BBn.SetBinContent(j,i,val)
reM2017BBn.GetYaxis().SetTitle("Gen Mass")
reM2017BBn.GetXaxis().SetTitle("Rec Mass")
reM2017BBn.Draw("COLZ")
c3.Print("reM/response_matrix_2017BB.pdf")

c4=ROOT.TCanvas("c4","c4",800,800)
c4.SetLogy()
c4.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
	norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2017BE.GetBinContent(j,i)
	for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2017BE.GetBinContent(j,i)
		if norm !=0 and val !=0:
                	val=val/norm
                reM2017BEn.SetBinContent(j,i,val)
reM2017BEn.GetYaxis().SetTitle("Gen Mass")
reM2017BEn.GetXaxis().SetTitle("Rec Mass")
reM2017BEn.Draw("COLZ")
c4.Print("reM/response_matrix_2017BE.pdf")

c5=ROOT.TCanvas("c5","c5",800,800)
reM2018BBn.GetYaxis().SetTitle("Gen Mass")
reM2018BBn.GetXaxis().SetTitle("Rec Mass")
c5.SetLogy()
c5.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
	norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2018BB.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2018BB.GetBinContent(j,i)
		if norm !=0 and val !=0:
                	val=val/norm
                reM2018BBn.SetBinContent(j,i,val)

reM2018BBn.Draw("COLZ")
c5.Print("reM/response_matrix_2018BB.pdf")

c6=ROOT.TCanvas("c6","c6",800,800)
c6.SetLogy()
c6.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
	norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reM2018BE.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reM2018BE.GetBinContent(j,i)
		if norm !=0 and val !=0:
                	val=val/norm
                reM2018BEn.SetBinContent(j,i,val)

reM2018BEn.GetYaxis().SetTitle("Gen Mass")
reM2018BEn.GetXaxis().SetTitle("Rec Mass")
reM2018BEn.Draw("COLZ")
c6.Print("reM/response_matrix_2018BE.pdf")

c7=ROOT.TCanvas("c7","c7",800,800)
c7.SetLogy()
c7.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
	norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reMBB.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reMBB.GetBinContent(j,i)
		if norm !=0 and val !=0:
                	val=val/norm
                reMBBn.SetBinContent(j,i,val)

reMBBn.GetYaxis().SetTitle("Gen Mass")
reMBBn.GetXaxis().SetTitle("Rec Mass")
reMBBn.Draw("COLZ")
c7.Print("reM/response_matrix_run2BB.pdf")

c8=ROOT.TCanvas("c8","c8",800,800)
c8.SetLogy()
c8.SetLogx()
for i in range(reM2017BB.GetNbinsX()+2):
	norm=0
        for j in range(reM2017BB.GetNbinsX()+2):
                norm+=reMBE.GetBinContent(j,i)
        for j in range(reM2017BB.GetNbinsX()+2):
                val=reMBE.GetBinContent(j,i)
		if norm !=0 and val !=0:
                	val=val/norm
                reMBEn.SetBinContent(j,i,val)

reMBEn.GetYaxis().SetTitle("Gen Mass")
reMBEn.GetXaxis().SetTitle("Rec Mass")
reMBEn.Draw("COLZ")
c8.Print("reM/response_matrix_run2BE.pdf")
f=ROOT.TFile("ResponseMatrix.root","RECREATE")
reMBB.Write()
reMBE.Write()
reMBBn.Write()
reMBEn.Write()
genBB.Write()
genBE.Write()
recBB.Write()
recBE.Write()
f.Close()
