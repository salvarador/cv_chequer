#!/usr/bin/env python3
"""
Simple test script to verify PDF text extraction without AWS dependencies
"""

import os
import sys
import pdfplumber
import PyPDF2


def test_pdfplumber(pdf_path: str) -> str:
    """Test pdfplumber extraction"""
    try:
        print(f"Testing pdfplumber on {os.path.basename(pdf_path)}...")
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            print(f"  PDF has {len(pdf.pages)} pages")
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
                print(f"  Page {page_num}: {len(page_text) if page_text else 0} characters")
        
        print(f"✓ pdfplumber extracted {len(text)} total characters")
        return text
    except Exception as e:
        print(f"✗ pdfplumber failed: {str(e)}")
        return ""


def test_pypdf2(pdf_path: str) -> str:
    """Test PyPDF2 extraction"""
    try:
        print(f"\nTesting PyPDF2 on {os.path.basename(pdf_path)}...")
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"  PDF has {len(pdf_reader.pages)} pages")
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
                print(f"  Page {page_num}: {len(page_text) if page_text else 0} characters")
        
        print(f"✓ PyPDF2 extracted {len(text)} total characters")
        return text
    except Exception as e:
        print(f"✗ PyPDF2 failed: {str(e)}")
        return ""


def preview_text(text: str, max_chars: int = 500):
    """Show a preview of the extracted text"""
    if not text:
        print("No text to preview")
        return
    
    preview = text[:max_chars]
    if len(text) > max_chars:
        preview += "..."
    
    print(f"\nText Preview (first {min(len(text), max_chars)} chars):")
    print("-" * 60)
    print(preview)
    print("-" * 60)


def main():
    if len(sys.argv) != 2:
        print("Usage: python test_pdf_extraction.py <path_to_pdf>")
        print("\nExample PDFs available:")
        for root, dirs, files in os.walk("CV_FullStack"):
            for file in files:
                if file.endswith('.pdf'):
                    print(f"  {os.path.join(root, file)}")
        return
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return
    
    print(f"Testing PDF text extraction methods on: {pdf_path}")
    print("=" * 70)
    
    # Test pdfplumber
    text1 = test_pdfplumber(pdf_path)
    if text1:
        preview_text(text1)
    
    # Test PyPDF2
    text2 = test_pypdf2(pdf_path)
    if text2:
        preview_text(text2)
    
    # Compare results
    print(f"\nComparison:")
    print(f"pdfplumber: {len(text1)} characters")
    print(f"PyPDF2:     {len(text2)} characters")
    
    if text1 and text2:
        if len(text1) > len(text2):
            print("✓ pdfplumber extracted more text")
        elif len(text2) > len(text1):
            print("✓ PyPDF2 extracted more text")
        else:
            print("✓ Both methods extracted similar amounts of text")
    elif text1:
        print("✓ Only pdfplumber succeeded")
    elif text2:
        print("✓ Only PyPDF2 succeeded")
    else:
        print("✗ Both methods failed")


if __name__ == "__main__":
    main()
