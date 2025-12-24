#!/usr/bin/env python3
import unittest
import os
from pypdf import PageObject
from pdfgridcat.cli import concat_pdf, concat_pdf_pages

class TestPdfGridCatCLI(unittest.TestCase):
    def setUp(self):
        # Create real blank pages
        self.page1 = PageObject.create_blank_page(width=100, height=200)
        self.page2 = PageObject.create_blank_page(width=50, height=150)

        # Temporary input files for testing
        self.input_files = ['tmp1.pdf', 'tmp2.pdf']
        for i, page in enumerate([self.page1, self.page2]):
            from pypdf import PdfWriter
            writer = PdfWriter()
            writer.add_page(page)
            with open(self.input_files[i], 'wb') as f:
                writer.write(f)

    def tearDown(self):
        # Remove temporary input and output files
        for f in self.input_files + ['out.pdf']:
            if os.path.exists(f):
                os.remove(f)

    def test_concat_pdf_horizontal(self):
        """Test horizontal concatenation sets correct mediabox dimensions."""
        result = concat_pdf([self.page1, self.page2], horizontal=True)
        self.assertEqual(result.mediabox.width, 150)
        self.assertEqual(result.mediabox.height, 200)

    def test_concat_pdf_vertical(self):
        """Test vertical concatenation sets correct mediabox dimensions."""
        result = concat_pdf([self.page1, self.page2], horizontal=False)
        self.assertEqual(result.mediabox.width, 100)
        self.assertEqual(result.mediabox.height, 350)

    def test_concat_pdf_pages_creates_file(self):
        """Test that concat_pdf_pages generates a real PDF file."""
        output_file = 'out.pdf'
        try:
            concat_pdf_pages(self.input_files, output_file, 2, 1)
            # Check that the output file is created
            self.assertTrue(os.path.exists(output_file))
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
