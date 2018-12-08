
module fp_12(
	input clk, rst,
	input op,  // op-code :0 is add, 1 is subtract
	input [31:0] a, b,
	output logic [31:0] c);

	logic signa;
	logic signb;

	logic [7:0] exponenta,exponentb;


	logic [7:0] workingExponent;

	logic [5:0] encoderShift;
	// three extra bit padded with {overflow, signbit, hidden, Mantissa}
	logic [25:0] OCNa,OCNb, sum;

	// not putting in sign bit yet to avoid shifting errors


	logic [7:0] exponentDiff;

	priority_enc myenc(.in(sum[23:0]),  .out(encoderShift));


	always_comb begin

	signa= a[31];
	signb= b[31];
	exponenta = a[30:23];
	exponentb = b[30:23];

	OCNa = {3'b001, a[22:0]};
	OCNb = {3'b001, b[22:0]};


	if((exponenta > exponentb)) begin

		// taking the diffrence
		exponentDiff=exponenta-exponentb;
		workingExponent=exponenta;
		// if a is larger, then shift B to the right by exponentDiff bits
		OCNb = OCNb >> exponentDiff;
	end else if ((exponenta < exponentb)) begin
		exponentDiff=exponentb-exponenta;
		workingExponent=exponentb;
		// if b is larger, then shift A to the right by exponentDiff bits
		OCNa = OCNa >> exponentDiff;
	end else begin // equal case
		exponentDiff=0;
		workingExponent=exponentb;
	end

	// put in the sign bit from the input a and b
	OCNa[24]=signa;
	OCNb[24]=signb;

	case({op,signa,signb})
		3'b001: OCNb[23:0] = ~OCNb[23:0]; // (+) + (-), flipping B's Mantissa + hidden bit
		3'b010: OCNa[23:0] = ~OCNa[23:0]; // (-) + (+), flipping A's Mantissa + hidden bit
		3'b011: begin OCNb[23:0] = ~OCNb[23:0]; OCNa[23:0] = ~OCNa[23:0]; end // (-) + (-) , flipping A and B's Mantissa + hidden bit
		3'b100: OCNb[24:0] = ~OCNb[24:0]; // (+) - (+), flipping all of B except for overflow bit
		3'b101: OCNb[24] = ~OCNb[24]; // (+) - (-), flipping B's sign bit
		3'b110: begin OCNa[23:0] = ~OCNa[23:0]; OCNb[24:0] = ~OCNb[24:0]; end// (-) - (+), flipping all of B except for overflow bit AND A's Mantissa + hidden bit
		3'b111: begin OCNa[23:0] = ~OCNa[23:0]; OCNb[24] = ~OCNb[24]; end // (-) - (-), flipping A's Mantissa + hidden bit, flipping B's sign bit
		default: begin end
	endcase

	sum= OCNa+OCNb;
	if(sum[25]) begin
		sum+=1;
	end



	if(OCNa[24] ==0 && OCNb[24] ==0 ) begin
	// launch  finesse algrithom
		if(sum[24])begin
			workingExponent	+=1;
			sum[22:0] = sum[22:0] >>1;
			sum[24]=0;
			//set hidden bit to one in this case
			sum[23]=1;

		end
	end else if(OCNa[24] ==1 && OCNb[24] ==1 ) begin
	// launch  finesse algrithom
		if(sum[24]==0)begin
			workingExponent	+=1;
			sum[22:0] = {1'b1,sum[22:1]};
			sum[24]=1;
			//set hidden bit to one in this case
			sum[23]=0;
		end
	end

	// filp OCN resuult back to stupid ass mantissa format if result has negative sign
	if (sum[24]) begin
		sum[23:0]=~sum[23:0];

	end

	// if hidden bit is zero, that indicates as underflow
	// use prioirity encoder to check how much to shift by
	if(encoderShift>0)begin
		c = {sum[24], workingExponent-encoderShift, sum[22:0] << encoderShift};
	end else begin
		c = {sum[24], workingExponent, sum[22:0]};
	end


end


endmodule


module priority_enc (
    input wire [23:0] in,
    output logic [4:0] out
  );
logic [4:0] temp;
assign temp = (in[23] == 1'b1) ? 'd23:
(in[22] == 1'b1) ? 'd22:
(in[21] == 1'b1) ? 'd21:
(in[20] == 1'b1) ? 'd20:
(in[19] == 1'b1) ? 'd19:
(in[18] == 1'b1) ? 'd18:
(in[17] == 1'b1) ? 'd17:
(in[16] == 1'b1) ? 'd16:
(in[15] == 1'b1) ? 'd15:
(in[14] == 1'b1) ? 'd14:
(in[13] == 1'b1) ? 'd13:
(in[12] == 1'b1) ? 'd12:
(in[11] == 1'b1) ? 'd11:
(in[10] == 1'b1) ? 'd10:
(in[9] == 1'b1) ? 'd9:
(in[8] == 1'b1) ? 'd8:
(in[7] == 1'b1) ? 'd7:
(in[6] == 1'b1) ? 'd6:
(in[5] == 1'b1) ? 'd5:
(in[4] == 1'b1) ? 'd4:
(in[3] == 1'b1) ? 'd3:
(in[2] == 1'b1) ? 'd2:
(in[1] == 1'b1) ? 'd1: 'd0;

assign out = 23-temp;


endmodule
