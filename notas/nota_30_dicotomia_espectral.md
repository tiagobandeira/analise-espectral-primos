# Nota 30 — Dicotomia Espectral entre Primos e Compostos

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

Dados os sinais espectrais $R_{\text{primo}}(t)$ e $R_{\text{comp}}(t)$,
que isolam respectivamente as contribuições dos primos e dos compostos de
$\{2, \ldots, N\}$, observa-se uma dicotomia espectral robusta em três
camadas distintas. Primeiro, a razão das transformadas de Fourier
$\mathcal{R}(f) = |\mathcal{F}[R_{\text{primo}}](f)| \,/\, |\mathcal{F}[R_{\text{comp}}](f)|$
é consistentemente maior que 1 nas frequências dos primos e menor que 1
nas frequências dos compostos — dicotomia de picos (Exp comparação).
Segundo, o nível de base de $R_{\text{comp}}$ cresce como $\sqrt{N}$ com
$T_{\max}$ fixo enquanto o de $R_{\text{primo}}$ permanece estável em
torno de 1,7 — dicotomia de piso (Exp Q). Terceiro, os vales locais entre
picos têm mediana ~1,3 em $R_{\text{primo}}$ vs ~4,5 em $R_{\text{comp}}$,
com R_comp muito mais irregular (desvio ~5,2 vs ~0,9) — dicotomia de vales.
Os três fenômenos têm origem comum na irredutibilidade logarítmica dos primos
(Nota 21) e na ortogonalidade assintótica das funções $\cos(t \log m)$. A
escala de $T_{\max}$ necessária para sustentar a dicotomia é a mesma
identificada na Nota 28: $T_{\max} \sim \pi \cdot q_{\text{twin}}(N)$,
crescimento exponencial em $\log N$.

---

## 1. Definições e contexto

Dado $N \geq 2$, define-se a aproximação de primeira ordem do log-módulo:

$$Z_N(t) = -\sum_{n=2}^{N} \frac{\cos(t \log n)}{\sqrt{n}}$$

com $Z_N(t) \approx \log|Z_N(\tfrac{1}{2}+it)|$ (Nota 17). Particionando
$\{2, \ldots, N\}$ em primos $\mathcal{P}_N$ e compostos $\mathcal{C}_N$:

$$R_{\text{primo}}(t) = -\sum_{p \in \mathcal{P}_N} \frac{\cos(t \log p)}{\sqrt{p}},
\qquad
R_{\text{comp}}(t) = -\sum_{c \in \mathcal{C}_N} \frac{\cos(t \log c)}{\sqrt{c}}$$

Por construção, $Z_N = R_{\text{primo}} + R_{\text{comp}}$. Os dois sinais
são o complemento um do outro: remover os compostos de $Z_N$ deixa apenas
$R_{\text{primo}}$; remover os primos deixa apenas $R_{\text{comp}}$.

Denotam-se $\mathcal{F}[R](f)$ a transformada de Fourier e
$f_m = \log(m)/(2\pi)$ a frequência característica de $m$.

---

## 2. Dicotomia de picos: razão espectral

### 2.1 Observação

A razão $\mathcal{R}(f) = |\mathcal{F}[R_{\text{primo}}](f)| \,/\,
|\mathcal{F}[R_{\text{comp}}](f)|$ exibe comportamento dicotômico
sistemático (Exp comparação, $N = 50, 100, 200$):

- Nas frequências dos primos $f_p$: $\mathcal{R}(f_p) \gg 1$
  (valores típicos $10$–$10^3$ em escala log)
- Nas demais frequências: $\mathcal{R}(f) < 1$

### 2.2 Justificativa teórica

**Caso $m = p$ primo.** Em $R_{\text{primo}}$, o termo direto
$-\cos(t \log p)/\sqrt{p}$ contribui com amplitude $\approx 1/\sqrt{p}$
na frequência $f_p$. Em $R_{\text{comp}}$, $p$ não está presente. Qualquer
componente em $f_p$ provém de intermodulações entre compostos, que envolvem
somas da forma $\log c = \sum e_i \log p_i$. Como $\log p$ é logaritmicamente
irredutível (Nota 21, Proposição), nenhuma combinação inteira de logs de
compostos $< p$ reproduz $\log p$ exatamente. Pelo Teorema de Invariância
(Nota 21), a contribuição de tais intermodulações em $f_p$ é
$O(T_{\max}^{-1})$ — vazamento espectral não-ressonante que desaparece
no limite $T_{\max} \to \infty$. Portanto:

$$\mathcal{R}(f_p) \approx \frac{1/\sqrt{p}}{O(T_{\max}^{-1})} \gg 1.$$

**Caso $m = c$ composto.** Em $R_{\text{comp}}$, o termo direto contribui
com amplitude $\approx 1/\sqrt{c}$. Em $R_{\text{primo}}$, a fatoração
$c = \prod p_i^{e_i}$ implica $\log c = \sum e_i \log p_i$, de modo que
as intermodulações entre os primos $p_i$ produzem uma componente
*ressonante* em $f_c$ — ressonante porque a igualdade $\log c = \sum e_i
\log p_i$ é exata, não aproximada. A amplitude dessa componente é
proporcional a $\prod 1/\sqrt{p_i}^{e_i} = 1/\sqrt{c}$, da mesma ordem
que o termo direto de $R_{\text{comp}}$. Logo:

