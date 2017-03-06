#Makefile for compilations
all:
	@clear
	$(MAKE) -C bin covgen

test:
	@clear
	$(MAKE) -C bin test

decode:
	@clear
	$(MAKE) -C bin decode

data:
	$(MAKE) -C bin data

run:
	@echo "Run the executables"

clean:
	$(MAKE) -C bin clean
