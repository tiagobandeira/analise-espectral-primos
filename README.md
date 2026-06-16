# Análise Espectral de Primos via Produtos de Intervalos Binários

**T. Bandeira · 2026**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20666130.svg)](https://doi.org/10.5281/zenodo.20674285)

---

## Resultado central

A partir da análise espectral do produto $Q(p) = \prod_{x=2^{n-1}}^{p-1} x$ (bloco binário), descobriu-se uma caracterização puramente aritmética de primalidade: **um inteiro $m$ é primo se e somente se seu logaritmo $\log m$ não pode ser escrito como combinação linear inteira dos logaritmos de primos menores**. Este critério, denominado *irredutibilidade logarítmica*, é geometricamente exato e independe de qualquer oráculo externo.

O método resultante é um crivo autônomo de dois estágios:

1. **Recursão sobre blocos binários** – constrói todos os primos menores que $2^{n-1}$ usando apenas divisibilidade e os primos já encontrados (indutivamente).
2. **Classificação do bloco $[2^{n-1}, p-1]$** – cada candidato é testado por divisibilidade pelos primos obtidos na etapa 1. A correção é garantida pelo Teorema 1 da Nota MDC: todo composto no bloco tem seu menor fator primo em $\mathcal{P_<}$ (conjunto dos primos $< 2^{n-1}$).

Nenhuma dependência externa é necessária: sem $\zeta(s)$, sem `isprime()`, sem lista prévia de primos.

---
> **Descoberta recente (Nota 33):** Com resolução espectral suficiente (`T_max = 6500` para primos até 299), a amplitude normalizada em `f_{p+2}` separa completamente pares gêmeos de pares mistos (acurácia 100%, 62/62, Mann‑Whitney p < 10⁻¹⁰). Para `T_max` fixo (1500), a acurácia cai para 51,6% – indistinguível do acaso. O resultado confirma que a irredutibilidade logarítmica de primos se manifesta localmente no espectro e que a resolução espectral é o gargalo determinante.

## Evolução teórica

A análise de $\log|Z_Q(\frac12+it)|$ mostrou que picos da FFT nas frequências $\frac{\log q}{2\pi}$ correspondem a primos $q$. O conceito de *irredutibilidade logarítmica* formalizou a separação primo/composto (Nota 21). Com a introdução do critério contínuo $\rho(m)$ (distância de $\log m$ ao reticulado gerado por primos menores), atingiu-se 80% de acurácia sem aritmética inteira (Nota 19). A versão adaptativa $\rho_{\text{adapt}}$ provou a equivalência completa com o teste de divisibilidade, mostrando que a aritmética inteira é o algoritmo ótimo para implementar o critério (Nota 26). Por fim, determinou-se a cota assintótica $\rho_{\min}(k) \sim 1/(2^{k+1}(k+1)\log 2)$, que permite ajustar o limiar de classificação para qualquer escala (Nota 27).

---

## Algoritmo final

```python
def extrair_primos(p):
    n = floor(log2(p))
    # Etapa A: constrói primos < 2^(n-1)
    P_less = []
    for m in range(2, 2**(n-1)):
        primo = True
        for b in P_less:
            if b*b > m: break
            if m % b == 0: primo = False; break
        if primo: P_less.append(m)
    # Etapa B: classifica bloco [2^(n-1), p-1]
    primos_bloco = []
    for m in range(2**(n-1), p):
        primo = True
        for b in P_less:
            if b*b > m: break
            if m % b == 0: primo = False; break
        if primo: primos_bloco.append(m)
    return P_less + primos_bloco
```

Complexidade: $O(p\sqrt{p}/\log p)$ – mesma ordem da divisão de tentativas, mas com constante melhor devido à estrutura de blocos (ganho de 2× a 6× na prática).

---

## Validação

Testado para $p$ até 1009 com 100% de acurácia (0 falsos positivos, 0 falsos negativos), em contraste com as versões espectrais anteriores que perdiam primos por resolução finita de $t_{\max}$.

| $p$   | Primos reais | Detectados | Taxa  |
|-------|--------------|------------|-------|
| 67    | 18           | 18         | 100%  |
| 131   | 31           | 31         | 100%  |
| 257   | 54           | 54         | 100%  |
| 503   | 95           | 95         | 100%  |
| 1009  | 168          | 168        | 100%  |

---

## Papel da teoria espectral

O percurso espectral não foi um desvio, mas a ferramenta que revelou a estrutura de blocos binários, o critério de irredutibilidade logarítmica e a justificativa formal para os parâmetros do algoritmo. Sem ele, não haveria motivo para adotar a partição em blocos $A_k = [2^k, 2^{k+1}-1]$ nem prova de que $\mathcal{P_<}$ é a base exata para classificar o bloco. A FFT e $t_{\max}$ foram substituídas por aritmética onde eram ineficientes, mas a teoria permaneceu.

---

## Questões abertas

> 1. **Lei de escala de `T_max` para classificação de pares.** A separação perfeita entre gêmeos e mistos exige `T_max` muito maior que `π p`. Experimentos indicam crescimento mais rápido que linear (`T_max = 6500` para `p ≤ 299`). A caracterização analítica dessa escala permanece em aberto.
> 2. **Detecção de fatores por ressonância espectral** – sem divisibilidade, seria possível identificar fatores comuns apenas pela interferência de picos? (Hipótese B, Nota 20.)
> 3. **Prova formal do padrão de `ρ_min(k)`** – o maior primo do bloco sempre realiza o menor `ρ`; observado até `k=11`, mas não provado.
> 4. **Universalidade da assinatura de gêmeos.** A separação espectral foi verificada apenas até `p ≤ 299`. Testes para primos muito maiores, com `T_max` escalado adequadamente, são necessários para confirmar a robustez do critério (Exp DD proposto).

---

## Citação

```bibtex
@misc{bandeira2026espectral,
  author = {T. Bandeira},
  title = {Análise Espectral de Primos via Produtos de Intervalos Binários},
  year = {2026},
  doi = {10.5281/zenodo.20674285}
}
```

## Licença

- Documentação e notas: [CC BY 4.0](LICENSE.txt)
- Código-fonte: [MIT License](LICENSE-MIT.txt)