# Análise Espectral de Primos via Produtos de Intervalos Binários

**T. Bandeira · 2026**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20666130.svg)](https://doi.org/10.5281/zenodo.24546064)

Repositório de uma investigação sobre a representação espectral da aritmética
elementar: o que acontece quando se olha para os primos como frequências. Contém
o artigo final, o código que produziu cada figura, as notas de percurso e uma
formalização em Lean 4 dos resultados aritméticos. Todo o conteúdo está também
arquivado no Zenodo, sob o DOI acima.

---

## O que tem aqui

| pasta | conteúdo |
|---|---|
| [`artigo/`](artigo/) | **o artigo**: [`artigo.pdf`](artigo/artigo.pdf) (30 pp), fonte LaTeX, figuras vetoriais e os scripts que as geram |
| [`formalizacao/`](formalizacao/) | demonstrações em Lean 4 (Mathlib), sem `sorry` — ver o [`README`](formalizacao/README.md) para compilar |
| [`codigo/`](codigo/) | o extrator espectral original: pipeline de dois estágios sobre `Q(p)` |
| [`notas/`](notas/) | 27 arquivos: as notas 16–40 e a metodologia |
| [`notebooks/`](notebooks/) | 31 notebooks com os experimentos, incluindo os que não deram certo |

## O artigo

**Uma representação espectral da aritmética: primos, compostos e crivos em
frequência** — [`artigo/artigo.pdf`](artigo/artigo.pdf).

Autocontido: não cita as notas, e todos os resultados que usa estão demonstrados
nele. Constrói um dicionário entre a aritmética multiplicativa e a reta real —
produto vira soma, suavidade vira pertencer a um reticulado, primalidade vira
irredutibilidade — e desenha o crivo em frequência.

A tese, em uma frase: a irredutibilidade de um inteiro é fielmente representável
no espectro, e o custo de ler essa representação é explícito e mensurável.

### Principais resultados

- **Teorema 2.7** — um inteiro pode ser escrito como combinação inteira de
  logaritmos de primos menores se, e somente se, é composto.
- **Lema 3.2 e Teorema 3.3** — todo composto do bloco `A_k = [2^k, 2^{k+1})` tem
  um fator primo abaixo de `2^k`. Logo o bloco anterior é a base canônica para
  classificar o seguinte, e o crivo se torna uma recursão.
- **Teoremas 4.2 e 4.4** — a geometria exata do reticulado: para todo primo `q`
  de um bloco, a distância relativa de `log q` ao reticulado gerado pelos primos
  menores vale **exatamente** `log(1+1/q)/log q`. A margem de classificação é
  `ρ_min(k) = log(1+1/q_max)/log q_max ~ 1/(q log q)`, atingida no maior primo do
  bloco.
- **Teorema 6.4** — a janela de observação necessária para desenhar um bloco é
  `τ(Seed_k) = Θ(2^k/k)`, por casa de pombos sobre os gaps da semente (sem
  depender da conjectura de primos gêmeos). No nível local, `Θ(q)`.
- **Proposição 6.6** — critério da janela de leitura: `2W+1 < T/(πq)`.
- **Proposição 7.2** — contagem coerente: `k` candidatos com o mesmo núcleo
  somam exatamente `k` vezes o mesmo cosseno, de modo que a altura de um pico é
  uma contagem inteira.
- **Proposição 8.1** — a assinatura de um par: sinal `1` contra fundo `O(q/T)`.

O Apêndice A do artigo traz os enunciados das oito declarações verificadas em
Lean 4; o Apêndice B, os dados numéricos completos.

## Como reproduzir

```bash
pip install numpy matplotlib

python artigo/experimentos/figuras_artigo.py       # as 6 figuras (PDF), ~8 min
python artigo/experimentos/verificar_teoremas.py   # tabelas e verificações, ~2 min

cd artigo && pdflatex --enable-installer artigo.tex  # duas vezes
cd formalizacao && lake exe cache get && lake build  # Lean 4 + Mathlib
```

Nenhum cálculo usa amostragem aleatória; os valores das tabelas são reprodutíveis
em precisão dupla.

## O percurso

As notas (16–40) registram a investigação como ela aconteceu, incluindo as
tentativas que não funcionaram: o pipeline espectral com ζ, o detector contínuo
`ρ`, a hipótese de detectar fatores por ressonância. O algoritmo aritmético que
sobrou é a divisão de tentativas organizada por blocos — mesma ordem
assintótica, `O(p√p/log p)`, com a base montada por indução; medições da Nota 29
indicam constante menor que a da divisão ingênua.

[`artigo/auditoria-e-correcoes.md`](artigo/auditoria-e-correcoes.md) confronta as
notas com os cálculos e registra três correções: a lei de `T_max` é **linear** em
`p` e não superlinear; a rota via formas lineares de Baker é desnecessária (a
cota correta é elementar); e os "80,1% de acurácia" do detector contínuo medem
incompletude da busca, não sobreposição geométrica.

## Validação do algoritmo

A extração por blocos devolve exatamente os primos abaixo de `p`, sem oráculo
externo, para toda a faixa testada:

| `p` | primos `< p` | recuperados |
|---|---|---|
| 131 | 31 | 31 |
| 503 | 95 | 95 |
| 1 009 | 168 | 168 |
| 2 003 | 303 | 303 |
| 8 009 | 1 007 | 1 007 |
| 16 381 | 1 899 | 1 899 |

## Questões abertas

1. **A constante da assinatura de gêmeos.** A Proposição 8.1 dá a ordem `q/T`;
   o fator entre essa ordem e o máximo medido (da ordem de 1,8) não foi
   determinado — exigiria controlar a interferência conjunta de todos os primos
   do sinal, não só do vizinho imediato.
2. **Outras bases.** Para base `b > 2` vale o análogo da cota, mas não sabemos se
   vale o valor exato do Teorema 4.4: quando `q` não é ímpar, o vizinho `q+1`
   deixa de estar garantidamente no reticulado.
3. **Órbitas e a função de Dickman.** O tamanho da órbita é o objeto da teoria de
   números suaves; a representação espectral dá a `Ψ(X, y)` uma leitura local
   (altura do pico), mas a conexão não foi formalizada.
4. **Cascata além da profundidade 3.** O detector em lote da Nota 37–38 desce a
   árvore de fatores por níveis; profundidade `≥ 4` exige janela maior.
5. **Universalidade da assinatura.** Verificada até `p ≤ 299`; escalas maiores
   com `T` proporcional a `p` continuam não testadas.

## Citação

```bibtex
@misc{bandeira2026espectral,
  author = {T. Bandeira},
  title = {Análise Espectral de Primos via Produtos de Intervalos Binários},
  year = {2026},
  doi = {10.5281/zenodo.20674285}
}
```

Para citar o artigo em si:

```bibtex
@misc{bandeira2026representacao,
  author = {T. Bandeira},
  title = {Uma representação espectral da aritmética: primos, compostos e
           crivos em frequência},
  year = {2026}
}
```

## Licença

- Documentação e notas: [CC BY 4.0](LICENSE.txt)
- Código-fonte: [MIT License](LICENSE-MIT.txt)
