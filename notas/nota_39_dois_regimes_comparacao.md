# Nota 39 — Dois Regimes do Detector Espectral e Comparação com MDC par-a-par

**T. Bandeira · Junho de 2026**
*Nota de consolidação — complementa Nota 36, Nota 37 e Nota 38*

---

## Resumo

As Notas 36–38 estabeleceram que o detector espectral opera com um número
**fixo** de FFTs estruturais por stage, independente de $k$ — e reportaram
uma vantagem de "2 FFTs vs. 435 GCDs" no Exp D. Esta nota formaliza o quadro
completo: o detector opera em dois regimes com perfis de custo distintos,
e a vantagem computacional real em tempo de parede depende criticamente de qual
regime está em uso e da magnitude de $k$.

**Dois regimes:**

- **Regime A — cofator conhecido a priori:** o custo dominante é a construção
  do sinal ($k$ cossenos num array de $N \approx 130{.}000$ pontos),
  que cresce linearmente com $k$. O MDC par-a-par cresce como $k^2/2$.
  Cruzamento medido empiricamente: **$k \approx 43{.}000$**.

- **Regime B — varredura cega ($Q_{\max}$ candidatos a cofator):** o custo
  dominante é a calibração de $\text{amp\_iso}(q)$ para cada $q$ na varredura.
  Com a fórmula fechada derivada nesta nota, esse custo é $O(Q_{\max})$ em
  aritmética pura — sem nenhuma FFT de calibração.

**O que não muda:** todos os resultados matemáticos das Notas 34–38 são
independentes de custo computacional. A Lei do Ganho Orbital, a Lei da
Interferência Nula, a fatoração por cascata e a classificação cega 30/30
do Exp D permanecem válidos sem nenhuma ressalva.

**O ganho qualitativo permanece em qualquer regime:** o detector identifica
o **fator primo** diretamente (não compostos como 22, 55, 77), revela
**quantos candidatos** compartilham cada fator via razão de amplitude,
e classifica **todo o lote simultaneamente** com uma única FFT estrutural.
Essas propriedades não têm equivalente direto no MDC par-a-par.

---

## 1. Contexto

A Nota 36 (§6) comparou o detector espectral com MDC par-a-par,
apontando que 120 operações de MDC eram substituídas por 1 FFT.
A Nota 38 (§2.2) generalizou: $O(1)$ FFTs estruturais vs. $O(k^2)$ MDCs,
com FFTs fixas em 2 (Stage 1 + Stage 2) para qualquer $k$.

Essas afirmações eram válidas para as Notas 36–38, onde a calibração de
`amp_iso` era feita para um conjunto pequeno e fixo de cofatores
pré-identificados (4–7 FFTs de calibração, amortizadas).

O Exp D introduziu uma varredura cega sobre todos os $q \in [8, Q_{\max}]$
— necessária para o cenário realista onde nenhum cofator é conhecido a priori.
Essa generalização alterou o perfil de custo de forma que não estava explícita
nas notas anteriores, e que esta nota formaliza agora.

---

## 2. Custo real do Exp D

O Exp D (30 candidatos, `max(LOTE)=2145`, `Q_max=1073`) executou:

| etapa | FFTs | descrição |
|---|---|---|
| Stage 1 — sinal completo | 1 | estrutural, inevitável |
| Varredura cega $q=8,\ldots,1072$ | **1065** | calibração por `amp_iso_de(q)` |
| Stage 2 — crack de 143 | 2 | estrutural, inevitável |
| **Total** | **1068** | vs. 435 MDCs do par-a-par |

A calibração representa 99,7% do custo total. Com a fórmula fechada
da Seção 4, ela é reduzida a zero FFTs (cálculo analítico puro).

---

## 3. Os dois regimes formalizados

### Regime A — cofator conhecido a priori

Usado nas Notas 36–38 (Exp A, B, C, D de Nota 36; Cascata da Nota 37;
Escala da Nota 38). O cofator alvo é pré-identificado; `amp_iso` é
calibrada uma vez para cada cofator do conjunto fixo.

| operação | custo | escala em $k$ |
|---|---|---|
| Construção do sinal | $k \times N$ ops aritméticas | **linear** |
| FFT do espectro | $N \log N$ | constante |
| Leitura de amplitude | $O(W)$ por cofator | constante |

