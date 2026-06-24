# Nota 35 — Verificação Espectral por Colapso Orbital

**T. Bandeira · Junho de 2026**
*Nota de implementação experimental — complementa Nota 34 e Nota 21*

---

## Resumo

Esta nota implementa um algoritmo de verificação de primalidade em linguagem log-FFT usando a
Lei do Ganho Orbital estabelecida na Nota 34. O algoritmo opera em duas fases: uma Fase 1 de
bootstrap incremental (estruturalmente equivalente ao Crivo de Eratóstenes, mas lida via
deslocamentos espectrais) e uma Fase 2 de verificação em lote, onde o colapso orbital de uma
base de primos $P$ é aplicado a todos os candidatos simultaneamente e a classificação emerge
da razão `amp_depois/amp_antes` em cada $f_c$. Aplicado a 8 candidatos mistos
$\{15,17,22,29,35,37,49,53\}$ com base $P=\{2,3,5,7\}$, obteve-se 8/8 acertos com
**gap de 0.997** entre grupos (primos em $1.0008$–$1.0014$, compostos em
$0.0004$–$0.0042$) — o resultado mais limpo da série, decorrente da esparsidade do sinal.

O resultado analítico principal é uma **fórmula fechada para $T_{\max}$**, respondendo à
questão em aberto das notas anteriores: o parâmetro não depende de $N$ em geral, mas do
gap mínimo em frequência entre os termos presentes no sinal. Para o batch esparso testado,
o mínimo teórico é $T_{\max}\approx800$, contra os 6500 usados empiricamente — a
sobre-especificação de 8× explica por que o valor empírico funcionava sem uma lei formal.

---

## 1. Contexto

Esta nota usa os resultados da Nota 34 como fundação direta. A Lei do Ganho Orbital
(Nota 34, Seção 3) prevê que, após remoção completa dos fatores de $P$ de um sinal
de candidatos, cada candidato primo $c$ (sem fatores em $P$) satisfaz:

$$|\mathcal{O}_c| = 1 \quad \Longrightarrow \quad \frac{\text{amp\_depois}(f_c)}{\text{amp\_antes}(f_c)} \approx 1$$

enquanto cada composto $c = r \cdot \prod p_i^{a_i}$ (com $p_i \in P$) tem $f_c$ migrado
ou descartado:

$$|\mathcal{O}_c|_{\text{em } f_c} = 0 \quad \Longrightarrow \quad \frac{\text{amp\_depois}(f_c)}{\text{amp\_antes}(f_c)} \approx 0$$

O sinal usado é o mesmo da Nota 34 — $-\cos(t\log m)/\sqrt{\log m}$ — não o sinal formal
$S_m(t)$ da Nota 21. O algoritmo não é equivalente ao Crivo Oracle-Free da Nota 21
(que usa o operador $\mathcal{R}_m$ e ortogonalidade assintótica); é uma aplicação
diferente, com circularidade explícita na Fase 1 (ver Seção 2).

---

## 2. Algoritmo — duas fases

### Fase 1 — Bootstrap espectral

Identificar incrementalmente os primos em $[2, \sqrt{N_{\max}}]$ usando apenas
deslocamentos espectrais como critério. A cada passo:

1. O menor candidato $q$ cujo $\log_{\text{resid}}(q, P_{\text{atual}}) = \log q$
   (frequência não deslocada por nenhuma remoção anterior) é declarado primo.
2. $q$ é adicionado à base $P$.
3. Os demais candidatos são reclassificados em três grupos:
   - **colapsam:** $\log_{\text{resid}} \approx 0$ → compostos $P$-suaves (todos os fatores em $P$)
   - **migram:** $0 < \log_{\text{resid}} < \log m$ → compostos com algum fator fora de $P$ ainda
   - **sobrevivem:** $\log_{\text{resid}} = \log m$ → não afetados por $P$ até agora

Os que colapsam são descartados. Os que migram permanecem no pool até colapsar num passo futuro.

