# Nota 36 — Detector Espectral de Fator Comum em Lote

**T. Bandeira · Junho de 2026**
*Nota experimental — complementa Nota 34 e Nota 35*

---

## Resumo

Esta nota demonstra que a Lei do Ganho Orbital (Nota 34) implica um
**detector de fator comum em lote**: quando $k$ candidatos compartilham
um fator primo $q$ (após remoção de uma base $P$ de primos pequenos),
seus picos espectrais convergem coerentemente para $f_q = \log q/(2\pi)$
com amplitude exatamente $k \times \text{amp\_iso}(q)$. O detector
identifica qual fator é compartilhado e por quantos candidatos —
com uma única FFT e sem operações aritméticas sobre os candidatos.

Três experimentos confirmam a lei e demonstram o detector:

- **Exp B:** crescimento linear exato com $k=1,\ldots,7$ — razão$/k = 1.00000$
  com **erro máximo 0.00000** (cinco casas decimais zeradas).
- **Exp C:** três fatores simultâneos (5×11, 3×13, 2×17) detectados com erro $< 0.011$.
- **Exp D:** 16 candidatos sem revelação de estrutura — detector identifica
  corretamente q=11 (7 candidatos) e q=13 (5 candidatos), com razões 6.990 e 4.986.
  Gap sinal/fundo: **4.96×**.

O resultado qualitativo mais importante emerge da comparação com MDC par-a-par:
o detector espectral identifica o **cofator primo** diretamente, enquanto o MDC
retorna fatores compostos (22, 55, 77 em vez de 11) que requerem etapa
adicional de fatoração.

---

## 1. Contexto

A Lei do Ganho Orbital (Nota 34, Seção 3) estabelece que após remoção
dos fatores de $P$ de um sinal de candidatos, a amplitude em $f_r$
cresce proporcionalmente a $|\mathcal{O}_r|$ — o número de candidatos
cujo cofator é $r$. Essa lei foi verificada nos experimentos FA-LOG-2
com erros de $\pm 2\%$, atribuídos ao ruído de lotação espectral de
sinais densos (Nota 34, Seção 5).

Esta nota aplica a mesma lei a sinais **esparsos** (poucos candidatos),
onde o ruído de fundo é $\sim 10^{-4}$ e a lei se verifica com precisão
numérica exata. O resultado transforma a Lei do Ganho Orbital num
mecanismo de detecção prático: dado um lote de candidatos, o espectro
residual identifica todos os fatores primos compartilhados
simultaneamente, sem nenhuma comparação par a par.

Base $P = \{2, 3, 5, 7\}$ em todos os experimentos
($\lfloor\sqrt{\max \mathcal{C}}\rfloor \leq 13$ para os candidatos usados).

---

## 2. Calibração — amplitude isolada por cofator

A amplitude de referência de um único termo $-\cos(t\log q)/\sqrt{\log q}$
na FFT (sinal com apenas esse componente) é:

$$\text{amp\_iso}(q) \approx \frac{T_{\max}}{2\sqrt{\log q}}$$

Esta fórmula tem erro variável com $q$ por efeito de vazamento espectral
(o sinal começa em $t = 0.1$, não $t = 0$, e o número de ciclos completos
em $[0.1, T_{\max}]$ depende de $q$). Os valores medidos empiricamente:

| $q$ | $\text{amp\_iso\_med}$ | $\text{amp\_iso\_teo}$ | fator de correção |
|---|---|---|---|
| 11 | 1592.20 | 2098.79 | 0.759 |
| 13 | 1495.18 | 2029.29 | 0.737 |
| 17 | 1917.10 | 1930.83 | 0.993 |
| 19 | 1893.94 | 1894.01 | **1.000** |
| 23 | 1470.72 | 1835.40 | 0.801 |
| 29 | 1262.78 | 1771.10 | 0.713 |
| 37 | 1168.10 | 1710.31 | 0.683 |

