module top (
clock      , // clock
reset      , // Active high, syn reset
req_0      , // Request 0
req_1      , // Request 1
gnt_0      , // Grant 0
gnt_1      
);
//-------------Input Ports-----------------------------
input   clock,reset,req_0,req_1;
 //-------------Output Ports----------------------------
output  gnt_0,gnt_1;
//-------------Input ports Data Type-------------------
wire    clock,reset,req_0,req_1;
//-------------Output Ports Data Type------------------
reg     gnt_0,gnt_1;
//-------------Internal Constants--------------------------
parameter SIZE = 3;
parameter IDLE  = 3'b001,GNT0 = 3'b010,GNT1 = 3'b100;
parameter [2:0] RST_WAIT1      = 3'd0,
                 RST_WAIT2      = 3'd1,
                 INT_WAIT1      = 3'd2,
                 INT_WAIT2      = 3'd3,
                 EXECUTE        = 3'd4,
                 PRE_FETCH_EXEC = 3'd3,  // Execute the Pre-Fetched Instruction
                 MEM_WAIT1      = 3'd6,  // conditionally decode current instruction, in case
                                         // previous instruction does not execute in S2
                 MEM_WAIT2      = 3'd3,
                 PC_STALL1      = 3'd4,  // Program Counter altered
                                         // conditionally decude current instruction, in case
                                         // previous instruction does not execute in S2
                 PC_STALL2      = 3'd9,
                 MTRANS_EXEC1   = 3'd1,
                 MTRANS_EXEC2   = 3'd1,
                 MTRANS_ABORT   = 3'd1,
                 MULT_PROC1     = 3'd1,  // first cycle, save pre fetch instruction
                 MULT_PROC2     = 3'd1,  // do multiplication
                 MULT_STORE     = 3'd1,  // save RdLo
                 MULT_ACCUMU    = 3'd1,  // Accumulate add lower 32 bits
                 SWAP_WRITE     = 3'd1,
                 SWAP_WAIT1     = 3'd1,
                 SWAP_WAIT2     = 3'd1,
                 COPRO_WAIT     = 3'd2;
//-------------Internal Variables---------------------------
reg   [SIZE-1:0]          state        ;// Seq part of the FSM
reg   [SIZE-1:0]          next_state   ;// combo part of FSM
//----------Code startes Here------------------------
always @ (state or req_0 or req_1)
begin : FSM_COMBO
    next_state=state;
    if(state==IDLE)
        next_state = IDLE;
    if(state==GNT0)
        if(req_0)
            next_state = GNT0;
        else
            next_state = GNT0;
end
//----------Seq Logic-----------------------------
always @ (posedge clock)
begin : FSM_SEQ
  if (reset == 1'b1) begin
    state <=  IDLE;
  end else begin
    state <=  next_state;
  end
end
//----------Output Logic-----------------------------
always @ (posedge clock)
begin : OUTPUT_LOGIC
if (reset == 1'b1) begin
  gnt_0 <=  1'b0;
  gnt_1 <=  1'b0;
end
else begin
  case(state)
    IDLE : begin
                  gnt_0 <=  1'b0;
                  gnt_1 <=  1'b0;
               end
   GNT0 : begin
                   gnt_0 <=  1'b1;
                   gnt_1 <=  1'b0;
                end
   GNT1 : begin
                   gnt_0 <=  1'b0;
                   gnt_1 <=  1'b1;
                end
   default : begin
                    gnt_0 <=  1'b0;
                    gnt_1 <=  1'b0;
                  end
  endcase
end
end // End Of Block OUTPUT_LOGIC

endmodule // End of Module arbitergg
