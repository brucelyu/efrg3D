#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : plotScD.py
# Author            : Xinliang(Bruce) Lyu <lyu@issp.u-tokyo.ac.jp>
# Date              : 25.09.2023
# Last Modified Date: 25.09.2023
# Last Modified By  : Xinliang(Bruce) Lyu <lyu@issp.u-tokyo.ac.jp>
import argparse
import tensornetworkrg.rg3d_pres as rg3d
import pickle as pkl
import matplotlib.pyplot as plt

# argument parser
argdesp = ("Extract scaling dimensions from linearzed RG map")
parser = argparse.ArgumentParser(description=argdesp)
parser.add_argument("--scheme", type=str,
                    help="TNRG scheme (default is --blockHOTRG--)",
                    default="blockHOTRG")
parser.add_argument("--ver", type=str,
                    help="TNRG scheme version (default is --base--)",
                    default="base")
parser.add_argument("--chi", type=int,
                    help="bond dimension (default: 2)",
                    default=2)
parser.add_argument("--chis", type=int,
                    help="Entanglement filtering bond dimension",
                    default=4)
parser.add_argument("--chiM", type=int,
                    help="intermediate bond dimension (default: 2)",
                    default=2)
parser.add_argument("--chiMs", type=int,
                    help="Loop-filtering bond dimension",
                    default=4)
parser.add_argument("--startn", type=int,
                    help="starting RG step (default: 1)",
                    default=0)
parser.add_argument("--endn", type=int,
                    help="ending RG step (default: 8)",
                    default=None)
parser.add_argument("--isParal",
                    help="whether to use parallel computation codes",
                    action="store_true")


# function for plotting in a single spin-flip sector
def plotSpinSector(figax, rgsteps, scDList,
                   shift100, shift010, shift001, shift110, shift101, shift011,
                   sector000Shift, sector000Color, sector000Marker,
                   sector100Shift, sector100Color, sector100Marker,
                   sector110Shift, sector110Color, sector110Marker,
                   spinchg=0, NumPlot=[7, 3, 2]):
    for rgn, scD in zip(rgsteps, scDList):
        [
            scD000, scD100, scD010, scD001, scD110, scD101, scD011
        ] = scD
        for k in range(NumPlot[0]):
            # lattice-reflection (000)
            figax.plot(rgn + sector000Shift[k], scD000[spinchg][k],
                       sector000Color[k] + sector000Marker[k])
            # Relative error of first two primary fields
            if spinchg == 0:
                # energy density operator ε
                e_best = 1.412625
                e_est = scD000[spinchg][1]
                eErr = abs(e_est - e_best) / e_best
                plt.text(rgn + 0.06, e_est, "{:.1%}".format(eErr),
                         size=14)
            elif spinchg == 1:
                # spin operator σ
                s_best = 0.5181489
                s_est = scD000[spinchg][0]
                sErr = abs(s_est - s_best) / s_best
                plt.text(rgn + 0.06, s_est, "{:.1%}".format(sErr),
                         size=14)
        for k in range(NumPlot[1]):
            # lattice-reflection (100)
            figax.plot(rgn + shift100 + sector100Shift[k], scD100[spinchg][k],
                       sector100Color[k] + sector100Marker[k])
            # lattice-reflection (010)
            figax.plot(rgn + shift010 + sector100Shift[k], scD010[spinchg][k],
                       sector100Color[k] + sector100Marker[k])
            # lattice-reflection (001)
            figax.plot(rgn + shift001 + sector100Shift[k], scD001[spinchg][k],
                       sector100Color[k] + sector100Marker[k])
        for k in range(NumPlot[2]):
            # lattice-reflection (110)
            figax.plot(rgn + shift110 + sector110Shift[k], scD110[spinchg][k],
                       sector110Color[k] + sector110Marker[k])
            # lattice-reflection (101)
            figax.plot(rgn + shift101 + sector110Shift[k], scD101[spinchg][k],
                       sector110Color[k] + sector110Marker[k])
            # lattice-reflection (011)
            figax.plot(rgn + shift011 + sector110Shift[k], scD011[spinchg][k],
                       sector110Color[k] + sector110Marker[k])


