#=======================================================================
# SRAM_test.py
#=======================================================================
# Unit Tests for SRAM model

import pytest
import random

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from sram.SRAM import SRAM

#-------------------------------------------------------------------------
# SRAM to be tested
#-------------------------------------------------------------------------
# If you add a new SRAM, make sure add it here to test it.

sram_configs = [ (16, 32), (32, 256), (128, 256) ]

# ''' TUTORIAL TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''
# Add (64,64) configuration to sram_configs
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# We define the header string here since it is so long. Then reference
# the header string and include a comment to label each of the columns.

header_str = \
  ( "port0_val",  "port0_type",  "port0_idx",
    "port0_wben", "port0_wdata", "port0_rdata*" )

#-----------------------------------------------------------------------
# Directed test for 16x32 SRAM
#-----------------------------------------------------------------------

def test_direct_16x32( cmdline_opts ):
  run_test_vector_sim( SRAM(16, 32), [ header_str,
    # val type idx  wben  wdata   rdata
    [ 1,  1,   0x0, 0b11, 0x0000, '?'    ], # one at a time
    [ 1,  0,   0x0, 0b11, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b11, 0x0000, 0x0000 ],
    [ 1,  1,   0x0, 0b11, 0xbeef, '?'    ],
    [ 1,  0,   0x0, 0b11, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b11, 0x0000, 0xbeef ],
    [ 1,  1,   0x1, 0b11, 0xcafe, '?'    ],
    [ 1,  0,   0x1, 0b11, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b11, 0x0000, 0xcafe ],
    [ 1,  1,   0xf, 0b11, 0x0a0a, '?'    ],
    [ 1,  0,   0xf, 0b11, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b11, 0x0000, 0x0a0a ],

    [ 1,  1,   0xe, 0b11, 0x0b0b, '?'    ], # streaming reads
    [ 1,  0,   0xe, 0b11, 0x0000, '?'    ],
    [ 1,  0,   0xf, 0b11, 0x0000, 0x0b0b ],
    [ 1,  0,   0x1, 0b11, 0x0000, 0x0a0a ],
    [ 1,  0,   0x0, 0b11, 0x0000, 0xcafe ],
    [ 0,  0,   0x0, 0b11, 0x0000, 0xbeef ],

    [ 1,  1,   0xd, 0b11, 0x0c0c, '?'    ], # streaming writes/reads
    [ 1,  0,   0xd, 0b11, 0x0000, '?'    ],
    [ 1,  1,   0xc, 0b11, 0x0d0d, 0x0c0c ],
    [ 1,  0,   0xc, 0b11, 0x0000, '?'    ],
    [ 1,  1,   0xb, 0b11, 0x0e0e, 0x0d0d ],
    [ 1,  0,   0xb, 0b11, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b11, 0x0000, 0x0e0e ],

    [ 1,  1,   0x0, 0b11, 0x0000, '?'    ], # partial writes
    [ 1,  1,   0x1, 0b11, 0x0000, '?'    ],
    [ 1,  1,   0xf, 0b11, 0x0000, '?'    ],
    [ 1,  1,   0x0, 0b01, 0xbeef, '?'    ],
    [ 1,  0,   0x0, 0b00, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b00, 0x0000, 0x00ef ],
    [ 1,  1,   0x1, 0b10, 0xcafe, '?'    ],
    [ 1,  0,   0x1, 0b00, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b00, 0x0000, 0xca00 ],
    [ 1,  1,   0xf, 0b00, 0x0a0a, '?'    ],
    [ 1,  0,   0xf, 0b00, 0x0000, '?'    ],
    [ 0,  0,   0x0, 0b00, 0x0000, 0x0000 ],
], cmdline_opts )

#-----------------------------------------------------------------------
# Directed test for 32x256 SRAM
#-----------------------------------------------------------------------

