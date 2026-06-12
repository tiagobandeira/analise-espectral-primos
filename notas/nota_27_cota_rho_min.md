# Nota 27 — Cota Assintótica para $\rho_{\min}(k)$ e Limiar Adaptativo

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

O limiar $\rho^* = 10^{-6}$ usado como classificador nas Notas 20–26 é
robusto para toda a faixa testada ($p \leq 499$, $k \leq 9$), mas a Nota 26
deixou em aberto o comportamento assintótico de $\rho_{\min}(k)$ — o menor
valor de $\rho_{\text{adapt}}$ entre primos do bloco $A_k$ — e em que escala
o limiar atual se torna insuficiente.

O Exp F resolve essa questão de forma mais direta e mais tight do que a rota
original via Baker. A análise empírica (F1–F3) revela um padrão estrutural
preciso: o primo que realiza $\rho_{\min}(k)$ é sempre o **maior primo do
bloco** $q_{\max} \in A_k$, e a combinação logarítmica mais próxima é sempre
$\log(q_{\max} \pm 1)$ — o vizinho composto imediato. Isso reduz o problema
de aproximação logarítmica a um problema sobre gaps de primos:

$$\rho_{\min}(k) = \frac{|\log q_{\max} - \log(q_{\max} \pm 1)|}{\log q_{\max}}
\approx \frac{1}{q_{\max} \cdot \log q_{\max}}$$

Como $q_{\max} \leq 2^{k+1} - 1$, a cota inferior assintoticamente tight é:

$$\rho_{\min}(k) \gtrsim \frac{1}{2^{k+1}(k+1)\log 2}$$

A razão entre o valor observado e essa cota converge para 1 conforme $k$
cresce (razão $= 1{,}005$ para $k = 10$). Isso é muito mais informativo do
que qualquer cota via Baker, que é frouxa por $10^{20}$ ou mais para esses
valores.

A extrapolação prática:

| $\rho^*$ | $k$ de cruzamento | Primos de ordem |
|---|---|---|
| $10^{-6}$ | $k \approx 16$ | $\sim 10^{4{,}8}$ |
| $10^{-8}$ | $k \approx 22$ | $\sim 10^{6{,}6}$ |
| $10^{-10}$ | $k \approx 28$ | $\sim 10^{8{,}4}$ |

Para escalar o método além de $k \approx 16$, o limiar adaptativo natural é
$\rho^*(k) = c / (2^{k+1}(k+1)\log 2)$ com $c < 1$, garantindo separação
para todo $k$.

---

## 1. Contexto

A Nota 26 estabeleceu que $\rho_{\text{adapt}}(q) > 0$ para todo primo $q \in
A_k$ pelo Teorema Fundamental da Aritmética — existe separação, mas sem cota
quantitativa. A questão prática era: quão rápido decai $\rho_{\min}(k)$, e
em que $k$ o limiar $\rho^* = 10^{-6}$ se torna insuficiente?

A tabela empírica do Exp F1 mostrava decaimento sistemático:

| $k$ | $\rho_{\min}(k)$ | $\rho_{\min} \cdot k$ | $\rho_{\min} \cdot k^2$ |
|-----|-----------------|----------------------|------------------------|
| 4   | $9{,}25 \times 10^{-3}$ | 0,037 | 0,148 |
| 6   | $1{,}62 \times 10^{-3}$ | 0,010 | 0,058 |
| 8   | $3{,}16 \times 10^{-4}$ | 0,003 | 0,020 |
| 10  | $6{,}44 \times 10^{-5}$ | 0,001 | 0,006 |
| 11  | $2{,}95 \times 10^{-5}$ | 0,000 | 0,004 |

Nem $\rho_{\min} \cdot k$ nem $\rho_{\min} \cdot k^2$ são constantes — o
decaimento não é simples lei de potência em $k$. O padrão verdadeiro emerge
da análise estrutural dos primos que realizam o mínimo.

---

## 2. Proposição: $\rho_{\min}(k)$ é realizado pelo maior primo do bloco

**Observação (Exp F3).** Para $k = 2, \ldots, 11$, o primo $q \in A_k$ que
realiza $\rho_{\min}(k)$ é o maior primo do bloco, e a combinação logarítmica
mais próxima é $\log(q \pm 1)$.

| $k$ | $q$ (realiza $\rho_{\min}$) | maior primo de $A_k$ | $m^*$ (mais próximo) |
|---|---|---|---|
| 4  | 31  | 31  | $32 = 2^5$ |
| 5  | 61  | 61  | $62 = 2 \cdot 31$ |
| 6  | 127 | 127 | $128 = 2^7$ |
| 7  | 251 | 251 | $250 = 2 \cdot 5^3$ |
| 8  | 509 | 509 | $508 = 4 \cdot 127$ |
| 9  | 1021| 1021| $1020 = 4 \cdot 255$ |
| 10 | 2039| 2039| $2038 = 2 \cdot 1019$ |
| 11 | 4093| 4093| $4092 = 4 \cdot 1023$ |