$$\mathcal{R}(f_c) \lesssim 1.$$

A distinção é estrutural: primos geram picos isolados e não-ressonantes
em $R_{\text{comp}}$; compostos geram picos ressonantes tanto em
$R_{\text{primo}}$ (via intermodulação) quanto em $R_{\text{comp}}$
(via termo direto), mas o direto domina.

---

## 3. Dicotomia de piso: nível de base

### 3.1 Observação (Exp Q)

Para $T_{\max} = 1000$ fixo e $N$ variando de 30 a 500:

| $N$ | base $R_{\text{primo}}$ | base $R_{\text{comp}}$ | razão |
|---|---|---|---|
| 30  | 1,92 | 2,67 | 0,90 |
| 50  | 1,79 | 3,72 | 0,93 |
| 100 | 1,44 | 4,08 | 1,21 |
| 200 | 1,55 | 5,05 | 1,20 |
| 300 | 1,86 | 5,67 | 1,37 |
| 500 | 2,15 | 6,90 | 1,47 |

O nível de base de $R_{\text{primo}}$ oscila em torno de ~1,7 sem
tendência crescente. O de $R_{\text{comp}}$ cresce sistematicamente, e
a razão entre os dois aumenta com $N$.

### 3.2 Estimativa analítica

O piso de $R_{\text{comp}}$ é determinado pela superposição incoerente das
contribuições de todos os compostos fora de suas frequências próprias. Pela
ortogonalidade assintótica (Nota 21), cada composto $c$ contribui com
$\approx 1/\sqrt{c}$ na frequência $f_c$ e com $O(T_{\max}^{-1})$ nas demais.
O piso coletivo é proporcional à soma dos vazamentos:

$$B_N^{\text{comp}} \sim \sum_{\substack{c \leq N \\ c \text{ composto}}}
\frac{1}{\sqrt{c} \cdot T_{\max}} \sim \frac{2\sqrt{N}}{T_{\max}}$$

pela aproximação $\int_2^N x^{-1/2}\,dx \approx 2\sqrt{N}$. O Exp Q
confirma esse crescimento numericamente.

Para $R_{\text{primo}}$, o mesmo argumento dá $B_N^{\text{primo}} \sim
2\sqrt{\pi(N)}/T_{\max}$, onde $\pi(N) \sim N/\log N$ — crescimento mais
lento que $\sqrt{N}$, consistente com a estabilidade observada para
$T_{\max} = 1000$ e $N \leq 500$.

### 3.3 Consequência

A dicotomia de piso **fortalece com $N$** quando $T_{\max}$ é fixo: a razão
base$_{\text{comp}}$/base$_{\text{primo}}$ cresce de 0,9 (N=30) para 1,47
(N=500). Para $T_{\max} \propto N$, ambos os pisos convergem
($B_N \sim 2\sqrt{N}/N \to 0$), e a dicotomia precisa ser avaliada
em regime diferente.

---

## 4. Dicotomia de vales

### 4.1 Observação

Medindo os mínimos locais dos espectros na região entre frequências de
primos (N=100, $T_{\max}=1000$):

| | média | mediana | desvio | máx |
|---|---|---|---|---|
| $R_{\text{primo}}$ | 1,37 | 1,28 | 0,91 | 3,62 |
| $R_{\text{comp}}$  | 5,26 | 4,47 | 5,16 | 18,12 |

Duas propriedades distintas:

- **Nível:** mediana de $R_{\text{comp}}$ é ~3,5× maior que a de
  $R_{\text{primo}}$.
- **Regularidade:** o desvio de $R_{\text{primo}}$ (~0,9) é muito menor
  que o de $R_{\text{comp}}$ (~5,2). Os vales dos primos são estáveis;
  os dos compostos são irregulares e têm distribuição de cauda pesada
  (desvio ≈ média).

### 4.2 Interpretação

Os vales estáveis de $R_{\text{primo}}$ refletem a independência
logarítmica dos primos: as funções $\cos(t \log p)$ para primos distintos
$p$ se cancelam quase ortogonalmente fora dos picos, produzindo um nível
de fundo baixo e regular. É a contrapartida espectral da irredutibilidade:
primos não interferem construtivamente entre si em frequências arbitrárias.

Os vales irregulares de $R_{\text{comp}}$ refletem as relações de
dependência logarítmica entre compostos: compostos com fatores comuns
($c_1 = 2^3 \cdot 3$, $c_2 = 2^2 \cdot 3^2$) compartilham componentes
espectrais e criam interferência construtiva persistente em frequências
que não são frequências próprias de nenhum composto individual. O resultado
é um piso irregular elevado, com variância comparável à média.

---

## 5. Conexão com a escala de $T_{\max}$

Os três fenômenos dependem de $T_{\max}$ da mesma forma. Pela análise do
Exp Q (Seção 3.2):

