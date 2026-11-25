# Nota 38 — Escalabilidade, Profundidade 3 e a Lei da Interferência Nula

**T. Bandeira · Junho de 2026**
*Nota experimental — complementa Nota 37*

---

## Resumo

Esta nota apresenta dois experimentos que estendem os resultados da Nota 37:

**Exp A (Escalabilidade):** testar $k = 5, 10, 20, 30, 50$ candidatos compartilhando
o mesmo cofator 143=11×13. Resultado: Stage 1 e Stage 2 produzem razão **exatamente
$k$** com erro **0.00000** para todos os $k$ — incluindo Stage 1.

Isso refina a hipótese da Nota 37 (Stage 2 exato porque sub-sinal tem destino único):
o mesmo princípio vale para Stage 1 quando há apenas um grupo no sinal.
A **Lei da Interferência Nula** é estabelecida: *o erro de medição é zero sempre que
o sinal contém um único destino espectral ativo, independentemente do número de candidatos $k$.*
O erro observado em Stage 1 da Nota 37 era causado pelos 4 grupos simultâneos,
não pelo número de candidatos por grupo.

**Exp C (Profundidade 3 com P1={2}):** reduzindo a base para P1={2}, o cofator
$105 = 3 \times 5 \times 7$ emerge no Stage 1 com boa resolução (9.9 bins).
Três rounds de colapso fatoram 105 completamente: Stage 1 → $f_{105}$,
Stage 2 ($-\log 3$) → $f_{35}$, Stage 3 ($-\log 5$) → $f_7$ (primo).
**Primeira cascata de profundidade 3 da série**, dentro do $T_{\max}=6500$.
Stages 2 e 3 têm erro **0.00000 exato**; Stage 1 tem erros de 0.00016–0.00362
(4 grupos simultâneos, consistente com a Lei da Interferência Nula).

O resultado central desta nota é que **P1 é um parâmetro de design** — ajustá-lo
controla diretamente a profundidade da cascata e o regime de operação do detector.

---

## 1. Contexto

A Nota 37 estabeleceu que:
1. Stage 2 tem erro 0.00000 (sub-sinal com destino único).
2. Stage 1 tem erros de ~0.003 (4 grupos coexistindo no mesmo sinal).

A hipótese era que Stage 2 era exato porque seus sub-sinais têm um único destino,
enquanto Stage 1 sofre interferência cruzada entre grupos.
Esta nota testa se essa hipótese escala: com $k$ grande num único grupo,
Stage 1 também deveria ser exato.

Paralelamente, a Nota 37 ficou limitada a profundidade 2 porque os menores
cofatores compostos disponíveis com P1={2,3,5,7} eram $\geq 11 \times 13 = 143$.
Reduzindo P1={2}, cofatores como $105 = 3 \times 5 \times 7$ aparecem com 9.9 bins
de resolução — suficiente para Stage 1 detectar corretamente.

---

## 2. Exp A — Escalabilidade com k grande

**Configuração:** P1={2,3,5,7}, cofator único 143=11×13,
candidatos = primeiros $k$ valores de $\{s \times 143 : s \in \mathbb{Z}_{P_1\text{-smooth}}, s \geq 2\}$.

### 2.1 Resultados

| $k$ | S1 razão | S1 erro | S2 razão | S2 erro | MDC par-a-par |
|---|---|---|---|---|---|
| 5 | 5.00000 | **0.00000** | 5.00000 | **0.00000** | 10 |
| 10 | 10.00000 | **0.00000** | 10.00000 | **0.00000** | 45 |
| 20 | 20.00000 | **0.00000** | 20.00000 | **0.00000** | 190 |
| 30 | 30.00000 | **0.00000** | 30.00000 | **0.00000** | 435 |
| 50 | 50.00000 | **0.00000** | 50.00000 | **0.00000** | 1225 |

Erro máximo em todos os $k$, para Stage 1 e Stage 2: **0.00000**.

### 2.2 A Lei da Interferência Nula

O resultado de Stage 1 exato para $k=50$ confirma que o mecanismo responsável
pelo erro em Stage 1 da Nota 37 não era o número de candidatos — era a
coexistência de múltiplos grupos no mesmo sinal:

> **Lei da Interferência Nula:** a razão medida pelo colapso orbital é exatamente $k$
> sempre que o sinal contém um único destino espectral ativo.
> O desvio da exatidão é proporcional à interferência de sidelobe entre grupos
> com destinos distintos, não ao número de candidatos por grupo.

