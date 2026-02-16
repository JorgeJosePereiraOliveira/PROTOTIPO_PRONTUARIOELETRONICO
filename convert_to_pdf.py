from weasyprint import HTML
import os

html_file = r'd:\Engenharia_de_Software_TCC\Prototipo_ProntuarioEletronico\DOCUMENTACAO_PRONTUARIO_COMPLETA.html'
pdf_file = r'd:\Engenharia_de_Software_TCC\Prototipo_ProntuarioEletronico\DOCUMENTACAO_PRONTUARIO_COMPLETA.pdf'

try:
    HTML(html_file).write_pdf(pdf_file)
    size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
    with open(r'd:\Engenharia_de_Software_TCC\Prototipo_ProntuarioEletronico\conversao_log.txt', 'w') as f:
        f.write(f"OK|{pdf_file}|{size_mb}")
except Exception as e:
    with open(r'd:\Engenharia_de_Software_TCC\Prototipo_ProntuarioEletronico\conversao_log.txt', 'w') as f:
        f.write(f"ERRO|{str(e)}")