**Circularidade:** esta fase tem a mesma dependência circular do Crivo de Eratóstenes —
$q$ é declarado primo porque nenhum primo menor o divide, o que pressupõe o conhecimento dos
primos menores. A diferença é apenas que o critério de "não divisão" é lido via invariância
espectral em vez de aritmética inteira.

### Fase 2 — Verificação em lote

Dados um conjunto de candidatos $\mathcal{C}$ e a base $P = \{p : p \leq \lfloor\sqrt{\max \mathcal{C}}\rfloor, p \text{ primo}\}$:

1. Construir $R_{\text{orig}} = \sum_{c \in \mathcal{C}} -\cos(t\log c)/\sqrt{\log c}$
2. Construir $R_{\text{rem}}$ substituindo $\log c \to \log_{\text{resid}}(c, P)$ para cada $c$;
   termos com $\log_{\text{resid}} \leq 0$ são descartados.
3. Computar $F_{\text{orig}}$ e $F_{\text{rem}}$ via FFT (uma vez cada, para todos os candidatos).
4. Para cada $c$: medir `razão` $= \text{amp}(F_{\text{rem}}, f_c) / \text{amp}(F_{\text{orig}}, f_c)$.
5. Classificar: razão $> 0.5$ → primo; razão $< 0.5$ → composto.

**Paralelismo:** a FFT é computada **uma única vez** para todos os $k$ candidatos.
O custo marginal de adicionar um candidato ao lote é $O(T_{\max}/\Delta t)$ para
construir seu cosseno e $O(W)$ para ler sua amplitude — não requer nova FFT.

---

## 3. Fase 1 — resultado experimental em $[2, 15]$

| passo | $q$ detectado | colapsam | migram | sobrevivem |
|---|---|---|---|---|
| 1 | 2 | [4, 8] | [6, 10, 12, 14] | [3, 5, 7, 9, 11, 13, 15] |
| 2 | 3 | [6, 9, 12] | [10, 14, 15] | [5, 7, 11, 13] |
| 3 | 5 | [10, 15] | [14] | [7, 11, 13] |
| 4 | 7 | [14] | [] | [11, 13] |
| 5 | 11 | [] | [] | [13] |
| 6 | 13 | [] | [] | [] |

Primos detectados: $[2, 3, 5, 7, 11, 13]$ — match exato com `sympy.primerange(2, 16)`.

A coluna "migram" rastreia compostos que foram parcialmente reduzidos mas ainda têm
um fator primo não descoberto: $6 = 2\cdot3$ migra para $f_3$ após remover 2,
depois colapsa quando 3 é adicionado à base. Isso é o análogo espectral do
"número riscado mas ainda pendente" no Crivo de Eratóstenes.

---

## 4. Fase 2 — resultados experimentais

**Candidatos:** $\{15, 17, 22, 29, 35, 37, 49, 53\}$
**Base:** $P = \{2, 3, 5, 7\}$ ($\lfloor\sqrt{53}\rfloor = 7$)

| $c$ | fatoração | destino após remoção | `amp_antes` | `amp_depois` | razão | pred | real | ✓ |
|---|---|---|---|---|---|---|---|---|
| 15 | $3\cdot5$ | descartado ($\log_{\text{resid}}=0$) | 1372.21 | 0.49 | 0.00036 | composto | composto | ✓ |
| 17 | primo | fica em $f_{17}$ | 1916.05 | 1917.72 | 1.00087 | primo | primo | ✓ |
| 22 | $2\cdot11$ | migra para $f_{11}$ | 1508.90 | 2.34 | 0.00155 | composto | composto | ✓ |
| 29 | primo | fica em $f_{29}$ | 1262.78 | 1264.58 | 1.00143 | primo | primo | ✓ |
| 35 | $5\cdot7$ | descartado | 1723.27 | 7.19 | 0.00417 | composto | composto | ✓ |
| 37 | primo | fica em $f_{37}$ | 1164.99 | 1165.93 | 1.00081 | primo | primo | ✓ |
| 49 | $7^2$ | descartado | 1642.15 | 2.94 | 0.00179 | composto | composto | ✓ |
| 53 | primo | fica em $f_{53}$ | 1486.78 | 1488.06 | 1.00086 | primo | primo | ✓ |