A razão é estrutural: o maior primo do bloco está mais próximo de $2^{k+1}$,
que é altamente composto ($= 2 \cdot 2^k$), minimizando a distância logarítmica
ao reticulado. Primos menores dentro do bloco estão mais afastados do limite
superior e têm $\rho_{\text{adapt}}$ maior.

---

## 3. Cota assintótica

**Lema.** Para $q$ primo ímpar e $m^* = q + 1$ (composto par), a distância
logarítmica relativa é:

$$\frac{|\log q - \log m^*|}{\log q} = \frac{|\log(1 - 1/m^*)|}{\log q}
\approx \frac{1}{m^* \log q} \approx \frac{1}{q \log q}$$

para $q$ grande. A aproximação é exata no sentido de que a razão
$\left(\frac{1}{q \log q}\right) \Big/ \rho_{\min}(k)$ converge para 1
conforme $k \to \infty$ (verificado numericamente até $k = 11$).

**Corolário (Cota inferior tight).** Como o maior primo do bloco satisfaz
$q_{\max} \leq 2^{k+1} - 1$, e todo primo tem pelo menos um vizinho composto
imediato ($q \pm 1$ é par para $q$ ímpar):

$$\rho_{\min}(k) \approx \frac{1}{q_{\max} \cdot \log q_{\max}}
\gtrsim \frac{1}{2^{k+1} \cdot (k+1) \log 2}$$

**Verificação numérica:**

| $k$ | cota $\frac{1}{2^{k+1}(k+1)\log 2}$ | $\rho_{\min}$ observado | razão |
|---|---|---|---|
| 4  | $9{,}017 \times 10^{-3}$ | $9{,}245 \times 10^{-3}$ | 1,025 |
| 6  | $1{,}610 \times 10^{-3}$ | $1{,}619 \times 10^{-3}$ | 1,006 |
| 8  | $3{,}131 \times 10^{-4}$ | $3{,}155 \times 10^{-4}$ | 1,008 |
| 10 | $6{,}404 \times 10^{-5}$ | $6{,}438 \times 10^{-5}$ | 1,005 |
| 11 | $2{,}935 \times 10^{-5}$ | $2{,}949 \times 10^{-5}$ | 1,005 |

A razão converge para 1 e a cota é tight para $k \geq 6$.

**Comparação com Baker.** A cota de Baker-Wüstholz para a forma linear
$|\log q - e \log p|$ com $q, p$ primos e $e \leq e^*(p,k)$ é da ordem de
$\exp(-C \cdot k \log^2 2 \cdot \log k)$, que é inferior ao observado por um
fator de $10^{20}$ para $k = 5$ e piora rapidamente. Baker garante que
$\rho_{\min} > 0$ para todo $k$, mas não fornece informação útil sobre a
taxa de decaimento na escala prática. A cota acima, derivada diretamente da
estrutura dos gaps de primos, é a ferramenta correta para este problema.

---

## 4. Extrapolação e limiar adaptativo

A cota tight permite extrapolação precisa. O limiar $\rho^*$ torna-se
insuficiente quando $\rho_{\min}(k) \lesssim \rho^*$, ou seja, quando:

$$\frac{1}{2^{k+1}(k+1)\log 2} \lesssim \rho^* \implies
2^{k+1}(k+1) \gtrsim \frac{1}{\rho^* \log 2}$$

Resolvendo numericamente:

| $\rho^*$ | $k$ de cruzamento | Escala de primos |
|---|---|---|
| $10^{-6}$ (atual) | $k \approx 16$ | $\sim 65000$ |
| $10^{-8}$ | $k \approx 22$ | $\sim 4 \times 10^6$ |
| $10^{-10}$ | $k \approx 28$ | $\sim 3 \times 10^8$ |
| $10^{-15}$ | $k \approx 44$ | $\sim 10^{13}$ |

Para $k \leq 16$ (primos até $\sim 65000$), $\rho^* = 10^{-6}$ é seguro.
Para escalas maiores, o limiar adaptativo natural é:

$$\rho^*(k) = \frac{c}{2^{k+1}(k+1)\log 2}, \quad c \in (0, 1)$$

com $c$ escolhido para manter margem de segurança adequada. A escolha $c = 0{,}1$
dá $\rho^*(k) = \rho_{\min}(k) / 10$ — uma ordem de grandeza de margem para
erros de ponto flutuante — e é robusta para qualquer $k$.

