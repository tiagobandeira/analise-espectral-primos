# Análise Espectral de Primos via Produtos de Intervalos Binários

**T. Bandeira · 2026**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20602446.svg)](https://doi.org/10.5281/zenodo.20636392)


---

## O resultado central

Para um primo $p$ com $n = \lfloor \log_2 p \rfloor$, define-se o produto sobre o bloco binário:

$$Q(p) = \prod_{x=2^{n-1}}^{p-1} x$$

construído a partir de inteiros consecutivos, sem qualquer conhecimento de quais são primos. A observação central, validada computacionalmente:

> A FFT de $\log|Z_Q(\frac{1}{2}+it)|$ — onde $Z_Q$ é o produto de Euler truncado sobre $[2^{n-1}, p-1]$ — exibe picos nas frequências $\log(q)/(2\pi)$ de todos os primos $q < p$. A estrutura primorial está codificada na geometria do intervalo binário e é recuperável espectralmente, sem conhecimento prévio dos primos e sem os zeros de $\zeta$.

O fundamento teórico (Nota 21): um inteiro $m$ é *logaritmicamente irredutível* — i.e., $\log m$ não pode ser escrito como combinação inteira $\sum e_i \log p_i$ com $p_i < m$ — se e somente se $m$ é primo. O crivo remove iterativamente as contribuições redutíveis do sinal; os picos sobreviventes são exatamente os primos. A correção do filtro segue do Teorema de Invariância: as funções $t \mapsto \cos(t \log m)$ são assintoticamente ortogonais, então remover a contribuição de um composto não contamina a de nenhum primo.

| Abordagem | Entrada | Requer |
|---|---|---|
| Produto de Euler | primos conhecidos | lista de primos |
| Fórmula explícita de Riemann–Mangoldt | zeros de $\zeta$ | zeros de $\zeta$ |
| **Este método** | inteiros consecutivos | $\zeta$ na Etapa 2 |

> **Nota honesta:** $\zeta$ é usada na Etapa 2 como referência de normalização para extrair os primos menores que $2^{n-1}$. A Nota 20 elimina o verificador externo de primalidade (`isprime`), não $\zeta$. A questão de substituir $\zeta$ por uma referência intrinsecamente espectral está em aberto.

---

## Origem

Este repositório nasceu como subproduto da série [Motor de Herança Estrutural](https://github.com/tiagobandeira/conjectura-de-goldbach), um projeto independente sobre a Conjectura de Goldbach. Durante a investigação das âncoras do operador $W_i(C)$ e das sequências hierárquicas $L(P_n)$, surgiu a necessidade de extrair primoriais sem depender de um crivo externo — o que levou ao método documentado aqui.

---

## Estrutura do repositório

```
analise-espectral-primos/
├── README.md
├── notas/
│   ├── nota_16_espectral_bloco_binario_primorial.md
│   ├── nota_17_ferramenta_espectral_Qp.md
│   ├── nota_18_benchmark_espectral.md
│   ├── nota_19_detector_espectral.md
│   ├── nota_20_crivo_espectral_sem_oraculo.md
│   ├── nota_21_formalizacao.md          ← teoria formal (nova)
│   └── nota_22_metodo.md                ← algoritmo reproduzível (nova)
└── notebooks/
    ├── benchmark_espectral.ipynb
    ├── crivo_espectral_v2.ipynb
    ├── crivo_sem_oraculo.ipynb
    ├── detector_frequencia_3.ipynb
    └── fundamentos_teoricos_v2.ipynb    ← SNR, ρ_min, escalabilidade (novo)
```

---

## Notas

### Nota 16 — Conexão Espectral entre Blocos Binários e a Hierarquia Primorial

$Q(p)$ contém todos os primos menores que $p$ como divisores — consequência do Teorema 1 dos [blocos binários](https://github.com/tiagobandeira/primalidade-blocos-binarios). Introduz a análise de $Z_Q/\zeta$ e identifica o efeito de cancelamento: a divisão por $\zeta$ remove os primos do intervalo $[2^{n-1}, p-1]$, recuperando apenas os primos menores que $2^{n-1}$. Motivação para o pipeline de dois estágios da Nota 17.

### Nota 17 — Ferramenta Espectral via $Q(p)$: Fundamentação e Validação

Resolve o cancelamento com o pipeline de dois estágios. Validado para $p \in \{37, 41, 53\}$, com recuperação de 100% dos primos para $p \leq 41$ e 93% para $p = 53$ (primo 41 recuperável com $t_{\max} = 300$).

### Nota 18 — Benchmark Espectral: Primorial, Fatorial e $Q(p)$

Compara as três funções como base para extração espectral ($p \in \{37, 41, 53\}$):

| Função | Taxa média | Tempo médio |
|--------|-----------|-------------|
| $Q(p)$ | **97,8%** | **0,08 s** |
| Primorial P# | 92,0% | 0,12 s |
| Fatorial $(p-1)!$ | 31,3% | 5,46 s |

$Q(p)$ supera inclusive o primorial. Na faixa $f \in [0.4, 0.6]$ (bloco binário), exibe picos quase periódicos de alta nitidez ausentes nos outros extratores — o recorte binário atua como filtro natural de banda passante.

Resultados do `fundamentos_teoricos_v2.ipynb` (Exp 3 e 4b) respondem as questões assintóticas: o SNR da Etapa 1 é estável em $[0.72, 0.98]$ para $p \leq 499$; o SNR da Etapa 2 é o gargalo (cai com $p$, requer $t_{\max}$ crescente). O valor mínimo de $\rho$ entre primos do bloco decai com $p$ mas permanece acima de $3.3 \times 10^{-4}$ para $p \leq 499$.

### Nota 19 — Detector Espectral de Primalidade: da Razão $R(k)$ à Irredutibilidade Logarítmica

Três abordagens progressivas para detecção do próximo primo sem oráculo. A formulação final: $m$ é primo $\iff$ $\log m$ é irredutível no reticulado inteiro gerado por $\{\log p_i : p_i < m\}$. O resíduo contínuo $\rho(m)$ atinge 80,1% de separação sem aritmética inteira. Resultado inesperado: correlação negativa entre $\rho(m)$ e distância ao primo mais próximo (Spearman $-0.45$) — compostos próximos de primos têm resíduo *maior*, não menor.

Contém tabela empírica de $t_{\min}$ para pares gêmeos até $(461, 463)$, confirmando crescimento $\sim p / \log p$.

### Nota 20 — Crivo Espectral sem Oráculo de Primalidade

Elimina `isprime()` substituindo-o pelo critério $\rho(m \mid P_<) > \rho^*$, onde $P_< = \{q : q \text{ primo}, q < 2^{n-1}\}$. O critério é exato pelo Corolário do Teorema 1 dos blocos binários: todo composto em $[2^{n-1}, p-1]$ tem todos os seus fatores primos em $P_<$, portanto $\rho = 0$ exatamente para compostos. O pipeline inverte a ordem das etapas (Etapa 2 → Etapa 1): $P_<$ é extraída primeiro e fornece a base para o classificador $\rho$ na Etapa 1. Validado para $p \in \{37, 41, 53, 59, 67\}$.

### Nota 21 — Formalização do Crivo Espectral Oracle-Free *(nova)*

Formaliza a teoria a partir de uma definição central — Redutibilidade Logarítmica — da qual todos os resultados derivam. Estrutura:

- **Proposição:** $m$ é logaritmicamente irredutível $\iff$ $m$ é primo (prova via TFA)
- **Lema $\rho$:** $\rho(m \mid P_<) = 0 \iff m$ é composto no bloco (corolário do Teorema 1 da Nota MDC)
- **Teorema de Invariância:** $R_m$ remove a contribuição de $m$ sem afetar nenhum primo $q \neq m$, no limite $T \to \infty$ (prova via ortogonalidade das funções de Dirichlet)
- **Corolário:** após eliminação iterativa dos redutíveis, os sobreviventes são exatamente os primos do bloco

A FFT não é objeto da teoria — é o instrumento que implementa o Corolário na prática.

### Nota 22 — Método do Crivo Espectral Oracle-Free *(nova)*

Descrição reproduzível e agnóstica de linguagem do algoritmo. Contém pseudocódigo completo, tabela de parâmetros com justificativas, checklist de verificação da implementação, e documentação das limitações conhecidas com soluções. Parâmetros recomendados: $t_{\max} > 2\pi/(\log q_2 - \log q_1)$ para o par mais próximo no bloco; $\rho^* = 10^{-6}$ (robusto para $p \leq 499$).

---

## Notebooks

| Notebook | Conteúdo |
|---|---|
| `benchmark_espectral.ipynb` | Comparação $Q(p)$ vs primorial vs fatorial; métricas de precisão, tempo e eficiência |
| `crivo_espectral_v2.ipynb` | Crivo por subtração iterativa de $S_m(t)$ sem lista prévia de compostos |
| `crivo_sem_oraculo.ipynb` | Pipeline sem `isprime()`; calibração de $\rho^*$; comparação com referência |
| `detector_frequencia_3.ipynb` | Irredutibilidade logarítmica; distribuição de $\rho(m)$; correlação com distância ao primo |
| `fundamentos_teoricos_v2.ipynb` | SNR como função de $p$ até 499; estabilidade de $\rho_{\min}$; $t_{\min}$ para pares gêmeos *(novo)* |

---

## Dependências

```bash
pip install numpy scipy mpmath sympy
```

O cálculo de $\zeta(1/2 + it)$ via mpmath é o gargalo computacional (~8–15s para 3000 pontos). O cache automático por parâmetros garante reutilização entre chamadas com a mesma grade $(t_{\min}, t_{\max}, \Delta t)$.

---

## Questões abertas

1. **Substituição de $\zeta$** — existe referência espectral construída a partir de $Z_Q$ sem $\zeta$? Blocos binários e uniões de blocos foram testados e falharam por obstrução estrutural (Nota 20, Seção 7). Em aberto.

2. **Escala de $t_{\max}$** — para primos gêmeos, $t_{\min} \sim O(p / \log p)$ empiricamente (Nota 19, tabela até $p = 463$). A questão analítica — se existe $t_{\max}$ polinomial em $p$ que garanta separação de todos os pares — está em aberto.

3. **SNR assintótico da Etapa 2** — o SNR da Etapa 1 é estável para $p \leq 499$; o da Etapa 2 degrada. A escala exata de $t_{\max}$ necessária para manter SNR > 1 na Etapa 2 como função de $n$ está em aberto.

4. **Crivo espectral autônomo completo** — existe operador que, a partir dos picos irredutíveis de $Z_{Q(p)}$, produz o próximo primo sem aritmética inteira e sem $\zeta$? (Questão 4, Nota 19.)

---

## Conexões

- **[Motor de Herança Estrutural](https://github.com/tiagobandeira/conjectura-de-goldbach)** — série sobre Goldbach que motivou este trabalho; as sequências $L(P_n)$ (Nota 14) e classes residuais módulo primoriais (Nota 15) estão nessa série.
- **[Primalidade por Blocos Binários](https://github.com/tiagobandeira/primalidade-blocos-binarios)** — Teorema 1 (caracterização por MDC) e Proposição 2 (divisibilidade por $P(N)$), que fundamentam o classificador $\rho$ da Nota 20 e a Proposição da Nota 21.

---

## Citação

```
T. Bandeira, "Análise Espectral de Primos via Produtos de Intervalos Binários",
notas de pesquisa independente, 2026.
DOI: 10.5281/zenodo.20636392
```

---

## Licença

- Documentação e notas matemáticas: [CC BY 4.0](LICENSE.txt)
- Código-fonte: [MIT License](LICENSE-MIT.txt)