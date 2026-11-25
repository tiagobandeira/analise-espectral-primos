# Artigo — Irredutibilidade logarítmica: anatomia de um crivo espectral

Este diretório contém o artigo, as figuras e os experimentos que o sustentam.

```
artigo/
  artigo.md                      texto completo (Markdown + LaTeX)
  figuras/*.png                  figuras 1–5, geradas pelos scripts
  experimentos/
    verificar_teoremas.py        V1–V5: auditoria dos teoremas por força bruta
    experimentos_espectrais.py   E1–E5: experimentos e figuras
    resultados.json              valores brutos de E1–E5
    verificacao_teoremas.json    valores brutos de V1–V5
```

## O que o artigo argumenta

O programa espectral do repositório (Notas 16–40) produziu um crivo correto, mas
por um caminho que ele mesmo desmonta: cada camada espectral (ζ, FFT, t_max,
isprime) foi substituída por aritmética até restarem dois laços de divisibilidade.
O artigo reconstrói esse percurso e separa o que sobreviveu do que era narrativa.

Resultados demonstrados (não apenas observados):

| # | Resultado | Onde |
|---|---|---|
| Teorema 3 | irredutibilidade logarítmica ⟺ primalidade | §2.1 |
| Lema 4 | composto em `A_k` tem fator primo `< 2^k` | §3.1 |
| Teorema 7 | `ρ(q) ≥ 1/(2^{k+1}(k+1)log 2)` sobre o bloco | §4.2 |
| Teorema 9 | `ρ(q) = log(1+1/q)/log q` **exato**, para todo primo do bloco | §4.3 |
| Corolário 10 | `ρ_min(k) = log(1+1/q_max)/log q_max` | §4.3 |
| Teorema 12 | `t_max(n) = Θ(2^n/n)`, sem depender da conjectura de gêmeos | §5.3 |
| Proposição 13 | lei do ganho orbital é identidade exata | §6.1 |
| Proposição 14 | assinatura de gêmeos decai como `p/T` | §6.2 |
| Proposição 15 | janela de leitura: `2W+1 < T/(π q)` | §6.2 |

Correções ao corpus (Seção 9): a lei de `T_max` é linear em `p` e não
superlinear; a rota de Baker é desnecessária (a cota correta é elementar); os
"80,1% de acurácia" do detector contínuo medem incompletude da busca, não
sobreposição geométrica; o "Teorema de Invariância" da Nota 21 é a definição do
operador, e seu conteúdo real é a ortogonalidade (Lema 11).

## Como reproduzir

```bash
pip install numpy scipy matplotlib sympy   # mpmath não é necessário
python experimentos/verificar_teoremas.py       # ~2 min
python experimentos/experimentos_espectrais.py  # ~6 min, gera figuras/
```

Cada script aceita seleção de etapas, por exemplo `experimentos_espectrais.py e3 e5`.

Nenhum experimento usa amostragem aleatória; todos são determinísticos.

## Formalização

O núcleo aritmético/analítico está em `../formalizacao/` (Lean 4 + Mathlib).
Veja a Seção 8 do artigo e o `README.md` daquele diretório.
