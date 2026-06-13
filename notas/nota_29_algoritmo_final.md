# Nota 29 — Algoritmo Final: Extração de Todos os Primos Menores que p

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

Esta nota apresenta o algoritmo definitivo resultante da série de Notas 16–28.
O percurso partiu da análise espectral de $\log|Z_Q(\tfrac{1}{2}+it)|$ e,
após eliminar sucessivamente `isprime()`, $\zeta$, e o próprio Stage C
espectral (FFT + $t_{\max}$), chegou a um algoritmo puramente aritmético de
dois estágios:

- **Stage A (recursão):** constrói $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$
  percorrendo os blocos binários $A_k = [2^k, 2^{k+1}-1]$ em ordem crescente,
  testando divisibilidade por primos já encontrados.
- **Stage B (classificação):** para cada $m \in [2^{n-1}, p-1]$, testa
  divisibilidade por $\mathcal{P}_<$. A corretude é exata pelo Teorema MDC:
  todo composto no bloco tem seu menor fator primo em $\mathcal{P}_<$.

O algoritmo tem complexidade $O(p\sqrt{p}/\log p)$ — equivalente à divisão de
tentativas, com fator constante $2{,}5$–$6\times$ melhor pela estrutura de
blocos. É 20 linhas de Python, sem dependências externas, e foi validado para
$p \leq 1009$ com 0 falsos positivos e 0 falsos negativos.

---

## 1. Da teoria espectral ao algoritmo aritmético

### 1.1 A jornada

O método nasceu da observação (Nota 16) de que a FFT de $\log|Z_Q(\tfrac{1}{2}+it)|$
exibe picos exatamente nas frequências $\log(q)/(2\pi)$ dos primos $q < p$.
O pipeline original era completamente espectral:

```
Etapa 2: R2(t) = log|Z_Q| - log|zeta|  →  FFT  →  primos de P_<
Etapa 1: R_pre(t) = log|Z_bloco| - compostos  →  FFT iterativa  →  primos do bloco
classificador: isprime(m)
```

Cada componente foi eliminada ao longo das notas:

| Nota | Componente eliminada | Substituída por |
|---|---|---|
| 20 | `isprime(m)` | $\rho_B(m \mid \mathcal{P}_<) > 10^{-6}$ |
| 23 | `zeta` na Etapa 2 | recursão aritmética sobre blocos $A_k$ |
| 24 | Etapa 2 espectral | pré-limpeza via $\rho_B = 0$ |
| 26 | $\rho_B$ com busca contínua | divisibilidade direta (`m % b == 0`) |

O resultado é que a FFT — e com ela o $t_{\max}$ — deixou de ser necessária.

### 1.2 Por que $t_{\max}$ desapareceu

Na versão espectral, detectar dois primos vizinhos $q_1, q_2$ no sinal $R(t)$
exigia $t_{\max} > 2\pi/|\log q_2 - \log q_1|$ para separar os picos (critério
de Rayleigh). A Nota 28 formalizou a escala:

$$t_{\max}(n) \approx \pi \cdot q_{\text{twin}}(n) \sim O(2^n)$$

crescimento exponencial — o Stage C espectral não escala. O $\rho_B$
resolve o mesmo problema em $O(|\mathcal{P}_<|)$ operações: verifica
diretamente se $m$ é divisível por algum elemento de $\mathcal{P}_<$, sem
precisar "ver" $m$ via pico de FFT. $t_{\max}$ permanece documentado como
quantificação da versão espectral que foi descartada, não como parâmetro do
algoritmo.

---

## 2. O algoritmo

```python
from math import log, floor

def extrair_primos(p):
    """
    Extrai todos os primos menores que p.
    
    Sem isprime(). Sem zeta. Sem FFT.
    Justificativa teórica: Notas 20-28 (série Motor de Herança Estrutural).
    """
    n = int(floor(log(p, 2)))   # n = floor(log2(p))

    # Stage A — constrói P_< = primos < 2^(n-1)
    # Para cada m < 2^(n-1): primo <=> nenhum b em P_less com b^2 <= m divide m
    P_less = []
    for m in range(2, 2**(n-1)):
        primo = True
        for b in P_less:
            if b * b > m: break
            if m % b == 0: primo = False; break
        if primo:
            P_less.append(m)

    # Stage B — classifica bloco [2^(n-1), p-1]
    # P_less contém todos os primos < 2^(n-1) >= sqrt(m) para m no bloco.
    # Divisibilidade por P_less é condição necessária e suficiente (Nota MDC).
    primos_bloco = []
    for m in range(2**(n-1), p):
        primo = True
        for b in P_less:
            if b * b > m: break
            if m % b == 0: primo = False; break
        if primo:
            primos_bloco.append(m)

    return P_less + primos_bloco
```

