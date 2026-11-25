#!/usr/bin/env python3
"""
experimentos_espectrais.py -- os experimentos que sustentam o artigo.

E1  Impressao digital espectral de Z_Q e colapso por resolucao (p = 37).
E2  Custo exponencial de t_max: par gemeo gargalo em P_<, t_min ~ pi * q_twin.
E3  rho_min(k): valor exato vs cota 1/(2^(k+1)(k+1)log2); cruzamento de 1e-6.
E4  Lei do ganho orbital e detector de fator comum em lote (exatidao).
E5  Assinatura de gemeos: coeficiente de Fourier exato vs FFT retangular.

Saida: figuras/*.png e resultados.json
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

FIG = Path(__file__).resolve().parents[1] / "figuras"
FIG.mkdir(parents=True, exist_ok=True)
LOG2 = math.log(2.0)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9,
    "axes.grid": True, "grid.alpha": 0.25, "axes.spines.top": False,
    "axes.spines.right": False, "figure.autolayout": True,
})

RES = {}


# ------------------------------------------------------------------ utilidades
def sieve(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return s


def primes_upto(n):
    return np.nonzero(sieve(n))[0]


def log_modZ(xs, t):
    """log|Z(1/2+it)| para Z(s) = prod_{x em xs} (1-x^-s)^-1."""
    xs = np.asarray(xs, dtype=float)
    if xs.size == 0:
        return np.zeros_like(t)
    lx = np.log(xs)
    a = np.exp(-0.5 * lx)
    theta = np.outer(t, lx)
    term = 1.0 - 2.0 * a[None, :] * np.cos(theta) + (a * a)[None, :]
    return -0.5 * np.log(np.maximum(term, 1e-300)).sum(axis=1)


def picos(amp, freq, fmin, fmax, altura_rel=0.05, dist=3):
    m = (freq >= fmin) & (freq <= fmax)
    a, f = amp[m], freq[m]
    if a.size == 0:
        return []
    lim = a.max() * altura_rel
    idx = [i for i in range(1, len(a) - 1)
           if a[i] >= lim and a[i] >= a[i - 1] and a[i] >= a[i + 1]]
    out = []
    for i in sorted(idx, key=lambda j: -a[j]):
        if all(abs(i - j) > dist for j in out):
            out.append(i)
    return sorted(int(round(math.exp(2 * math.pi * f[i]))) for i in out)


# ------------------------------------------------------------------ E1
def E1_impressao_digital():
    """Espectro de log|Z_Q| para p = 37: picos nos primos do bloco."""
    p = 37
    n = p.bit_length() - 1
    ini = 2 ** (n - 1)
    xs = np.arange(ini, p)
    isp = sieve(p)
    xs_c = np.array([x for x in xs if not isp[x]])
    xs_p = np.array([x for x in xs if isp[x]])

    fig, ax = plt.subplots(2, 2, figsize=(10.5, 6.0))

    for col, (tmax, dt) in enumerate([(150.0, 0.05), (300.0, 0.02)]):
        t = np.arange(0.1, tmax, dt)
        Z = log_modZ(xs, t)
        Zc = log_modZ(xs_c, t)
        R = Z - Zc
        R = R - R.mean()
        amp = np.abs(np.fft.rfft(R))
        freq = np.fft.rfftfreq(len(R), d=dt)
        df = 1.0 / (len(R) * dt)

        fmin = math.log(ini) / (2 * math.pi) - 0.05
        fmax = math.log(p) / (2 * math.pi) + 0.05
        for axx, (sig, tit) in zip(ax[col], [(Z, r"$\log|Z_Q|$ (todos os $x$)"),
                                             (R, r"$\log|Z_Q|-\log|Z_{\mathrm{comp}}|$")]):
            s = sig - sig.mean()
            A = np.abs(np.fft.rfft(s))
            axx.plot(freq, A / A.max(), lw=0.8, color="0.35")
            for q in xs_p:
                axx.axvline(math.log(q) / (2 * math.pi), color="crimson", lw=0.8,
                            ls="--", alpha=0.7)
                axx.text(math.log(q) / (2 * math.pi), 1.02, str(q), rotation=90,
                         ha="center", va="bottom", fontsize=8, color="crimson")
            axx.set_xlim(fmin, fmax)
            axx.set_ylim(0, 1.25)
            axx.set_title(f"{tit}  ($t_{{\\max}}={tmax:g}$, $\\Delta f={df:.4f}$)", fontsize=9)
            axx.set_xlabel("$f=\\log x/2\\pi$")
            axx.set_ylabel("amplitude normalizada")

        cand = picos(amp, freq, fmin, fmax, altura_rel=0.03, dist=2)
        RES.setdefault("E1", {})[f"tmax={tmax}"] = {
            "candidatos": cand,
            "primos_no_bloco": [int(q) for q in xs_p],
            "recuperados": [q for q in cand if q in set(int(x) for x in xs_p)],
            "df": df,
        }
        print(f"E1 tmax={tmax}: candidatos={cand} primos={[int(q) for q in xs_p]}")

    fig.suptitle(r"E1 — Impressão digital espectral do bloco $[16,36]$ de $Q(37)$",
                 fontsize=10)
    fig.savefig(FIG / "e1_impressao_digital.png", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ E2
def E2_custo_tmax():
    """t_min de Rayleigh para o par gargalo de P_<: crescimento ~ 2^n."""
    ns, tmin, qtwin, piqt, pares = [], [], [], [], []
    for n in range(4, 23):
        lim = 2 ** (n - 1)
        ps = primes_upto(lim - 1)
        ps = ps[ps >= 2]
        melhor, par = 0.0, (None, None)
        for a, b in zip(ps[:-1], ps[1:]):
            tt = 2 * math.pi / (math.log(b) - math.log(a))
            if tt > melhor:
                melhor, par = tt, (int(a), int(b))
        ns.append(n)
        tmin.append(melhor)
        qtwin.append(par[1])
        piqt.append(math.pi * par[1])
        pares.append(par)
        if n <= 14:
            print(f"E2 n={n}: par={par} t_min={melhor:.1f} pi*q={math.pi * par[1]:.1f}")

    RES["E2"] = {"n": ns, "t_min": tmin, "q_twin": qtwin, "pi_q": piqt,
                 "pares": pares, "razao": [a / b for a, b in zip(tmin, piqt)]}

    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.8))
    ax[0].semilogy(ns, tmin, "o-", ms=4,
                   label=r"$t_{\min}=2\pi/\log(q_2/q_1)$ (par gargalo)")
    ax[0].semilogy(ns, piqt, "--", lw=1, label=r"$\pi\,q_{\mathrm{twin}}$")
    ax[0].semilogy(ns, [math.pi * 2 ** (n - 2) for n in ns], ":", lw=1,
                   label=r"$\pi\,2^{n-2}$")
    ax[0].set_xlabel(r"$n$  (semente $[2^{n-2},2^{n-1}-1]$)")
    ax[0].set_ylabel(r"$t_{\max}$ necessário")
    ax[0].set_title(r"(a) o custo espectral cresce como $2^n$")
    ax[0].legend(fontsize=8)

    ax[1].plot(ns, RES["E2"]["razao"], "o-", ms=4, color="crimson")
    ax[1].axhline(1, color="0.5", lw=0.8)
    ax[1].set_xlabel("$n$")
    ax[1].set_ylabel(r"$t_{\min}/(\pi q_{\mathrm{twin}})$")
    ax[1].set_title(r"(b) convergência para a lei $t_{\max}\approx\pi q_{\mathrm{twin}}$")
    ax[1].set_ylim(0.9, 1.02)
    fig.suptitle("E2 — Por que a etapa espectral não escala", fontsize=10)
    fig.savefig(FIG / "e2_custo_tmax.png", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ E3
def E3_rho_min():
    """rho(q) = log(1+1/q)/log q exato; rho_min em q_max; cruzamento do limiar.

    Usa o Lema 4: para 2 <= m <= 2^(k+1), ser S_k-suave equivale a ser composto
    ou estar abaixo de 2^k. Verificado por crivo ate k = 22.
    """
    ks, med, cota, viz, verif = [], [], [], [], []
    for k in range(2, 23):
        lim = 2 ** (k + 1)
        isp = sieve(lim)
        idx = np.arange(lim + 1)
        suave = (idx < 2 ** k) | (~isp)
        suave[0] = suave[1] = False
        qs = np.nonzero(isp[2 ** k:lim])[0] + 2 ** k
        ok_viz = bool(np.all(suave[qs + 1]) and np.all(suave[qs - 1]))
        ok_mais = bool(np.all(np.abs(np.log(qs + 1) - np.log(qs))
                              <= np.abs(np.log(qs) - np.log(qs - 1))))
        rho = np.log1p(1.0 / qs) / np.log(qs)
        qmax = int(qs.max())
        ks.append(k)
        med.append(float(rho.min()))
        cota.append(1.0 / (2 ** (k + 1) * (k + 1) * LOG2))
        viz.append(int(qs[int(np.argmin(rho))]))
        verif.append({"k": k, "vizinhos_suaves": ok_viz, "q+1_mais_perto": ok_mais,
                      "argmin_e_qmax": viz[-1] == qmax})
        if k <= 18:
            print(f"E3 k={k:2d} q_max={qmax:7d} rho_min={med[-1]:.4e} "
                  f"cota={cota[-1]:.4e} razao={med[-1] / cota[-1]:.6f} "
                  f"argmin={viz[-1]}")

    kcruz = next(k for k in range(2, 60) if 1.0 / (2 ** (k + 1) * (k + 1) * LOG2) < 1e-6)
    tabela = []
    for k in range(2, 25):
        lim = 2 ** (k + 1)
        isp = sieve(lim)
        qmax = int(np.nonzero(isp[2 ** k:lim])[0][-1] + 2 ** k)
        tabela.append({"k": k, "q_max": qmax,
                       "rho_min": math.log1p(1.0 / qmax) / math.log(qmax),
                       "cota": 1.0 / (2 ** (k + 1) * (k + 1) * LOG2)})

    tudo_ok = all(v["vizinhos_suaves"] and v["q+1_mais_perto"] and v["argmin_e_qmax"]
                  for v in verif)
    print("E3 verificacao estrutural (k = 2..22):", tudo_ok)
    RES["E3"] = {"k": ks, "rho_min": med, "cota": cota, "argmin": viz,
                 "verificacao": verif, "tabela": tabela, "tudo_ok": tudo_ok,
                 "k_cruzamento_1e-6": kcruz,
                 "cota_cruzamento_1e-6": 1.0 / (2 ** (kcruz + 1) * (kcruz + 1) * LOG2)}

    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.9))
    razao = [a / b for a, b in zip(med, cota)]
    ax[0].plot(ks, razao, "o-", ms=4,
               label=r"$\rho_{\min}(k)$ / cota $2^{-(k+1)}/((k+1)\log 2)$")
    ax[0].plot([t["k"] for t in tabela],
               [t["rho_min"] * t["q_max"] * math.log(t["q_max"]) for t in tabela],
               "s--", ms=3.5, lw=1,
               label=r"$\rho_{\min}(k)$ / $(1/(q_{\max}\log q_{\max}))$")
    ax[0].axhline(1, color="0.4", lw=0.8)
    ax[0].set_xlabel("$k$")
    ax[0].set_ylabel("razão para a cota")
    ax[0].set_title("(a) a cota é justa: razão tende a 1")
    ax[0].legend(fontsize=7)

    ax[1].semilogy([t["k"] for t in tabela], [t["cota"] for t in tabela], "--",
                   lw=1, label="cota")
    ax[1].semilogy([t["k"] for t in tabela], [t["rho_min"] for t in tabela], "o",
                   ms=3.5, label=r"$\rho_{\min}(k)$ exato")
    ax[1].axhline(1e-6, color="crimson", lw=1, label=r"$\rho^\ast=10^{-6}$")
    ax[1].axvline(kcruz, color="0.4", ls=":", lw=1)
    ax[1].annotate(f"$k={kcruz}$:\no limiar fixo\ndeixa de valer", (kcruz - 0.4, 3e-4),
                   fontsize=8, ha="right", color="0.25")
    ax[1].set_xlabel("$k$")
    ax[1].set_title("(b) colapso do limiar fixo")
    ax[1].legend(fontsize=8)
    fig.suptitle(r"E3 — $\rho_{\min}(k)$ exato, e a validade do limiar $10^{-6}$",
                 fontsize=10)
    fig.savefig(FIG / "e3_rho_min.png", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ E4
def E4_ganho_orbital():
    """Lei do ganho orbital e detector de fator comum em lote."""
    T, dt = 6500.0, 0.0005
    t = np.arange(0.1, T, dt)
    N = len(t)
    df = 1.0 / (N * dt)

    def sinal(freqs_log):
        s = np.zeros(N)
        for lg in freqs_log:
            s += -np.cos(t * lg) / math.sqrt(lg)
        return s

    def amp(sig, q, W=8):
        S = np.abs(np.fft.rfft(sig - sig.mean()))
        k0 = int(round((math.log(q) / (2 * math.pi)) / df))
        lo, hi = max(0, k0 - W), min(len(S), k0 + W + 1)
        return float(S[lo:hi].max())

    base = [2, 3, 5, 7]

    def nucleo(m):
        r, acc = m, 0.0
        for b in base:
            while r % b == 0:
                r //= b
                acc += math.log(b)
        return math.log(m) - acc

    cal = {q: amp(sinal([math.log(q)]), q) for q in [11, 13, 17, 19, 23, 29, 37]}

    cand11 = []
    for m in range(2, 4000):
        r = m
        for b in base:
            while r % b == 0:
                r //= b
        if r == 11:
            cand11.append(m)
        if len(cand11) == 7:
            break
    cresc = []
    for k in range(1, 8):
        a = amp(sinal([nucleo(m) for m in cand11[:k]]), 11)
        cresc.append({"k": k, "amp": a, "razao": a / cal[11],
                      "razao_por_k": a / cal[11] / k})
        print(f"E4 ganho k={k}: razao={a / cal[11]:.5f} razao/k={a / cal[11] / k:.6f}")

    lote = [22, 33, 44, 55, 77, 110, 154, 26, 39, 52, 65, 91, 34, 46, 58, 74]
    sig = sinal([nucleo(m) for m in lote])
    det = {q: amp(sig, q) / cal[q] for q in [11, 13, 17, 23, 29, 37]}
    contagem = {11: 7, 13: 5, 17: 1, 23: 1, 29: 1, 37: 1}
    print("E4 detector (razao medida):", {q: round(v, 4) for q, v in det.items()})
    RES["E4"] = {"calibracao": cal, "crescimento": cresc, "cand11": cand11,
                 "detector": {"razoes": det, "contagem_real": contagem, "lote": lote}}

    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.8))
    kk = [c["k"] for c in cresc]
    ax[0].plot(kk, [c["razao"] for c in cresc], "o", ms=5, label="razão medida")
    ax[0].plot(kk, kk, "-", lw=1, color="crimson", label="$k$ (ganho orbital)")
    ax[0].set_xlabel("$k$ candidatos com o mesmo núcleo 11")
    ax[0].set_ylabel(r"$\mathrm{amp}(f_{11})/\mathrm{amp}_{\mathrm{iso}}(11)$")
    ax[0].set_title("(a) ganho orbital: exato em $k$")
    ax[0].legend(fontsize=8)

    qs = [11, 13, 17, 23, 29, 37]
    cores = ["crimson", "crimson"] + ["0.6"] * 4
    ax[1].bar([str(q) for q in qs], [det[q] for q in qs], color=cores)
    ax[1].axhline(1.8, color="k", ls="--", lw=1, label="limiar 1,8")
    for i, q in enumerate(qs):
        ax[1].text(i, det[q] + 0.08, f"{det[q]:.3f}", ha="center", fontsize=7)
    ax[1].set_xlabel(r"cofator testado $q$")
    ax[1].set_ylabel("razão = contagem")
    ax[1].set_title("(b) detector cego de fator comum (16 candidatos)")
    ax[1].legend(fontsize=8)
    fig.suptitle("E4 — O que o espectro faz melhor: detectar fatores em lote",
                 fontsize=10)
    fig.savefig(FIG / "e4_ganho_orbital.png", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ E5
def E5_gemeos():
    """Assinatura de pares gemeos: coeficiente de Fourier exato vs FFT."""
    N0 = 300
    isp = sieve(N0)
    ps = np.array([q for q in range(2, N0 + 1) if isp[q]], dtype=float)
    w = np.log(ps)
    amp_p = 1.0 / np.sqrt(ps)

    def coef_exato(omegas, T):
        def F(a):
            a = np.asarray(a, dtype=complex)
            out = np.empty_like(a)
            small = np.abs(a) < 1e-14
            out[~small] = (np.exp(1j * a[~small] * T) - 1) / (1j * a[~small])
            out[small] = T
            return out
        A = np.zeros(len(omegas), dtype=complex)
        for i, oq in enumerate(omegas):
            A[i] = -0.5 * np.sum(amp_p * (F(w - oq) + F(-w - oq)))
        return A

    def FFT_amp(omegas, T, dt, janela=False, W=0):
        t = np.arange(0.1, T, dt)
        s = np.zeros_like(t)
        for wi, ai in zip(w, amp_p):
            s += -ai * np.cos(t * wi)
        s = s - s.mean()
        ganho = 1.0
        if janela:
            s = s * np.hanning(len(s))
            ganho = 2.0            # ganho coerente da janela de Hann
        S = np.abs(np.fft.rfft(s)) * dt * ganho
        df = 1.0 / (len(s) * dt)
        out = []
        for oq in omegas:
            k0 = int(round((oq / (2 * math.pi)) / df))
            lo, hi = max(0, k0 - W), min(len(S), k0 + W + 1)
            out.append(S[lo:hi].max())
        return np.array(out)

    pares, tipos = [], []
    for q in ps.astype(int):
        if q + 2 <= N0:
            pares.append(q)
            tipos.append("gemeo" if isp[q + 2] else "misto")
    pares = np.array(pares, dtype=float)
    tipos = np.array(tipos)
    alvo = np.log(pares + 2)
    norm = np.sqrt(pares + 2)

    linhas = []
    for T in [500.0, 1000.0, 1500.0, 3000.0, 6500.0, 12000.0]:
        ah = np.abs(coef_exato(alvo, T)) / (T / (2 * norm))
        sep = np.median(ah[tipos == "gemeo"]) - np.median(ah[tipos == "misto"])
        acc = np.mean((ah > 0.5) == (tipos == "gemeo"))
        linhas.append({"metodo": "exato", "T": T, "acuracia": float(acc), "sep": float(sep),
                       "med_gemeo": float(np.median(ah[tipos == "gemeo"])),
                       "med_misto": float(np.median(ah[tipos == "misto"])),
                       "max_misto": float(ah[tipos == "misto"].max()),
                       "min_gemeo": float(ah[tipos == "gemeo"].min())})
        print(f"E5 exato T={T:7.0f}: acc={acc:.3f} med_g={linhas[-1]['med_gemeo']:.3f} "
              f"med_m={linhas[-1]['med_misto']:.4f} max_m={linhas[-1]['max_misto']:.4f}")

    for T, dt in [(1500.0, 0.005), (6500.0, 0.002)]:
        for jan in [False, True]:
            for W in [0, 2, 10]:
                ah = FFT_amp(alvo, T, dt, janela=jan, W=W) / (T / (2 * norm))
                sep = np.median(ah[tipos == "gemeo"]) - np.median(ah[tipos == "misto"])
                acc = np.mean((ah > 0.5) == (tipos == "gemeo"))
                linhas.append({"metodo": f"fft{'_hann' if jan else ''}", "T": T, "dt": dt,
                               "W": W, "acuracia": float(acc), "sep": float(sep),
                               "med_gemeo": float(np.median(ah[tipos == "gemeo"])),
                               "med_misto": float(np.median(ah[tipos == "misto"])),
                               "max_misto": float(ah[tipos == "misto"].max()),
                               "min_gemeo": float(ah[tipos == "gemeo"].min())})
                print(f"E5 fft{'(hann)' if jan else ''} T={T:7.0f} dt={dt} W={W}: "
                      f"acc={acc:.3f} max_m={linhas[-1]['max_misto']:.4f} "
                      f"min_g={linhas[-1]['min_gemeo']:.3f}")

    RES["E5"] = {"n_pares": len(pares), "n_gemeos": int((tipos == "gemeo").sum()),
                 "linhas": linhas, "pares": pares.tolist(), "tipos": tipos.tolist()}

    ah = np.abs(coef_exato(alvo, 6500.0)) / (6500.0 / (2 * norm))
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.8))
    bins = np.linspace(0, 1.1, 45)
    ax[0].hist(ah[tipos == "gemeo"], bins=bins, alpha=0.8, label="gêmeos", color="crimson")
    ax[0].hist(ah[tipos == "misto"], bins=bins, alpha=0.8, label="mistos", color="0.45")
    ax[0].axvline(0.5, color="k", ls="--", lw=1)
    ax[0].set_xlabel(r"$\hat a_{p+2}$  (coeficiente de Fourier exato, $T=6500$)")
    ax[0].set_ylabel("contagem")
    ax[0].set_yscale("log")
    ax[0].legend(fontsize=8)
    ax[0].set_title(r"(a) separação completa, $N=300$")

    ex = [l for l in linhas if l["metodo"] == "exato"]
    ax[1].plot([l["T"] for l in ex], [l["max_misto"] for l in ex], "o-", ms=4,
               label=r"máx. dos mistos")
    ax[1].plot([l["T"] for l in ex], [l["min_gemeo"] for l in ex], "s-", ms=4,
               label=r"mín. dos gêmeos")
    xx = np.linspace(300, 14000, 400)
    ax[1].plot(xx, 300 / xx, ":", lw=1.2, color="k", label=r"$p_{\max}/T$")
    ax[1].set_xscale("log")
    ax[1].set_yscale("log")
    ax[1].set_xlabel("$T$")
    ax[1].set_ylabel(r"$\hat a_{p+2}$")
    ax[1].set_title(r"(b) o resíduo dos mistos decai como $p/T$")
    ax[1].legend(fontsize=8)
    fig.suptitle("E5 — A assinatura espectral de pares gêmeos, medida exatamente",
                 fontsize=10)
    fig.savefig(FIG / "e5_gemeos.png", bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ main
def main():
    """Uso: python experimentos_espectrais.py [e1 e2 e3 e4 e5]  (padrao: todos)."""
    sel = {a.lower() for a in sys.argv[1:]} or {"e1", "e2", "e3", "e4", "e5"}
    if "e1" in sel:
        E1_impressao_digital()
    if "e2" in sel:
        E2_custo_tmax()
    if "e3" in sel:
        E3_rho_min()
    if "e4" in sel:
        E4_ganho_orbital()
    if "e5" in sel:
        E5_gemeos()
    out = Path(__file__).resolve().parent / "resultados.json"
    anterior = {}
    if out.exists():
        anterior = json.loads(out.read_text(encoding="utf-8"))
    anterior.update(RES)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(anterior, f, indent=1, ensure_ascii=False, default=float)
    print("\nfiguras em", FIG)


if __name__ == "__main__":
    sys.exit(main())
