As condicoes de pouso foram convertidas em 6 variaveis boleanas calculadas para cada modulo.

| Var. | Significado | Condição simulada | Origem do dado |
|------|-------------|-------------------|----------------|
| C | Combustível suficiente | combustível ≥ 30 % | módulo |
| A | Atmosfera aceitável | vento ≤ 15 m/s | Estação meteorológica simulada |
| T | Tempestade severa | vento > 25 m/s | Estação meteorológica simulada |
| D | Pista de pouso disponível | pistas livres | Estado da base |
| S | Sensores íntegros | diagnóstico sem falhas | Módulo |
| PA | Prioridade alta | prioridade ≥ 4 | módulo |


Notação: “·” = AND,“+” = OR, “¬” = NOT. Um pouso normal exige as quatro condições favoráveis
```
N = C · A · D · S (pouso normal)
E = PA · ¬C · D · S · ¬T (pouso de emergência)
P = N + E (pouso autorizado)
```
quando P (pouso autorizado) e classificado em alerta ou seja ha uma alguma falha ou quando adiado tem algum problema externo:

```
ALERTA = ¬P · (¬S + ¬C) 
ADIADO = ¬P · S · C
```

a tabela de alerta e adiado pode ser encontrada em [tabela_pouso_alerta.md](tabela_pouso_alerta.md)