$$B_N^{\text{comp}} \sim \frac{2\sqrt{N}}{T_{\max}}$$

Para que a dicotomia de picos seja robusta — piso de $R_{\text{comp}}$ em
$f_p$ muito menor que o pico direto de $R_{\text{primo}}$ em $f_p$ — é
necessário que $T_{\max}$ seja suficientemente grande para que
$O(T_{\max}^{-1})$ seja desprezível frente a $1/\sqrt{p}$.

### 5.1 O princípio da Nota 28 e sua aplicação aqui

A Nota 28 foi desenvolvida num contexto distinto: determinou a escala de
$t_{\max}$ necessária para separar espectralmente os primos de
$\mathcal{P}_< = \{q < 2^{n-1}\}$ no sinal $R_2(t)$ do pipeline com
$Z_Q$. O resultado foi:

$$t_{\max}^{(Z_Q)}(n) \approx \pi \cdot q_{\text{twin}}(\mathcal{P}_<)$$

onde $q_{\text{twin}}(\mathcal{P}_<)$ é o maior par gêmeo em
$\mathcal{P}_<$ — o par gargalo pelo critério de Rayleigh.

O contexto desta nota é diferente: $R_{\text{primo}}$ e $R_{\text{comp}}$
são construídos sobre $\{2, \ldots, N\}$ (todos os inteiros, não o bloco
binário). O par gargalo aqui é o maior par gêmeo em $\{2, \ldots, N\}$,
e pelo mesmo princípio de Rayleigh:

$$T_{\max}^{(\{2,N\})} \approx \pi \cdot q_{\text{twin}}(N)$$

O princípio é idêntico — critério de Rayleigh aplicado ao par gêmeo
mais alto do intervalo — mas o intervalo muda: $\mathcal{P}_<$ na
Nota 28 vs $\{2, \ldots, N\}$ aqui. Para $N = 2^n$, o maior par gêmeo
em $\{2, \ldots, N\}$ é aproximadamente o dobro do maior par gêmeo em
$\mathcal{P}_< = \{q < 2^{n-1}\}$, então
$T_{\max}^{(\{2,N\})} \approx 2 \cdot t_{\max}^{(Z_Q)}(n)$ — mesma
ordem, fator 2 de diferença.

### 5.2 Suficiência do limiar

A condição $T_{\max} \gg 2\sqrt{N}$ (para $B_N^{\text{comp}} \ll
1/\sqrt{p_{\min}}$) é satisfeita por $T_{\max} \sim \pi \cdot q_{\text{twin}}(N)$
quando $q_{\text{twin}}(N) \gg 2\sqrt{N}/\pi$. Como
$q_{\text{twin}}(N) \lesssim N$ e $2\sqrt{N}/\pi \ll N$ para $N$ grande,
a condição é satisfeita para toda a faixa testada ($N \leq 500$,
$T_{\max} = 1000$).

Portanto, o mesmo princípio de escala da Nota 28 — $T_{\max} \approx \pi
\cdot q_{\text{twin}}$ do intervalo considerado — é simultaneamente
suficiente para manter as três camadas da dicotomia: picos, piso e vales.
A diferença de contexto ($Z_Q$ vs $\{2,\ldots,N\}$) altera a constante
mas não a lei de escala.

---

## 6. Questões em aberto

**Questão 1 — Cota para a razão de picos.** A análise da Seção 2.2
mostra que $\mathcal{R}(f_p) \sim T_{\max}/\sqrt{p}$ assintoticamente,
mas o prefator não foi determinado. Uma cota explícita conectaria a razão
à teoria de Baker via $\rho_{\min}$ (Nota 27).

**Questão 2 — Regularidade dos vales de $R_{\text{primo}}$.** O desvio
dos vales (~0,9) é não-nulo — primos pequenos como 2 e 3 criam picos tão
dominantes que seus bordos elevam os vales adjacentes. A questão é se o
desvio dos vales de $R_{\text{primo}}$ converge para zero quando os
primos pequenos são excluídos da análise (janela restrita a $f > f_{p_k}$
para algum primo de corte $p_k$).

**Questão 3 — Regime $T_{\max} \propto N$.** Com $T_{\max}$ proporcional
a $N$, ambos os pisos tendem a zero. A dicotomia sobrevive nesse regime?
O comportamento da razão $B_N^{\text{comp}}/B_N^{\text{primo}}$ quando
ambos convergem a zero não foi investigado.

---

## Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026).  
[Nota 27] T. Bandeira, *Cota Assintótica para $\rho_{\min}(k)$* (2026).  
[Nota 28] T. Bandeira, *Escala de $t_{\max}$ para a Etapa 2: Par Gêmeo
Gargalo e Lei Assintótica* (2026).  
[Exp comparação] T. Bandeira, `exp_comparacao_residuos.ipynb` —
$R_{\text{primo}}$ vs $R_{\text{comp}}$ para N = 50, 100, 200 (2026).  
[Exp Q] T. Bandeira, `exp_q_analise.ipynb` — nível de base de
$R_{\text{comp}}$: convergência e estimativa $B_N \sim 2\sqrt{N}/T_{\max}$
(2026).
