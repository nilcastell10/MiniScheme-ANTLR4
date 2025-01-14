ANTLR_JAR=antlr-4.13.2-complete.jar
GRAMMAR=scheme.g4
OUTPUT_DIR=.
PYTHON_TARGET=Python3

.PHONY: all clean

all: compile

compile:
	java -jar $(ANTLR_JAR) -Dlanguage=$(PYTHON_TARGET) -visitor -no-listener $(GRAMMAR)

clean:
	rm -f $(OUTPUT_DIR)/*.tokens
	rm -f $(OUTPUT_DIR)/*.interp
	rm -f $(OUTPUT_DIR)/*.pyc
	rm -f $(OUTPUT_DIR)/*Visitor.py
	rm -f $(OUTPUT_DIR)/*Lexer.py
	rm -f $(OUTPUT_DIR)/*Parser.py

# Nota: Els fitxers `scheme.py`, `scheme.g4` i `programa.scm` no es toquen
