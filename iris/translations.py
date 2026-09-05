"""Translations for Iris: Spanish, English, and Brazilian Portuguese."""

MESSAGES = {
    "desc": {
        "es": "Convierte imágenes a WebP con procesamiento en paralelo.",
        "en": "Converts images to WebP with parallel processing.",
        "pt": "Converte imagens para WebP com processamento em paralelo.",
    },
    "input_help": {
        "es": "Carpeta de origen (default: input)",
        "en": "Source folder (default: input)",
        "pt": "Pasta de origem (padrão: input)",
    },
    "output_help": {
        "es": "Carpeta de destino (default: output)",
        "en": "Destination folder (default: output)",
        "pt": "Pasta de destino (padrão: output)",
    },
    "quality_help": {
        "es": "Calidad WebP 0-100 (default: 85)",
        "en": "WebP quality 0-100 (default: 85)",
        "pt": "Qualidade WebP 0-100 (padrão: 85)",
    },
    "workers_help": {
        "es": "Hilos en paralelo (default: 4)",
        "en": "Parallel workers (default: 4)",
        "pt": "Trabalhadores em paralelo (padrão: 4)",
    },
    "dry_run_help": {
        "es": "Simula la conversión sin generar archivos",
        "en": "Simulate conversion without creating files",
        "pt": "Simula a conversão sem criar arquivos",
    },
    "skip_existing_help": {
        "es": "Omitir archivos ya convertidos",
        "en": "Skip already converted files",
        "pt": "Ignorar arquivos já convertidos",
    },
    "lang_help": {
        "es": "Idioma: es, en, pt (default: en)",
        "en": "Language: es, en, pt (default: en)",
        "pt": "Idioma: es, en, pt (padrão: en)",
    },
    "quality_range_err": {
        "es": "--quality debe estar entre 0 y 100",
        "en": "--quality must be between 0 and 100",
        "pt": "--quality deve estar entre 0 e 100",
    },
    "workers_min_err": {
        "es": "--workers debe ser al menos 1",
        "en": "--workers must be at least 1",
        "pt": "--workers deve ser pelo menos 1",
    },
    "input_missing": {
        "es": "❌ La carpeta de entrada no existe: {folder}",
        "en": "❌ Input folder does not exist: {folder}",
        "pt": "❌ Pasta de entrada não existe: {folder}",
    },
    "no_images": {
        "es": "❌ No se encontraron imágenes compatibles en '{folder}'",
        "en": "❌ No supported images found in '{folder}'",
        "pt": "❌ Nenhuma imagem compatível encontrada em '{folder}'",
    },
    "formats": {
        "es": "   Formatos: {formats}",
        "en": "   Formats: {formats}",
        "pt": "   Formatos: {formats}",
    },
    "starting": {
        "es": "🚀 Iniciando conversión a WebP...",
        "en": "🚀 Starting WebP conversion...",
        "pt": "🚀 Iniciando conversão para WebP...",
    },
    "input": {
        "es": "📁 Entrada : {path}",
        "en": "📁 Input   : {path}",
        "pt": "📁 Entrada : {path}",
    },
    "output": {
        "es": "📁 Salida  : {path}",
        "en": "📁 Output  : {path}",
        "pt": "📁 Saída   : {path}",
    },
    "images_found": {
        "es": "🖼️  Imágenes: {count}",
        "en": "🖼️  Images  : {count}",
        "pt": "🖼️  Imagens : {count}",
    },
    "quality": {
        "es": "⚙️  Calidad : {quality}",
        "en": "⚙️  Quality : {quality}",
        "pt": "⚙️  Qualidade: {quality}",
    },
    "workers": {
        "es": "🔧 Workers : {workers}",
        "en": "🔧 Workers : {workers}",
        "pt": "🔧 Workers : {workers}",
    },
    "dry_run_mode": {
        "es": "👁️  MODO: SIMULACIÓN (no se genera ningún archivo)",
        "en": "👁️  MODE: DRY-RUN (no files will be created)",
        "pt": "👁️  MODO: SIMULAÇÃO (nenhum arquivo será criado)",
    },
    "dry_sim": {
        "es": "   [simulado] → {name}",
        "en": "   [simulated] → {name}",
        "pt": "   [simulado] → {name}",
    },
    "ok": {
        "es": "✅ {rel} → {out}",
        "en": "✅ {rel} → {out}",
        "pt": "✅ {rel} → {out}",
    },
    "dims": {
        "es": "   📏 {dims}  📦 {os} → {ns}  📉 {red:.1f}%",
        "en": "   📏 {dims}  📦 {os} → {ns}  📉 {red:.1f}%",
        "pt": "   📏 {dims}  📦 {os} → {ns}  📉 {red:.1f}%",
    },
    "skipped": {
        "es": "⏭️  Omitido (ya existe): {name}",
        "en": "⏭️  Skipped (already exists): {name}",
        "pt": "⏭️  Ignorado (já existe): {name}",
    },
    "failed": {
        "es": "❌ Fallo: {name} — {error}",
        "en": "❌ Failed: {name} — {error}",
        "pt": "❌ Falha: {name} — {error}",
    },
    "summary_title": {
        "es": "📊 RESUMEN",
        "en": "📊 SUMMARY",
        "pt": "📊 RESUMO",
    },
    "dry_summary": {
        "es": "👁️  SIMULACIÓN: {count} imágenes listas para convertir",
        "en": "👁️  DRY-RUN: {count} images ready to convert",
        "pt": "👁️  SIMULAÇÃO: {count} imagens prontas para converter",
    },
    "converted": {
        "es": "✅ Convertidas : {count}",
        "en": "✅ Converted   : {count}",
        "pt": "✅ Convertidas : {count}",
    },
    "skipped_count": {
        "es": "⏭️  Omitidas   : {count}",
        "en": "⏭️  Skipped    : {count}",
        "pt": "⏭️  Ignoradas  : {count}",
    },
    "failed_count": {
        "es": "❌ Fallidas    : {count}",
        "en": "❌ Failed     : {count}",
        "pt": "❌ Falharam   : {count}",
    },
    "sizes": {
        "es": "📦 Tamaño     : {os} → {ns}",
        "en": "📦 Size       : {os} → {ns}",
        "pt": "📦 Tamanho    : {os} → {ns}",
    },
    "reduction": {
        "es": "📉 Reducción  : {red:.1f}%",
        "en": "📉 Reduction  : {red:.1f}%",
        "pt": "📉 Redução    : {red:.1f}%",
    },
}


def text(lang, key, **kwargs):
    """Translate and format a message."""
    template = MESSAGES[key][lang]
    return template.format(**kwargs)
