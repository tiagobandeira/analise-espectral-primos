# Nota 16 — Conexão Espectral entre Blocos Binários e a Hierarquia Primorial

**T. Bandeira · Junho de 2026**  
*Série Motor de Herança Estrutural — Notas complementares*

---

## Resumo

Mostramos que o produto $Q(p)$ de todos os inteiros desde o início do bloco
binário anterior até um primo $p$ (exclusive) contém, fatorados, todos os
primos menores que $p$. A análise espectral (FFT) da razão $Z_Q/\zeta$ revela
picos nas frequências $\log(q)/(2\pi)$ associados aos primos $q < 2^{n-1}$ —
aqueles que aparecem no intervalo apenas via múltiplos compostos. Os primos
$q \in [2^{n-1}, p-1]$ são cancelados pela divisão por $\zeta$ e requerem o
pipeline de dois estágios desenvolvido na Nota 17 para serem recuperados. Os
primoriais assim extraídos, usados como razões em progressões aritméticas,
geram sequências com alta densidade de primos — conectando a caracterização de
primalidade por blocos binários (Teorema 1) com a hierarquia $L(P_n)$ da
Nota 14.

---

## 1. Definições e resultado básico

Para um primo $p$, seja $n = \lfloor\log_2 p\rfloor$ (i.e.,
$p \in A_n = [2^n, 2^{n+1}-1]$). Defina:

$$Q(p) = \prod_{x = 2^{n-1}}^{p-1} x$$

**Proposição.** $Q(p)$ é um múltiplo do primorial de todos os primos menores
que $p$:

$$\prod_{q < p} q \ \mid\ Q(p)$$

*Demonstração.* O intervalo $[2^{n-1}, p-1]$ contém o bloco $A_{n-1}$, cujo
produto já contém todos os primos $\le 2^n - 1$ (Nota MDC, Teorema 1). Os
primos entre $2^n$ e $p-1$ aparecem diretamente como fatores. $\square$

---

## 2. Análise espectral de $Z_Q/\zeta$

Seja:

$$Z_Q(s) = \prod_{x = 2^{n-1}}^{p-1} \frac{1}{1-x^{-s}}, \qquad s =
\tfrac{1}{2} + it$$

Considere o sinal:

$$R(t) = \log\left|\frac{Z_Q(\tfrac{1}{2}+it)}{\zeta(\tfrac{1}{2}+it)}\right|$$

A FFT de $R(t)$ amostrado em $t$ exibe picos nas frequências
$f_q = \log(q)/(2\pi)$. A divisão por $\zeta$ remove o "ruído de fundo"
comum, realçando as contribuições dos primos contidos em $Q(p)$.

**Ressalva sobre o alcance espectral de $Z_Q/\zeta$.**
A afirmação de que $R(t)$ exibe picos para *todo* primo $q < p$ requer
qualificação. A análise experimental revela um efeito de cancelamento: os
primos $q \in [2^{n-1}, p-1]$ aparecem como fatores tanto em $Z_Q$ quanto em
$\zeta$, e sua contribuição é cancelada pela divisão. O que $R(t)$
efetivamente carrega são os picos dos primos $q < 2^{n-1}$ — aqueles que
aparecem no intervalo apenas indiretamente, via múltiplos compostos.

Para $p = 37$ ($n = 5$, intervalo $[16, 36]$): os primos $\{17,19,23,29,31\}$
são cancelados; os primos $\{2,3,5,7,11,13\}$ são recuperados. O método
recupera portanto o primorial $d = 2 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot
13 = 30030$, correspondente ao nível $P_6 = 13$ da hierarquia da Nota 14 —
não o primorial completo até $p$.

A Proposição (que $\prod_{q<p} q \mid Q(p)$) permanece válida. O que esta
seção descreve é o comportamento de $Z_Q/\zeta$ isoladamente. A recuperação
de *todos* os primos $< p$ — incluindo os do intervalo $[2^{n-1}, p-1]$ —
requer o pipeline de dois estágios da Nota 17, que substitui $\zeta$ por
referências mais cirúrgicas.

**Nota sobre o sinal.** A fórmula correta para $\log|Z_Q(\tfrac{1}{2}+it)|$
usa o sinal negativo:

$$\log|Z_Q| = -\tfrac{1}{2}\sum_x \log\!\left(1 - 2x^{-1/2}\cos(t\log x)
+ x^{-1}\right)$$

Uma implementação com $+\tfrac{1}{2}$ computa $\log|1/Z_Q|$; o efeito sobre
os picos da FFT é nulo (amplitude simétrica), mas a semântica está invertida.

---

## 3. Verificação experimental

