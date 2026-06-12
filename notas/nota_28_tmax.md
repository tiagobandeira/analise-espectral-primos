# Nota 28 — Escala de $t_{\max}$ para a Etapa 2: Par Gêmeo Gargalo e Lei Assintótica

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

A Etapa 2 do pipeline espectral original (extração de $\mathcal{P}_<$ via
$R_2(t) = \log|Z_Q(\tfrac{1}{2}+it)| - \log|\zeta(\tfrac{1}{2}+it)|$) requer
um $t_{\max}$ suficiente para separar espectralmente todos os primos de
$\mathcal{P}_<$. A questão da escala exata de $t_{\max}$ como função de $n$
estava em aberto desde a Nota 18.

O Exp G resolve essa questão em três passos. Primeiro (G1): o par de primos
consecutivos em $\mathcal{P}_<$ que exige maior $t_{\max}$ pelo critério de
Rayleigh é sempre um **par gêmeo** — verificado para $n = 4, \ldots, 12$ sem
exceção. Segundo (G5): para gap $g = 2$, o critério simplifica assintoticamente para

$$t_{\min}(n) = \frac{2\pi}{\log\!\left(1 + \tfrac{2}{q_{\text{twin}}}\right)}
\xrightarrow{q \to \infty} \pi \cdot q_{\text{twin}}(n)$$

onde $q_{\text{twin}}(n)$ é o maior elemento do maior par gêmeo em
$\mathcal{P}_<$. A razão observada/$(\pi q_{\text{twin}})$ converge para 1
(valor $0{,}9995$ para $n = 12$). Terceiro (G3): comparando com $1/\rho_{\min}$
da Nota 27, ambas as escalas crescem exponencialmente como $2^n$, mas com
fatores polinomiais distintos:

$$t_{\min}(n) \sim \pi \cdot q_{\text{twin}}(n) \sim \pi \cdot 2^{n-2}$$
$$1/\rho_{\min}(n) \sim q_{\max}(n) \cdot \log q_{\max}(n) \sim 2^{n+1}(n+1)\log 2$$

A Questão 3 da Nota 27 — se $t_{\max}$ e $1/\rho^*$ crescem à mesma taxa — é
respondida parcialmente: mesma escala exponencial dominante $2^n$, fator
polinomial distinto (1/rho_min cresce um fator $\sim n \log 2$ mais rápido).

---

## 1. Contexto

A Etapa 2 do pipeline espectral extrai $\mathcal{P}_< = \{q \text{ primo} :
q < 2^{n-1}\}$ a partir do sinal residual $R_2(t)$. A regra empírica
$t_{\max} > 2\pi / (\log q_2 - \log q_1)$ para o par mais próximo estava
documentada desde a Nota 22, mas a dependência de $t_{\max}$ com $n$ não havia
sido determinada. O Exp 3 do `fundamentos_teoricos_v2.ipynb` mostrava que o
SNR da Etapa 2 decai com $n$, indicando crescimento de $t_{\max}$ mais rápido
do que linear. Esta nota determina a lei de escala exata.

---

## 2. Par gargalo: sempre um par gêmeo

**Definição.** O par gargalo de $\mathcal{P}_<$ no nível $n$ é o par de primos
consecutivos $(q_1, q_2) \in \mathcal{P}_<$ que maximiza o $t_{\min}$ de
Rayleigh:

$$t_{\min}(q_1, q_2) = \frac{2\pi}{\log q_2 - \log q_1} = \frac{2\pi}{\log(q_2/q_1)}$$

**Observação empírica (G1).** Para todo $n = 4, \ldots, 12$, o par gargalo é
o maior par gêmeo (gap $= 2$) em $\mathcal{P}_<$:

| $n$ | Par gargalo | Gap | Par gêmeo? | $t_{\min}$ |
|---|---|---|---|---|
| 4  | $(5, 7)$       | 2 | sim | 18,7  |
| 5  | $(11, 13)$     | 2 | sim | 37,6  |
| 6  | $(29, 31)$     | 2 | sim | 94,2  |
| 7  | $(59, 61)$     | 2 | sim | 188,5 |
| 8  | $(107, 109)$   | 2 | sim | 339,3 |
| 9  | $(239, 241)$   | 2 | sim | 754,0 |
| 10 | $(461, 463)$   | 2 | sim | 1451,4|
| 11 | $(1019, 1021)$ | 2 | sim | 3204,4|
| 12 | $(2027, 2029)$ | 2 | sim | 6371,2|

