# Tabela Verdade do Circuito

## Expressões lógicas

- **G5** = ¬S + ¬C
- **G6 (ALERTA)** = ¬P · G5 = ¬P · (¬S + ¬C)
- **G7 (ADIADO)** = ¬P · S · C

## Tabela

| P | S | C | ¬P | ¬S | ¬C | G5 = ¬S + ¬C | ALERTA (G6) | ADIADO (G7) |
|---|---|---|----|----|----|--------------|-------------|-------------|
| 0 | 0 | 0 | 1  | 1  | 1  | 1            | **1**       | **0**       |
| 0 | 0 | 1 | 1  | 1  | 0  | 1            | **1**       | **0**       |
| 0 | 1 | 0 | 1  | 0  | 1  | 1            | **1**       | **0**       |
| 0 | 1 | 1 | 1  | 0  | 0  | 0            | **0**       | **1**       |
| 1 | 0 | 0 | 0  | 1  | 1  | 1            | **0**       | **0**       |
| 1 | 0 | 1 | 0  | 1  | 0  | 1            | **0**       | **0**       |
| 1 | 1 | 0 | 0  | 0  | 1  | 1            | **0**       | **0**       |
| 1 | 1 | 1 | 0  | 0  | 0  | 0            | **0**       | **0**       |

## Observações

- **ALERTA** = 1 quando P = 0 e pelo menos um entre S e C é 0.
- **ADIADO** = 1 somente quando P = 0, S = 1 e C = 1.
- ALERTA e ADIADO nunca são 1 ao mesmo tempo (são mutuamente exclusivos).
- Se P = 1, ambas as saídas ficam em 0.

| C | A | D | S | PA | T | P | Classe | Caso na simulação |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|---|
| 1 | 1 | 1 | 1 | x | 0 | 1 | Autorizado (normal) | ENE-02 e MED-05, janela 1 |
| 0 | 0 | 1 | 1 | 1 | 0 | 1 | Autorizado (emergência) | HAB-01, janela 2 (vento 22 m/s) |
| 1 | 0 | 1 | 1 | x | 0 | 0 | Adiado (vento) | LOG-04, janela 2 |
| 1 | 1 | 0 | 1 | x | 0 | 0 | Adiado (sem pista) | HAB-01 e LOG-04, janela 1 |
| x | x | x | 0 | x | x | 0 | Alerta (sensor) | LAB-03, janela 1 |
| 0 | x | x | 1 | 0 | x | 0 | Alerta (combustível) | LOG-04, janela 3 (27 %) |
| 0 | 0 | 1 | 1 | 1 | 1 | 0 | Alerta (tempestade bloqueia emergência) | caso previsto, não ocorreu |
