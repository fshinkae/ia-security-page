# Resumo: Prolog - Fatos e Regras

## O que é Prolog?

Prolog é uma linguagem de programação lógica baseada em **fatos** e **regras**. Ela funciona através de **consultas** que tentam provar se uma afirmação é verdadeira usando o conhecimento armazenado.

## Fatos

**Definição:** Afirmações verdadeiras sobre o mundo, sem condições.

**Sintaxe:**
```prolog
predicado(argumento1, argumento2).
```

**Exemplos:**
```prolog
pai(joão, maria).
gosta(ana, chocolate).
idade(carlos, 25).
```

## Regras

**Definição:** Definem novas informações a partir de fatos existentes. Possuem uma **cabeça** (conclusão) e um **corpo** (condições).

**Sintaxe:**
```prolog
cabeça :- corpo.
```

Lê-se como: "cabeça é verdadeira **se** corpo for verdadeiro"

**Exemplos:**
```prolog
avô(X, Z) :- pai(X, Y), pai(Y, Z).
imortal(X) :- deus(X).
genitor(X, Y) :- pai(X, Y).
genitor(X, Y) :- mãe(X, Y).
```

## Comparação

| Característica | Fatos | Regras |
|---|---|---|
| **Estrutura** | Simples | Cabeça :- corpo |
| **Condições** | Não possui | Possui |
| **Verdade** | Sempre verdadeiro | Depende do corpo |

## Exemplo Prático Completo

```prolog
% === FATOS ===
pai(joão, pedro).
pai(pedro, carlos).
mãe(maria, pedro).

% === REGRAS ===
avô(X, Z) :- pai(X, Y), pai(Y, Z).
genitor(X, Y) :- pai(X, Y).
genitor(X, Y) :- mãe(X, Y).

% === CONSULTAS ===
?- avô(joão, carlos).    % Resposta: true
?- genitor(maria, pedro). % Resposta: true
```

## Como Funciona

1. Você define **fatos** (dados conhecidos)
2. Você define **regras** (como deduzir novos dados)
3. Você faz **consultas** (perguntas)
4. Prolog tenta **provar** a consulta usando fatos e regras

Prolog é excelente para problemas de lógica, inteligência artificial e bancos de dados relacionais.