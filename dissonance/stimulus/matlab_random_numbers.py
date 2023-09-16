import os
os.environ["LD_LIBRARY_PATH"]="/usr/local/MATLAB/MATLAB_Runtime/R2023a/runtime/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2023a/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2023a/sys/os/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2023a/extern/bin/glnxa64:/usr/local/MATLAB/MATLAB_Runtime/R2023a/sys/opengl/lib/glnxa64"

import numpy as np
import standardNormal
import matlab


class MatlabRNorm:
    def __init__(self):
        self.sn = standardNormal.initialize()

    def sample(self, seed, m:int, n:int) -> np.ndarray:
        seed = matlab.int32([seed], size=(1, 1))
        M = matlab.int32([m], size=(1,1))
        N = matlab.int32([n], size=(1,1))
        yOut = self.sn.standardNormal(seed, M, N)
        return np.asarray(yOut)

    def __enter__(self):
        self.sn = standardNormal.initialize()
        return self

    def __exit__(self, ext, exv, trb):
        self.sn.terminate()

    def __del__(self):
        self.sn.terminate()