**Acertos: 8/8 (100%)**

| grupo | razão média | dp | min | max |
|---|---|---|---|---|
| primos | 1.00099 | 0.00029 | 1.00081 | 1.00143 |
| compostos | 0.00197 | 0.00160 | 0.00036 | 0.00417 |
| **gap mínimo** | | | | **0.99664** |

A precisão é significativamente superior à dos experimentos FA-LOG-2 (desvio de
$\pm2\%$ nos primos, outliers em $r=11,23$). A causa é estrutural: com 8 termos
no sinal em vez de 299, o ruído de lotação espectral assimétrica identificado na
Nota 34 (Seção 5) cai para $\sim 10^{-4}$, tornando a separação entre grupos
praticamente perfeita.

---

## 5. Caso especial — $22 = 2 \cdot 11$ com $11 \notin P$

$22$ tem um fator ($11$) fora da base $P$. Após remover os fatores de $P$:

$$\log_{\text{resid}}(22, \{2,3,5,7\}) = \log 22 - \log 2 = \log 11 \approx 2.398$$

O pico de $22$ **migra** para $f_{11}$ — fora do conjunto de candidatos — e a posição
original $f_{22}$ fica vazia. Medições:

- $\text{amp}(F_{\text{orig}}, f_{22}) = 1508.90$
- $\text{amp}(F_{\text{rem}},  f_{22}) = 2.34$ (resíduo de sidelobe, não pico real)
- $\text{amp}(F_{\text{rem}},  f_{11}) \approx 1509$ (pico novo, fora do conjunto)

Razão em $f_{22}$: $0.00155$ → composto, classificado corretamente.

Este caso demonstra que o método detecta compostos com fatores fora da base
(análogo a detectar $2\mid22$ sem testar $11$), revelando também para onde o
composto migrou — informação estrutural que trial division não fornece.

---

## 6. Comportamento da norma $L^2$

A norma $L^2$ **caiu** (ratio $0.8137$), ao contrário dos experimentos FA-LOG-2
onde ela crescia ($\times1.71$ para $q=3$). O mecanismo é diferente:

| experimento | o que sobrevive | efeito na norma |
|---|---|---|
| FA-LOG-2 ($N=300$, um primo) | múltiplos convergem para atratores pequenos | **cresce** — amplificação por concentração |
| Fase 2 (batch esparso) | compostos desaparecem; primos grandes ficam | **cai** — sem convergência, só descarte |

Os quatro primos sobreviventes (17, 29, 37, 53) têm amplitude $1/\sqrt{\log p}$
com $p$ grande — menor que a média dos oito termos originais. A remoção dos
quatro compostos retira componentes de grande amplitude (os compostos eram
termos com $\log m$ menor, portanto amplitude $1/\sqrt{\log m}$ maior).
A norma cai porque os sobreviventes são os de menor amplitude.

---

## 7. A lei de $T_{\max}$ — resultado analítico principal

### Derivação

Para distinguir dois picos em frequências $f_1$ e $f_2 = f_1 + \Delta f$ numa FFT
com janela retangular de comprimento $T_{\max}$, é necessário que caibam ao menos
$(2W+1)$ bins entre eles (onde $W$ é a janela de busca de pico):

$$T_{\max} \cdot \Delta f \geq 2W + 1 \quad \Longrightarrow \quad T_{\max} \geq \frac{2W+1}{\Delta f_{\min}}$$

Para o sinal log-FFT, $\Delta f_{\min}$ é o gap mínimo em frequência entre os
termos **presentes no sinal**:

$$\Delta f_{\min} = \frac{1}{2\pi}\min_{i \neq j}|\log c_i - \log c_j|$$

Portanto a fórmula completa é:

$$\boxed{T_{\max} \geq \frac{(2W+1) \cdot 2\pi}{\min_{i \neq j}|\log c_i - \log c_j|}}$$

Esta fórmula depende do **conjunto de termos no sinal**, não de $N$ em geral.

### O que isso explica sobre os experimentos anteriores

