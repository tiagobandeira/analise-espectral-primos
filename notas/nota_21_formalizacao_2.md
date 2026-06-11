# Nota 21 — Formalização do Crivo Espectral Oracle-Free

**T. Bandeira · Junho de 2026**  
*Nota de formalização — base para o artigo teórico*

---

## Resumo

Formalizamos o Crivo Espectral Oracle-Free a partir de uma definição central —
a Redutibilidade Logarítmica — da qual todos os resultados subsequentes derivam
por cadeia lógica direta. A Proposição (equivalência entre redutibilidade
logarítmica e composição) é o núcleo: seus dois sentidos correspondem aos
resultados que nas versões anteriores apareciam como Teoremas 1 e 2 separados.
O Teorema de Invariância (anteriormente Teorema 3) estabelece que o operador
de eliminação $\mathcal{R}_m$ atua apenas sobre elementos redutíveis, deixando
irredutíveis intactos — consequência da ortogonalidade das funções de Dirichlet
no limite $T \to \infty$. O Corolário fecha a cadeia: após eliminação completa
das contribuições redutíveis de um bloco binário, os sobreviventes são
exatamente os elementos logaritmicamente irredutíveis, i.e., os primos do bloco.
A FFT não é objeto da teoria — é o instrumento que implementa o Corolário na
prática.

---

## 1. Preliminares: o espaço de Dirichlet

Seja $\mathcal{H}$ o espaço de funções $f : [0,\infty) \to \mathbb{R}$ da forma

$$f(t) = \sum_{m \geq 2} a_m \cos(t \log m), \qquad a_m \in \mathbb{R},$$

com apenas finitos $a_m$ não nulos. Define-se o produto interno

$$\langle f, g \rangle_T = \frac{1}{T} \int_0^T f(t)\, g(t)\, dt.$$

**Lema de Ortogonalidade.** Para inteiros $m \neq m'$, ambos $\geq 2$:

