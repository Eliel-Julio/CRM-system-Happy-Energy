import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 #(595.2755905511812, 841.8897637795277)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def file_route(filename: str, src_path: str='render/src/imagens'):
    if not filename:
        raise ValueError("filename é obrigatório")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', src_path, filename)
    return os.path.normpath(file_path)

def render_proposta_p1(DadosProposta: dict):
    if not DadosProposta:
        raise ValueError("DadosProposta não pode ser vazio")
    p_LINE_HEIGHT = 20


    documento = canvas.Canvas(f"proposta_{DadosProposta['id']}.pdf", pagesize=A4)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, 'src', 'TrebuchetMS.ttf')
    font_name = 'TrebuchetMS'
    if os.path.exists(font_path):pdfmetrics.registerFont(TTFont(font_name, font_path))


    # Tentar registrar variante Bold (TrebuchetMS-Bold.ttf)
    bold_font_path = os.path.join(base_dir, 'src', 'Trebuchet MS Bold.ttf')
    bold_font_name = font_name + '-Bold'
    if os.path.exists(bold_font_path):pdfmetrics.registerFont(TTFont(bold_font_name, bold_font_path))

    documento.drawImage(file_route("capa.png"), 0, 0, width=A4[0], height=A4[1])


    cabeçalho_y = 300
    tamanho_fonte = 18

    linhas_cabecalho = [
        ("Proposta Nº: ", f"{DadosProposta['id']}", ""),
        ("Data: ", f"{DadosProposta.get('data', 'N/A')}", ""),
        ("Cliente: ", f"{DadosProposta.get('nome_completo', 'N/A')}", ""),
        ("Potência a ser instalada: ", f"{DadosProposta.get('potencia_kit', 'N/A')}", " kWp"),
        ("Cidade: ", f"{DadosProposta.get('cidade-uf', 'N/A')}", "")
    ]

    for i, (rotulo, valor, sufixo) in enumerate(linhas_cabecalho, start=1):
        y_atual = cabeçalho_y - i * p_LINE_HEIGHT
        x_atual = 75

        documento.setFont(bold_font_name, tamanho_fonte)
        documento.drawString(x_atual, y_atual, rotulo)

        x_atual += documento.stringWidth(rotulo, bold_font_name, tamanho_fonte)

        documento.setFont(font_name, tamanho_fonte)
        documento.drawString(x_atual, y_atual, f"{valor}{sufixo}")
    documento.setFont(font_name, 12)

    return documento

def render_proposta_p2(dados: dict, documento):
    documento.showPage()
    whdth, height = 500, 700
    x, y = (A4[0] - whdth) / 2, (A4[1] - height) / 2
    documento.drawImage(file_route("contracapa.png"), x, y, width=whdth, height=height)
    return documento
    
def render_proposta_p3(dados: dict, documento):
    documento.showPage()
    documento.drawImage(file_route("missao.png"), 10,10, width=A4[0]-20, height=A4[1]-20)
    return documento

def render_proposta_p4(dados: dict, documento):
    documento.showPage()
    documento.drawImage(file_route("projetos.png"), 10,10, width=A4[0]-20, height=A4[1]-20)
    return documento

def render_proposta_p5(dados: dict, documento):
    documento.showPage()
    documento.drawImage(file_route("dados do cliente.png"), 15, A4[1]-100, width=100, height=30)
    return documento
def render_proposta(dados: dict):
    documento = render_proposta_p1(dados)
    documento = render_proposta_p2(dados, documento)
    documento = render_proposta_p3(dados, documento)
    documento = render_proposta_p4(dados, documento)
    documento = render_proposta_p5(dados, documento)
    return documento

dados={"id": 1, "nome": "Proposta de Projeto", "descricao": "Descrição detalhada do projeto."}
render_proposta(dados).save()