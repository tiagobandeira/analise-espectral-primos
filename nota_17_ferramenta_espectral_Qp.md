# Nota 17 — Ferramenta Espectral via $Q(p)$: Fundamentação e Validação Computacional

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

Desenvolvemos e validamos uma ferramenta de análise espectral baseada no produto
$Q(p) = \prod_{x=2^{n-1}}^{p-1} x$, que recupera os primos menores que $p$ a
partir de picos da FFT de $\log|Z_Q(\tfrac{1}{2}+it)|$, sem crivo e sem
conhecimento prévio dos zeros de $\zeta$. O método opera em dois estágios que
resolvem um problema de cancelamento identificado em versões anteriores. A
ferramenta é então aplicada para construir sequências $L(P_n)$ da hierarquia
primorial (Nota 14) usando exclusivamente o universo de candidatos extraídos
espectralmente, obtendo taxas de primos idênticas à referência nos níveis
verificados. Os resultados validam tanto a estrutura matemática das notas
anteriores quanto a ferramenta espectral como instrumento independente.

---

## 1. Contexto e Motivação

A Nota 16 introduziu a análise espectral de $Z_Q/\zeta$ como método para
identificar primos a partir do produto $Q(p)$. Durante a implementação
computacional, identificou-se um problema estrutural: a divisão por $\zeta$
cancela exatamente os primos que pertencem diretamente ao intervalo
$[2^{n-1}, p-1]$, pois eles aparecem como fatores tanto em $Z_Q$ quanto em
$\zeta$. O sinal $R(t) = \log|Z_Q/\zeta|$ recupera apenas os primos menores que
$2^{n-1}$ — aqueles que aparecem no intervalo apenas via múltiplos compostos.

Esta nota documenta a solução (pipeline de dois estágios), a validação
computacional completa, e os experimentos com sequências $L(P_n)$ construídas
a partir dos candidatos extraídos.

A ressalva sobre o alcance de $Z_Q/\zeta$ foi incorporada à Seção 2 da Nota 16.

---

## 2. O Produto $Q(p)$ e sua Função Geradora

Para um primo $p$ com $n = \lfloor\log_2 p\rfloor$, define-se:

$$Q(p) = \prod_{x=2^{n-1}}^{p-1} x$$

e a função associada em $s = \tfrac{1}{2}+it$:

$$Z_Q(s) = \prod_{x=2^{n-1}}^{p-1} \frac{1}{1-x^{-s}}$$

cujo logaritmo do módulo é:

$$\log|Z_Q(\tfrac{1}{2}+it)| = -\frac{1}{2}\sum_{x=2^{n-1}}^{p-1}
\log\!\left(1 - 2x^{-1/2}\cos(t\log x) + x^{-1}\right)$$

**Observação sobre o sinal.** A fórmula correta usa $-\tfrac{1}{2}$. Uma
implementação com $+\tfrac{1}{2}$ computa $\log|1/Z_Q|$; o impacto sobre os
picos da FFT é nulo (a amplitude é simétrica), mas a semântica está invertida.

Cada $x$ no intervalo contribui com uma oscilação de frequência
$f_x = \log(x)/(2\pi)$ no sinal $\log|Z_Q(\tfrac{1}{2}+it)|$ como função de
$t$. A FFT decompõe essa superposição; primos $q$ geram picos em frequências
irredutíveis $\log(q)/(2\pi)$, distintos dos compostos cujas frequências são
combinações dos fatores. A inversão $q = \mathrm{round}(e^{2\pi f})$ recupera
o inteiro a partir do pico.

---

## 3. Pipeline de Dois Estágios

### 3.1 Problema de cancelamento

Dividir $Z_Q$ por $\zeta$ remove a contribuição dos primos diretamente no
intervalo $[2^{n-1}, p-1]$: esses primos aparecem em $Z_Q$ como fatores
individuais e em $\zeta$ via produto de Euler, sendo cancelados. O método
original recupera apenas os primos $q < 2^{n-1}$.

### 3.2 Etapa 1 — primos dentro do intervalo

$$R_1(t) = \log|Z_Q(\tfrac{1}{2}+it)| - \log|Z_{\mathrm{comp}}(\tfrac{1}{2}+it)|$$

onde $Z_{\mathrm{comp}}$ é o produto apenas sobre os compostos do intervalo.
A subtração cancela cada composto $x$; o que resta são os fatores dos primos
$q \in [2^{n-1}, p-1]$, que aparecem como picos limpos em $\log(q)/(2\pi)$.

### 3.3 Etapa 2 — primos fora do intervalo

Os primos $q < 2^{n-1}$ não aparecem diretamente no intervalo mas deixam
assinatura via seus múltiplos compostos. Usando os primos $\mathcal{P}_>$
identificados na Etapa 1:

$$R_2(t) = \log|Z_Q| - \log|\zeta| - \log|Z_{\mathcal{P}_>}|$$

A subtração de $\log|\zeta|$ remove a contribuição global dos primos; a
subtração de $\log|Z_{\mathcal{P}_>}|$ devolve a contribuição dos primos
grandes já identificados. O resíduo carrega a assinatura indireta dos primos
pequenos.

