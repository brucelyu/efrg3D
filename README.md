# Entanglement Filtering Renormalization Group in 3D
We demonstrate how to implement an entanglement-filtering-enhanced tensor-network renormalization group (TNRG) in 3D.
The scheme is applied to the 3D Ising model to estimate its scaling dimensions from the linearized RG map.
We call it **Entanglemeng Filtering Renormalizaiong Group (EFRG)** here, which will be reported in an arXiv preprint before the end of year 2024.

This repostory contains three scripts for obatining a critical fixed-point tensor of the 3D Ising model and estimating scaling dimensions from the linearized RG map, as well as an addition script for plotting the scaling dimensions.
The implementation of the tensor RG map is in another repository [tensornetworkrg](https://github.com/brucelyu/tensornetworkrg), which is included here as a submodule.
Therefore, after cloning this repository to your computer, remember using the following command to pull from the submodule:
 ```console
 git submodule update --init --recursive
 ```

## Requirements
The codes are written in Python.
The standard tool kit for scientific computating for python is [Ananconda](https://www.anaconda.com/download/).
In addition, we need the following packages for tensor network manipulations:
- [ncon](https://github.com/mhauru/ncon), for tensor network contractions
- [abeliantensors](https://github.com/mhauru/abeliantensors), for imposing $\mathbb{Z}_2$ spin-flip symmetry of the Ising model
- [tn-tools](https://github.com/mhauru/tntools), for producing the initial tensor of the Ising model


## How to run the scripts
We run the three scripts to estimate the scaling dimensions of the 3D Ising model.
This procedure is established in [our 2021 paper](https://arxiv.org/abs/2102.08136) and its [companion GitHub repository](https://github.com/brucelyu/tensorRGflow).
- `bisectTc.py` uses bisection method to estimate the critical temperature $T_c$ by checking whether a RG flow reaches the high-T or the low-T fixed-point tensor. This script outputs the estimated $T_c$ as a file `Tc.pkl`.
- `flow2FixTen.py` reads the `Tc.pkl` and generate the tensor RG flow at this estimated $T_c$. The tensors will be saved to the disk.
- `textbookRG.py` reads the tensors from the tensor RG flow , constructs the linearized RG map, and extracts scaling dimensions.
- `plotScD.py` plots the scaling dimensions versus the RG step.

## An example
We run the algorithm to reproduce the result in the paper.
The parameter of the algorithm is $\chi=6, \chi_s=\chi_m=4$ and $\chi_i = \chi^{1.5} = 15, \chi_{ii} = \chi^2=36$.

1. To esimate $T_c$:
> note: if you want to do this calculating from scratch, delete the `efrg_base_out` folder, which contains a sample $T_c$ estimate
```
python bisectTc.py --scheme efrg --chi 6 --chiM 4 --chiI 15 --chiII 36 --chis 4 --chienv 16 --rgn 16 --itern 9 --Tlow 4.47 --Thi 4.55 --epsilon 1e-6
```
where`chienv` ($\chi_{\text{env}}$) is for initializing the filtering matrices and we simply choose $\chi_{\text{env}} = \chi_s^2$ here.
`--itern` specifies the number of iterations in the bisection method.
In our script, we choose it to be multiples of 3.
This script outputs the estimated $T_c$ into a file `efrg_base_out/chi06s4M4/Tc.pkl`.
If you want higer precision, increase this number, or run this command one more time, since it will read previous esitmated $T_c$.
Using my 2023 Macbook Pro, this scripts took about 20 minutes if `--itern` is 6.
If you are in a hurry, skip this step and use the sample `Tc.pkl` file in the next step.


2. Next, generate the tensor RG flow: 
```
python flow2FixTen.py --scheme efrg --chi 6 --chiM 4 --chiI 15 --chiII 36 --chis 4 --chienv 16  --rgn 9 --epsilon 1e-6 
```
This script reads the `efrg_base_out/chi06s4M4/Tc.pkl`, generates the RG flow and saves the tensor RG flow into files in the folder `efrg_base_out/chi06s4M4/tensors/`.
Using my 2023 Macbook Pro, this scripts too about 3 minutes.

3. Finally, esimate scaling dimensions from the linearized RG:
```
python textbookRG.py --scheme efrg  --chi 6 --chis 4 --chiM 4 --rgstart 3 --rgend 7
```
The script reads tensors in `efrg_base_out/chi06s4M4/tensors/`, constructs linearized RG map, and extracts scaling dimensions from the eigenvalues of the lienarized RG map.
Using my 2023 Macbook Pro, for each RG step, this calculation took about 40 secondes.
This script estimates at 4 RG steps, so it takes about 3 minutes.
The result is save in the file `efrg_base_out/chi06s4M4/tensors/scDimSep.pkl`.
To plot the scaling dimensions versus the RG step, do
```
python plotScD.py --scheme efrg  --chi 6 --chis 4 --chiM 4
```

## More explanations