$$\langle \cos(t \log m),\, \cos(t \log m') \rangle_T
\;=\; \frac{\sin(T(\log m - \log m'))}{2T(\log m - \log m')}
\;\xrightarrow{T\to\infty}\; 0$$

e

$$\langle \cos(t \log m),\, \cos(t \log m) \rangle_T
\;=\; \frac{1}{2} + \frac{\sin(2T \log m)}{4T \log m}
\;=\; \frac{1}{2} + O(T^{-1}).$$

*Demonstração.* Cálculo direto via identidade de produto de cossenos e
integração. $\square$

**Corolário do Lema.** A família $\{\cos(t \log m)\}_{m \geq 2}$ é
assintoticamente ortogonal em $\mathcal{H}$: no limite $T \to \infty$,
cada função é ortogonal a todas as demais.

**Observação (independência logarítmica dos primos).** Para primos distintos
$p \neq q$, a razão $\log p / \log q$ é irracional. De fato, $\log p / \log q
\in \mathbb{Q}$ implicaria $p^b = q^a$ para inteiros $a, b \geq 1$,
contradizendo o Teorema Fundamental da Aritmética. Portanto o denominador
$\log m - \log m'$ nunca é nulo para $m \neq m'$ sem relação de potência, e
o erro $O(T^{-1})$ no Lema é uniforme nesses casos.

---

## 2. Definição central e Proposição

**Definição (Redutibilidade Logarítmica).** Um inteiro $m \geq 2$ é
*logaritmicamente redutível* se existe uma decomposição

$$\log m = \sum_{i=1}^{k} \alpha_i \log p_i, \qquad
p_i \text{ primo},\quad p_i < m,\quad \alpha_i \in \mathbb{Z}_{\geq 1}.$$

Um inteiro $m \geq 2$ é *logaritmicamente irredutível* se não admite tal
decomposição.

Em termos de frequências: $m$ é redutível se e somente se
$f_m = \sum_i \alpha_i f_{p_i}$, onde $f_x = \log(x)/(2\pi)$.

---

**Proposição (Equivalência com Primalidade).** Um inteiro $m \geq 2$ é
logaritmicamente irredutível se e somente se $m$ é primo.

*Demonstração.*

$(\Rightarrow)$ Se $m$ é composto, existe fatoração
$m = p_1^{\alpha_1} \cdots p_k^{\alpha_k}$ com $p_i < m$ e $\alpha_i \geq 1$.
Tomando logaritmos: $\log m = \sum_i \alpha_i \log p_i$. Logo $m$ é
logaritmicamente redutível.

$(\Leftarrow)$ Se $m$ é primo, qualquer decomposição
$\log m = \sum_i \alpha_i \log p_i$ com $p_i$ primos e $p_i < m$,
$\alpha_i \geq 1$, implicaria $m = \prod_i p_i^{\alpha_i}$,
contradizendo a primalidade de $m$. Logo $m$ é logaritmicamente
irredutível. $\square$

**Corolário imediato.** Primos distintos têm frequências características
distintas e irredutíveis: para $p \neq q$ primos, $f_p \neq f_q$ e
nenhuma das duas é combinação linear inteira da outra.

---

## 3. O sinal de um inteiro e o operador de eliminação

### 3.1 Sinal associado a um inteiro

Para $m \geq 2$, define-se a função $S_m : [0,\infty) \to \mathbb{R}$:

$$S_m(t) = -\frac{1}{2}\log\!\left(1 - 2\,m^{-1/2}\cos(t\log m) + m^{-1}\right)$$

Expandindo via série de Taylor de $-\frac{1}{2}\log(1-u)$:

$$S_m(t) = \sum_{k=1}^{\infty} \frac{c_k(m)}{k}\cos(kt\log m),
\qquad c_k(m) = 2^k m^{-k/2} + O(m^{-(k+1)/2})$$

O termo dominante ($k=1$) oscila na frequência $f_m = \log(m)/(2\pi)$ com
amplitude $c_1 \approx 2m^{-1/2}$. Os harmônicos superiores ($k \geq 2$)
oscilam em múltiplos $k f_m$ com amplitudes decrescentes.

### 3.2 Sinal do bloco e operador de eliminação

Para $I \subset \mathbb{Z}_{\geq 2}$ finito, define-se:

$$Z_I(t) = \sum_{m \in I} S_m(t)$$

O **operador de eliminação** por $m \in I$ é:

$$\mathcal{R}_m[Z_I] \;=\; Z_I - S_m \;=\; Z_{I \setminus \{m\}}$$

---

## 4. Teorema de Invariância

**Teorema (Invariância dos Primos sob o Filtro).**
Seja $I$ finito, $m \in I$ logaritmicamente redutível, e
$q \in I$ logaritmicamente irredutível (primo). Então:

$$\langle \mathcal{R}_m[Z_I] - Z_{I \setminus \{m\}},\;
\cos(t\log q) \rangle_T = O(T^{-1})$$

No limite $T \to \infty$:

$$\mathcal{R}_m[Z_I] = Z_{I \setminus \{m\}} \quad \text{em } \mathcal{H}$$

Ou seja: o operador $\mathcal{R}_m$ remove exatamente a contribuição de $m$
e não altera a contribuição de nenhum primo $q \neq m$.

*Demonstração.*

Por definição, $\mathcal{R}_m[Z_I] = Z_I - S_m = \sum_{m' \in I\setminus\{m\}} S_{m'}$
— identidade exata. A questão é se a remoção de $S_m$ contamina a componente
de $q$ via correlação cruzada.

Pelo Lema de Ortogonalidade, para cada par de harmônicos $k, l \geq 1$:

$$\langle \cos(kt\log m),\, \cos(lt\log q) \rangle_T \to 0
\quad \text{quando } T \to \infty$$

desde que $k\log m \neq l\log q$, i.e., $\log m/\log q \neq l/k$.

Como $m$ é redutível e $q$ é primo irredutível, $m$ não é potência de $q$
(pois $q \nmid m$ ou $m = q^j$ implicaria $q \mid m$, logo $q$ aparece na
fatoração de $m$, e nesse caso $f_m = j f_q$ com $j \geq 2$, e a correlação
entre $\cos(t\log m)$ e $\cos(t\log q)$ ainda tende a zero pelo Lema).
Portanto todos os termos cruzados $\langle S_m, S_q \rangle_T \to 0$.

Logo a remoção de $S_m$ não afeta a componente de $q$ no limite. $\square$

**Observação sobre comutatividade.** Para $m, m'$ ambos redutíveis:

$$\mathcal{R}_m \circ \mathcal{R}_{m'} = \mathcal{R}_{m'} \circ \mathcal{R}_m
\quad \text{em } \mathcal{H}$$

A ordem de eliminação dos compostos não afeta o resultado. O filtro é
comutativo.

**Interpretação.** O Teorema de Invariância diz que $\mathcal{H}$, equipado
com $\langle \cdot, \cdot \rangle_T$ para $T$ grande, é essencialmente um
espaço de frequências: cada inteiro ocupa sua própria linha espectral $f_m$,
e removê-la não contamina as demais. Redutíveis e irredutíveis ocupam linhas
espectrais estruturalmente distintas — os redutíveis em frequências que são
combinações de outras, os irredutíveis em frequências que não são.

---

## 5. Corolário — O Crivo Oracle-Free

### 5.1 Configuração

Seja $p$ primo com $n = \lfloor\log_2 p\rfloor$. Define-se o bloco binário:

$$\mathcal{B} = [2^{n-1},\, p-1]$$

com subconjuntos:

$$\mathcal{B}_{\text{irred}} = \{m \in \mathcal{B} : m \text{ primo}\}
\qquad \mathcal{B}_{\text{red}} = \{m \in \mathcal{B} : m \text{ composto}\}$$

e o conjunto de primos do bloco anterior:

$$\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$$

### 5.2 Identificação de redutíveis sem oráculo externo

**Lema $\rho$ (Nota 20, Corolário do Teorema 1 da Nota MDC).**
Para todo $m \in \mathcal{B}_{\text{red}}$, todo fator primo de $m$
pertence a $\mathcal{P}_<$. Portanto:

$$m \in \mathcal{B}_{\text{red}}
\;\iff\; \exists\, b \in \mathcal{P}_< : b \mid m
\;\iff\; \rho(m \mid \mathcal{P}_<) = 0$$

O critério $\rho(m \mid \mathcal{P}_<) = 0$ é exato e não usa oráculo
externo de primalidade — apenas divisibilidade por elementos de $\mathcal{P}_<$.

### 5.3 Enunciado

**Corolário (Crivo Oracle-Free).**

Seja $Z_{\mathcal{B}}(t) = \sum_{m \in \mathcal{B}} S_m(t)$. Aplicando
iterativamente $\mathcal{R}_m$ para cada $m \in \mathcal{B}_{\text{red}}$
(identificado pelo critério $\rho$):

$$Z_{\text{res}}(t)
= \Bigl(\bigcirc_{m \in \mathcal{B}_{\text{red}}} \mathcal{R}_m\Bigr)
  [Z_{\mathcal{B}}(t)]$$

então, no limite $T \to \infty$:

$$Z_{\text{res}}(t) = Z_{\mathcal{B}_{\text{irred}}}(t)
= \sum_{q \in \mathcal{B}_{\text{irred}}} S_q(t)$$

Os elementos de $\mathcal{B}$ cujos sinais sobrevivem à eliminação são
exatamente os elementos logaritmicamente irredutíveis de $\mathcal{B}$,
i.e., os primos de $\mathcal{B}$.

*Demonstração.*

Pelo Teorema de Invariância, cada aplicação de $\mathcal{R}_m$ com $m$
redutível remove $S_m$ sem afetar $S_q$ para nenhum $q$ irredutível
(no limite). Pelo Lema $\rho$, o critério $\rho = 0$ identifica exatamente
os redutíveis de $\mathcal{B}$. Após remover todos os redutíveis, restam
apenas os sinais dos irredutíveis. Pela Proposição, irredutíveis = primos.
$\square$

---

## 6. O pipeline em dois estágios

O Corolário requer $\mathcal{P}_<$ para o critério $\rho$ da Etapa 1.
A obtenção de $\mathcal{P}_<$ sem oráculo é a Etapa 2.

### 6.1 Etapa 2: extração de $\mathcal{P}_<$

Define-se o sinal de referência:

$$R_2(t) = Z_{\mathcal{B}}(t) - \log|\zeta(\tfrac{1}{2}+it)|$$

O produto de Euler $\zeta(s) = \prod_q (1-q^{-s})^{-1}$ satisfaz
$\log|\zeta(\tfrac{1}{2}+it)| \approx \sum_q S_q(t)$ sobre todos os primos.
Para $q \in \mathcal{B}_{\text{irred}}$, $S_q$ aparece em $Z_{\mathcal{B}}$
e em $\log|\zeta|$; pelo Teorema de Invariância, a diferença $R_2$ cancela
essas contribuições e preserva a assinatura indireta dos elementos de
$\mathcal{P}_<$ via seus múltiplos redutíveis em $\mathcal{B}$.

A filtragem dos candidatos em $R_2$ usa o critério $\rho$ iterativo (Nota 20):
candidatos são aceitos em ordem crescente, e cada candidato $c$ é aceito
somente se $\rho(c \mid \text{aceitos anteriores}) > \rho^*$, eliminando
falsos positivos sem oráculo externo.

### 6.2 Naturalidade de $\zeta$

$\zeta$ aparece na Etapa 2 não como escolha arbitrária mas como consequência
estrutural: é o único denominador limpo disponível sem conhecimento prévio
de primos — produto de Euler sobre primos, sem elementos redutíveis, sem
frequências parasitas. Substituições por produtos sobre blocos finitos
introduzem redutíveis no denominador, que geram frequências de intermodulação
e falsos positivos (testado e documentado na Nota 20, Seção 7).

### 6.3 Estrutura hierárquica e indução

A Etapa 1 usa $\mathcal{P}_<$ obtida na Etapa 2. $\mathcal{P}_<$ consiste
nos primos de $[2, 2^{n-1}-1]$ — tratados como conhecidos relativamente ao
bloco atual. O mesmo procedimento aplica-se ao bloco anterior para obter
$\mathcal{P}_<$, com $\mathcal{P}_{<<}$ como base, e assim sucessivamente.
O caso base é $\mathcal{B} = [2, 3]$, onde os primos são trivialmente
identificáveis.

Isso não é circularidade lógica — é indução na hierarquia de blocos binários,
cuja terminação é garantida pelo decrescimento estrito do índice $n$.

---

## 7. Papel da FFT

A FFT não aparece em nenhum enunciado ou prova das seções anteriores.
Ela entra como instrumento de implementação do Corolário:

O sinal $Z_{\text{res}}(t)$, calculado para $t \in [T_{\min}, T_{\max}]$
com passo $\Delta t$, é transformado via FFT. Os picos do espectro de amplitude
em frequências $f_q = \log(q)/(2\pi)$ identificam os $q$ cujos sinais $S_q$
sobreviveram à eliminação — i.e., os irredutíveis de $\mathcal{B}$.

A FFT não decide quais elementos são irredutíveis: essa decisão está no
critério $\rho$ e no Corolário. A FFT torna visíveis as frequências
sobreviventes com resolução $\Delta f = 1/(N\Delta t)$.

**Limitação prática.** O Teorema de Invariância é exato no limite
$T \to \infty$. Para $T_{\max}$ finito, o operador $\mathcal{R}_m$ deixa
resíduo de ordem $O(T_{\max}^{-1})$ nas componentes de $m' \neq m$.
A condição prática para separar dois irredutíveis $q_1 < q_2$ é
$T_{\max} > 2\pi/(\log q_2 - \log q_1)$. As consequências para parâmetros
de implementação são tratadas na Nota 22.

---

## 8. Mapa da teoria

```
Fatoração única (TFA)
        │
        └─► Definição: Redutibilidade Logarítmica
                │
                └─► Proposição: m irredutível ⟺ m primo
                        │
                ┌───────┴────────┐
                │                │
        Lema de Ortogonalidade   Lema ρ
        (espaço de Dirichlet)    (Teorema 1, Nota MDC)
                │                │
                └───────┬────────┘
                        │
              Teorema de Invariância
        ℛ_m age apenas sobre redutíveis;
          irredutíveis permanecem intactos
                        │
                    Corolário
              Crivo Oracle-Free:
        sobreviventes = irredutíveis = primos
                        │
                       FFT
            (instrumento de implementação)
```

---

## 9. Status das afirmações

| Afirmação | Status |
|-----------|--------|
| Lema de Ortogonalidade | Prova por cálculo direto |
| Independência logarítmica dos primos | Prova pelo TFA |
| Definição de redutibilidade logarítmica | Definição |
| Proposição (equivalência com primalidade) | Prova elementar via TFA |
| Lema $\rho$ (exatidão do classificador) | Prova via Teorema 1, Nota MDC |
| Teorema de Invariância | Prova no limite $T \to \infty$ |
| Corolário — Crivo Oracle-Free | Prova condicional ($T \to \infty$) |
| Cancelamento de $\mathcal{B}_{\text{irred}}$ em $R_2$ | Verificado empiricamente (Nota 20) |
| SNR não degrada com $p$ | Verificado parcialmente: Etapa 1 estável em $[0{,}72;\, 0{,}98]$ para $p \leq 499$ (Exp 3, `fundamentos_teoricos_v2`); Etapa 2 é o gargalo — SNR cai de $3{,}8$ ($n=5$) a $0{,}22$ ($n=7$), requer $t_{\max}$ crescente |
| $\rho_{\min} > \rho^*$ para todo $p$ | Verificado empiricamente para $p \leq 499$: $\rho_{\min} \in [3{,}3 \times 10^{-4},\, 9{,}3 \times 10^{-3}]$, muito acima de erros de ponto flutuante; limiar robusto $\rho^* = 10^{-6}$ (Exp 4b, `fundamentos_teoricos_v2`) |

O Corolário é "condicional" no sentido de que a prova é exata no limite
$T \to \infty$; para $T_{\max}$ finito, a detectabilidade prática depende
do SNR e da resolução espectral, estudados empiricamente nas Notas 18–21.
O resultado central — o filtro remove exatamente os redutíveis e preserva
os irredutíveis — não depende de $T_{\max}$ finito.

---

## 10. Conclusão

A estrutura matemática do Crivo Espectral Oracle-Free repousa sobre uma
definição central (Redutibilidade Logarítmica), uma Proposição que a conecta
à primalidade via fatoração única, e um Teorema de Invariância que conecta
essa álgebra ao espaço de funções de Dirichlet. O Corolário fecha a cadeia:
o crivo remove exatamente os redutíveis e preserva os irredutíveis — sem
oráculo externo, sem conhecimento prévio de primos.

A FFT é o instrumento que torna o Corolário computacionalmente operacional.
A hierarquia de blocos binários garante que o pipeline em dois estágios é
bem fundado por indução. $\zeta$ aparece como consequência estrutural da
Etapa 2, não como pressuposto do método.

O artigo principal a ser desenvolvido a partir desta nota terá a Definição,
a Proposição e o Teorema de Invariância como corpo teórico, o Corolário como
resultado principal, e as Notas 17–22 como validação computacional e descrição
de método.

---

## Referências

[TFA] Teorema Fundamental da Aritmética.  
[Nota MDC] T. Bandeira, *Uma caracterização de primalidade via partições
binárias e MDC em intervalos reduzidos* (2026).  
[Nota 17] T. Bandeira, *Ferramenta Espectral via $Q(p)$* (2026).  
[Nota 18] T. Bandeira, *Benchmark Espectral* (2026).  
[Nota 19] T. Bandeira, *Detector Espectral de Primalidade* (2026).  
[Nota 20] T. Bandeira, *Crivo Espectral sem Oráculo de Primalidade* (2026).  
[Nota 22] T. Bandeira, *Método do Crivo Espectral Oracle-Free* (2026).  
H. L. Montgomery, R. C. Vaughan, *Multiplicative Number Theory I* (2007).  
E. C. Titchmarsh, *The Theory of the Riemann Zeta-Function* (1986).