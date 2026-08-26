# Makefile for Typst presentation with Touying

MAIN = main.typ
OUTPUT = main.pdf

.PHONY: all build watch clean

all: build

build:
	typst compile $(MAIN) $(OUTPUT)

watch:
	typst watch $(MAIN) $(OUTPUT)

clean:
	rm -f $(OUTPUT)
