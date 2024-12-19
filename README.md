# Entanglement Filtering Renormalization Group in 3D
We demonstrate how to implement an entanglement-filtering-enhanced tensor-network renormalization group (TNRG) in 3D.
The scheme is applied to the 3D Ising model to estimate its scaling dimensions from the linearized RG map.
We call it **Entanglemeng Filtering Renormalizaiong Group (EFRG)** here.
This 3D real space RG method is introduced in our preprint [Three-dimensional real space renormalization group with well-controlled approximations](https://arxiv.org/abs/2412.13758).

This repostory contains three scripts for obatining a critical fixed-point tensor of the 3D Ising model and estimating scaling dimensions from the linearized RG map, as well as an addition script for plotting the scaling dimensions.
The implementation of the tensor RG map is in another repository [tensornetworkrg](https://github.com/brucelyu/tensornetworkrg), which is included here as a submodule.
Therefore, after cloning this repository to your computer, remember using the following command to pull from the submodule:
 ```console
 git submodule update --init --recursive
 ```

## I. Requirements
The codes are written in Python.
The standard tool kit for scientific computating for python is [Ananconda](https://www.anaconda.com/download/).
In addition, we need the following packages for tensor network manipulations:
- [ncon](https://github.com/mhauru/ncon), for tensor network contractions
- [abeliantensors](https://github.com/mhauru/abeliantensors), for imposing $\mathbb{Z}_2$ spin-flip symmetry of the Ising model
- [tn-tools](https://github.com/mhauru/tntools), for producing the initial tensor of the Ising model


## II. How to run the scripts
We run the three scripts to estimate the scaling dimensions of the 3D Ising model.
This procedure is established in [our 2021 paper](https://arxiv.org/abs/2102.08136) and its [companion GitHub repository](https://github.com/brucelyu/tensorRGflow).
- `bisectTc.py` uses bisection method to estimate the critical temperature $T_c$ by checking whether a RG flow reaches the high-T or the low-T fixed-point tensor. This script outputs the estimated $T_c$ as a file `Tc.pkl`.
- `flow2FixTen.py` reads the `Tc.pkl` and generate the tensor RG flow at this estimated $T_c$. The tensors will be saved to the disk.
- `textbookRG.py` reads the tensors from the tensor RG flow , constructs the linearized RG map, and extracts scaling dimensions.
- `plotScD.py` plots the scaling dimensions versus the RG step.

## III. An example
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

## IV. More explanations
All procedures are implemented in the submodule [tensornetworkrg](https://github.com/brucelyu/tensornetworkrg).
The three scripts, `bisectTc.py`, `flow2FixTen.py` and `textbookRG.py`, call functions implemented in the module `tensornetworkrg.rg3d_pres`, which we refer to as `rg3d`.
The most relevant code in each file is essential a single line:

```python
from tensornetworkrg import rg3d_pres as rg3d

# For finding Tc using `bisectTc.py`
rg3d.findTc(...)

# For generating the tensor RG flow at Tc using `flow2FixTen.py`
rg3d.generateRGflow(...)

# For extracting scaling dimensions from the linearized RG using `textbookRG.py`
rg3d.linRG2scaleD(...)    # all symmetry sectors and for several RG steps
# When it is run on a supercomputer to push to the largest bond dimension
rg3d.linRG2scaleD1rg(...) # A single RG step and a specified symmetry sector 
```

### IV.1. Generating tensor RG flows
For easier description, we import some modules from the package `tensornetworkrg`:
```python
from tensornetworkrg import rg3d_pres as rg3d
from tensornetworkrg import tnrg
from tensornetworkrg import benchmark
```
The two functions `rg3d.findTc` and `rg3d.generateRGflow` call the function `benchmark.tnrg3dIterate(...)` to generate tensor RG flows by applying the tensor RG map repeatedly.
In this function, we input an instance of the class `tnrg.TensorNetworkRG3D`.
The EFRG map is implemented as a method of this class.
In summary,
- ***The EFRG map is implemented in the method `tnrg.TensorNetworkRG3D.entfree_blockrg` of the class `tnrg.TensorNetworkRG3D`.***
- This map is called repeatedly in the function `benchmark.tnrg3dIterate(tnrg3dCase,...)`, where `tnrg3dCase` is an instance of the class `tnrg.TensorNetworkRG3D`. The basic structure of this is
    ```python
    # The basic structure of the function `benchmark.tnrg3dIterate(tnrg3dCase,...)`
    scheme = "efrg"
    for k in range(rg_n):
        # other codes
        (
        lrerrs, SPerrs # entanglement filtering errors and the block-tensor errors
        ) = tnrg3dCase.rgmap(scheme=scheme, ...)
        # other codes
    ```

### IV.2. Linearizing the RG map 
The function `rg3d.linRG2scaleD ` calls `rg3d.linRG2x` at each RG step.
The basic structure of `rg3d.linRG2x` is
```python
from tensornetworkrg import tnrg
# construct linearized RG map
ising3d = tnrg.TensorNetworkRG3D("ising3d")
linearRGSet = ising3d.linear_block_hotrg(isEF=True, ...)
# diagonalize the linearized RG map to estimate scaling dimensions
scDims = ising3d.linearRG2scaleD(linearRGSet, ...)
```
The method `.linear_block_hotrg(isEF=True, ...)` uses the function `tensornetworkrg.coarse_grain_3d.efrg.linrgmap` to build the linearized RG map.
