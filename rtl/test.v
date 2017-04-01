module arb2 (
clock      , // clock
reset      , // Active high, syn reset
req      , // Request 1
gnt_0      , // Grant 0
gnt_1      
);
//-------------Input Ports-----------------------------
input   clock,reset;
input [2:0] req;
 //-------------Output Ports----------------------------
output  gnt_0,gnt_1;
//-------------Input ports Data Type-------------------
wire    clock,reset;
//-------------Output Ports Data Type------------------
reg     gnt_0,gnt_1;
//-------------Internal Constants--------------------------
parameter SIZE = 3;
parameter IDLE  = 3'b001,GNT0 = 3'b010,GNT1 = 3'b100;
//-------------Internal Variables---------------------------
reg   [SIZE-1:0]          state        ;// Seq part of the FSM
reg   [SIZE-1:0]          next_state   ;// combo part of FSM
//----------Code startes Here------------------------
always @ (state or req[0] or req[1])
begin : FSM_COMBO
    next_state=state;
    if(state==IDLE)
        next_state = IDLE;
    if(state==GNT0)
        if(req[0])
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

module top(
input clock      , // clock
input reset      , // Active high, syn reset
input [1:0] req      , // Request 0
output gnt_0      , // Grant 0
output gnt_1      ,
input something
);

arb arb1(.reset(reset), .gnt_0(gnt_0), .req({req[1:0], something}),.clock(clock), .gnt_1(gnt_1));
//ccx_buff_macro__dbuff_32x__rep_1__stack_none__width_8 i_buf_test_r     (
//	.din	({scan_in[1:0],tcu_pce_ov, tcu_aclk, 
//              tcu_bclk, tcu_scan_en, cluster_arst_l,tcu_atpg_mode}),
//	.dout	({scan_in_buf[1:0],tcu_pce_ov_buf,tcu_aclk_buf, 
//              tcu_bclk_buf, tcu_scan_en_buf, cluster_arst_l_buf,tcu_atpg_mode_buf})
//);

endmodule