A razão é estrutural: pares gêmeos têm o menor gap relativo $g/q = 2/q$
possível, minimizando $\log(q_2/q_1) = \log(1 + 2/q_1)$ e portanto
maximizando $t_{\min}$. Primos consecutivos com gap maior têm $t_{\min}$ menor.
O maior par gêmeo de $\mathcal{P}_<$ está sempre próximo do topo da distribuição
$q \lesssim 2^{n-1}$, combinando o gap mínimo com o maior $q$.

---

## 3. Lei assintótica: $t_{\min}(n) \to \pi \cdot q_{\text{twin}}(n)$

Para um par gêmeo $(q, q+2)$ com $q$ grande:

$$t_{\min} = \frac{2\pi}{\log\!\left(\frac{q+2}{q}\right)}
= \frac{2\pi}{\log\!\left(1 + \frac{2}{q}\right)}
\approx \frac{2\pi}{\frac{2}{q} - \frac{2}{q^2} + \cdots}
= \pi q \cdot \frac{1}{1 - \frac{1}{q} + \cdots}
\to \pi q$$

A convergência é verificada pelo Exp G5:

| $n$ | $q_{\text{twin}}$ | $t_{\min}$ observado | $\pi \cdot q_{\text{twin}}$ | razão |
|---|---|---|---|---|
| 6  | 31   | 94,2   | 97,4   | 0,9674 |
| 8  | 109  | 339,3  | 342,4  | 0,9908 |
| 10 | 463  | 1451,4 | 1454,6 | 0,9978 |
| 12 | 2029 | 6371,2 | 6374,3 | 0,9995 |

**Resultado:**

$$\boxed{t_{\max}^*(n) \approx \pi \cdot q_{\text{twin}}(n)}$$

onde $q_{\text{twin}}(n)$ é o maior elemento do maior par gêmeo de
$\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$.

O crescimento é exponencial em $n$: $q_{\text{twin}}(n) \lesssim 2^{n-1}$,
portanto $t_{\max}^*(n) = O(2^n)$ — confirmando o gargalo exponencial
indicado pelo Exp 3.

---

## 4. Comparação com $\rho_{\min}(k)$ (Questão 3, Nota 27)

A Nota 27 estabeleceu $\rho_{\min}(k) \approx 1/(q_{\max}(k) \cdot \log
q_{\max}(k))$, portanto $1/\rho_{\min}(k) \approx q_{\max}(k) \cdot \log
q_{\max}(k)$. O Exp G3 compara diretamente:

| $n$ | $t_{\min}(n)$ | $1/\rho_{\min}(n-1)$ | razão |
|---|---|---|---|
| 4  | 18,7   | 33,3   | 0,560 |
| 6  | 94,2   | 250,8  | 0,376 |
| 8  | 339,3  | 1386,9 | 0,244 |
| 10 | 1451,4 | 5929,6 | 0,245 |
| 12 | 6371,2 | 24990  | 0,255 |

A razão não é constante — decresce com $n$, indicando que $1/\rho_{\min}$
cresce mais rápido. Explicitando:

$$t_{\min}(n) \sim \pi \cdot q_{\text{twin}}(n) \sim \pi \cdot 2^{n-2}$$

$$\frac{1}{\rho_{\min}(n-1)} \sim q_{\max}(n-1) \cdot \log q_{\max}(n-1)
\sim 2^n \cdot n \log 2$$

A razão é $t_{\min} / (1/\rho_{\min}) \sim \pi/(4 n \log 2) \to 0$, confirmando
que os dois crescimentos, embora ambos exponenciais em base $2^n$, diferem por
um fator polinomial $n \log 2$.

**Conclusão sobre a Questão 3 da Nota 27:** as duas escalas têm a mesma
base exponencial $2^n$ mas fatores polinomiais distintos. A equivalência é
de ordem de grandeza ($O(2^n)$), não de lei exata. A diferença polinomial
tem interpretação precisa:

- $t_{\min}(n)$ é determinado pelo **par gêmeo mais alto de $\mathcal{P}_<$**
  (diretamente proporcional a $q_{\text{twin}}$).
