import argparse
import os
import subprocess
from pdf2docx import Converter as PDF2DOCXConverter
from docx2pdf import convert as DOCX2PDFConverter

def find_file(filename):
    try:
        result = subprocess.run(f"find / -name {filename} 2>/dev/null", capture_output=True, text=True, shell=True)
        found_files = result.stdout.strip().split('\n')
        if found_files and found_files[0]:  
            return found_files[0]
        else:
            return None
    except Exception as e:
        print(f"Error finding file '{filename}': {e}")
        return None

def ppt_pdf(input_file, output_file):
    found_file = find_file(input_file)
    if found_file:
        try:
            input_dir = os.path.dirname(found_file)
            full_output_path = os.path.join(input_dir, output_file)

            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', found_file], check=True)
            pdf_file = found_file.replace('.pptx', '.pdf')
            
            if os.path.exists(pdf_file):
                os.rename(pdf_file, full_output_path)
                print(f"Converted {found_file} to {full_output_path}")
            else:
                print(f"Conversion successful, but output file not found: {pdf_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {found_file} to PDF: {e}")
    else:
        print(f"No file found matching '{input_file}'")

def pdf_docx(input_file, output_file):
    found_file = find_file(input_file)
    if found_file:
        try:
            input_dir = os.path.dirname(found_file)
            full_output_path = os.path.join(input_dir, output_file)
            converter = PDF2DOCXConverter(found_file)
            converter.convert(full_output_path)
            print(f"Converted {found_file} to {full_output_path}")
        except Exception as e:
            print(f"Error converting {found_file} to DOCX: {e}")
    else:
        print(f"No file found matching '{input_file}'")

def docx_pdf(input_file, output_file):
    found_file = find_file(input_file)
    if found_file:
        try:
            input_dir = os.path.dirname(found_file)
            full_output_path = os.path.join(input_dir, output_file)

            subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', found_file], check=True)
            pdf_file = found_file.replace('.docx', '.pdf')
            if os.path.exists(pdf_file):
                os.rename(pdf_file, full_output_path)
                print(f"Converted {found_file} to {full_output_path}")
            else:
                print(f"Conversion successful, but output file not found: {pdf_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {found_file} to PDF: {e}")
    else:
        print(f"No file found matching '{input_file}'")

def main():
    parser = argparse.ArgumentParser(description="QuickDoc CLI Tool")
    parser.add_argument('command', choices=['convert'], help='Command to execute')
    parser.add_argument('conversion_type', choices=['ppt2pdf', 'pdf2docx', 'docx2pdf'], help='Type of conversion')
    parser.add_argument('--input', required=True, help='Input file name')
    parser.add_argument('--output', required=True, help='Output file name')

    args = parser.parse_args()

    if args.command == 'convert':
        if args.conversion_type == 'ppt2pdf':
            ppt_pdf(args.input, args.output)
        elif args.conversion_type == 'pdf2docx':
            pdf_docx(args.input, args.output)
        elif args.conversion_type == 'docx2pdf':
            docx_pdf(args.input, args.output)

if __name__ == '__main__':
    main()
