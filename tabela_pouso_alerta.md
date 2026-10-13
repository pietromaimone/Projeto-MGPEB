# Tabela Verdade do Circuito ADIADO E FALHA 

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
