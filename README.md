# 🌈 Iris — WebP Image Converter

Convierte imágenes (**SVG, JPG, JPEG, PNG**) a **WebP** con procesamiento en paralelo, preservando la estructura de carpetas original y con estadísticas detalladas de compresión.

## ✨ Características

- 📁 **Recursivo**: busca imágenes en todas las subcarpetas automáticamente
- 🗂️ **Preserva estructura**: mantiene el árbol de carpetas en la salida
- ⚡ **Procesamiento en paralelo**: usa múltiples hilos (`--workers`)
- 📊 **Estadísticas**: dimensiones, tamaño original vs nuevo, % de reducción
- 👁️ **Modo dry-run**: simula la conversión sin generar archivos
- ⏭️ **`--skip-existing`**: omite archivos ya convertidos
- 🎨 **Calidad configurable** (0-100)

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

> **SVG**: para convertir archivos SVG necesita `cairosvg` (opcional):
> `pip install cairosvg`

## 📖 Uso

```bash
# Básico (usa input/ y output/)
python iris.py

# Entrada personalizada
python iris.py --input ./mis_fotos

# Calidad y workers
python iris.py --input ./fotos --output ./out --quality 90 --workers 8

# Modo simulación (no convierte nada)
python iris.py --input ./fotos --dry-run

# Omitir archivos ya convertidos
python iris.py --input ./fotos --skip-existing
```

### Argumentos

| Argumento | Default | Descripción |
|-----------|---------|-------------|
| `--input, -i` | `input` | Carpeta de origen |
| `--output, -o` | `output` | Carpeta de destino |
| `--quality, -q` | `85` | Calidad WebP (0-100) |
| `--workers, -w` | `4` | Hilos en paralelo |
| `--dry-run` | off | Simula sin convertir |
| `--skip-existing` | off | Omite ya convertidos |

## 📁 Estructura

```
input/
  ├── foto1.jpg
  └── galeria/
      └── foto2.png

output/webp_conversion_20241009_123456_ab12cd34/
  ├── foto1.webp
  └── galeria/
      └── foto2.webp
```

## 🛠️ Formatos

| Entrada | Salida | Nota |
|---------|--------|------|
| SVG | WebP | requiere `cairosvg` |
| JPG/JPEG | WebP | directo |
| PNG | WebP | preserva transparencia |

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
