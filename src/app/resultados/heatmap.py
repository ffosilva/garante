import numpy as np
import matplotlib.pyplot as plt

from resultados.resultado import CachedResultadosClient, Resultado
from core.posicao import posicao

# Generate random data points for demonstration
data_points = []  # Normal distribution


client = CachedResultadosClient('lotofacil')
ultimo_concurso = 2811
ultimo_concurso = client.get_resultado().concurso
print(ultimo_concurso)
for i in range(1, ultimo_concurso + 1):
    resultado = client.get_resultado(i)
    print(resultado)
    print(posicao(resultado, 25))
    data_points.append(posicao(resultado, 25))

# Create a histogram heatmap
bins = 25  # Number of bins for the histogram
counts, bin_edges = np.histogram(sorted(data_points), bins=bins)

# Create the heatmap
plt.figure(figsize=(20, 8))
plt.imshow(counts[np.newaxis, :], cmap='hot', aspect='auto', extent=[bin_edges[0], bin_edges[-1], 0, 1])

# Customize the axis and labels
# plt.colorbar(label='Density')
# plt.xlabel('Value')
# plt.title('1D Heatmap of Data Points')
# plt.yticks([])  # Remove y-axis ticks

bin_labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges) - 1)]
plt.xticks(ticks=np.linspace(bin_edges[0], bin_edges[-1], len(bin_labels)), labels=bin_labels, rotation=45, ha='right')
plt.colorbar(label='Density')
plt.xlabel('Value Intervals')
plt.title('1D Heatmap with Bin Intervals')
plt.yticks([])  # Remove y-axis ticks
plt.tight_layout()



plt.savefig("heatmap_mega.png")  # Save the figure to a file
print("Heatmap saved as 'heatmap.png'")