def test_direct_32x256( cmdline_opts ):
  run_test_vector_sim( SRAM(32, 256), [ header_str,
    # val type idx  wben    wdata       rdata
    [ 1,  1,  0x00, 0b1111, 0x00000000, '?'        ], # one at a time
    [ 1,  0,  0x00, 0b1111, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b1111, 0x00000000, 0x00000000 ],
    [ 1,  1,  0x00, 0b1111, 0xdeadbeef, '?'        ],
    [ 1,  0,  0x00, 0b1111, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b1111, 0x00000000, 0xdeadbeef ],
    [ 1,  1,  0x01, 0b1111, 0xcafecafe, '?'        ],
    [ 1,  0,  0x01, 0b1111, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b1111, 0x00000000, 0xcafecafe ],
    [ 1,  1,  0x1f, 0b1111, 0x0a0a0a0a, '?'        ],
    [ 1,  0,  0x1f, 0b1111, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b1111, 0x00000000, 0x0a0a0a0a ],

    [ 1,  1,  0x1e, 0b1111, 0x0b0b0b0b, '?'        ], # streaming reads
    [ 1,  0,  0x1e, 0b1111, 0x00000000, '?'        ],
    [ 1,  0,  0x1f, 0b1111, 0x00000000, 0x0b0b0b0b ],
    [ 1,  0,  0x01, 0b1111, 0x00000000, 0x0a0a0a0a ],
    [ 1,  0,  0x00, 0b1111, 0x00000000, 0xcafecafe ],
    [ 0,  0,  0x00, 0b1111, 0x00000000, 0xdeadbeef ],

    [ 1,  1,  0x1d, 0b1111, 0x0c0c0c0c, '?'        ], # streaming writes/reads
    [ 1,  0,  0x1d, 0b1111, 0x00000000, '?'        ],
    [ 1,  1,  0x1c, 0b1111, 0x0d0d0d0d, 0x0c0c0c0c ],
    [ 1,  0,  0x1c, 0b1111, 0x00000000, '?'        ],
    [ 1,  1,  0x1b, 0b1111, 0x0e0e0e0e, 0x0d0d0d0d ],
    [ 1,  0,  0x1b, 0b1111, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b1111, 0x00000000, 0x0e0e0e0e ],

    [ 1,  1,  0x00, 0b1111, 0x00000000, '?'        ], # partial writes
    [ 1,  1,  0x01, 0b1111, 0x00000000, '?'        ],
    [ 1,  1,  0x0f, 0b1111, 0x00000000, '?'        ],
    [ 1,  1,  0x00, 0b0001, 0xdeadbeef, '?'        ],
    [ 1,  0,  0x00, 0b0000, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b0000, 0x00000000, 0x000000ef ],
    [ 1,  1,  0x01, 0b0100, 0xcafecafe, '?'        ],
    [ 1,  0,  0x01, 0b0000, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b0000, 0x00000000, 0x00fe0000 ],
    [ 1,  1,  0x0f, 0b0000, 0x0a0a0a0a, '?'        ],
    [ 1,  0,  0x0f, 0b0000, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b0000, 0x00000000, 0x00000000 ],
], cmdline_opts )

#-----------------------------------------------------------------------
# Directed test for 128x256 SRAM
#-----------------------------------------------------------------------