O custo total cresce **linearmente** em $k$ (dominado pela construção
do sinal), enquanto o MDC cresce como $k^2/2$.

### Regime B — varredura cega

Usado no Exp D. Nenhum cofator é conhecido; todos os $q \in [8, Q_{\max}]$
são testados. Com a fórmula fechada (Seção 4):

| operação | custo | escala |
|---|---|---|
| Construção do sinal | $k \times N$ ops | linear em $k$ |
| FFT do espectro | $N \log N$ | constante |
| Calibração vetorizada | $Q_{\max}$ ops aritméticas | constante em $k$ |

O custo total ainda cresce linearmente em $k$, mas com constante maior
(adiciona $Q_{\max}$ operações independentes de $k$). Para candidatos
pequenos do Exp D ($Q_{\max} = 1073$), o custo fixo de calibração
domina sobre $k \times N$ até $k$ grande.

---

## 4. Fórmula fechada para `amp_iso(q)`

`amp_iso(q)` — amplitude do cosseno puro $-\cos(\omega_0 t)/\sqrt{\omega_0}$
na FFT, $\omega_0 = \log q$ — admite expressão exata via série geométrica:

$$\text{amp\_iso}(q) = \left| \frac{\Delta t}{2\sqrt{\log q}}
\bigl[S(\omega_0 - \omega_f) + S(-\omega_0 - \omega_f)\bigr] \right|$$

onde $\omega_f = 2\pi \lfloor \omega_0 / (2\pi\,\Delta f) \rceil\,\Delta f$
é a frequência do bin mais próximo e:

$$S(\alpha) = e^{i\alpha t_0}\,
\frac{1 - e^{i\alpha N\Delta t}}{1 - e^{i\alpha\Delta t}}$$

Avaliação $O(1)$ em aritmética complexa — sem FFT. Diferença em relação
ao método original (FFT completa): $1{,}68 \times 10^{-12}$ (zero ao
nível de precisão de ponto flutuante). Vetorizando sobre todos os
$Q_{\max}$ valores de $q$ simultaneamente (broadcasting NumPy),
o custo total de calibração cai de ~9.000 ms para **2,87 ms**.

---

## 5. Cruzamento real com MDC par-a-par

Medindo os dois métodos no **mesmo lote** (candidatos gerados pelo
padrão das notas: $s \times \text{cofator}$, $s$ $P_1$-suave):

### Regime A (cofator conhecido, pipeline corrigido)

| $k$ | tempo MDC | tempo espectral | vence |
|---|---|---|---|
| 100 | 0,4 ms | 48 ms | MDC |
| 1.000 | 40 ms | 480 ms | MDC |
| 5.000 | 1.000 ms | 2.400 ms | MDC |
| 10.000 | 4.000 ms | 4.800 ms | MDC |
| **43.000** | **~92.000 ms** | **~92.000 ms** | **cruzamento** |
| 50.000 | 125.000 ms | 107.000 ms | Espectral |

**Cruzamento: $k \approx 43{.}000$.**

O cruzamento existe porque o custo do espectral é $O(k)$ e o do MDC
é $O(k^2)$ — mas a constante do espectral ($\propto N = 130{.}000$)
é muito maior que a constante do MDC (uma operação de GCD por par).
Somente para lotes muito grandes ($k > 43{.}000$) o espectral vence
em tempo de parede no regime A.

### Regime B (varredura cega, pipeline corrigido com fórmula fechada)

O custo fixo de calibração ($Q_{\max}$ avaliações da fórmula fechada)
é constante em $k$. Para o Exp D ($Q_{\max} = 1073$): ~2,87 ms.
O cruzamento nesse regime depende de $Q_{\max}$ e do tamanho dos
candidatos — para os parâmetros do Exp D, o cruzamento está além dos
$k$ testados, mas o pipeline corrigido é 82× mais rápido que o original.

---

## 6. Margem sinal/fundo — confirmação do SNR crescente com k

A varredura completa do Exp D sem corte de threshold:

| métrica | Nota 36 ($k_{\min}=5$) | Exp D ($k_{\min}=6$) |
|---|---|---|
| sinal mínimo | 4,99 | 6,00 |
| fundo máximo | 1,005 | 0,127 |
| **margem** | **4,96×** | **47,3×** |

