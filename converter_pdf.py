#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para converter HTML notebook para PDF
"""

from weasyprint import HTML
import os
import sys

def converter_html_para_pdf():
    """Converte o HTML gerado do notebook para PDF"""
    
    diretorio = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(diretorio, 'DOCUMENTACAO_PRONTUARIO_COMPLETA.html')
    pdf_file = os.path.join(diretorio, 'DOCUMENTACAO_PRONTUARIO_COMPLETA.pdf')
    
    print("=" * 80)
    print("CONVERSOR NOTEBOOK → PDF")
    print("=" * 80)
    
    if not os.path.exists(html_file):
        print(f"❌ Arquivo HTML não encontrado: {html_file}")
        sys.exit(1)
    
    print(f"\n📄 Convertendo HTML para PDF...")
    print(f"   Origem: {html_file}")
    print(f"   Destino: {pdf_file}")
    
    try:
        # Converter HTML para PDF
        HTML(html_file).write_pdf(pdf_file)
        
        # Verificar tamanho do arquivo
        tamanho_mb = os.path.getsize(pdf_file) / (1024 * 1024)
        
        print(f"\n✅ PDF gerado com sucesso!")
        print(f"   📁 Arquivo: {os.path.basename(pdf_file)}")
        print(f"   📊 Tamanho: {tamanho_mb:.2f} MB")
        print(f"   📍 Caminho: {pdf_file}")
        print("\n" + "=" * 80)
        print("Você pode agora abrir o arquivo PDF em qualquer leitor de PDF!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erro ao converter: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    converter_html_para_pdf()
