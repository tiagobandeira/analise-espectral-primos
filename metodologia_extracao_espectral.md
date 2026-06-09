## A ideia central: primos deixam impressão digital no espectro

Considere a função de um inteiro $x$ avaliada em $s = \frac{1}{2} + it$:

$$\frac{1}{1 - x^{-s}}$$

O módulo quadrado desse fator é:

$$\left|1 - x^{-s}\right|^2 = 1 - 2x^{-1/2}\cos(t \log x) + x^{-1}$$

O termo $\cos(t \log x)$ **oscila em $t$ com frequência $\frac{\log x}{2\pi}$**. Quando você soma os logaritmos de muitos desses fatores e faz a FFT, cada $x$ contribui com um pico em exatamente essa frequência. Então:

$$\text{pico em } f = \frac{\log x}{2\pi} \quad \Longleftrightarrow \quad x = e^{2\pi f}$$

Essa é a inversão que o código usa: `q = round(exp(2*pi*f))`. Cada número no intervalo deixa uma "impressão digital" espectral na frequência $\log(x)/(2\pi)$. Primos têm frequências irracionais entre si, o que os torna distinguíveis.

---

## O que é $Z_Q(s)$

Para o intervalo $Q(p) = [2^{n-1}, p-1]$ define-se:

$$Z_Q(s) = \prod_{x=2^{n-1}}^{p-1} \frac{1}{1 - x^{-s}}$$

O logaritmo do módulo em $s = \frac{1}{2}+it$ é o que o código calcula como `log_modZ`:

$$\log|Z_Q| = -\frac{1}{2} \sum_{x} \log\!\left(1 - 2x^{-1/2}\cos(t\log x) + x^{-1}\right)$$

O sinal inteiro como função de $t$ é uma **superposição de oscilações** — uma por cada $x$ no intervalo. A FFT decompõe essa superposição e identifica quais frequências estão presentes, ou seja, quais $x$ contribuem com sinal forte.

---

## Por que o intervalo $[2^{n-1}, p-1]$ e não outro?

Vem do **Teorema 1** do manuscrito `primalidade-mdc-blocos-binarios`. Para $p \in [2^n, 2^{n+1}-1]$, o intervalo $A_{\lfloor n/2 \rfloor} = [2^{n-1}, 2^n - 1]$ já contém todos os menores fatores primos de qualquer composto em $[2^n, 2^{n+1}-1]$. O produto $Q(p)$ herda essa estrutura: todos os primos $< p$ dividem algum elemento de $[2^{n-1}, p-1]$.

---

## O problema do método original: cancelamento

O método original usava $R(t) = \log|Z_Q/\zeta|$. Mas $\zeta(s) = \prod_p (1-p^{-s})^{-1}$ inclui *todos* os primos. Os primos que estão diretamente no intervalo — para $p=37$, são $\{17,19,23,29,31\}$ — aparecem em $Z_Q$ como fatores individuais **e** em $\zeta$. A divisão os cancela.

O que sobrava eram apenas os primos $< 16$, que aparecem indiretamente via múltiplos compostos (ex: $2$ via $16, 18, 20, \ldots$; $13$ via $26$).

---

## O pipeline de dois estágios

O insight é que os dois grupos de primos — dentro e fora do intervalo — precisam de referências diferentes para ficar visíveis.

### Etapa 1 — primos dentro de $[2^{n-1}, p-1]$

$$R_1(t) = \log|Z_Q| - \log|Z_{\text{compostos}}|$$

$Z_{\text{compostos}}$ é o produto apenas sobre os $x$ compostos do intervalo. Subtraindo:

- A contribuição de cada composto $x$ cancela com seu próprio fator em $Z_Q$
- O que sobra são **somente os fatores dos primos** do intervalo
- Cada primo $q \in [2^{n-1}, p-1]$ aparece como pico limpo em $\log(q)/(2\pi)$

Para $p=37$: o intervalo tem $\{16,17,18,\ldots,36\}$. Os compostos $\{16,18,20,21,\ldots\}$ se cancelam. Sobram os primos $\{17,19,23,29,31\}$ — exatamente o que a Etapa 1 encontra.

### Etapa 2 — primos fora do intervalo ($< 2^{n-1}$)

Agora que os primos grandes foram identificados na Etapa 1, pode-se removê-los manualmente:

$$R_2(t) = \log|Z_Q| - \log|\zeta| - \log|Z_{\text{primos\_dentro}}|$$

- $\log|\zeta|$ remove a contribuição global de todos os primos
- $\log|Z_{\text{primos\_dentro}}|$ *devolve* a contribuição dos primos grandes (que $\zeta$ removeu a mais)
- O resultado líquido: cancela compostos via $\zeta$, preserva a assinatura indireta dos primos pequenos via seus múltiplos

Para $p=37$: $\zeta$ remove tudo, o termo $Z_{\{17,19,23,29,31\}}$ devolve esses cinco, e o que fica são as oscilações dos compostos $\{16,18,20,\ldots\}$ — que carregam as frequências de seus fatores $\{2,3,5,7,11,13\}$.

### União

$$\text{primos}(p) = \underbrace{\{17,19,23,29,31\}}_{\text{Etapa 1}} \cup \underbrace{\{2,3,5,7,11,13\}}_{\text{Etapa 2}} = \{2,3,5,7,11,13,17,19,23,29,31\}$$

---

## O papel da resolução espectral

A resolução da FFT é $\Delta f = 1/(N \cdot \Delta t)$. Com 14995 amostras e $\Delta t = 0.02$:

$$\Delta f = \frac{1}{14995 \times 0.02} \approx 0.00334$$

Para separar dois primos $q_1 < q_2$, precisa-se que:

$$\frac{\log q_2 - \log q_1}{2\pi} > \Delta f$$

O par mais difícil no caso $p=53$ é $(43, 47)$: gap $= \frac{\log 47 - \log 43}{2\pi} \approx 0.014$, que é $4\times$ a resolução — suficiente para separar. É por isso que $p=53$ falhava com $t_{\max}=200$ (resolução pior) e passa com $t_{\max}=300$.

---

## Resumo visual do fluxo

```
Q(p) = [start, p-1]
       ├── primos do intervalo: {17, 19, 23, 29, 31}   ─┐
       └── compostos          : {16, 18, 20, ...}        │
                                    │                     │
              Z_compostos ──────────┘ (cancela)           │
                                                          ▼
    R1 = log|Z_Q / Z_compostos|  ──FFT──►  {17,19,23,29,31}  ✓ Etapa 1

              ζ  ──────────────────────── (cancela tudo)
              Z_{17,19,23,29,31} ──────── (devolve os grandes)
                                    │
    R2 = log|Z_Q / ζ / Z_pd|  ──FFT──►  {2,3,5,7,11,13}     ✓ Etapa 2

    União → todos os primos < p                               ✓
```

O método não usa nenhum crivo nem lista de primos conhecidos — apenas produtos de inteiros consecutivos, a função zeta, e FFT.