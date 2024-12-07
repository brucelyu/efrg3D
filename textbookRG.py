#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : textbookRG.py
# Author            : Xinliang(Bruce) Lyu <lyu@issp.u-tokyo.ac.jp>
# Date              : 23.02.2023
# Last Modified Date: 23.02.2023
# Last Modified By  : Xinliang(Bruce) Lyu <lyu@issp.u-tokyo.ac.jp>
"""
Given the RG flow at criticality,
linearize the RG map and extract scaling dimensions
"""
import argparse
from tensornetworkrg import rg3d_pres as rg3d

# argument parser
argdesp = ("Extract scaling dimensions from linearzed RG map")
parser = argparse.ArgumentParser(description=argdesp)
parser.add_argument("--scheme", type=str,
                    help="TNRG scheme (default is --hotrg3d--)",
                    default="hotrg3d")
parser.add_argument("--ver", type=str,
                    help="TNRG scheme version (default is --base--)",
                    default="base")
parser.add_argument("--chi", type=int,
                    help="bond dimension (default: 2)",
                    default=2)
parser.add_argument("--chis", type=int,
                    help="Cube-filtering bond dimension",
                    default=4)
parser.add_argument("--chiM", type=int,
                    help="intermediate bond dimension (default: 2)",
                    default=2)
parser.add_argument("--chiMs", type=int,
                    help="Loop-filtering bond dimension",
                    default=4)
parser.add_argument("--rgstart", type=int,
                    help="starting RG step (default: 1)",
                    default=1)
parser.add_argument("--rgend", type=int,
                    help="ending RG step (default: 8)",
                    default=8)
parser.add_argument("--sectorChoice", type=str,
                    help="spin-sector (default is --both--)",
                    default="both",
                    choices=["both", "even", "odd"])
parser.add_argument("--reflChoice", type=str,
                    help="reflection-sector (default is --000--)",
                    default="000",
                    choices=["000",
                             "100", "010", "001",
                             "110", "101", "011"
                             ]
                    )
parser.add_argument("--outDir", type=str,
                    help="output directory to save rg flows and Tc",
                    default="./")
parser.add_argument("--isParal",
                    help="whether to use parallel computation codes",
                    action="store_true")

# read argument
args = parser.parse_args()
scheme = args.scheme
ver = args.ver
chi = args.chi
chis = args.chis
chiM = args.chiM
chiMs = args.chiMs
rgstart = args.rgstart
rgend = args.rgend
sectorChoice = args.sectorChoice
reflChoice = args.reflChoice
outDir = args.outDir
isParal = args.isParal

# take care of the parallelization
if isParal:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
else:
    comm = None
    rank = 0

if scheme == "hotrg3d":
    pars = {"isZ2": True, "rg_n": 0,
            "chi": chi, "cg_eps": 1e-8, "display": False,
            "dataDir": None, "determPhase": False}
elif scheme == "blockHOTRG":
    pars = {"isZ2": True, "rg_n": 0,
            "chi": chi, "chiM": chi, "chiI": chi, "chiII": chi,
            "cg_eps": 1e-8, "display": False,
            "dataDir": None, "determPhase": False}
elif scheme == "efrg":
    if ver == "base":
        pars = {"isZ2": True, "rg_n": 0,
                "chi": chi, "chis": chis, "chiM": chiM,
                "display": False,
                "dataDir": None, "determPhase": False}
    elif ver == "bistage":
        pars = {"isZ2": True, "rg_n": 0,
                "chi": chi, "chis": chis, "chiM": chiM, "chiMs": chiMs,
                "display": False,
                "dataDir": None, "determPhase": False}

# extracting scaling dimensions
if sectorChoice == "both":
    rg3d.linRG2scaleD(scheme, ver, pars,
                      rgstart, rgend, evenN=10, oddN=10,
                      outDir=outDir, comm=comm)
else:
    scaleNDic = {"even000": 7, "odd000": 5,
                 "even100": 3, "odd100": 4,
                 "even010": 3, "odd010": 4,
                 "even001": 3, "odd001": 4,
                 "even110": 2, "odd110": 2,
                 "even101": 2, "odd101": 2,
                 "even011": 2, "odd011": 2
                 }
    curSector = "{:s}{:s}".format(sectorChoice, reflChoice)
    rg3d.linRG2scaleD1rg(scheme, ver, pars,
                         rgn=rgstart, scaleN=scaleNDic[curSector],
                         outDir=outDir, comm=comm,
                         sectorChoice=sectorChoice,
                         reflChoice=reflChoice)