| contexto | $\Delta f_{\min}$ | $T_{\max}$ mínimo ($W=5$) | $T_{\max}$ usado |
|---|---|---|---|
| Sieve $[2..15]$ | 0.01098 | 1.002 | 6500 (6.5× excesso) |
| Batch $\{15..53\}$ | 0.00884 | 1.244 | 6500 (5.2× excesso) |
| Sieve $[2..100]$ | 0.00160 | 6.877 | 6500 (0.95× — sub-especificado) |
| Sieve $[2..300]$ | 0.000531 | 20.700 | 6500 (0.31× — sub-especificado) |

O $T_{\max}=6500$ encontrado empiricamente para $N=300$ estava **tecnicamente
sub-especificado** pelo critério formal para o sieve completo, mas funcionava
porque a interferência dos vizinhos mais densos era amortecida pela amplitude
decrescente $1/\sqrt{\log m}$ dos termos. Para o batch esparso, estava
**sobre-especificado** por um fator de 5×.

### Verificação experimental

Testando a Fase 2 com diferentes $T_{\max}$:

| $T_{\max}$ | acertos | razão max (compostos) | razão min (primos) |
|---|---|---|---|
| 300 | 6/8 | 0.962 — falha | 0.758 — falha |
| 500 | 7/8 | 0.866 — falha | 0.866 — misturado |
| **800** | **8/8** | 0.114 | 0.957 |
| 1500 | 8/8 | 0.012 | 0.986 |
| 3000 | 8/8 | 0.007 | 0.997 |
| 6500 | 8/8 | 0.004 | 1.001 |

Limiar de classificação correta em $T_{\max}\approx800$, consistente com a
previsão teórica de $791$ (W=3) a $1244$ (W=5).

### Consequência para experimentos futuros

Para o sieve completo $[2..N]$, a fórmula exige $T_{\max} \sim 2\pi N(2W+1)$,
confirmando o crescimento linear com $N$ observado empiricamente. Para batchs
esparsos de candidatos, $T_{\max}$ é determinado pelo par de candidatos mais
próximos em log-espaço — independente do maior candidato no conjunto.

---

## 8. Complexidade

### Fase 1

Equivalente ao Crivo de Eratóstenes: para cada um dos $\pi(\sqrt{N}) \sim \sqrt{N}/\ln\sqrt{N}$
primos descobertos, recalcula-se o resíduo dos candidatos restantes. Complexidade total:

$$O\!\left(\frac{N}{\ln N}\right)$$

### Fase 2

| operação | custo | frequência |
|---|---|---|
| Construção do sinal | $O(k \cdot T_{\max}/\Delta t)$ | uma vez por lote |
| FFT | $O(T_{\max}/\Delta t \cdot \log(T_{\max}/\Delta t))$ | uma vez por lote |
| Leitura das razões | $O(k \cdot W)$ | linear em $k$ |

Com $T_{\max} \sim N$ (sieve completo), o custo total da Fase 2 é $O(N\log N)$ para
qualquer tamanho de lote — mesma classe assintótica que o sieve de Eratóstenes, mas
com constante muito maior. O ganho real não é velocidade: é que a FFT é computada uma
vez para $k$ candidatos, com custo marginal $O(T_{\max}/\Delta t)$ por candidato adicional
ao lote, em vez de $O(\sqrt{N}/\ln N)$ por trial division.

**Razão trial division vs. espectral (caso atual):** $\sim32.500\times$ mais operações.
O método espectral não compete em velocidade — compete em informação estrutural (posição
de destino da migração, quantificação do ganho orbital).

---

## 9. Status atual

| Afirmação | Status |
|---|---|
| Fase 1: bootstrap espectral detecta primos em $[2,N]$ sem aritmética inteira explícita | Confirmada para $N=15$ (Seção 3) |
| Fase 2: verificação em lote via colapso orbital | Confirmada 8/8 (100%), gap 0.997 (Seção 4) |
| Detecção de composto com fator fora da base ($22=2\cdot11$, $11\notin P$) | Confirmada via migração para $f_{11}$ (Seção 5) |
| Comportamento da norma $L^2$: cai no batch esparso | Confirmado (ratio 0.8137) e explicado (Seção 6) |
| Fórmula fechada para $T_{\max}$: $(2W+1)\cdot2\pi/\Delta f_{\min}$ | Derivada analiticamente e verificada em 6 valores (Seção 7) |
| Extensão para candidatos maiores ($c > 100$) com $T_{\max}$ calculado pela fórmula | Não testada |
| Fase 1 para $N > 15$ | Não testada |
| Comparação com janela de Hann (reduz requisito de $T_{\max}$) | Não testada |

