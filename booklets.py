import fitz
import argparse
import os
import sys
from pathlib import Path

def detect_content_bbox(page, margin_pts):
    content_rects = []

    # --- 1. Bloques de texto
    for block in page.get_text("blocks"):
        content_rects.append(fitz.Rect(block[:4]))

    # --- 2. Imágenes (detectadas en contenido crudo)
    raw_dict = page.get_text("rawdict")
    for block in raw_dict.get("blocks", []):
        if block.get("type") == 1 and "bbox" in block:
            content_rects.append(fitz.Rect(block["bbox"]))

    # --- 3. Dibujos (líneas, rectángulos, etc.)
    for item in page.get_drawings():
        rect = item.get("rect")
        if rect and rect.is_valid:
            content_rects.append(rect)

    # --- Si no se detectó nada, devolver toda la página
    if not content_rects:
        return page.rect

    # --- Combinar todos los rectángulos
    x0 = min(r.x0 for r in content_rects)
    y0 = min(r.y0 for r in content_rects)
    x1 = max(r.x1 for r in content_rects)
    y1 = max(r.y1 for r in content_rects)
    bbox = fitz.Rect(x0, y0, x1, y1)

    # --- Aplicar margen externo (respetando límites de página)
    clip_rect = fitz.Rect(
        max(bbox.x0 - margin_pts, 0),
        max(bbox.y0 - margin_pts, 0),
        min(bbox.x1 + margin_pts, page.rect.width),
        min(bbox.y1 + margin_pts, page.rect.height),
    )

    return clip_rect if clip_rect.is_valid else page.rect

def add_watermark_to_first_page(doc):
    if len(doc) == 0:
        return
    page = doc[0]
    text = "*"
    font_size = 20
    margin = 20
    text_width = fitz.get_text_length(text, fontname="helv", fontsize=font_size)
    x = page.rect.width - text_width - margin
    y = margin + font_size
    page.insert_text((x, y), text, fontsize=font_size, fontname="helv", color=(0, 0, 0))


def create_booklet(input_pdf_path: str, output_pdf_path: str, margin_cm=0.5, add_watermark=False):
    margin_pts = margin_cm * 72 / 2.54  # convertir cm a puntos
    doc_in = fitz.open(input_pdf_path)
    doc_out = fitz.open()

    # A4 horizontal (landscape)
    out_width = 842  # ancho A4 pts (horizontal)
    out_height = 595  # alto A4 pts (horizontal)
    margin_out = margin_pts

    total_pages = doc_in.page_count
    while total_pages % 4 != 0:
        doc_in.insert_page(-1)  # añadir página en blanco al final
        total_pages += 1

    left_pages = list(range(total_pages - 1, total_pages // 2 - 1, -1))
    right_pages = list(range(0, total_pages // 2))

    for i, (left_idx, right_idx) in enumerate(zip(left_pages, right_pages), start=1):
        page_out = doc_out.new_page(width=out_width, height=out_height)

        page_left = doc_in[left_idx]
        page_right = doc_in[right_idx]

        bbox_left = detect_content_bbox(page_left, margin_pts)
        bbox_right = detect_content_bbox(page_right, margin_pts)

        col_width = (out_width - 3 * margin_out) / 2
        col_height = out_height - 2 * margin_out

        # Si la página salida es impar, rotamos ambas 180 grados
        rot_left = (page_left.rotation + 180) % 360 if i % 2 == 1 else page_left.rotation
        rot_right = (page_right.rotation + 180) % 360 if i % 2 == 1 else page_right.rotation

        def place_page(page_in, bbox, x_pos, y_pos, rotation):
            scale = min(col_width / bbox.width, col_height / bbox.height)
            w_scaled = bbox.width * scale
            h_scaled = bbox.height * scale
            x_draw = x_pos + (col_width - w_scaled) / 2
            y_draw = y_pos + (col_height - h_scaled) / 2

            try:
                page_out.show_pdf_page(
                    fitz.Rect(x_draw, y_draw, x_draw + w_scaled, y_draw + h_scaled),
                    doc_in,
                    page_in.number,
                    clip=bbox if bbox != page_in.rect else None,
                    rotate=rotation,
                )
            except ValueError:
                try:
                    page_out.show_pdf_page(
                        fitz.Rect(x_pos, y_pos, x_pos + col_width, y_pos + col_height),
                        doc_in,
                        page_in.number,
                        rotate=rotation,
                    )
                except ValueError:
                    # Página vacía: rellena con blanco
                    page_out.draw_rect(
                        fitz.Rect(x_pos, y_pos, x_pos + col_width, y_pos + col_height),
                        color=(1, 1, 1), fill=(1, 1, 1)
                    )

        # Intercambiamos posición derecha <-> izquierda
        place_page(page_right, bbox_right, margin_out, margin_out, rot_right)            # derecha a la izquierda
        place_page(page_left, bbox_left, margin_out * 2 + col_width, margin_out, rot_left)  # izquierda a la derecha

        if add_watermark:
            add_watermark_to_first_page(doc_out)


    doc_out.save(output_pdf_path)
    doc_out.close()
    doc_in.close()

def main():
    parser = argparse.ArgumentParser(description="Generar un folleto (booklet) a partir de un PDF.")
    parser.add_argument("input_pdf", help="Ruta al archivo PDF de entrada.")
    parser.add_argument("--output", "-o", type=str, help="Ruta al archivo PDF de salida.")
    parser.add_argument("--margin", "-m", type=float, default=1.0, help="Margen en cm a dejar (default: 1.0).")
    parser.add_argument("--add_watermark", "-w", action="store_true", help="Añadir marca de agua en la primera página.")

    args = parser.parse_args()

    input_pdf = args.input_pdf
    margin_cm = args.margin
    add_watermark = args.add_watermark

    if not os.path.isfile(input_pdf):
        print(f"Error: No se encontró el archivo: {input_pdf}")
        sys.exit(1)

    if args.output:
        output_pdf = args.output
    else:
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_pdf = f"{base_name}_booklet.pdf"

    print("Creando folleto PDF...")
    create_booklet(input_pdf, output_pdf, margin_cm=margin_cm, add_watermark=add_watermark)
    print(f"Folleto generado en: {output_pdf}")

if __name__ == "__main__":
    main()
