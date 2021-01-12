import PyPDF2
import sys
from tqdm import tqdm


def separate_laudos(pdf):

    with open(pdf, "rb") as f:
        pdfReader = PyPDF2.PdfFileReader(f)

        for pageNum in tqdm(range(pdfReader.numPages), ascii=True):
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText()
            patient = text.split("\n")[7].replace(" ", "_")
            number = text.split("\n")[9]
            if "ELISA" in text:
                exam = "ELISA"
            elif "RT-qPCR" in text:
                exam = "RT-qPCR"
            data = f"{number}_{patient}_{exam}.pdf"

            with open(data, "wb") as j:
                pdfWriter = PyPDF2.PdfFileWriter()
                pdfWriter.addPage(pageObj)
                pdfWriter.write(j)


separate_laudos(sys.argv[1])