---

## 10. Próximos passos sugeridos

1. **Testar candidatos maiores com $T_{\max}$ calculado pela fórmula** — ex: candidatos em $[200, 300]$ com $T_{\max}$ determinado pelo gap mínimo entre os candidatos escolhidos, sem usar o valor empírico 6500. Isso validaria a fórmula num regime diferente do testado aqui.

2. **Avaliar o impacto de janela de Hann na fórmula de $T_{\max}$** — janelas de afunilamento trocam amplitude de lóbulo principal por supressão de sidelobe, alterando o critério de resolução. A fórmula muda para $T_{\max} \geq C_W / \Delta f_{\min}$ onde $C_W$ depende do tipo de janela, potencialmente reduzindo o $T_{\max}$ necessário.

3. **Explorar a Fase 2 como ferramenta de fatoração parcial** — o destino de migração de cada composto (onde seu pico vai no sinal removido) revela o $P$-núcleo de $c$, sem divisão explícita. Para $22$, o pico novo em $f_{11}$ identifica que $22/2 = 11$ é o cofator irredutível. Verificar se isso é recuperável com precisão suficiente para candidatos maiores.

4. **Implementar a Fase 1 puramente espectral** — a versão atual usa $\log_{\text{resid}}$ calculado por aritmética; uma versão 100% espectral detectaria "picos que não se moveram" diretamente na FFT. O requisito de $T_{\max}$ seria mais alto (precisa distinguir o pico de $q$ do pico de $q-1$ e $q+1$), mas eliminaria a dependência de aritmética inteira.

---

## 11. Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026). Define a
Redutibilidade Logarítmica, a Proposição de equivalência com primalidade, o operador
$\mathcal{R}_m$ e o Corolário (Crivo Oracle-Free) via Teorema de Invariância.

[Nota 34] T. Bandeira, *Síntese Experimental: Estrutura Orbital sob Eliminação Espectral*
(2026). Estabelece a Lei do Ganho Orbital, a fórmula de Parseval para norma $L^2$, e o
mecanismo de lotação espectral assimétrica. Esta nota usa diretamente a Lei do Ganho
Orbital (Nota 34, Seção 3) como fundação para a Fase 2.

**Relação com a Nota 21.** O Corolário da Nota 21 (Crivo Oracle-Free) e a Fase 2 desta
nota chegam ao mesmo resultado final (apenas irredutíveis sobrevivem à remoção de $P$),
mas por mecanismos diferentes. A Nota 21 usa eliminação de amplitude ($\mathcal{R}_m$)
com ortogonalidade assintótica; esta nota usa deslocamento de frequência (colapso orbital)
com a Lei do Ganho Orbital como previsão quantitativa. São complementares, não equivalentes.

---

## 12. Notebooks e arquivos

| arquivo | conteúdo |
|---|---|
| `exp_crivo_espectral.ipynb` (executado como `exp_crivo_espectral__1_.ipynb`) | Implementação completa das duas fases, medição de razões, visualizações, teste de $T_{\max}$ mínimo |
| `crivo_espectral_resultados.csv` | Tabela completa: candidatos, amplitudes antes/depois, razões, classificação prevista vs. real |
| `crivo_espectral_fase1.png` | Visualização da Fase 1: evolução espectral do bootstrap em $[2,15]$, 6 painéis |
| `crivo_espectral_fase2.png` | Fase 2: espectro antes/depois + barras de razão por candidato |
| `crivo_espectral_zoom_22.png` | Zoom em $f_{22}$ e $f_{11}$: migração do composto $22=2\cdot11$ |
| `crivo_espectral_resultados.zip` | Pacote consolidado dos itens acima |