# read argument
args = parser.parse_args()
scheme = args.scheme
ver = args.ver
chi = args.chi
chis = args.chis
chiM = args.chiM
chiMs = args.chiMs
startn = args.startn
endn = args.endn
isParal = args.isParal

# take care of the parallelization
if isParal:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
else:
    comm = None
    rank = 0

# read scaling dimensions data
saveDir = rg3d.saveDirName(
    scheme, ver, {"chi": chi, "chis": chis, "chiM": chiM, "chiMs": chiMs},
    "./", comm
)
tenDir = rg3d.tensorsDir(saveDir)
scDFile = tenDir + "/scDimSep.pkl"
with open(scDFile, "rb") as f:
    rgsteps, scDList = pkl.load(f)

# slice part of the RG flow
rgsteps = rgsteps[startn:endn]
scDList = scDList[startn:endn]


# ---PLOT and save the figure---
# markers
# I.1 Spin-flip EVEN && lattice-reflection (000)
even000Marker = [".", "*", "s", "s", "x", "x", "x"]
even000Color = ["k", "k", "k", "k", "b", "b", "b"]
even000Shift = [0, 0, -0.03, 0.03, -0.03, 0, 0.03]
# I.2 Spin-flip EVEN && lattice-reflection (100) and two alikes
even100Marker = ["+", "1", "1"]
even100Color = ["b", "b", "b"]
even100Shift = [0, -0.01, 0.01]
# I.3 Spin-flip EVEN && lattice-reflection (110) and two alikes
even110Marker = ["s", "x"]
even110Color = ["k", "b"]
even110Shift = [0, 0]

# II.1 Spin-flip ODD && lattice-reflection (000)
odd000Marker = [".", "x", "x", "x"]
odd000Color = ["k", "b", "b", "b"]
odd000Shift = [0, -0.03, 0, 0.03]
# II.2 Spin-flip ODD && lattice-reflection (100) and two alikes
odd100Marker = ["+", "1", "1", "1"]
odd100Color = ["b", "b", "b", "b"]
odd100Shift = [0, -0.03, 0, 0.03]
# II.2 Spin-flip ODD && lattice-reflection (110) and two alikes
odd110Marker = ["x"]
odd110Color = ["b"]
odd110Shift = [0]

# shift of reflection-reflection sectors
shift100 = 0.2 - 0.05
shift010 = 0.2
shift001 = 0.2 + 0.05
shift110 = 0.35 - 0.05
shift101 = 0.35
shift011 = 0.35 + 0.05

plt.figure(figsize=(12, 8))
# I. Spin-flip EVEN
ax1 = plt.subplot(211)
plotSpinSector(ax1, rgsteps, scDList,
               shift100, shift010, shift001, shift110, shift101, shift011,
               even000Shift, even000Color, even000Marker,
               even100Shift, even100Color, even100Marker,
               even110Shift, even110Color, even110Marker,
               spinchg=0, NumPlot=[7, 3, 2]
               )

# best-known values
plt.hlines(1.412625, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="black", linestyles="dashed", alpha=0.2)
plt.hlines(2.412625, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="blue", linestyles="dashed", alpha=0.2)
plt.hlines(3, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="black", linestyles="dashed", alpha=0.2)
plt.hlines(3.412625, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="blue", linestyles="dashed", alpha=0.2)
plt.hlines(4.000000, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="blue", linestyles="dashed", alpha=0.2)
# set axis ranges
plt.xticks(rgsteps)
if len(rgsteps) == 1:
    plt.xlim([rgsteps[0] - 1, rgsteps[0] + 1])
# plt.ylim([-0.1, 4.2])
plt.ylim([-0.1, 3.4])
plt.ylabel("Even sector")

arrowpps = dict(arrowstyle="->", alpha=0.2, color='blue')
# Put explanations on the figure
plt.text(rgsteps[0] - 0.06, 1.41 + 0.10, r"$\epsilon$", size=14)
plt.text(rgsteps[0] - 0.15, 3 + 0.10, r"$T_{kk}$", size=14)
plt.text(rgsteps[0] + shift011 + 0.03, 3 + 0.10, r"$T_{mn}$", size=14)
# 1) 1st descendant of ε
# plt.text(rgsteps[0] + 0.48, 2.41 - 0.25, r"$\partial_i \epsilon$",
#          size=14, color="blue")
plt.annotate("", xy=(rgsteps[0] + shift010, 2.41 - 0.02),
             xytext=(rgsteps[0], 1.41 + 0.20),
             arrowprops=arrowpps
             )
