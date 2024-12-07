#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : bisectTc.py
# Author            : Xinliang(Bruce) Lyu <lyu@issp.u-tokyo.ac.jp>
# Date              : 21.02.2023
# Last Modified Date: 10.08.2023
# Last Modified By  : Xinliang(Bruce) Lyu <lyu@issp.u-tokyo.ac.jp>
import argparse
from tensornetworkrg import rg3d_pres as rg3d
from datetime import datetime
from dateutil.relativedelta import relativedelta

# argument parser
argdesp = ("Find critical temperature given---" +
           "1) 3D TNRG scheme and 2) bond dimension")
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
parser.add_argument("--rgn", type=int,
                    help="maximal rg iteration (default: 12)",
                    default=12)
parser.add_argument("--itern", type=int,
                    help="iteration of finding the Tc (default:6)",
                    default=6)
parser.add_argument("--outDir", type=str,
                    help="output directory to save rg flows and Tc",
                    default="./")
parser.add_argument("--Tlow", type=float,
                    help="Estimated lower bound for critical temperature",
                    default=4.0)
parser.add_argument("--Thi", type=float,
                    help="Estimated higher bound for critical temperature",
                    default=5.0)
parser.add_argument("--isParal",
                    help="whether to use parallel computation codes",
                    action="store_true")

# for block-tensor RG
parser.add_argument("--chiM", type=int,
                    help="intermediate bond dimension (default: 2)",
                    default=2)
parser.add_argument("--chiI", type=int,
                    help="first inner bond dimension (default: 2)",
                    default=2)
parser.add_argument("--chiII", type=int,
                    help="second inner bond dimension (default: 2)",
                    default=2)
# for entanglement filtering
parser.add_argument("--chis", type=int,
                    help="Cube-filtering bond dimension",
                    default=4)
parser.add_argument("--chienv", type=int,
                    help="For cube-environment initial svd truncation",
                    default=16)
parser.add_argument("--epsilon", type=float,
                    help="For cube-environment initial svd truncation",
                    default=1e-6)
parser.add_argument("--chiMs", type=int,
                    help="Loop-filtering bond dimension",
                    default=4)
parser.add_argument("--chiMenv", type=int,
                    help="For loop-environment initial svd truncation",
                    default=16)
parser.add_argument("--epsilonM", type=float,
                    help="For loop-environment initial svd truncation",
                    default=1e-6)
parser.add_argument("--loopOff",
                    help="whether to turn off the loop filtering",
                    action="store_true")
parser.add_argument("--cubeOff",
                    help="whether to turn off the cube filtering",
                    action="store_true")

# read argument
args = parser.parse_args()
scheme = args.scheme
ver = args.ver
chi = args.chi
cgeps = 1e-8
rg_n = args.rgn
iter_n = args.itern
outDir = args.outDir
isParal = args.isParal


# for block-tensor RG bond dimensions
chiM = args.chiM
chiI = args.chiI
chiII = args.chiII

# For entanglement filtering
# - Cube filtering
chis = args.chis
chienv = args.chienv
init_epsilon = args.epsilon
cubeOff = args.cubeOff

# - Loop filtering
chiMs = args.chiMs
chiMenv = args.chiMenv
init_epsilonM = args.epsilonM
loopOff = args.loopOff

# take care of the parallelization
if isParal:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
else:
    comm = None
    rank = 0

if scheme == "hotrg3d":
    pars = {"isZ2": True, "rg_n": rg_n,
            "chi": chi, "cg_eps": cgeps, "display": False,
            "dataDir": None, "determPhase": True}
elif scheme == "blockHOTRG":
    pars = {"isZ2": True, "rg_n": rg_n,
            "chi": chi, "chiM": chi, "chiI": chi, "chiII": chi,
            "cg_eps": cgeps, "display": False,
            "dataDir": None, "determPhase": True}
elif scheme == "efrg":
    if ver == "base":
        pars = {"isZ2": True, "rg_n": rg_n,
                "chi": chi, "chiM": chiM, "chiI": chiI, "chiII": chiII,
                "cg_eps": cgeps, "display": False,
                "chis": chis, "chienv": chienv, "epsilon": init_epsilon,
                "dataDir": None, "determPhase": True}
    elif ver == "bistage":
        pars = {"isZ2": True, "rg_n": rg_n,
                "chi": chi, "chiM": chiM, "chiI": chiI, "chiII": chiII,
                "cg_eps": cgeps, "display": False,
                "chis": chis, "chienv": chienv, "epsilon": init_epsilon,
                "chiMs": chiMs, "chiMenv": chiMenv, "epsilonM": init_epsilonM,
                "dataDir": None, "determPhase": True,
                "cubeFilter": not cubeOff, "loopFilter": not loopOff}


Tlow = args.Tlow
Thi = args.Thi

if rank == 0:
    start_now = datetime.now()
    current_time = start_now.strftime("%Y-%m-%d. %H:%M:%S")
    print("Running Time is", current_time)
    print("Using the RG scheme {:s} with version {:s}.".format(scheme, ver))
    print("    Bond dimension is --{:d}--".format(chi))
    print("    Max RG steps is --{:d}--".format(rg_n))
    print("    Bisection iteration number is --{:d}--".format(iter_n))
    print("----------------------------------")
# find Tc
rg3d.findTc(iter_n, Tlow, Thi,
            scheme, ver,
            pars, outDir,
            comm=comm)

if rank == 0:
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d. %H:%M:%S")
    print("----------------------------------")
    print("Finished Time is", current_time)
    diffT = relativedelta(now, start_now)
    print("Elapsed wall time is {} days {} hours {} minutes {} seconds.".format(
        diffT.days, diffT.hours, diffT.minutes, diffT.seconds
    )
          )