Consequência: **o número de FFTs necessários permanece constante** em 2 (Stage 1 + Stage 2)
independentemente de $k$, enquanto o MDC par-a-par cresce como $k(k-1)/2$:

| $k$ | FFTs (constante) | MDC par-a-par | razão MDC/FFT |
|---|---|---|---|
| 10 | 2 | 45 | 22× |
| 30 | 2 | 435 | 217× |
| 50 | 2 | 1.225 | **612×** |

E o detector espectral identifica o fator primo 13 diretamente, enquanto MDC
par-a-par retornaria compostos (286, 572, 858, ...) exigindo pós-processamento.

---

## 3. Exp C — Cascata de profundidade 3 com P1={2}

**Configuração:** P1={2}, 10 candidatos com três profundidades distintas:

| grupo | candidatos | cofator Stage 1 | profundidade |
|---|---|---|---|
| Grupo 1 | 210, 420, 840, 1680, 3360 | **105=3×5×7** (composto) | **3** |
| Grupo 2 | 30, 60, 120 | **15=3×5** (composto) | **2** |
| Controle | 14, 22 | **7, 11** (primos) | **1** |

**Resolução espectral Stage 1 (P1={2}):**

| cofator | separação (bins) | status |
|---|---|---|
| 105 | 9.9 | OK ✓ |
| 15 | 71.4 | OK ✓ |
| 7 | 159.5 | OK ✓ |
| 11 | 98.6 | OK ✓ |

### 3.1 Resultados

| stage | operação | previsto | razão | erro |
|---|---|---|---|---|
| Stage 1 | detectar $f_{105}$ | 5 | 4.99853 | 0.00147 |
| Stage 1 | detectar $f_{15}$ | 3 | 2.99923 | 0.00077 |
| Stage 1 | detectar $f_7$ | 1 | 0.99984 | 0.00016 |
| Stage 1 | detectar $f_{11}$ | 1 | 0.99638 | 0.00362 |
| **Stage 2** | **105 → 35** | **5** | **5.00000** | **0.00000** |
| **Stage 2** | **15 → 5** | **3** | **3.00000** | **0.00000** |
| **Stage 3** | **35 → 7** | **5** | **5.00000** | **0.00000** |

**10/10 candidatos completamente fatorados. 3 rounds. 4 FFTs.**

### 3.2 Análise dos erros de Stage 1

O maior erro de Stage 1 é em $f_{11}$ (0.00362), o menor em $f_7$ (0.00016).
O padrão segue a Lei da Interferência Nula: com 4 grupos no sinal,
o erro em cada destino $f_q$ é proporcional à interferência dos sidelobes dos outros grupos.
$f_{11}$ tem amplitude isolada menor (1592 vs 2327 para $f_7$),
tornando a perturbação relativa dos sidelobes dos vizinhos maior.
Todos os erros são $<0.4\%$ — suficientes para classificação correta
com threshold de 1.8.

Stages 2 e 3 operam em sub-sinais de grupo único → Lei da Interferência Nula
garante erro 0.00000, confirmado em todas as três medições.

### 3.3 A cascata completa

```
P1={2}

Stage 1:  {210,420,840,1680,3360} → f_105 (5×, composto)
          {30,60,120}             → f_15  (3×, composto)
          {14}                    → f_7   (1×, primo ✓)
          {22}                    → f_11  (1×, primo ✓)

Stage 2:  Grupo1: log(105)-log(3)=log(35) → f_35 (5×, composto 5×7)
          Grupo2: log(15)-log(3) =log(5)  → f_5  (3×, primo ✓) → 15=3×5

Stage 3:  Grupo1: log(35)-log(5)=log(7)  → f_7  (5×, primo ✓) → 35=5×7 → 105=3×5×7
```

**Fatoração completa:**
$210 = 2\cdot3\cdot5\cdot7$, $420 = 2^2\cdot3\cdot5\cdot7$, $840 = 2^3\cdot3\cdot5\cdot7$,
$1680 = 2^4\cdot3\cdot5\cdot7$, $3360 = 2^5\cdot3\cdot5\cdot7$,
$30 = 2\cdot3\cdot5$, $60 = 2^2\cdot3\cdot5$, $120 = 2^3\cdot3\cdot5$,
$14 = 2\cdot7$, $22 = 2\cdot11$.

---

## 4. P1 como parâmetro de design

Os dois experimentos revelam que P1 não é uma constante do método —
é um **parâmetro de design** que controla o trade-off profundidade/resolução:

