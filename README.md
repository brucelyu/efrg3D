# Entanglement Filtering Renormalization Group in 3D
We demonstrate how to implement an entanglement-filtering-enhanced tensor-network renormalization group (TNRG) in 3D.
The scheme is applied to the 3D Ising model to estimate its scaling dimensions from the linearized RG map.

## How to run the scripts
We run the three scripts to estimate the scaling dimensions of the 3D Ising model
- `bisectTc.py` uses bisection method to estimate the critical temperature $T_c$ by checking whether a RG flow reaches the high-$T$ or the low-$T$ fixed-point tensor.
