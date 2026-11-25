# Formalização em Lean 4

Verificação mecânica dos resultados aritméticos e analíticos do artigo
*Irredutibilidade logarítmica: anatomia de um crivo espectral*.

Toolchain: `leanprover/lean4:v4.37.0-rc1` · Mathlib `master` (commit
`aad247f9`). Nada de `sorry`, nenhum axioma além dos de Lean/Mathlib.

## Conteúdo

| módulo | declaração | artigo |
|---|---|---|
| `Espectral/Bloco.lean` | `minFac_lt_dois_pow` | Lema 4 (metade) |
| | `existe_fator_primo_na_semente` | **Lema 4** — composto em `A_k` tem fator primo `< 2^k` |
| | `bloco_primo_iff` | **Corolário 5** — corretude do crivo por blocos |
| | `LogRedutivel` | Definição 2 |
| | `log_prod_pow` | auxiliar: `log` de produto de potências |
| | `eq_prod_of_log_eq` | auxiliar: decomposição logarítmica ⟹ igualdade de produtos |
| | `logRedutivel_iff` | **Teorema 3** — irredutibilidade logarítmica ⟺ composto |
| `Espectral/Rho.lean` | `log_dist_ge` | **Lema 6** — o vizinho inteiro minimiza a distância |
| | `inv_succ_le_log_ratio` | `log(1+1/q) ≥ 1/(q+1)` |
| | `log_dist_succ_eq` | a cota é atingida em `q+1` (metade do **Teorema 9**) |
| | `cota_rho` | **Teorema 7** — `ρ ≥ 1/(2^(k+1)(k+1)log 2)` |
| | `cota_antitone` | a cota decresce com `k` |

## Como compilar

A via **verificada** nesta máquina (toolchain `leanprover/lean4:v4.37.0-rc1`,
Mathlib `master`, oleans do cache oficial):

```bash
lean -o Espectral/Bloco.olean Espectral/Bloco.lean
lean -o Espectral/Rho.olean   Espectral/Rho.lean
lean -o Espectral.olean       Espectral.lean
```

com `LEAN_PATH` apontando para os `.lake/build/lib/lean` de cada pacote de
Mathlib e para este diretório. As três compilações terminam sem erros e sem
avisos.

A via convencional é:

```bash
lake exe cache get   # baixa os oleans pré-compilados do Mathlib (~1 GB)
lake build
```

(Observação: como os oleans do Mathlib foram obtidos por `cache unpack` e não por
uma compilação local, o `lake build` pode decidir recompilar o grafo do Mathlib
antes de tocar nestes dois arquivos; a via acima contorna isso.)

## O que não está formalizado

* a definição de `ρ` como ínfimo sobre o reticulado (formalizamos as duas metades
  que o Teorema 9 usa: a cota inferior para todo inteiro e o ponto que a atinge);
* a igualdade completa do Teorema 9 (depende do Lema 8, suavidade de `q+1`, que é
  aritmética elementar mas exige `Nat.factorization` em extensão);
* o corolário numérico "`ρ* = 10^{-6}` vale até `k = 15`" (falta uma cota
  numérica de `log 2` em Mathlib; verificado numericamente);
* as Proposições 13–15, que são afirmações sobre transformadas de Fourier de
  somas de cossenos.

## Observação

O Teorema 3 — o "resultado central" do corpus espectral — sai em poucas linhas a
partir da fatoração única (`Nat.prod_primeFactors_pow_factorization`). O peso
matemático do programa não estava no critério, mas na sua versão contínua
(Teoremas 7 e 9) e na sua leitura espectral (Teorema 12, Proposições 13–15).