| P1 | primes removidas | cofatores mínimos | profundidade max (T_max=6500) |
|---|---|---|---|
| {2,3,5,7} | 4 primos | $\geq 11\times13=143$ | 2 (Nota 37) |
| {2,3} | 2 primos | $\geq 5\times7=35$ | 2 (cofatores menores mas ainda 2) |
| **{2}** | **1 primo** | **$\geq 3\times5=15$** | **3** (Exp C) |
| {} | nenhum | qualquer inteiro | ilimitada (mas Stage 1 testa tudo) |

Para testar profundidade 4 com T_max=6500 seria necessário P1={} e candidatos
com cofator $\geq 3\times5\times7\times11=1155$ — porém a resolução espectral
de $f_{1155}$ é de apenas 0.9 bins (insuficiente). O limite prático com T_max=6500
é **profundidade 3** com P1={2}, confirmado pelo Exp C.

Para profundidade 4 seria necessário aumentar T_max — conforme a fórmula
da Nota 35: $T_{\max} \geq (2W+1) \cdot 2\pi / \Delta f_{\min}$.

---

## 5. Status atual

| Afirmação | Status |
|---|---|
| Lei da Interferência Nula: erro=0 com 1 grupo, qualquer $k$ | Confirmada — k=5,10,20,30,50 com erro 0.00000 (Seção 2) |
| FFTs constantes (O(1)) vs MDC par-a-par (O(k²)) | Confirmada — 2 FFTs para k=5..50 vs 10..1225 MDCs (Seção 2.2) |
| Cascata de profundidade 3 com P1={2} e T_max=6500 | Confirmada — 105=3×5×7 em 3 stages (Seção 3) |
| Stages 2 e 3 com erro 0.00000 (sub-sinais com destino único) | Confirmada — 3 medições independentes (Seção 3.1) |
| P1 como parâmetro de design controlando profundidade | Estabelecida — tabela de trade-offs (Seção 4) |
| Profundidade 4 com T_max=6500 | Não viável — requer aumento de T_max (Seção 4) |
| Profundidade 4 com T_max maior | Não testado |

---

## 6. Próximos passos sugeridos

1. **Exp D — Simulação batch realista:** 30 candidatos misturados (alguns compartilhando
   cofator $q_1$, outros $q_2$, outros únicos) apresentados ao detector sem revelar
   estrutura. Demonstra o método no cenário mais próximo de aplicação prática —
   e com $k$ grande, a vantagem sobre MDC par-a-par é de centenas a milhares de vezes.

2. **Profundidade 4 com T_max aumentado:** calcular T_max mínimo pela fórmula da Nota 35
   para o cofator de profundidade 4 mais acessível e testar a cascata com 4 stages.
   Confirma que a Lei da Interferência Nula continua exata em profundidade arbitrária.

3. **Derivar fórmula do erro de Stage 1 em função dos grupos:**
   quantificar analiticamente o erro em $f_q$ como função das amplitudes e distâncias
   espectrais dos outros grupos. Isso transformaria a observação empírica num resultado
   analítico preciso — o "modelo de interferência" que complementa a Lei da Interferência Nula.

---

## 7. Referências

[Nota 35] T. Bandeira, *Verificação Espectral por Colapso Orbital* (2026).
Deriva a fórmula de $T_{\max}$ usada para verificar resolução dos cofatores desta nota.

[Nota 36] T. Bandeira, *Detector Espectral de Fator Comum em Lote* (2026).
Estabelece a comparação com MDC par-a-par. O Exp A desta nota estende
essa comparação para $k$ grande.

[Nota 37] T. Bandeira, *Fatoração Prima Completa por Cascata de Colapso Orbital* (2026).
Estabelece a cascata de profundidade 2. Esta nota refina a explicação dos erros
de Stage 1 (Lei da Interferência Nula) e estende para profundidade 3.

---

## 8. Notebooks e arquivos

| arquivo | conteúdo |
|---|---|
| `exp_escala_stage3.ipynb` | Implementação completa: Exp A (k=5..50, Stage 1+2), Exp C (Stage 1+2+3 com P1={2}), visualizações, tabela de design de P1 |
| `escala_exp_a.png` | Exp A: razão vs k (retas exatas sobre a diagonal) + FFTs vs MDC (O(1) vs O(k²)) |
| `cascata_stage3_depth3.png` | Exp C: três painéis mostrando a migração espectral em cada stage (f_105 → f_35 → f_7) |
| `cascata_arvore_depth3.png` | Árvore de fatoração com três níveis: Stage 1, Stage 2, Stage 3 |
| `escala_stage3_resultados.zip` | Pacote consolidado das figuras |