def test_direct_128x256( cmdline_opts ):
  run_test_vector_sim( SRAM(128, 256), [ header_str,
    # val type idx  wben    wdata       rdata
    [ 1,  1,  0x00, 0xffff, 0x00000000, '?'        ], # one at a time
    [ 1,  0,  0x00, 0xffff, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0xffff, 0x00000000, 0x00000000 ],
    [ 1,  1,  0x00, 0xffff, 0xdeadbeef, '?'        ],
    [ 1,  0,  0x00, 0xffff, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0xffff, 0x00000000, 0xdeadbeef ],
    [ 1,  1,  0x01, 0xffff, 0xcafecafe, '?'        ],
    [ 1,  0,  0x01, 0xffff, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0xffff, 0x00000000, 0xcafecafe ],
    [ 1,  1,  0x2f, 0xffff, 0x0a0a0a0a, '?'        ],
    [ 1,  0,  0x2f, 0xffff, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0xffff, 0x00000000, 0x0a0a0a0a ],

    [ 1,  1,  0x2e, 0xffff, 0x0b0b0b0b, '?'        ], # streaming reads
    [ 1,  0,  0x2e, 0xffff, 0x00000000, '?'        ],
    [ 1,  0,  0x2f, 0xffff, 0x00000000, 0x0b0b0b0b ],
    [ 1,  0,  0x01, 0xffff, 0x00000000, 0x0a0a0a0a ],
    [ 1,  0,  0x00, 0xffff, 0x00000000, 0xcafecafe ],
    [ 0,  0,  0x00, 0xffff, 0x00000000, 0xdeadbeef ],

    [ 1,  1,  0x2d, 0xffff, 0x0c0c0c0c, '?'        ], # streaming writes/reads
    [ 1,  0,  0x2d, 0xffff, 0x00000000, '?'        ],
    [ 1,  1,  0x2c, 0xffff, 0x0d0d0d0d, 0x0c0c0c0c ],
    [ 1,  0,  0x2c, 0xffff, 0x00000000, '?'        ],
    [ 1,  1,  0x2b, 0xffff, 0x0e0e0e0e, 0x0d0d0d0d ],
    [ 1,  0,  0x2b, 0xffff, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0xffff, 0x00000000, 0x0e0e0e0e ],

    [ 1,  1,  0x00, 0b1111, 0x00000000, '?'        ], # partial writes
    [ 1,  1,  0x01, 0b1111, 0x00000000, '?'        ],
    [ 1,  1,  0x0f, 0b1111, 0x00000000, '?'        ],
    [ 1,  1,  0x00, 0b0001, 0xdeadbeef, '?'        ],
    [ 1,  0,  0x00, 0b0000, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b0000, 0x00000000, 0x000000ef ],
    [ 1,  1,  0x01, 0b0100, 0xcafecafe, '?'        ],
    [ 1,  0,  0x01, 0b0000, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b0000, 0x00000000, 0x00fe0000 ],
    [ 1,  1,  0x0f, 0b0000, 0x0a0a0a0a, '?'        ],
    [ 1,  0,  0x0f, 0b0000, 0x00000000, '?'        ],
    [ 0,  0,  0x00, 0b0000, 0x00000000, 0x00000000 ],
], cmdline_opts )

# ''' TUTORIAL TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''
# Add directed test for 32x128 configuration
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# Random testing
#-------------------------------------------------------------------------

def gen_rand_tvec( data_nbits, num_entries ):

  rgen = random.Random()
  rgen.seed(0xdeadbeef)

  num_tests = 100

  # enable all bytes
  wben_all = (2**(data_nbits//8))-1

  test_vectors = [ header_str,
    # val type addr wben      wdata       rdata
    [ 1,  0,   0,   wben_all, 0x00000000, '?'        ],
    [ 1,  0,   0,   wben_all, 0x00000000, '?'        ],
  ]

  for i in range(num_tests):
    addr  = rgen.randint( 0, num_entries-1 )
    wdata = rgen.randint( 0, (2**data_nbits)-1 )

    #           val type addr  wben      wdata  rdata
    vec_wr  = [ 1,  1,   addr, wben_all, wdata, '?'   ]
    vec_rd0 = [ 1,  0,   addr, wben_all, 0x0,   '?'   ]
    vec_rd1 = [ 1,  0,   addr, wben_all, 0x0,   wdata ]

    test_vectors.append( vec_wr  )
    test_vectors.append( vec_rd0 )
    test_vectors.append( vec_rd1 )

  return test_vectors

#-----------------------------------------------------------------------
# random test
#-----------------------------------------------------------------------

@pytest.mark.parametrize(("data_nbits", "num_entries"), sram_configs )
def test_random( cmdline_opts, data_nbits, num_entries):
  run_test_vector_sim( SRAM(data_nbits, num_entries),
                       gen_rand_tvec(data_nbits, num_entries),
                       cmdline_opts )

