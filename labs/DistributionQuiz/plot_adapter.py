import io
import numpy as np
import matplotlib
matplotlib.use("Agg")  # viktigt: ingen matplotlib-popup i pygame
import matplotlib.pyplot as plt
import pygame

def make_plot_surface(data, mode="hist", size_px=(800,700), bins=40, title=""):
    w, h = size_px
    dpi = 100
    fig_w, fig_h = w / dpi, h / dpi

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

    if title:
        ax.set_title(title)

    if mode == "hist":
        ax.hist(data, bins=bins)

    elif mode == "ogive":
        hist, edges = np.histogram(data, bins=bins)
        cdf = np.cumsum(hist) / np.sum(hist)
        ax.plot(edges[1:], cdf)
        ax.set_ylim(0, 1.0)

    else:
        raise ValueError(f"Unknown mode: {mode}")

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    surf = pygame.image.load(buf, "plot.png").convert_alpha()
    return surf

def make_hist_surface(data, size_px=(800, 700), bins=40, title=""):
    return make_plot_surface(data, mode="hist", size_px=size_px, bins=bins, title=title)