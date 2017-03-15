#Makefile for execution
covgen: clean
	@python ../src/main.py -t top ../rtl/wishbone.v

test: clean
	@python ../src/main.py -t top ../rtl/test.v

dataflow: clean
	@python ../src/example_dataflow_analyzer.py -t top ../rtl/wishbone.v

ex_parser:
	@python ../src/example_parser.py ../rtl/amber25/a25_wishbone.v

ex_dataflow:
	@python ../src/example_dataflow_analyzer.py -t a25_wishbone ../rtl/amber25/a25_wishbone.v

clean:
	rm -rf SVA/
