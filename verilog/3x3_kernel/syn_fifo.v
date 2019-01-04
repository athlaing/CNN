module syn_fifo(clk, data_in, data_out, read_en, write_en, reset, empty, full);
  parameter WORD_WIDTH = 'd16;
  parameter ADDR_LENGTH = 'd256;
  parameter ADDR_WIDTH = 'd8

  input clk;
  input reg [(WORD_WIDTH*3)-1:0] data_in;
  output reg [(WORD_WIDTH*3)-1:0] data_out;
  input reset;
  input read_en, write_en;
  output reg empty, full;
  reg [ADDR_WIDTH-1:0] count;

  reg [ADDR_WIDTH-1:0] write_ptr, read_ptr;
  reg [WORD_WIDTH-1:0] mem [ADDR_LENGTH-1:0];

  always @(posedge clk) begin
    if(reset) begin
      read_ptr <= 8'h00;
      write_prt <= 8'h00;
      count <= 8'h00;
      empty <= 1'b1;
      full <= 1'b0;
    end
    else begin
      if(read_en && !write_en) begin
        data_out[WORD_WIDTH-1:0] <= mem[read_ptr];
        data_out[WORD_WIDTH*2-1:WORD_WIDTH] <= mem[read_ptr + 8'h01];
        data[WORD_WIDTH*3-1:WORD_WIDTH*2] <= mem[read_ptr + 8'h02];
        read_ptr <= read_ptr + 8'h03;
        count <= count + 8'h03;
      end
      else if(write_en && !read_en) begin
        mem[write_ptr] <= data[];
        mem[write_ptr + 8'h01] <= data_in[WORD_WIDTH*2-1:WORD_WIDTH];
        mem[write_ptr + 8'h02] <= data_in[WORD_WIDTH*3-1:WORD_WIDTH*2]];
        write_ptr <= write_ptr + 8'h03;
        count <= count - 8'h03;
      end
      if(count == 8'h00) begin
        empty = 1'b1;
        full = 1'b0;
      end
      else if(count == ADDR_LENGTH-1) begin
        empty = 1'b0;
        full = 1'b1;
      end
      else begin
        empty = 1'b0;
        full = 1'b0;
      end
    end
  end
endmodule
