grammar scheme;

// Sintaxi

NUMBER: [0-9]+ ('.' [0-9]+)? ;
BOOLEAN: '#t' | '#f' ;
STRING: '"' (~["\\] | '\\' .)* '"' ;

// Paraules reservades

IF: 'if';
ELSE: 'else' ;
DEFINE: 'define';
LET: 'let';
DISPLAY: 'display';
READ: 'read';
NEWLINE: 'newline';
CAR: 'car';
CDR: 'cdr';
CONS: 'cons';
NULLP: 'null?';
COND: 'cond';

// Operadors i símbols

PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
MOD: 'mod' ;
LT: '<' ;
LE: '<=' ;
GT: '>' ;
GE: '>=' ;
EQ: '=' ;
NEQ: '<>' ;
AND: 'and' ;
OR: 'or' ;
NOT: 'not' ;
LPAREN: '(' ;
RPAREN: ')' ;
QUOTE: '\'' ;

// Identificador general

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_+-/*?=!]* ;



// Espais i comentaris

WS : [ \t\r\n]+ -> skip ;
COMMENT: ';' ~[\r\n]* -> skip ;

// Regles semantiques principals

root: option* EOF ;

option: definition
      | expression ;

definition: LPAREN DEFINE vardef RPAREN
          | LPAREN DEFINE funcdef RPAREN ;

vardef: IDENTIFIER expression ;

funcdef: LPAREN IDENTIFIER parameters RPAREN expression+ ;

parameters: IDENTIFIER* ;

expression: literal
          | IDENTIFIER
          | operatorExpression
          | logicalExpression
          | condExpression
          | letExpression
          | listExpression
          | quotedExpression 
          | inoutExpression
          | funcCall ;


operatorExpression: LPAREN operator expression+ RPAREN ;

logicalExpression: LPAREN logical expression+ RPAREN ;

literal: NUMBER
       | BOOLEAN
       | STRING ;

condExpression: LPAREN IF expression expression expression RPAREN
              | LPAREN COND condClause+ RPAREN ;

condClause: LPAREN (expression | ELSE ) expression+ RPAREN ;

letExpression: LPAREN LET LPAREN declaration+ RPAREN expression+ RPAREN ;

declaration: LPAREN IDENTIFIER expression RPAREN ;

listExpression: LPAREN (CAR | CDR | NULLP) expression RPAREN
              | LPAREN CONS expression expression RPAREN ;

quotedExpression: QUOTE LPAREN literal* RPAREN ;

inoutExpression: LPAREN DISPLAY expression RPAREN
               | LPAREN READ RPAREN
               | LPAREN NEWLINE RPAREN ;

funcCall: LPAREN IDENTIFIER expression* RPAREN ;

operator: PLUS
        | MINUS
        | MUL
        | DIV
        | MOD ;

logical:  LT
        | LE
        | GT
        | GE
        | EQ
        | NEQ
        | AND
        | OR
        | NOT ;
