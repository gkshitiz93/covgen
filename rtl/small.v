module test(
    input rst,
    input clk,
    input [31:0] A,
    output reg [31:0] out
);

reg [2:0] state;

always@(posedge clk)
begin
    if(rst) begin
        out<=32'h0;
    end
    else begin
        if(state==1) begin
            out<=A;
        end
        else begin
            out<=~A;
        end
    end
end

always@(posedge clk)
begin
    if(rst) begin
        state<=0;
    end
    else begin
        state<=state+1;
    end
end

endmodule

module TOP(
    input rst,
    input clk    
);

reg [31:0] A;
wire [31:0] out;

test dut(rst,clk,A,out);

endmodule