Tomamos $p = 37$ ($A_5$, intervalo $[16,36]$). Com $t \in [0.1, 50]$,
passo $0.1$, o método $Z_Q/\zeta$ recuperou:

$$[2, 3, 5, 7, 13, 17, 23, 29]$$

Os primos $\{11, 19, 31\}$ ficaram fora — $11$ e $19$ por limitação de
resolução; $17$ e $31$ aparecem porque seus picos sobrevivem parcialmente ao
cancelamento nessa configuração. Com o pipeline de dois estágios (Nota 17,
$t_{\max}=300$, $\Delta t=0.02$) a recuperação é completa: $11/11$ primos sem
falsos positivos.

Usando os primoriais extraídos como razões em progressões aritméticas:

| Primorial $d$ | Âncora | Primeiros 5 termos | Primos/5 |
|:---|:---|:---|:---|
| $2$ | $3$ | $3,5,7,9,11$ | 4 |
| $6$ | $5$ | $5,11,17,23,29$ | 5 |
| $30$ | $7$ | $7,37,67,97,127$ | 5 |
| $210$ | $13$ | $13,223,433,643,853$ | 5 |
| $2730$ | $17$ | $17,2747,5477,8207,10937$ | 3 |
| $46410$ | $23$ | $23,46433,92843,139253,185663$ | 1 |
| $1067430$ | $29$ | $29,1067459,2134889,3202319,4269749$ | 3 |
| $30955470$ | $29$ | $29,30955499,61910969,92866439,123821909$ | 1 |

A escolha de âncora aqui é simplificada (próximo primo na lista extraída), não
o $a_0 = 6C_0 + P_{n+1}$ da Nota 14. O objetivo é apenas mostrar que os
primoriais extraídos produzem sequências com alta densidade de primos,
validando a conexão estrutural. A busca por $C_0$ ótimo é o refinamento
natural (Nota 17, Seção 7).

---

## 4. Conexão com a hierarquia $L(P_n)$

Os primos extraídos, ordenados, são $q_1=2, q_2=3, q_3=5, \ldots$. Seus
produtos parciais:

$$d_k = \prod_{i=1}^{k} q_i$$

são exatamente os primoriais que aparecem como razões das progressões na
Nota 14. A conexão entre as notas é:

- **Nota MDC** (blocos binários): produtos de intervalos $[2^{\lfloor
  n/2\rfloor}, 2^{\lfloor n/2\rfloor+1}-1]$ decidem primalidade via MDC.
- **Nota 16** (presente): $Q(p)$ contém todos os primos $< p$; $Z_Q/\zeta$
  recupera os primos $< 2^{n-1}$ espectralmente.
- **Nota 17** (pipeline completo): pipeline de dois estágios recupera todos os
  primos $< p$, valida as sequências $L(P_n)$ com candidatos espectrais e
  posiciona o método na literatura.
- **Nota 14** (hierarquia): usa os primoriais como razões para construir
  progressões longas de primos, com âncora via $C_0$.

A estrutura primorial emerge naturalmente dos blocos binários e é detectável
espectralmente — sendo a base para a construção de progressões de primos sem
crivo e sem conhecimento prévio dos zeros de $\zeta$.

---

## 5. Conclusão

Unificamos três frentes:

1. Caracterização de primalidade por MDC em blocos binários (Nota MDC).
2. Recuperação espectral de primoriais via $Q(p)$ e $Z_Q/\zeta$, com
   limitação de cancelamento identificada e resolvida na Nota 17.
3. Construção de progressões aritméticas de primos com razão primorial
   (Nota 14).

O elo central é o primorial: aparece como fator de qualquer produto de
inteiros consecutivos suficientemente longo, e é recuperável espectralmente
sem conhecer os primos de antemão. A Nota 17 estende esse resultado ao caso
completo ($Z_Q/Z_{\text{comp}}$ para primos grandes,
$Z_Q/\zeta/Z_{\mathcal{P}_>}$ para primos pequenos) e documenta a validação
computacional das sequências $L(P_n)$.

---

## Referências

- **Nota MDC:** T. Bandeira, *Uma caracterização de primalidade via partições
  binárias e MDC em intervalos reduzidos* (2026).
- **Nota 14:** T. Bandeira, *Sequência de Sequências de Primos via Operador
  $W_i$ e Estrutura Primorial* (2026).
- **Nota 15:** T. Bandeira, *Estrutura Primorial, Classes Residuais e Conexões
  com a Função Zeta* (2026).
- **Nota 17:** T. Bandeira, *Ferramenta Espectral via $Q(p)$: Fundamentação e
  Validação Computacional* (2026).
- Green, B., Tao, T. (2008). *The primes contain arbitrarily long arithmetic
  progressions*. Annals of Mathematics.