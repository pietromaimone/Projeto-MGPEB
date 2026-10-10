as condicoes de pouso foram convertidas em 6 variaveis boleanas calculadas para cada modulo.

| Var. | Significado | Condição simulada | Origem do dado |
|------|-------------|-------------------|----------------|
| C | Combustível suficiente | combustível ≥ 30 % | módulo |
| A | Atmosfera aceitável | vento ≤ 15 m/s | Estação meteorológica simulada |
| T | Tempestade severa | vento > 25 m/s | Estação meteorológica simulada |
| D | Pista de pouso disponível | pistas livres | Estado da base |
| S | Sensores íntegros | diagnóstico sem falhas | Módulo |
| PA | Prioridade alta | prioridade ≥ 4 | módulo |