O fator de correção não é monotônico com $q$ — é determinado pela
fase de $t \cdot \log q$ nas bordas do sinal (valor de $6500 \cdot \log q \bmod 2\pi$).
Para $q = 19$ o alinhamento é quase perfeito; para $q = 37$ a discrepância
é ~32%. A calibração empírica (Exp A) corrige isso inteiramente:
os resultados do Exp D com calibração empírica têm erros $< 0.01$.

---

## 3. Exp B — Lei do ganho: crescimento linear exato

**Candidatos:** $\{22, 33, 44, 55, 77, 110, 154\}$ — todos com cofator 11
(respectivamente $2\cdot11$, $3\cdot11$, $4\cdot11$, $5\cdot11$,
$7\cdot11$, $2\cdot5\cdot11$, $2\cdot7\cdot11$).

| $k$ | $\text{amp}(f_{11})$ | razão | razão$/k$ | erro |
|---|---|---|---|---|
| 1 | 1592.20 | 1.00000 | 1.00000 | 0.0000% |
| 2 | 3184.40 | 2.00000 | 1.00000 | 0.0000% |
| 3 | 4776.60 | 3.00000 | 1.00000 | 0.0000% |
| 4 | 6368.80 | 4.00000 | 1.00000 | 0.0000% |
| 5 | 7961.01 | 5.00000 | 1.00000 | 0.0000% |
| 6 | 9553.21 | 6.00000 | 1.00000 | 0.0000% |
| 7 | 11145.41 | 7.00000 | 1.00000 | 0.0000% |

**Erro máximo: 0.00000** — cinco casas decimais zeradas.

Isso confirma que a Lei do Ganho Orbital não é uma aproximação —
é uma **identidade exata**. Cada candidato contribui com
$-\cos(t\log 11)/\sqrt{\log 11}$ após o colapso (independente
de qual era sua parte $P$-suave), e $k$ cossenos idênticos somam-se
com ganho exatamente $k$. Não há interferência residual porque
os $k$ termos são matematicamente o mesmo cosseno.

---

## 4. Exp C — Três fatores simultâneos

**Candidatos:** 10 números com estrutura oculta —
5 com cofator 11, 3 com cofator 13, 2 com cofator 17.

| fator $q$ | previsto | $\text{amp}(f_q)$ | razão | erro |
|---|---|---|---|---|
| 11 | 5 | 7951.88 | 4.99427 | 0.00573 |
| 13 | 3 | 4469.37 | 2.98920 | 0.01080 |
| 17 | 2 | 3836.81 | 2.00136 | 0.00136 |

Três fatores detectados simultaneamente na mesma FFT,
com erro máximo de **1.1%**. A presença de múltiplos
grupos não causa interferência cruzada entre $f_{11}$, $f_{13}$ e $f_{17}$
porque a separação mínima entre eles é de $\sim 100$ bins
(muito acima da janela $W = 5$ usada para medir amplitudes).

---

## 5. Exp D — Detector cego

**Candidatos:** 16 números apresentados ao algoritmo sem
informação de fatoração:

$$\{22, 33, 44, 55, 77, 110, 154,\ 26, 39, 52, 65, 91,\ 34, 46, 58, 74\}$$

**Estrutura oculta:** 7 candidatos com cofator 11,
5 com cofator 13, 4 com cofatores distintos (17, 23, 29, 37).

O detector varre o espectro residual para $q = 8, \ldots, 49$
e sinaliza posições com razão $> 1.8$:

| $q$ | $\text{amp}$ | razão (emp.) | detecção | real |
|---|---|---|---|---|
| 11 | 11129.13 | **6.98978** | *** COMPARTILHADO *** | 7× |
| 13 | 7454.88 | **4.98595** | *** COMPARTILHADO *** | 5× |
| 17 | 1919.40 | 1.00120 | fundo | 1× |
| 23 | 1478.58 | 1.00535 | fundo | 1× |
| 29 | 1254.09 | 0.99312 | fundo | 1× |
| 37 | 1157.63 | 0.99104 | fundo | 1× |