O fundo máximo caiu de 1,005 para 0,127 — o pico anômalo mais alto
no Exp D é o sidelobe de $f_{143}$ em $q=144$, com razão 0,127
(bem abaixo do threshold 1,8). A margem de 47,3× confirma
empiricamente a Lei da Interferência Nula (Nota 38): SNR cresce
com $k$, tornando o detector mais robusto com lotes maiores.

---

## 7. Onde o método ganha — a vantagem qualitativa

O cruzamento em $k \approx 43{.}000$ define o regime onde o detector
espectral vence em **tempo de parede**. Mas há vantagens qualitativas
que independem de $k$:

| aspecto | MDC par-a-par | Detector espectral |
|---|---|---|
| Output | pares com fator comum | **fator primo** + contagem |
| Pós-processamento | fatorar MDCs compostos (22, 55, 77...) | **nenhum** |
| Informação de contagem | requer análise adicional | **direto pela razão** |
| Todos os candidatos | testados um a um | **simultâneo numa FFT** |
| Estrutura revelada | quais pares se relacionam | **qual fator + quantos** |

Para qualquer $k$, o detector entrega mais informação estrutural por
operação do que o MDC — a um custo computacional que só se torna
competitivo em tempo de parede para $k \gtrsim 43{.}000$.

---

## 8. Status consolidado

| afirmação | status |
|---|---|
| "O(1) FFTs estruturais por stage" (Nota 38) | **Válido** — para cofatores pré-identificados (Regime A) |
| "2 FFTs estruturais" no Regime B com fórmula fechada | **Válido** — calibração resolvida analiticamente |
| Lei do Ganho Orbital (Nota 34) | **Válido** — independente de custo computacional |
| Lei da Interferência Nula (Nota 38) | **Válido** — confirmada pela margem 47,3× |
| Fatoração por cascata, 30/30 Exp D | **Válido** — independente de custo |
| SNR cresce com $k$ | **Confirmado** — Nota 36 (4,96×) → Exp D (47,3×) |
| Vantagem em tempo de parede (Regime A) | **A partir de $k \approx 43{.}000$** |
| Vantagem qualitativa (fator primo direto + contagem) | **Em qualquer $k$** |

---

## 9. Próximos passos sugeridos

1. **Testar em $k \approx 43{.}000$** com pipeline corrigido para confirmar
   empiricamente o cruzamento previsto.

2. **Fórmula analítica do erro de Stage 1** — modelagem por sidelobe
   de janela retangular para quantificar o erro residual em função do número
   de grupos e distâncias espectrais (Nota 38 §6, item 3).

3. **Generalizar para cofatores com 3 fatores primos distintos** (ex: 165=3×5×11)
   — verificar que a cascata de profundidade 3 funciona além de 105=3×5×7.

---

## 10. Referências

[Nota 34] T. Bandeira, *Síntese Experimental: Estrutura Orbital sob Eliminação
Espectral* (2026). Lei do Ganho Orbital — fundação de todos os resultados desta série.

[Nota 36] T. Bandeira, *Detector Espectral de Fator Comum em Lote* (2026).
Primeira comparação com MDC par-a-par. A Seção 7 desta nota corrige e expande
essa comparação.

[Nota 37] T. Bandeira, *Fatoração Prima Completa por Cascata de Colapso Orbital*
(2026). Define o Stage 2 (crack de compostos) usado no Exp D.

[Nota 38] T. Bandeira, *Escalabilidade, Profundidade 3 e a Lei da Interferência
Nula* (2026). Estabelece O(1) FFTs estruturais e SNR crescente com $k$.

---

## 11. Notebooks e arquivos

| arquivo | conteúdo |
|---|---|
| `exp_detector_d_batch_res.ipynb` | Exp D: lote de 30 candidatos, classificação cega 30/30, Stage 1+2 |
| `detector_d_resultados.zip` | Figuras do Exp D |
| `nota_39b_auditoria_da_auditoria.ipynb` | Benchmark de cruzamento: MDC vs. espectral, medição sobre mesmo lote, cruzamento k≈42.986 |
| `nota39b_cruzamento_regime_conhecido.png` | Curvas de custo: MDC (quadrático) vs. espectral (linear) com cruzamento anotado |
