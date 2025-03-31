import requests
import pdfplumber
import pandas as pd
import zipfile
from pathlib import Path

pdf_url = "https://www.gov.br/ans/pt-br/arquivos/assuntos/consumidor/o-que-seu-plano-deve-cobrir/anexo_i_rol_2021rn_4652021.pdf"

# Nomes dos arquivos
pdf_filename = "Anexo_I_Rol_Procedimentos.pdf"
csv_filename = "Rol_de_Procedimentos_GuilhermeMacena.csv"
zip_filename = "Teste_GuilhermeMacena.zip"

# Download do PDF
response = requests.get(pdf_url)
with open(pdf_filename, 'wb') as f:
    f.write(response.content)

# Dicionário de substituições conforme a legenda
substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial",
    "HCO": "Seg. Hospitalar Com Obstetrícia",
    "HSO": "Seg. Hospitalar Sem Obstetrícia",
    "REF": "Plano Referência",
    "PAC": "Procedimento de Alta Complexidade",
    "DUT": "Diretriz de Utilização"
}

# Lista para armazenar os dados extraídos
dados_tabela = []

# Extração dos dados do PDF
with pdfplumber.open(pdf_filename) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if any(row):  # Ignorar linhas vazias
                    dados_tabela.append(row)

# Criar um DataFrame com os dados extraídos
df = pd.DataFrame(dados_tabela)

# Substituir abreviações conforme a legenda
df.replace(substituicoes, inplace=True)

# Salvar em CSV
df.to_csv(csv_filename, index=False, encoding='utf-8')

# Compactar o CSV em um arquivo ZIP
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_filename)

# Remover o arquivo CSV original após compactação
Path(csv_filename).unlink()

print(f"Processo finalizado com sucesso! Arquivo ZIP gerado: {zip_filename}")