plt.text(rgsteps[0] + 0.15*shift010, 0.5*(1.41+2.41), r"$\partial_i$",
         size=14, color="blue", alpha=0.2)
# 2) 2nd descendant of ε
# plt.text(rgsteps[0] + 0.48, 3.41 - 0.25, r"$\partial_i\partial_j \epsilon$",
#          size=14, color="blue")

# plt.annotate("", xy=(rgsteps[0] + 0.06, 3.41 - 0.02),
#              xytext=(rgsteps[0] + shift010, 2.41 + 0.10),
#              arrowprops=arrowpps
#              )
# plt.annotate("", xy=(rgsteps[0] + shift110 - 0.02, 3.41 - 0.02),
#              xytext=(rgsteps[0] + shift010, 2.41 + 0.10),
#              arrowprops=arrowpps
#              )

# 3) 1st descendant of Tkk
plt.annotate("", xy=(rgsteps[0] + shift010, 4.00 - 0.02),
             xytext=(rgsteps[0], 3.00 + 0.10),
             arrowprops=arrowpps
             )
# bond dimension
plt.text(rgsteps[-1] - 1, 0.5,
         r"Bond dimension $\chi$={:d}".format(chi),
         fontsize=14)


# II. Spin-flip ODD
ax2 = plt.subplot(212)
plotSpinSector(ax2, rgsteps, scDList,
               shift100, shift010, shift001, shift110, shift101, shift011,
               odd000Shift, odd000Color, odd000Marker,
               odd100Shift, odd100Color, odd100Marker,
               odd110Shift, odd110Color, odd110Marker,
               spinchg=1, NumPlot=[4, 4, 1]
               )

# best-known values
plt.hlines(0.5181489, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="black", linestyles="dashed", alpha=0.2)
plt.hlines(1.5181489, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="blue", linestyles="dashed", alpha=0.2)
plt.hlines(2.5181489, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="blue", linestyles="dashed", alpha=0.2)
plt.hlines(3.5181489, rgsteps[0]-0.2, rgsteps[-1]+0.5,
           colors="blue", linestyles="dashed", alpha=0.2)
# set axis ranges
plt.xticks(rgsteps)
# plt.ylim([-0.1, 4.0])
plt.ylim([-0.1, 3.0])
plt.ylabel("Odd sector")
plt.xlabel("RG step")

# Put explanations on the figure
plt.text(rgsteps[0] - 0.06, 0.518 + 0.10, r"$\sigma$", size=14)
# 1) 1st descendant of σ
# plt.text(rgsteps[0] + 0.45, 1.518 - 0.2, r"$\partial_i\sigma$",
#          size=14, color="blue")
plt.annotate("", xy=(rgsteps[0] + shift010, 1.518 - 0.02),
             xytext=(rgsteps[0], 0.518 + 0.10),
             arrowprops=arrowpps
             )
plt.text(rgsteps[0] + 0.15*shift010, 0.5*(0.518+1.518), r"$\partial_i$",
         size=14, color="blue", alpha=0.2)
# 2) 2nd descendant of σ
# plt.text(rgsteps[0] + 0.45, 2.518 - 0.2,
#          r"$\partial_i \partial_j \sigma$", size=14, color="blue")
plt.annotate("", xy=(rgsteps[0] + 0.06, 2.518 - 0.02),
             xytext=(rgsteps[0] + shift010, 1.518 + 0.10),
             arrowprops=arrowpps
             )
plt.annotate("", xy=(rgsteps[0] + shift110 - 0.02, 2.518 - 0.02),
             xytext=(rgsteps[0] + shift010, 1.518 + 0.10),
             arrowprops=arrowpps
             )
# 3) 3rd descendant of σ
# plt.annotate("", xy=(rgsteps[0] + shift010, 3.518 - 0.02),
#              xytext=(rgsteps[0], 2.518 + 0.10),
#              arrowprops=arrowpps
#              )

if rank == 0:
    plt.savefig(saveDir + "/scDim.png",
                bbox_inches='tight', dpi=300)