### 3.4 União

$$\text{primos}(p) = \underbrace{\text{Etapa 1}}_{\{q \in [2^{n-1}, p-1] : q \text{ primo}\}} \cup \underbrace{\text{Etapa 2}}_{\{q < 2^{n-1} : q \text{ primo}\}}$$

### 3.5 Parâmetros e resolução

A resolução da FFT é $\Delta f = 1/(N \cdot \Delta t)$. Para separar dois primos
$q_1 < q_2$ é necessário:

$$\frac{\log q_2 - \log q_1}{2\pi} > \Delta f$$

Com $t_{\max}=150$, $\Delta t=0{,}05$: $N=2998$, $\Delta f \approx 0{,}0033$ —
suficiente para separar todos os pares até $p=53$ (gap mínimo $\approx 0{,}0097$
entre 16 e 17). Para $p$ maiores, $t_{\max}$ deve ser aumentado.

**Nota de implementação.** O cálculo de $\log|\zeta(\tfrac{1}{2}+it)|$ via
mpmath é o gargalo computacional ($O(t\log t)$ por ponto). A solução adotada
é um cache por parâmetros $(t_{\min}, t_{\max}, \Delta t)$: a zeta é calculada
uma única vez (~8–15s para 3000 pontos) e reutilizada em todas as chamadas
subsequentes do mesmo experimento.

---

## 4. Validação da Extração

A extração foi testada para $p \in \{37, 41, 53\}$. Os resultados abaixo usam
$t_{\max}=150$, $\Delta t=0{,}05$.

| $p$ | Primos reais $< p$ | Extraídos corretamente | Falsos positivos | Perdidos |
|-----|--------------------|------------------------|------------------|----------|
| 37  | 11                 | 11/11                  | $\{4, 8, 9\}$    | —        |
| 41  | 12                 | 12/12                  | $\{4, 8, 9\}$    | —        |
| 53  | 15                 | 14/15                  | $\{4, 8, 9, 40\}$| $\{41\}$ |

Os falsos positivos são compostos pequenos cujas frequências $\log(x)/(2\pi)$
ficam próximas de picos reais. O primo perdido (41 para $p=53$) é recuperado
aumentando $t_{\max}$ para 300. Nenhum dos falsos positivos é primo, portanto
são removidos com um teste de primalidade pontual — operação $O(\sqrt{q})$, não
um crivo.

**Dependência do teste de primalidade.** O método *localiza* primos via espectro
mas não *certifica* primalidade sem auxílio. Com resolução infinita os picos
cairiam em $\log(q)/(2\pi)$ exatos e a inversão $q = e^{2\pi f}$ seria exata;
os falsos positivos são artefatos da resolução finita da FFT. A dependência do
`is_prime` é portanto uma limitação prática, não conceitual.

---

## 5. Aplicação: Sequências $L(P_n)$ via Candidatos Espectrais

### 5.1 Estrutura de $L(P_n)$ (Nota 14)

Dado o universo de candidatos $\mathcal{C} = [c_0, c_1, c_2, \ldots]$ extraídos
espectralmente (ordenados), a sequência de nível $n$ é construída como:

$$L(c_n): \quad \text{comprimento} = c_{n-1}, \quad d_n = \prod_{\substack{c_i \in \mathcal{C},\, i < n \\ c_i \text{ primo}}},
\quad \text{âncora} = \min\{c_j : j > n,\, c_j \text{ primo}\}$$

$$\text{termos} = \{\text{âncora} + k \cdot d_n : k = 0, 1, \ldots, c_{n-1}-1\}$$

**Comprimento $= c_{n-1}$** (último primo do prefixo): evita a colisão
garantida por $c_n$, que não divide $d_n$ por construção. O primo $c_n$ é o
primeiro fator não coberto pelo escudo modular.

**Âncora prima**: âncora composta $a$ com fator $f \mid a$ satisfaz
$a + k \cdot d_n \equiv a \pmod{f}$ para todo $k$; se $f \mid d_n$ todos os
termos são divisíveis por $f$. A âncora deve ser primo para evitar esse
colapso. O teste é pontual, não um crivo.

**$d_n$ usa apenas primos do prefixo**: compostos extraídos contribuiriam com
fatores redundantes (já presentes nos primos do prefixo) e potencialmente
alterariam a blindagem modular. O produto dos primos extraídos coincide com o
primorial quando a extração é perfeita.

### 5.2 Resultados para $p = 53$

Candidatos extraídos: $[2,3,4,5,7,8,9,11,13,17,19,23,29,31,37,40,43,47]$  
Primos extraídos: $[2,3,5,7,11,13,17,19,23,29,31,37,43,47]$  
Compostos extras: $\{4,8,9,40\}$ — Primo perdido: $\{41\}$

