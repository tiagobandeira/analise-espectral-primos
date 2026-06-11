# Análise Espectral de Primos via Produtos de Intervalos Binários

**T. Bandeira · 2026**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20636392.svg)](https://doi.org/10.5281/zenodo.20636392)

---

## O resultado central

Para um primo $p$ com $n = \lfloor \log_2 p \rfloor$, define-se o produto sobre o bloco binário:

$$Q(p) = \prod_{x=2^{n-1}}^{p-1} x$$

construído a partir de inteiros consecutivos, sem qualquer conhecimento de quais são primos. A observação central, validada computacionalmente:

> A FFT de $\log|Z_Q(\frac{1}{2}+it)|$ — onde $Z_Q$ é o produto de Euler truncado sobre $[2^{n-1}, p-1]$ — exibe picos nas frequências $\log(q)/(2\pi)$ de todos os primos $q < p$. A estrutura primorial está codificada na geometria do intervalo binário e é recuperável espectralmente, **sem conhecimento prévio dos primos e sem os zeros de $\zeta$**.

O fundamento teórico (Nota 21): um inteiro $m$ é *logaritmicamente irredutível* — i.e., $\log m$ não pode ser escrito como combinação inteira $\sum e_i \log p_i$ com $p_i < m$ — se e somente se $m$ é primo. O crivo remove iterativamente as contribuições redutíveis do sinal; os picos sobreviventes são exatamente os primos. A correção do filtro segue do Teorema de Invariância: as funções $t \mapsto \cos(t \log m)$ são assintoticamente ortogonais, então remover a contribuição de um composto não contamina a de nenhum primo.

| Abordagem | Entrada | Requer |
|---|---|---|
| Produto de Euler | primos conhecidos | lista de primos |
| Fórmula explícita de Riemann–Mangoldt | zeros de $\zeta$ | zeros de $\zeta$ |
| **Este método (versão final)** | inteiros consecutivos | **nenhum** (autônomo) |

O método atual (Notas 23‑24) é completamente autônomo:  
- **Etapa A (recursão):** constrói $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$ usando apenas divisibilidade e o critério $\rho_B$, bloco a bloco.  
- **Pré‑limpeza:** subtrai de uma só vez todos os compostos do bloco, identificados por $\rho_B(m \mid \mathcal{P}_<)=0$, simulando o efeito de $\log|Z_Q| - \log|Z_{\text{compostos}}|$ sem $\zeta$.  
- **Crivo iterativo:** sobre o sinal já limpo, extrai os primos do bloco usando $\rho_B(m \mid \mathcal{P}_<) > 10^{-6}$ como classificador.

Nenhuma dependência analítica ($\zeta$) ou oráculo de primalidade (`isprime`) permanece.

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
│   ├── nota_21_formalizacao.md
│   ├── nota_22_metodo.md
│   ├── nota_23_recursao_blocos.md          ← substitui ζ por recursão
│   └── nota_24_prelimpeza.md               ← pré‑limpeza + equivalência com versão ζ
└── notebooks/
    ├── benchmark_espectral.ipynb
    ├── crivo_espectral_v2.ipynb
    ├── crivo_sem_oraculo.ipynb
    ├── detector_frequencia_3.ipynb
    ├── fundamentos_teoricos_v2.ipynb
    └── exp_c_recursao.ipynb                 ← validação da recursão (substituto de ζ)
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

### Nota 20 — Crivo Espectral sem Oráculo de Primalidade (versão original)

Elimina `isprime()` substituindo-o pelo critério $\rho(m \mid \mathcal{P}_<) > \rho^*$, onde $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$. O pipeline inverte a ordem das etapas (Etapa 2 → Etapa 1). **Ainda usava $\zeta$ na Etapa 2.** Validado para $p \in \{37, 41, 53, 59, 67\}$. A versão final, que elimina $\zeta$, é documentada nas Notas 23 e 24.

### Nota 21 — Formalização do Crivo Espectral Oracle-Free

Formaliza a teoria a partir de uma definição central — Redutibilidade Logarítmica — da qual todos os resultados derivam. Estrutura:

- **Proposição:** $m$ é logaritmicamente irredutível $\iff$ $m$ é primo (prova via TFA)
- **Lema $\rho$:** $\rho(m \mid \mathcal{P}_<) = 0 \iff m$ é composto no bloco (corolário do Teorema 1 da Nota MDC)
- **Teorema de Invariância:** $\mathcal{R}_m$ remove a contribuição de $m$ sem afetar nenhum primo $q \neq m$, no limite $T \to \infty$ (prova via ortogonalidade das funções de Dirichlet)
- **Corolário:** após eliminação iterativa dos redutíveis, os sobreviventes são exatamente os primos do bloco

A FFT não é objeto da teoria — é o instrumento que implementa o Corolário na prática.

### Nota 22 — Método do Crivo Espectral Oracle-Free

Descrição reproduzível e agnóstica de linguagem do algoritmo. Contém pseudocódigo completo, tabela de parâmetros com justificativas, checklist de verificação da implementação, e documentação das limitações conhecidas com soluções. Parâmetros recomendados: $t_{\max} > 2\pi/(\log q_2 - \log q_1)$ para o par mais próximo no bloco; $\rho^* = 10^{-6}$ (robusto para $p \leq 499$).

### Nota 23 — Extração Recursiva de Primos via Blocos Binários: Substituição de $\zeta$ na Etapa 2

**Elimina completamente $\zeta$.** A Etapa 2 (extração de $\mathcal{P}_<$) é substituída por uma recursão sobre os blocos $A_k = [2^k, 2^{k+1}-1]$, que constrói $\mathcal{P}_<$ indutivamente usando apenas o critério $\rho_B$ e divisibilidade. A correção é provada por indução a partir do Teorema 1 da Nota MDC. Validado para $n \in \{5,6,7,8\}$ (primos até $511$) com 100% de acerto. O pipeline resultante opera inteiramente sem dependências analíticas externas.

### Nota 24 — Pré‑limpeza e Equivalência com a Versão com $\zeta$

**Completa a autonomia do método.** A pré‑limpeza — passo explícito antes do crivo iterativo — subtrai de uma só vez todos os compostos do bloco (identificados por $\rho_B(m \mid \mathcal{P}_<)=0$), replicando o efeito de $\log|Z_Q| - \log|Z_{\text{compostos}}|$ que antes era obtido via $\zeta$. O sinal residual inicial contém apenas os primos do bloco, maximizando o SNR desde o início. A correção é garantida pelo Lema $\rho$ (Nota 20). A versão final do pipeline (Nota 23 + Nota 24) é **autônoma**: sem $\zeta$, sem `isprime()`, sem qualquer referência analítica externa.

---

## Notebooks

| Notebook | Conteúdo |
|---|---|
| `benchmark_espectral.ipynb` | Comparação $Q(p)$ vs primorial vs fatorial; métricas de precisão, tempo e eficiência |
| `crivo_espectral_v2.ipynb` | Crivo por subtração iterativa de $S_m(t)$ sem lista prévia de compostos (versão original com $\zeta$) |
| `crivo_sem_oraculo.ipynb` | Pipeline sem `isprime()`, com $\rho$ e recursão (pré‑limpeza incluída na versão final) |
| `detector_frequencia_3.ipynb` | Irredutibilidade logarítmica; distribuição de $\rho(m)$; correlação com distância ao primo |
| `fundamentos_teoricos_v2.ipynb` | SNR como função de $p$ até 499; estabilidade de $\rho_{\min}$; $t_{\min}$ para pares gêmeos |
| **`exp_c_recursao.ipynb`** | **Validação da extração recursiva de primos via blocos binários (substituto de $\zeta$). Cobre níveis até $2^8$, confirmando 100% de acerto sem falsos positivos.** |
---

## Dependências

```bash
pip install numpy scipy mpmath sympy
```

O cálculo de $\zeta(1/2 + it)$ via mpmath **não é mais necessário** na versão final (Notas 23‑24). Permanece apenas para comparação histórica.

---

## Questões abertas

1. **Escala de $t_{\max}$** — para primos gêmeos, $t_{\min} \sim O(p / \log p)$ empiricamente (Nota 19, tabela até $p = 463$). A questão analítica — se existe $t_{\max}$ polinomial em $p$ que garanta separação de todos os pares — está em aberto.

2. **SNR assintótico da Etapa 2** — o SNR da Etapa 1 é estável para $p \leq 499$; o da Etapa 2 degrada. A escala exata de $t_{\max}$ necessária para manter SNR > 1 na Etapa 2 como função de $n$ está em aberto.

3. **Crivo espectral autônomo completo** — existe operador que, a partir dos picos irredutíveis de $Z_{Q(p)}$, produz o próximo primo sem aritmética inteira e sem $\zeta$? (Questão 4, Nota 19.)

4. **Ressonância espectral como detector de fatores** — pode-se detectar diretamente a existência de um fator primo comum entre dois números pela interferência de seus picos, evitando qualquer divisibilidade? (Hipótese B, Nota 20, em investigação.)

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