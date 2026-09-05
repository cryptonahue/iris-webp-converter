# 🌈 Iris WebP Converter

Convierte imágenes (**SVG, JPG, JPEG, PNG**) a **WebP** con procesamiento en paralelo, preservando la estructura de carpetas original y mostrando estadísticas de compresión.

Repositorio: [cryptonahue/iris-webp-converter](https://github.com/cryptonahue/iris-webp-converter)

## ✨ Características

- 📁 **Recursivo**: busca imágenes en todas las subcarpetas automáticamente
- 🗂️ **Preserva estructura**: mantiene el árbol de carpetas en la salida
- ⚡ **Procesamiento en paralelo**: usa múltiples hilos (`--workers`)
- 📊 **Estadísticas**: dimensiones, tamaño original vs nuevo, % de reducción
- 👁️ **Modo dry-run**: simula la conversión sin generar archivos ni carpetas de salida
- ⏭️ **`--skip-existing`**: omite archivos ya convertidos
- 🎨 **Calidad configurable** (0-100)
- 🌎 **Idiomas**: español, inglés y portugués de Brasil

## 🚀 Instalación

Para usar el proyecto localmente:

```bash
pip install -e .
```

Para desarrollo, tests y lint:

```bash
pip install -e ".[dev]"
```

También podés instalar dependencias sin modo editable:

```bash
pip install -r requirements.txt
```

> **SVG**: para convertir archivos SVG necesitás `cairosvg` (opcional):
>
> ```bash
> pip install cairosvg
> ```

## 📖 Uso

```bash
# Básico (usa input/ y output/)
iris

# También puede ejecutarse como módulo o wrapper compatible
python -m iris
python iris.py

# Entrada personalizada
python iris.py --input ./mis_fotos

# Calidad y workers
python iris.py --input ./fotos --output ./out --quality 90 --workers 8

# Modo simulación: no convierte ni crea salida
python iris.py --input ./fotos --dry-run

# Omitir archivos ya convertidos
python iris.py --input ./fotos --skip-existing

# Elegir idioma
python iris.py --lang es
```

### Argumentos

| Argumento | Default | Descripción |
|-----------|---------|-------------|
| `--input, -i` | `input` | Carpeta de origen |
| `--output, -o` | `output` | Carpeta de destino |
| `--quality, -q` | `85` | Calidad WebP (0-100) |
| `--workers, -w` | `4` | Hilos en paralelo |
| `--dry-run` | off | Simula sin convertir ni crear salida |
| `--skip-existing` | off | Omite ya convertidos |
| `--lang, -l` | `en` | Idioma: `es`, `en`, `pt` |

## 📁 Estructura de salida

```text
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

## 🧪 Tests

El proyecto usa `pytest`, `ruff` y tiene TDD estricto habilitado en OpenSpec.

```bash
python -m ruff format --check .
python -m ruff check .
python -m pytest -q
```

Para formatear automáticamente:

```bash
python -m ruff format .
```

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
