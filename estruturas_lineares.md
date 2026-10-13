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
um pouso de energencia seria necessario somente se houver uma tempestade severa, pouco combustivel e a prioridade for alta porque a pista devera estar vazia para um pouso de emergencia
```
N = C · A · D · S (pouso normal)
E = PA · ¬C · D · S · ¬T (pouso de emergência)
P = N + E (pouso autorizado)
```
[circuito aprovado](assets/aprovado.png)
a tabela de pouso autorizado pode ser encontrada em [tabela_pouso_aprovado.md](tabela_pouso_aprovado.md)

quando P (pouso autorizado) e classificado em alerta ou seja ha uma alguma falha ou quando adiado tem algum problema externo:

```
ALERTA = ¬P · (¬S + ¬C) 
ADIADO = ¬P · S · C
```
[circuito emergencia](assets/emergencia.png)
a tabela de alerta e adiado pode ser encontrada em [tabela_pouso_alerta.md](tabela_pouso_alerta.md)