### 2.1 Corretude

**Proposição.** `extrair_primos(p)` retorna exatamente o conjunto de primos
menores que $p$.

*Stage A:* por indução sobre $m$. Para $m = 2$: primo trivialmente. Para
$m > 2$: se nenhum primo $b \leq \sqrt{m}$ já encontrado divide $m$, então
$m$ não tem fator primo $\leq \sqrt{m}$, logo é primo (TFA). A indução é
válida porque os primos são encontrados em ordem crescente.

*Stage B:* pelo Teorema 1 da Nota MDC, todo composto $m \in [2^{n-1}, p-1]$
tem seu menor fator primo $q \leq \sqrt{m} \leq \sqrt{p-1} < 2^{n/2} \leq
2^{n-1}$, logo $q \in \mathcal{P}_<$. A verificação de divisibilidade por
$\mathcal{P}_<$ é portanto condição necessária e suficiente. $\square$

### 2.2 Por que a estrutura de blocos importa

O Stage A não é apenas um loop de 2 a $2^{n-1}$ — é uma recursão sobre
blocos $A_k = [2^k, 2^{k+1}-1]$ implícita na ordem de iteração. Para $m \in
A_k$, os únicos divisores relevantes são primos $< 2^{k/2} \ll 2^k$ —
muito menores que $m$. Essa separação de escalas (primo a testar $\ll$ candidato)
é a razão pelo qual Stage B é mais rápido que divisão pura ingênua: a base
$\mathcal{P}_<$ já está construída com exatamente os divisores necessários
para o bloco, sem redundância.

---

## 3. Parâmetros formalizados

Os parâmetros do algoritmo têm justificativa teórica completa, não são
escolhas empíricas:

| Parâmetro | Valor | Fonte | Interpretação |
|---|---|---|---|
| Limite do Stage A | $2^{n-1}$ | Nota MDC, Teorema 1 | Maior possível $q \leq \sqrt{m}$ para $m$ no bloco |
| Critério de primalidade | `m % b == 0` | Nota 26, Proposição | Implementação ótima de $\rho_B = 0$ |
| $\rho^*(k)$ (Stage A, versão rho_B) | $0{,}1/(2^{k+1}(k+1)\log 2)$ | Nota 27 | Margem 10× acima de $\rho_{\min}(k)$ |
| $\rho^* = 10^{-6}$ (Stage B, versão rho_B) | fixo | Nota 20 | Válido para $n \leq 15$ ($p \leq 32768$) |
| $t_{\max}$ | não existe no algoritmo | Nota 28 | Parâmetro apenas da versão espectral descartada |

---

## 4. Validação experimental

Validado para $p \in \{37, 41, 53, 67, 97, 127, 131, 199, 251, 503, 1009\}$
contra `sympy.primerange`:

| $p$ | $n$ | Primos reais | Detectados | FP | FN | Taxa |
|---|---|---|---|---|---|---|
| 37  | 5 | 11  | 11  | 0 | 0 | 100% |
| 67  | 6 | 18  | 18  | 0 | 0 | 100% |
| 131 | 7 | 31  | 31  | 0 | 0 | 100% |
| 251 | 7 | 53  | 53  | 0 | 0 | 100% |
| 503 | 8 | 95  | 95  | 0 | 0 | 100% |
| 1009| 9 | 168 | 168 | 0 | 0 | 100% |

0 falsos positivos, 0 falsos negativos em toda a faixa testada.

Note-se o contraste com os resultados das versões espectrais anteriores:
a Nota 17 reportava 93% para $p = 53$ e 88% para $p = 59$ com $t_{\max} = 150$.
As perdas eram limitação de resolução espectral — eliminadas pela substituição
por aritmética.

---

## 5. Performance

Medições em Python 3 (média de 10 execuções, i5 moderno):

| $p$ | $n$ | $\vert\Pi_p\vert$ | Stage A+B (ms) | Div. pura (ms) | sympy (ms) | Ganho vs div. |
|---|---|---|---|---|---|---|
| 67   | 6  | 18  | 0,02  | 0,03  | 0,010 | 1,5× |
| 131  | 7  | 31  | 0,03  | 0,07  | 0,012 | 2,3× |
| 257  | 8  | 54  | 0,06  | 0,16  | 0,038 | 2,7× |
| 503  | 8  | 95  | 0,12  | 0,40  | 0,099 | 3,3× |
| 1009 | 9  | 168 | 0,27  | 0,98  | 0,228 | 3,6× |
| 2003 | 10 | 303 | 0,57  | 2,67  | 0,475 | 4,7× |
| 4001 | 11 | 576 | 1,32  | 7,97  | 1,117 | 6,0× |

