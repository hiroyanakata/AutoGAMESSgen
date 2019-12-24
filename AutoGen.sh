#!/bin/bash
#PJM -L "rscunit=ito-a"
#PJM -L "rscgrp=ito-s-dbg"
#PJM -L "vnode=1"
#PJM -L "vnode-core=36"
#PJM -L "elapse=30:00"
#PJM -j
#PJM -S

LANG=C

export I_MPI_ADJUST_ALLREDUCE=7
export I_MPI_HYDRA_BOOTSTRAP_EXEC=pjrsh
export I_MPI_DEVICE=rdma
export I_MPI_PERHOST=36
export I_MPI_DEBUG=5

#/home/usr0/n70210a/GAMESS.third/rungms  68240      00 36 36
python  AutoGen.v00.py  list
