\ Model NLP
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  pnot_x1
Subject To
 R0: x1 + pnot_x1 >= 1
 R1: pnot_x1 >= 1
 R2: pnot_x1 <= 1
 R3: (x1_pand_x2) >= 0
 R4: (x1_pand_x2) <= 0
 R5: - x1 + x2 + _x1 >= 0
 R6: x1 - x2 - _x1 >= -1
 R7: (x1_pimp_x2) >= 0
 R8: (x1_pimp_x2) <= 1
 qc0: (x1_pand_x2) + [ - x1 * x2 ] = 0
 qc1: (x1_pimp_x2) + _x1 + [ - _x1 * _x2 ] = 1
 qc2: - x2 + [ x1 * _x2 ] = 0
Bounds
 x1 <= 1
 x2 <= 1
 (x1_pand_x2) <= 1
 (x1_pimp_x2) <= 1
 _x2 <= 1
Binaries
 pnot_x1 _x1
End
