#Makefile for execution
covgen:
	@python ../src/main.py -t a25_wishbone ../rtl/amber25/a25_wishbone.v

test:
	@python ../src/test.py ../rtl/test.v

data:
	@python ../src/example_dataflow_analyzer.py ../rtl/test.v

ex_parser:
	@python ../src/example_parser.py ../rtl/amber25/a25_wishbone.v

ex_dataflow:
	@python ../src/example_dataflow_analyzer.py -t a25_wishbone ../rtl/amber25/a25_wishbone.v

clean:
	#rm *pyc *out