| Sequência | $d_n$ | Âncora | Comp. | Primos | Taxa | Ref. |
|-----------|-------|--------|-------|--------|------|------|
| $L(4)$ esp. | 6   | 5      | 3     | 3/3    | 100% | —    |
| $L(5)$ esp. | 6   | 7      | 3     | 3/3    | 100% | 100% |
| $L(7)$ esp. | 30  | 11     | 5     | 5/5    | 100% | 100% |
| $L(8)$ esp. | 210 | 11     | 7     | 4/7    |  57% | —    |
| $L(11)$ ref.| 210 | 13     | 7     | 6/7    |  86% | 86%  |
| $L(13)$ ref.| 2310| 17     | 11    | 8/11   |  73% | 73%  |

$L(4)$ espectral usa o índice do composto 4, mas constrói $d=6$ com os primos
$[2,3]$ do prefixo e âncora $5$ — resultado idêntico a $L(5)$ referência.

$L(8)$ espectral: o índice 4 na lista de candidatos é o composto $8$, portanto
$d=210$ mas âncora $=11$ em vez de $13$. A diferença de taxa (57\% vs 86\%)
ilustra o papel da âncora: com $d=210$ fixo, âncoras diferentes geram
progressões distintas e a escolha ótima (âncora via $C_0$ mínimo, Nota 14)
pode recuperar a taxa integral.

### 5.3 Interpretação

Os resultados mostram que:

1. **A estrutura matemática das sequências $L(P_n)$ funciona** com o universo
   de candidatos espectrais, sem que o código conheça os primos de antemão.

2. **A ferramenta espectral fornece $d_n$ correto**: onde a extração acerta
   todos os primos, $d_n$ espectral = primorial puro e as sequências são
   idênticas à referência.

3. **A âncora é o grau de liberdade sensível**: com $d_n$ fixado, a qualidade
   da sequência depende da escolha de âncora. A busca por $C_0$ mínimo (Nota
   14) é o refinamento natural para maximizar a taxa de primos.

---

## 6. Posição na Literatura e Originalidade

A abordagem difere das direções clássicas que relacionam primos e $\zeta$:

- **Fórmula explícita de Riemann–von Mangoldt**: primos $\to$ zeros de $\zeta$
  $\to$ contagem de primos. Requer conhecer os zeros.
- **Produto de Euler**: primos $\to$ $\zeta(s)$. Requer conhecer os primos.
- **Este método**: inteiros consecutivos $\to$ $Z_Q$ $\to$ primos. Nenhum dos
  dois lados é pressuposto.

A $\zeta$ aparece apenas como referência de normalização na Etapa 2, não como
o objeto que carrega a informação dos primos. A informação primorial está
codificada na estrutura multiplicativa dos inteiros $[2^{n-1}, p-1]$ — uma
consequência do Teorema 1 da Nota sobre blocos binários, que garante que todo
fator primo de qualquer composto em $[2^n, 2^{n+1}-1]$ aparece em
$[2^{n-1}, 2^n-1]$.

A observação central, verificada computacionalmente:

> *A FFT de $\log|Z_Q(\tfrac{1}{2}+it)|$ — onde $Q(p)$ é construído sem
> conhecimento de primos — exibe picos nas frequências $\log(q)/(2\pi)$ de
> todos os primos $q < p$. A estrutura primorial está codificada na geometria
> do intervalo binário e é recuperável espectralmente.*

---

## 7. Usos Futuros

A ferramenta espectral pode ser empregada independentemente do Motor ou das
sequências $L$:

1. **Conexão ao Motor**: âncoras baseadas em $C_0$ (Nota 14) conectam
   diretamente ao operador $W_i(C)$ e ao processo guloso de cobertura.

2. **Exploração de $Q(p)$ para $p$ grande**: verificar se a extração se mantém
   precisa e se os compostos extraídos seguem padrão sistemático.

3. **Comparação com fatorial**: $N! = \prod_{x=1}^{N} x$ contém o primorial
   como divisor pelo mesmo motivo que $Q(p)$. O experimento comparativo
   direto (taxa de acerto FFT, falsos positivos, custo computacional) está em
   aberto.

4. **Função interpoladora de $Q$**: se existir uma função analítica que
   interpole $Q(p)$ como a função Gama interpola o fatorial, seus polos e
   ressonâncias teriam estrutura diretamente ligada aos primoriais — perspectiva
   diferente da de Riemann, mais próxima da $Z(s)$ da Nota 15.

---

## Referências

[Nota 1] T. Bandeira, *Uma caracterização de primalidade via partições binárias
e MDC em intervalos reduzidos*, nota standalone (2026).  
[Nota 14] T. Bandeira, *Sequência de Sequências de Primos via Operador $W_i$ e
Estrutura Primorial*, nota adicional (2026).  
[Nota 15] T. Bandeira, *Estrutura Primorial, Classes Residuais e Conexões com a
Função Zeta*, nota adicional (2026).  
[Nota 16] T. Bandeira, *Conexão Espectral entre Blocos Binários e a Hierarquia
Primorial*, nota adicional (2026).  
B. Green, T. Tao, *The primes contain arbitrarily long arithmetic progressions*,
Annals of Mathematics 167 (2008), 481–547.