- $1/\rho_{\min}(n)$ é determinado pelo **maior primo do bloco $A_n$**
  multiplicado por $\log q_{\max}$ (o fator logarítmico extra vem da
  definição de $\rho$ como distância relativa em $\log$).

---

## 5. Nota sobre a Etapa 2 no pipeline atual

Na versão final do pipeline (Notas 23–24), a Etapa 2 foi substituída pela
recursão aritmética, que não depende de $t_{\max}$. A questão desta nota é
portanto sobre a versão espectral original e sobre o entendimento estrutural
do método — não sobre o pipeline em uso.

O resultado tem relevância prática para quem quiser usar a versão espectral
da Etapa 2 (por exemplo, em contextos onde a recursão aritmética não está
disponível): o $t_{\max}$ deve ser $\gtrsim \pi \cdot q_{\text{twin}}(n)$,
onde $q_{\text{twin}}(n)$ é facilmente identificável sem aritmética extra
(basta encontrar o maior par gêmeo em $\mathcal{P}_<$, que é conhecido
após a recursão).

---

## 6. Resolução das questões abertas

**Questão 2 da série** (*"Escala de $t_{\max}$ para SNR da Etapa 2"*, Nota 18,
Questão 3) — **Respondida:**

$$t_{\max}^*(n) \approx \pi \cdot q_{\text{twin}}(n) = O(2^n)$$

O gargalo é o maior par gêmeo de $\mathcal{P}_<$. O crescimento é exponencial,
confirmando que a Etapa 2 espectral não escala polinomialmente em $n$.

**Questão 3 da Nota 27** (*"Escala de $t_{\max}$ e de $\rho^*$ são
equivalentes?"*) — **Respondida parcialmente:** mesma escala exponencial $2^n$,
fator polinomial distinto. $1/\rho_{\min}$ cresce um fator $\sim n \log 2$
mais rápido que $t_{\min}$.

---

## 7. Questões em aberto remanescentes

**Questão 1 — Prova formal do par gêmeo gargalo.** A observação de que o
par gêmeo é sempre o gargalo foi verificada empiricamente para $n \leq 12$.
Uma prova formal precisaria mostrar que nenhum par de primos consecutivos
não-gêmeo em $\mathcal{P}_<$ tem $t_{\min}$ maior que o maior par gêmeo.
Isso equivale a mostrar que para todo par $(q_1, q_2)$ com gap $g \geq 4$ e
$q_2 \leq q_{\text{twin}}$, $\log(q_2/q_1) > \log(1 + 2/q_{\text{twin}})$.

**Questão 2 — Escala de $t_{\max}$ para primos gêmeos (Questão 1 da série).**
A tabela da Nota 19 mostrava $t_{\min} \sim O(p/\log p)$ para pares gêmeos
até $p = 463$. O Exp G5 mostra que a mesma lei $t_{\min} \approx \pi q$ vale
para os pares gêmeos gargalo de $\mathcal{P}_<$. A questão analítica de se
existe $t_{\max}$ polinomial em $p$ que garanta separação de todos os pares
gêmeos permanece em aberto — a evidência empírica aponta para $O(p)$, não
polinomial em $\log p$.

**Questão 3 — Fator polinomial entre $t_{\min}$ e $1/\rho_{\min}$.** A razão
$t_{\min}(n)/(1/\rho_{\min}(n)) \sim \pi/(4 n \log 2)$ é precisa mas não foi
formalizada analiticamente. Uma demonstração envolveria distribuição de primos
gêmeos em $\mathcal{P}_<$ e a distribuição do maior primo do bloco $A_n$.

---

## Referências

[Nota 18] T. Bandeira, *Benchmark Espectral: Primorial, Fatorial e $Q(p)$*,
nota adicional (2026).  
[Nota 19] T. Bandeira, *Detector Espectral de Primalidade*, nota adicional
(2026).  
[Nota 22] T. Bandeira, *Método do Crivo Espectral Oracle-Free*, nota
adicional (2026).  
[Nota 23] T. Bandeira, *Extração Recursiva de Primos via Blocos Binários*,
nota adicional (2026).  
[Nota 27] T. Bandeira, *Cota Assintótica para $\rho_{\min}(k)$ e Limiar
Adaptativo*, nota adicional (2026).  
[Exp G] T. Bandeira, `exp_g_tmax.ipynb` — Escala de $t_{\max}$ para Etapa 2:
par gêmeo gargalo e lei assintótica, Junho de 2026.