**Resultado:** 100% correto. As razões arredondam aos inteiros exatos
(7 e 5). O fundo oscila em $0.991$–$1.005$ — praticamente
unitário.

**Gap sinal/fundo:**
- Sinal mínimo (q=13, $k=5$): 4.9860
- Fundo máximo (q=17–37): 1.0053
- **Margem: 4.96× acima do fundo**

Com threshold de 1.8, a margem de segurança é quádrupla.
O detector precisaria do fundo aumentar $5\times$ (por exemplo,
por interferência de um sinal de alta intensidade em $f_q$) para
produzir um falso positivo. Isso não é esperado para sinais esparsos.

---

## 6. Comparação com MDC par-a-par

Para 16 candidatos, o MDC par-a-par requer $k(k-1)/2 = 120$ operações.
O resultado retornado foi:

| MDC encontrado | pares | tipo | fator raiz |
|---|---|---|---|
| 11 | 13 | primo | 11 |
| 13 | 9 | primo | 13 |
| **22** | **6** | **composto** (2·11) | requer fatoração adicional |
| **26** | **1** | **composto** (2·13) | requer fatoração adicional |
| **55** | **1** | **composto** (5·11) | requer fatoração adicional |
| **77** | **1** | **composto** (7·11) | requer fatoração adicional |

O MDC entre dois múltiplos de 11 que compartilham
também o fator 2 retorna 22, não 11. Para consolidar
que o fator raiz é 11, seria necessário fatorar 22, 55 e 77 — etapa
adicional após os 120 MDCs.

O detector espectral identifica $f_{11}$ diretamente porque a
remoção de $P = \{2, 3, 5, 7\}$ elimina as partes suaves antes da
análise. Candidatos $2\cdot11$, $3\cdot11$, $4\cdot11$ têm partes
suaves distintas — mas após o colapso todos convergem para
$\log 11$, colidindo no mesmo pico. **O cofator primo emerge do
espectro sem etapa adicional**.

| aspecto | MDC par-a-par | Detector espectral |
|---|---|---|
| operações | 120 MDCs | 1 FFT + 36 varreduras |
| output | pares com fator comum | fator primo + contagem |
| fator identificado | pode ser composto | **primo diretamente** |
| etapa adicional | fatoração dos MDCs compostos | nenhuma |
| informação de contagem | requer análise adicional | **direto pela razão** |

---

## 7. Por que o cofator primo emerge diretamente

O mecanismo é a sequência de duas operações:

1. **Remoção de $P$:** para cada candidato $c = s \cdot q$ (com $s$
   $P$-suave e $q$ primo $\notin P$), o colapso orbital subtrai
   $\log s$ e deixa $\log q$. Independente de qual era $s$,
   o resultado é sempre $\log q$.

2. **Soma coerente:** todos os candidatos com o mesmo cofator $q$
   produzem exatamente $-\cos(t\log q)/\sqrt{\log q}$, somando
   coerentemente em $f_q$.

O MDC par-a-par opera no domínio inteiro: $\gcd(2\cdot11, 4\cdot11) = 2\cdot11 = 22$,
porque 2 é fator comum e não há base de primos a remover. O método
espectral remove $P$ antes de medir, e por isso compara apenas
as partes $P$-livres — que coincidem em $q$.

Esta propriedade é uma consequência direta da estrutura do sinal,
não um ajuste ad hoc: o colapso orbital faz exatamente o que o
MDC faria se os candidatos fossem divididos por sua parte $P$-suave antes
da comparação.

---

## 8. Status atual

