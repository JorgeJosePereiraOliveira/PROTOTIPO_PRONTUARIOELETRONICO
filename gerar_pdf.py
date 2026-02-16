#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║    Conversor de Notebook para PDF                                          ║
║    Prontuário Eletrônico - Documentação Completa                           ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
from pathlib import Path

def converter_html_pdf():
    """Converte HTML para PDF usando WeasyPrint"""
    
    # Definir caminhos
    script_dir = Path(__file__).parent
    html_file = script_dir / "DOCUMENTACAO_PRONTUARIO_COMPLETA.html"
    pdf_file = script_dir / "DOCUMENTACAO_PRONTUARIO_COMPLETA.pdf"
    
    print("\n" + "="*80)
    print("  CONVERSOR: NOTEBOOK → HTML → PDF")
    print("="*80)
    
    # Verificar se arquivo HTML existe
    if not html_file.exists():
        print(f"\n❌ ERRO: Arquivo HTML não encontrado")
        print(f"   Esperado: {html_file}")
        print(f"\n   Solução: Execute primeiro o comando:")
        print(f"   python -m nbconvert --to html DOCUMENTACAO_PRONTUARIO_COMPLETA.ipynb")
        sys.exit(1)
    
    print(f"\n📄 Arquivo HTML encontrado: {html_file.name}")
    print(f"   Tamanho: {html_file.stat().st_size / 1024:.1f} KB")
    
    # Importar WeasyPrint
    try:
        from weasyprint import HTML
        print("\n✅ WeasyPrint disponível")
    except ImportError:
        print("\n❌ WeasyPrint não instalado")
        print("   Instale com: pip install weasyprint")
        sys.exit(1)
    
    # Converter para PDF
    print(f"\n⏳ Convertendo para PDF...")
    print(f"   Destino: {pdf_file.name}")
    
    try:
        HTML(str(html_file)).write_pdf(str(pdf_file))
        
        # Verificar sucesso
        if pdf_file.exists():
            size_kb = pdf_file.stat().st_size / 1024
            size_mb = size_kb / 1024
            
            print(f"\n✅ PDF GERADO COM SUCESSO!")
            print(f"\n   📁 Arquivo: {pdf_file.name}")
            print(f"   📊 Tamanho: {size_mb:.2f} MB ({size_kb:.1f} KB)")
            print(f"   📍 Caminho: {pdf_file}")
            
            print(f"\n" + "="*80)
            print(f"  Arquivo pronto para visualizar e imprimir!")
            print(f"="*80 + "\n")
            
            return True
        else:
            print(f"\n❌ Arquivo PDF não foi criado")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERRO na conversão:")
        print(f"   {type(e).__name__}: {str(e)}")
        
        print(f"\n💡 Solução alternativa:")
        print(f"   1. Abra o arquivo HTML em um navegador")
        print(f"   2. Pressione Ctrl+P (ou Cmd+P)")
        print(f"   3. Salve como PDF")
        
        sys.exit(1)

if __name__ == "__main__":
    converter_html_pdf()
