#!/usr/bin/env python3
"""
figuras_artigo.py -- figuras vetoriais (PDF) para o artigo em LaTeX.

Cada figura é autossuficiente: recalcula o que precisa a partir das definições
(nao depende de resultados.json nem dos notebooks). Salva em artigo/figuras/.

Uso: python figuras_artigo.py [f1 f2 f3 f4 f5]   (padrao: todas)
"""

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

# tipografia o mais proxima possivel da do artigo
plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "legend.fontsize": 7.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.grid": True,
    "grid.alpha": 0.22,
    "grid.linewidth": 0.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.constrained_layout.use": True,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

COR = "0.30"
DEST = "crimson"


def sieve(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return s


def log_modZ(xs, t):
    """log|Z(1/2+it)| com Z(s) = prod (1-x^-s)^-1."""
    xs = np.asarray(xs, dtype=float)
    if xs.size == 0:
        return np.zeros_like(t)
    lx = np.log(xs)
    a = np.exp(-0.5 * lx)
    theta = np.outer(t, lx)
    term = 1.0 - 2.0 * a[None, :] * np.cos(theta) + (a * a)[None, :]
    return -0.5 * np.log(np.maximum(term, 1e-300)).sum(axis=1)


# ---------------------------------------------------------------- F1
def f1_desenho():
    """O desenho: o bloco [16,36] antes e depois de remover os compostos."""
    p, tmax, dt = 37, 300.0, 0.02
    n = p.bit_length() - 1
    ini = 2 ** (n - 1)
    xs = np.arange(ini, p)
    isp = sieve(p)
    xs_c = np.array([x for x in xs if not isp[x]])
    xs_p = np.array([x for x in xs if isp[x]])

    t = np.arange(0.1, tmax, dt)
    Z = log_modZ(xs, t)
    R = Z - log_modZ(xs_c, t)

    fmin = math.log(ini) / (2 * math.pi) - 0.06
    fmax = math.log(p) / (2 * math.pi) + 0.06

    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5), sharey=True)
    for axx, (sig, tit) in zip(ax, [(Z, r"todos os $x\in[16,36]$"),
                                    (R, r"$Z_Q/Z_{\mathrm{comp}}$")]):
        s = sig - sig.mean()
        A = np.abs(np.fft.rfft(s))
        freq = np.fft.rfftfreq(len(s), d=dt)
        axx.plot(freq, A / A.max(), lw=0.7, color=COR)
        for q in xs_p:
            fq = math.log(q) / (2 * math.pi)
            axx.axvline(fq, color=DEST, lw=0.7, ls="--", alpha=0.75)
            axx.annotate(str(q), xy=(fq, 1.0), xytext=(fq, 1.12),
                         rotation=90, ha="center", va="bottom",
                         fontsize=8, color=DEST, annotation_clip=False)
        axx.set_xlim(fmin, fmax)
        axx.set_ylim(0, 1.30)
        axx.set_xlabel(r"frequência $f=\log x/2\pi$")
        axx.set_title(tit)
    ax[0].set_ylabel("amplitude (normalizada)")
    fig.savefig(FIG / "f1_desenho.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- F2
def f2_resolucao():
    """Duas escalas: (a) o bloco a 150 e a 300; (b) a lei de Rayleigh."""
    # (a) mesmo bloco, duas resoluções
    p = 53
    n = p.bit_length() - 1
    ini = 2 ** (n - 1)
    xs = np.arange(ini, p)
    isp = sieve(p)
    xs_c = np.array([x for x in xs if not isp[x]])
    xs_p = np.array([x for x in xs if isp[x]])
    fmin = math.log(ini) / (2 * math.pi) - 0.04
    fmax = math.log(p) / (2 * math.pi) + 0.04

    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    for axx, tmax in zip(ax, [120.0, 320.0]):
        dt = 0.02
        t = np.arange(0.1, tmax, dt)
        R = log_modZ(xs, t) - log_modZ(xs_c, t)
        s = R - R.mean()
        A = np.abs(np.fft.rfft(s))
        freq = np.fft.rfftfreq(len(s), d=dt)
        axx.plot(freq, A / A.max(), lw=0.7, color=COR)
        for q in xs_p:
            fq = math.log(q) / (2 * math.pi)
            axx.axvline(fq, color=DEST, lw=0.6, ls="--", alpha=0.7)
            axx.annotate(str(q), xy=(fq, 1.0), xytext=(fq, 1.10), rotation=90,
                         ha="center", va="bottom", fontsize=7, color=DEST,
                         annotation_clip=False)
        axx.set_xlim(fmin, fmax)
        axx.set_ylim(0, 1.28)
        df = 1.0 / (len(s) * dt)
        axx.set_title(rf"$t_{{\max}}={tmax:g}$   ($\Delta f={df:.4f}$)")
        axx.set_xlabel(r"$f$")
    ax[0].set_ylabel("amplitude (normalizada)")
    fig.savefig(FIG / "f2_resolucao.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- F3
def f3_lei():
    """A lei pi*q_gemeo: t_min do par gargalo cresce como 2^n."""
    ns, tmin, piq = [], [], []
    for n in range(4, 23):
        ps = np.nonzero(sieve(2 ** (n - 1) - 1))[0]
        ps = ps[ps >= 2]
        melhor, par = 0.0, (None, None)
        for a, b in zip(ps[:-1], ps[1:]):
            tt = 2 * math.pi / (math.log(b) - math.log(a))
            if tt > melhor:
                melhor, par = tt, (int(a), int(b))
        ns.append(n)
        tmin.append(melhor)
        piq.append(math.pi * par[1])

    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    ax[0].semilogy(ns, tmin, "o-", ms=3.2, lw=0.9, color=COR,
                   label=r"$2\pi/\log(q_2/q_1)$ (par gargalo)")
    ax[0].semilogy(ns, piq, "--", lw=0.9, color=DEST, label=r"$\pi\,q_{\rm gêmeo}$")
    ax[0].set_xlabel("$n$")
    ax[0].set_ylabel(r"$t_{\min}$")
    ax[0].legend(loc="upper left")
    ax[0].set_title("(a) a escala do desenho")

    rz = [a / b for a, b in zip(tmin, piq)]
    ax[1].plot(ns, rz, "o-", ms=3.2, lw=0.9, color=COR)
    ax[1].axhline(1, color="0.5", lw=0.7)
    ax[1].set_xlabel("$n$")
    ax[1].set_ylabel(r"$t_{\min}/(\pi q_{\rm gêmeo})$")
    ax[1].set_ylim(0.90, 1.02)
    ax[1].set_title("(b) a lei assintótica")
    fig.savefig(FIG / "f3_lei.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- F4
def f4_reticulado():
    """A geometria exata: rho(q) = log(1+1/q)/log q e a cota uniforme."""
    ks, rho, cota = [], [], []
    for k in range(2, 25):
        lim = 2 ** (k + 1)
        isp = sieve(lim)
        qmax = int(np.nonzero(isp[2 ** k:lim])[0][-1] + 2 ** k)
        ks.append(k)
        rho.append(math.log1p(1.0 / qmax) / math.log(qmax))
        cota.append(1.0 / (2 ** (k + 1) * (k + 1) * LOG2))
    rz = [a / b for a, b in zip(rho, cota)]

    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    ax[0].semilogy(ks, rho, "o", ms=3.2, color=COR, label=r"$\rho_{\min}(k)$")
    ax[0].semilogy(ks, cota, "--", lw=0.9, color=DEST,
                   label=r"$(2^{k+1}(k+1)\log 2)^{-1}$")
    ax[0].set_xlabel("$k$")
    ax[0].set_ylabel(r"$\rho$")
    ax[0].legend(loc="upper right")
    ax[0].set_title(r"(a) o valor e a cota")

    ax[1].plot(ks, rz, "o-", ms=3.2, lw=0.9, color=COR)
    ax[1].axhline(1, color="0.5", lw=0.7)
    ax[1].set_xlabel("$k$")
    ax[1].set_ylabel("razão para a cota")
    ax[1].set_ylim(0.93, 1.32)
    ax[1].set_title("(b) a cota é justa")
    fig.savefig(FIG / "f4_reticulado.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- F5
def f5_contagem():
    """Contagem coerente: razão = k, e o detector de cofator comum."""
    T, dt = 6500.0, 0.0005
    t = np.arange(0.1, T, dt)
    N = len(t)
    df = 1.0 / (N * dt)

    def sinal(freqs):
        s = np.zeros(N)
        for lg in freqs:
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

    cal = {q: amp(sinal([math.log(q)]), q) for q in [11, 13, 17, 23, 29, 37]}

    cand = []
    for m in range(2, 4000):
        r = m
        for b in base:
            while r % b == 0:
                r //= b
        if r == 11:
            cand.append(m)
        if len(cand) == 7:
            break
    razoes = []
    for k in range(1, 8):
        razoes.append(amp(sinal([nucleo(m) for m in cand[:k]]), 11) / cal[11])

    lote = [22, 33, 44, 55, 77, 110, 154, 26, 39, 52, 65, 91, 34, 46, 58, 74]
    sig = sinal([nucleo(m) for m in lote])
    det = {q: amp(sig, q) / cal[q] for q in [11, 13, 17, 23, 29, 37]}

    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    kk = list(range(1, 8))
    ax[0].plot(kk, razoes, "o", ms=4, color=COR, label="medido")
    ax[0].plot(kk, kk, "-", lw=0.9, color=DEST, label="$k$")
    ax[0].set_xlabel(r"$k$ candidatos com o mesmo núcleo")
    ax[0].set_ylabel(r"$\mathrm{amp}(f_{11})/\mathrm{amp}_{\rm iso}(11)$")
    ax[0].legend(loc="upper left")
    ax[0].set_title("(a) a contagem é exata")

    qs = [11, 13, 17, 23, 29, 37]
    cores = [DEST, DEST] + [COR] * 4
    ax[1].bar([str(q) for q in qs], [det[q] for q in qs], color=cores, width=0.62)
    ax[1].axhline(1.8, color="k", ls="--", lw=0.8)
    for i, q in enumerate(qs):
        ax[1].annotate(f"{det[q]:.2f}", xy=(i, det[q]), xytext=(0, 3),
                       textcoords="offset points", ha="center", fontsize=7)
    ax[1].set_xlabel(r"cofator testado $q$")
    ax[1].set_ylabel("razão $=$ contagem")
    ax[1].set_title("(b) dezesseis candidatos, um espectro")
    fig.savefig(FIG / "f5_contagem.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- F6
def f6_gemeos():
    """A assinatura de um par: presença do tom contra o fundo p/T."""
    N0 = 300
    isp = sieve(N0)
    ps = np.array([q for q in range(2, N0 + 1) if isp[q]], dtype=float)
    w = np.log(ps)
    am = 1.0 / np.sqrt(ps)

    def coef(omegas, T):
        def F(a):
            a = np.asarray(a, dtype=complex)
            out = np.empty_like(a)
            small = np.abs(a) < 1e-14
            out[~small] = (np.exp(1j * a[~small] * T) - 1) / (1j * a[~small])
            out[small] = T
            return out
        A = np.zeros(len(omegas), dtype=complex)
        for i, oq in enumerate(omegas):
            A[i] = -0.5 * np.sum(am * (F(w - oq) + F(-w - oq)))
        return A

    pares, tipos = [], []
    for q in ps.astype(int):
        if q + 2 <= N0:
            pares.append(q)
            tipos.append("g" if isp[q + 2] else "m")
    pares = np.array(pares, dtype=float)
    tipos = np.array(tipos)
    alvo = np.log(pares + 2)
    norm = np.sqrt(pares + 2)

    Ts = [500.0, 1000.0, 1500.0, 3000.0, 6500.0, 12000.0]
    maxm, ming = [], []
    for T in Ts:
        ah = np.abs(coef(alvo, T)) / (T / (2 * norm))
        maxm.append(float(ah[tipos == "m"].max()))
        ming.append(float(ah[tipos == "g"].min()))

    ah = np.abs(coef(alvo, 6500.0)) / (6500.0 / (2 * norm))

    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    bins = np.linspace(0, 1.06, 40)
    ax[0].hist(ah[tipos == "g"], bins=bins, alpha=0.85, color=DEST, label="gêmeos")
    ax[0].hist(ah[tipos == "m"], bins=bins, alpha=0.85, color=COR, label="mistos")
    ax[0].axvline(0.5, color="k", ls="--", lw=0.8)
    ax[0].set_yscale("log")
    ax[0].set_xlabel(r"$\hat a_{p+2}$")
    ax[0].set_ylabel("contagem")
    ax[0].legend(loc="upper center")
    ax[0].set_title(r"(a) $T=6500$, $N=300$")

    ax[1].loglog(Ts, maxm, "o-", ms=3.2, lw=0.9, color=COR, label="máx. dos mistos")
    ax[1].loglog(Ts, ming, "s-", ms=3.2, lw=0.9, color=DEST, label="mín. dos gêmeos")
    xx = np.linspace(400, 14000, 200)
    ax[1].loglog(xx, 300 / xx, ":", lw=1.0, color="k", label=r"$p/T$")
    ax[1].set_xlabel("$T$")
    ax[1].set_ylabel(r"$\hat a_{p+2}$")
    ax[1].legend(loc="lower left")
    ax[1].set_title("(b) o fundo decai como $1/T$")
    fig.savefig(FIG / "f6_gemeos.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- main
def main():
    sel = {a.lower() for a in sys.argv[1:]} or {"f1", "f2", "f3", "f4", "f5", "f6"}
    if "f1" in sel:
        f1_desenho(); print("f1 ok")
    if "f2" in sel:
        f2_resolucao(); print("f2 ok")
    if "f3" in sel:
        f3_lei(); print("f3 ok")
    if "f4" in sel:
        f4_reticulado(); print("f4 ok")
    if "f5" in sel:
        f5_contagem(); print("f5 ok")
    if "f6" in sel:
        f6_gemeos(); print("f6 ok")
    print("figuras em", FIG)


if __name__ == "__main__":
    main()
