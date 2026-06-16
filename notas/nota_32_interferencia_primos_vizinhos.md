# Nota 32 — Interferência Espectral entre Primos Vizinhos e Desvio do Numerador

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

O Exp X investigou o desvio do numerador $|\mathcal{F}[R_{\text{primo}}](f_p)|$
em relação à lei de escala $T_{\max}/(2\sqrt{p})$ da Nota 31. A hipótese
inicial — desvio controlado pelo gap ao vizinho via $\rho_{\min}$ da Nota 27
— não se confirmou. O resultado observado é distinto e mais rico: o desvio
é controlado pela **interferência entre primos vizinhos no espectro**.

Dentro de cada par de primos próximos $(p, p')$, um membro apresenta desvio
grande (amplitude abaixo da previsão) e o outro desvio pequeno (amplitude
próxima ou acima da previsão). A assimetria da interferência — qual dos dois
é "elevado" e qual é "suprimido" pelo vizinho — não é determinada pelo gap
aritmético mas pela posição relativa dos dois no espectro logarítmico.

A correlação com a soma residual $\epsilon_p$ é positiva ($+0.34$), confirmando
que primos com mais vizinhos espectrais influentes têm amplitude sistematicamente
elevada acima da previsão.

---

## 1. Configuração

Definições da Nota 31. Para cada primo $p \leq N$, define-se:

$$\text{desvio}_p = \frac{|\mathcal{F}[R_{\text{primo}}](f_p)| - T_{\max}/(2\sqrt{p})}{T_{\max}/(2\sqrt{p})}$$

e a soma residual dos outros primos:

$$\epsilon_p = \sum_{\substack{q \leq N \\ q \neq p,\, q \text{ primo}}}
\frac{1}{\sqrt{q}\,|\log q - \log p|}$$

Os dados abaixo foram obtidos com $N = 200$, $T_{\max} = 1500$.

---

## 2. Padrão observado: assimetria dentro dos pares

A tabela do Exp X revela um padrão sistemático nos pares de primos próximos:

| Par $(p, p')$ | desvio($p$) | desvio($p'$) | $\delta_{\min}$ |
|---|---|---|---|
| (41, 43) | $-35.1\%$ | $-2.1\%$ | 0.0476 |
| (59, 61) | $-18.8\%$ | $-21.2\%$ | 0.0333 |
| (71, 73) | $-26.1\%$ | $-10.0\%$ | 0.0278 |
| (101, 103) | $-18.6\%$ | $-17.8\%$ | 0.0196 |
| (107, 109) | $-35.2\%$ | $-0.2\%$ | 0.0185 |
| (137, 139) | $+0.4\%$ | $+1.1\%$ | 0.0145 |
| (149, 151) | $-1.9\%$ | $-1.2\%$ | 0.0133 |
| (179, 181) | $-4.4\%$ | $-3.9\%$ | 0.0111 |
| (191, 193) | $-2.9\%$ | $-2.4\%$ | 0.0104 |

Dois padrões distintos emergem:

**Pares assimétricos** (41/43, 71/73, 107/109): dentro do par, um membro
tem desvio grande ($> 25\%$) e o outro pequeno ($< 5\%$). A assimetria
sugere transferência de amplitude de um primo para o outro via interferência.

**Pares simétricos** (59/61, 101/103, 137/139, 149/151): ambos os membros
têm desvios comparáveis. A interferência é mais equilibrada.

---

## 3. Correlações

| Variável | corr com desvio | Interpretação |
|---|---|---|
| gap$_{\min}$ | $+0.085$ | Gap aritmético não prediz o desvio |
| $\delta_{\min} = \|\log q_{\text{viz}} - \log p\|$ | $-0.325$ | Primos espectralmente próximos têm desvio **menos negativo** |
| $1/\delta_{\min}$ | $-0.333$ | Confirma: proximidade espectral **eleva** amplitude |
| $\epsilon_p$ | $+0.339$ | Mais vizinhos influentes → amplitude mais elevada |
| $\delta_{\min}/\rho_{\min}(k)$ | $+0.278$ | Nota 27 não prediz o desvio |

A correlação negativa entre $\delta_{\min}$ e o desvio significa que primos
com vizinho espectral mais próximo tendem a ter desvio **menos negativo**
(amplitude acima da previsão) — efeito de interferência construtiva, não
destrutiva como a hipótese inicial previa.

---

## 4. Mecanismo: interferência construtiva entre primos próximos

A lei de escala $T_{\max}/(2\sqrt{p})$ deriva da contribuição do termo
$q = p$ na soma sobre primos. Os termos $q \neq p$ contribuem com:

$$\sum_{q \neq p} \frac{1}{\sqrt{q}} \cdot
\frac{T_{\max}}{2} \cdot \text{sinc}\!\left(\frac{(\log q - \log p)\,T_{\max}}{2\pi}\right)$$

Para dois primos gêmeos $p$ e $p' = p + 2$, a distância logarítmica é
$\delta = \log(p'/p) \approx 2/p$ — pequena para $p$ grande. O termo
sinc correspondente é:

$$\text{sinc}\!\left(\frac{2 T_{\max}}{2\pi p}\right)
\approx \frac{\pi p}{T_{\max}}$$

para $T_{\max} \gg p$. A contribuição de $p'$ ao pico de $p$ é então:

$$\frac{1}{\sqrt{p'}} \cdot \frac{T_{\max}}{2} \cdot \frac{\pi p}{T_{\max}}
= \frac{\pi p}{2\sqrt{p'}} \approx \frac{\pi\sqrt{p}}{2}$$

— da mesma ordem que o termo principal $T_{\max}/(2\sqrt{p})$ quando
$T_{\max} \sim \pi p$. Para $T_{\max} = 1500$ e $p \sim 100$, isso
representa uma correção de $\sim \pi \cdot 100/1500 \approx 20\%$ — consistente
com os desvios observados.

A assimetria dentro do par surge porque a contribuição de $p'$ ao pico de
$p$ e a contribuição de $p$ ao pico de $p'$ são iguais em magnitude mas
com fases opostas (o sinal do sinc depende do sinal de $\log q - \log p$).
Se as fases construtivamente se somam em $p$ e destrutivamente em $p'$,
obtém-se exatamente o padrão assimétrico observado.

---

## 5. Conexão com a Nota 30

Os vales estáveis de $R_{\text{primo}}$ entre os picos (Nota 30, Seção 4)
e a interferência entre primos próximos (esta nota) são o mesmo fenômeno
em duas escalas:

- **Escala local (picos):** interferência entre dois primos vizinhos modifica
  a amplitude de cada pico individualmente — esta nota.
- **Escala global (vales):** a superposição incoerente de todos os pares
  produz um nível de base estável entre os picos — Nota 30.

A regularidade dos vales é consequência da média dos efeitos de interferência
local: os desvios assimétricos dentro dos pares tendem a se cancelar em média,
produzindo um vale estável.

---

## 6. Questões em aberto

**Questão 1 — Critério de assimetria.** O que determina se um par é
assimétrico (41/43, 107/109) ou simétrico (59/61, 137/139)? A fase
relativa dos dois cossenos em $t = 0$ (determinada por $\log p \mod 2\pi$)
é uma candidata natural. Verificável numericamente.

**Questão 2 — Escala de $T_{\max}$.** O mecanismo prevê que a assimetria
dentro dos pares desaparece quando $T_{\max} \gg \pi p$ — as contribuições
cruzadas tornam-se desprezíveis. Verificável repetindo o Exp X com
$T_{\max} \gg p_{\max}$.

**Questão 3 — Primos isolados.** Primos com gap grande para ambos os
vizinhos (ex: 157 com gap 6 em ambos os lados) têm desvios pequenos
(157: $+0.9\%$). Isso é consistente com o mecanismo — sem vizinho próximo,
a interferência é fraca e a lei de escala vale com boa precisão.
Uma verificação sistemática consolidaria isso.

---

## Referências

[Nota 27] T. Bandeira, *Cota Assintótica para $\rho_{\min}(k)$* (2026).  
[Nota 30] T. Bandeira, *Dicotomia Espectral entre Primos e Compostos* (2026).  
[Nota 31] T. Bandeira, *Lei de Escala da Razão Espectral* (2026).  
[Exp X] T. Bandeira, `exp_x_desvio_numerador.ipynb` (2026).

---

*Esta nota é parte da série Motor de Herança Estrutural e está licenciada para uso acadêmico livre.*