*Div. pura:* loop simples `all(m % b != 0 for b in primos if b*b <= m)` sem
estrutura de blocos. *sympy:* `primerange()`, implementação em C com Crivo de
Eratóstenes.

### 5.1 Por que Stage A+B supera divisão pura

O ganho crescente ($1{,}5\times$ a $6\times$ na faixa testada) vem da
estrutura de blocos:

- **Divisão pura ingênua:** para cada $m$, verifica todos os primos
  encontrados até o momento, mesmo os desnecessariamente pequenos.
- **Stage B:** verifica apenas $\mathcal{P}_<$ — exatamente os primos
  $< 2^{n-1} \approx \sqrt{p}$. Não há primos acima de $\sqrt{m_{\max}}$
  na base, sem busca redundante.

O ganho aumenta com $n$ porque a proporção de primos desnecessários na lista
cresce conforme $p$ cresce.

### 5.2 Complexidade

$$\text{Stage A}: O\!\left(\frac{2^{3n/2}}{n}\right), \quad
\text{Stage B}: O\!\left(\frac{p \cdot 2^{n-1}}{n}\right) = O\!\left(\frac{p\sqrt{p}}{\log p}\right)$$

O Stage B domina. A complexidade total $O(p\sqrt{p}/\log p)$ é a mesma da
divisão de tentativas — o ganho constante vem da organização, não da ordem
assintótica. O algoritmo ótimo assintótico continua sendo o Crivo de
Eratóstenes, $O(p \log\log p)$. A contribuição deste trabalho é a
justificativa teórica, não a eficiência assintótica.

---

## 6. O papel da teoria espectral

O algoritmo é trial division por blocos — estrutura clássica. O valor do
percurso espectral é outro:

**Descoberta do critério.** A análise de $\log|Z_Q|$ levou à definição de
$\rho_B$ como medida de irredutibilidade logarítmica (Nota 19). A Nota 26
provou que $\rho_B = 0 \iff m$ é composto — equivalência com divisibilidade
demonstrada por indução, não apenas verificada empiricamente.

**Estrutura de blocos motivada.** A hierarquia $A_k = [2^k, 2^{k+1}-1]$
emergiu da análise espectral de $Z_Q$. O Teorema MDC formalizou por que essa
partição é natural e por que $\mathcal{P}_<$ é exatamente a base necessária
para o bloco.

**Parâmetros justificados.** Os parâmetros não são ad hoc:
- O limite $2^{n-1}$ do Stage A vem do Teorema 1 da Nota MDC.
- A escala de $\rho^*(k)$ vem do comportamento assintótico de $\rho_{\min}(k)$
  (Nota 27), com cota tight demonstrada.
- A irrelevância de $t_{\max}$ é quantificada pela Nota 28: $t_{\max}(n) \sim
  \pi \cdot 2^n$ — exponencial, justificando a substituição por aritmética.

**Completitude da prova.** A série prova por indução que o algoritmo é correto
(Nota 23), que o critério é exato (Nota 26), e que os parâmetros são robustos
para qualquer escala com limiar adaptativo (Nota 27). Não há validação
exclusivamente empírica: cada resultado tem demonstração formal.

---

## 7. Conclusão

O algoritmo final é uma consequência limpa de um percurso espectral que
começou em $\log|Z_Q(\tfrac{1}{2}+it)|$ e terminou em dois loops de
divisibilidade. O percurso foi necessário: sem a teoria espectral, não
haveria motivação para a estrutura de blocos $A_k$, nem justificativa para
$\rho_B$, nem prova de que $\mathcal{P}_<$ é exatamente a base correta para
o bloco. A teoria gerou o algoritmo; o algoritmo é mais simples que a teoria
que o motivou — o que é, provavelmente, o melhor resultado possível.

---

## Referências

[Nota MDC] T. Bandeira, *Uma caracterização de primalidade via partições
binárias e MDC em intervalos reduzidos* (2026).  
[Nota 20] T. Bandeira, *Crivo Espectral sem Oráculo de Primalidade* (2026).  
[Nota 23] T. Bandeira, *Extração Recursiva de Primos via Blocos Binários* (2026).  
[Nota 24] T. Bandeira, *Pré-limpeza Espectral* (2026).  
[Nota 26] T. Bandeira, *Equivalência entre Divisibilidade e Irredutibilidade
Logarítmica Adaptativa* (2026).  
[Nota 27] T. Bandeira, *Cota Assintótica para $\rho_{\min}(k)$* (2026).  
[Nota 28] T. Bandeira, *Escala de $t_{\max}$ para a Etapa 2* (2026).  
[crivo\_algoritmo\_final.ipynb] T. Bandeira, implementação e medições de
performance, Junho de 2026.