---

## 5. Estrutura do decaimento: conexão com a distribuição de primos

A cota $\rho_{\min}(k) \sim 1/(2^k \cdot k)$ pode ser reescrita em termos
do primo $q_{\max}$ diretamente:

$$\rho_{\min}(k) \approx \frac{1}{q_{\max} \cdot \log q_{\max}}$$

Isso é exatamente o inverso da função $\theta(x) = \sum_{p \leq x} \log p$
avaliada no maior primo do bloco — não uma coincidência, mas consequência
de que $\rho_{\min}$ mede a resolução logarítmica necessária para distinguir
$q_{\max}$ de seu vizinho composto.

A expressão tem uma interpretação direta: para o método espectral detectar
o primo $q_{\max}$ com $\rho_{\text{adapt}}$, o limiar $\rho^*$ precisa ser
menor que $1/(q_{\max} \log q_{\max})$. Isso é precisamente a condição para
que $\log q_{\max}$ e $\log(q_{\max} \pm 1)$ sejam distinguíveis pelo critério
— o mesmo requisito de resolução que aparece na condição $t_{\max} > 2\pi /
(\log q_2 - \log q_1)$ para separação espectral (Nota 22), agora no domínio
aritmético.

---

## 6. Resolução da Questão 1 da Nota 26

**Questão 1 da Nota 26** (*"Qual é o comportamento assintótico de $\rho_{\min}(k)$?
Cotas de Baker forneceriam garantia analítica para $\rho^* = 10^{-6}$."*)

**Resposta:** $\rho_{\min}(k) \sim 1/(2^{k+1}(k+1)\log 2)$, verificado
numericamente até $k = 11$ com razão observada/cota convergindo para $1$.
A rota via Baker não é o caminho correto para esta questão: Baker garante
positividade mas é frouxa por muitas ordens de grandeza. A cota tight vem
da estrutura dos gaps de primos — o primo que realiza $\rho_{\min}$ é sempre
o maior do bloco, e sua distância ao vizinho composto é $1$.

O limiar $\rho^* = 10^{-6}$ é seguro para $k \leq 15$ ($p \lesssim 32768$).
Para escalas maiores, usar $\rho^*(k) = c/(2^{k+1}(k+1)\log 2)$ com $c < 1$.

---

## 7. Questões em aberto remanescentes

**Questão 1 — Prova formal do padrão.** A observação de que o maior primo
do bloco realiza $\rho_{\min}$ foi verificada empiricamente para $k \leq 11$.
Uma prova formal precisaria mostrar que para todo primo $q < q_{\max}$ no
bloco, a distância ao reticulado é estritamente maior. Isso envolve propriedades
da distribuição de primos no bloco que não foram formalizadas.

**Questão 2 — Caso dos primos de Mersenne.** Para $k$ tal que $2^{k+1} - 1$
é primo de Mersenne (ex: $k = 6$, $2^7 - 1 = 127$), o maior primo do bloco
é $q_{\max} = 2^{k+1} - 1$ e $m^* = 2^{k+1}$, uma potência de 2. Nesse caso
$\rho_{\min}(k) = 1/(q_{\max} \log q_{\max})$ exatamente. Para $k$ sem primo
de Mersenne no topo, $q_{\max} < 2^{k+1} - 1$ e a cota é ligeiramente folga.
A influência dos primos de Mersenne no comportamento de $\rho_{\min}$ ao
longo de $k$ é uma questão aberta.

**Questão 3 — Conexão com $t_{\max}$.** A condição $\rho^* < \rho_{\min}(k)
\sim 1/(q_{\max} \log q_{\max})$ e a condição espectral $t_{\max} > 2\pi /
(\log q_2 - \log q_1) \sim 2\pi q / \log q$ têm a mesma dependência em
$q/\log q$. Isso sugere que os dois requisitos de escala — resolução aritmética
e resolução espectral — crescem à mesma taxa com o tamanho dos primos. A
formalização dessa equivalência está em aberto.

---

## Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026).  
[Nota 22] T. Bandeira, *Método do Crivo Espectral Oracle-Free* (2026).  
[Nota 25] T. Bandeira, *Critério $\rho$ sem Aritmética Inteira: Separabilidade
Logarítmica e Limites de Escala* (2026).  
[Nota 26] T. Bandeira, *Equivalência entre Divisibilidade e Irredutibilidade
Logarítmica Adaptativa* (2026).  
[Exp F] T. Bandeira, `exp_f_rho_min.ipynb` — Análise empírica de $\rho_{\min}(k)$,
ajuste assintótico e comparação com cota de Baker, Junho de 2026.  
A. Baker, *Transcendental Number Theory*, Cambridge University Press (1975).