| Afirmação | Status |
|---|---|
| Lei do ganho exata: razão$/k = 1.00000$ para $k=1,\ldots,7$ | Confirmada — erro máximo 0.00000 (Seção 3) |
| Múltiplos fatores simultâneos detectados com erro $< 1.1\%$ | Confirmada — 3 fatores, 10 candidatos (Seção 4) |
| Detector cego: 100% correto, contagem exata por arredondamento | Confirmada — 16 candidatos, gap 4.96× (Seção 5) |
| Cofator primo identificado diretamente (sem pós-fatoração) | Confirmada — comparação com MDC par-a-par (Seção 6) |
| Funcionamento com cofatores $> 100$ (resolução espectral adequada) | Não testado |
| Comportamento com $k=1$ entre muitos candidatos com fatores distintos | Confirmado (fundo $\approx 1.00$) |
| Escalabilidade para $|\mathcal{C}| \gg 16$ candidatos | Não testado |

---

## 9. Próximos passos sugeridos

1. **Testar cofatores maiores** (ex: $q = 101, 103, 107$) com o
   $T_{\max}$ calculado pela fórmula da Nota 35
   ($T_{\max} \geq (2W+1) \cdot 2\pi / \Delta f_{\min}$),
   verificando se a lei e o detector se sustentam para candidatos
   maiores sem aumentar arbitrariamente o sinal.

2. **Escalabilidade com $|\mathcal{C}|$:** testar com 50–100 candidatos
   partilhando fatores, verificando se o fundo cresce (por interferência
   de mais termos distintos) ou se permanece em $\approx 1.00$.
   A Lei do Ganho Orbital prevê que o sinal cresce linearmente com $k$
   e o fundo permanece constante, então o SNR deve crescer com $k$.

3. **Fatoração iterativa:** após identificar cofatores de primeira camada,
   aplicar o detector novamente ao conjunto de cofatores para extrair
   fatores de segunda camada (ex: se um cofator é $11 \cdot 13$, ele
   apareceria em $f_{11\cdot13}$; uma segunda rodada separaria 11 de 13).
   Isso seria o análogo espectral de fatoração hierárquica.

4. **Comparação com product tree GCD** (Bernstein, 2004) —
   o método clássico de batch GCD para $k$ candidatos com
   custo $O(k \log^2 N)$. O detector espectral usa $O(k T_{\max}/\Delta t)$
   para construção do sinal e $O(T_{\max}/\Delta t \cdot \log(T_{\max}/\Delta t))$
   para a FFT. Para $T_{\max} \sim N$, a comparação de custo depende de $k$
   e do tamanho dos candidatos.

---

## 10. Referências

[Nota 34] T. Bandeira, *Síntese Experimental: Estrutura Orbital sob Eliminação
Espectral* (2026). Estabelece a Lei do Ganho Orbital e a fórmula de Parseval
para norma $L^2$. Esta nota aplica a lei diretamente como mecanismo de detecção.

[Nota 35] T. Bandeira, *Verificação Espectral por Colapso Orbital* (2026).
Deriva a fórmula de $T_{\max}$ e demonstra a verificação de primalidade em lote.
O detector desta nota usa a mesma infraestrutura de colapso orbital.

**Conexão com literatura clássica.** O problema de encontrar fatores comuns
em lotes de candidatos é abordado classicamente por MDC par-a-par
($O(k^2 \log N)$) e pelo método de product tree GCD de Bernstein (2004)
($O(k \log^2 N)$). O detector espectral desta nota não compete diretamente
em assintótica para candidatos grandes, mas oferece uma característica
qualitativa ausente nos métodos clássicos: **identificação direta do
cofator primo** sem etapa de pós-fatoração dos resultados.

---

## 11. Notebooks e arquivos

| arquivo | conteúdo |
|---|---|
| `exp_detector_fator_comum.ipynb` | Implementação completa: Exp A (calibração), Exp B (lei linear), Exp C (três fatores), Exp D (detector cego), comparação MDC, análise de SNR |
| `detector_exp_b_linear.png` | Crescimento linear em $f_{11}$ para $k=1\ldots7$ + razão$/k$ vs $k$ |
| `detector_exp_c_dois_fatores.png` | Espectro com três picos distintos + barras de razão medida vs prevista |
| `detector_exp_d_cego.png` | Espectro residual de 16 candidatos + razões por $q$ com threshold |
| `detector_resultados.zip` | Pacote consolidado das figuras |
