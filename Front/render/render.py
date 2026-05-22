import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 #(595.2755905511812, 841.8897637795277)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CM = 28.3464567
p_LINE_HEIGHT = 20

def file_route(filename: str, src_path: str='render/src/imagens'):
    if not filename:
        raise ValueError("filename é obrigatório")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', src_path, filename)
    return os.path.normpath(file_path)

def register_font(doc, font_name='TrebuchetMS.ttf', call='TrebuchetMS'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, 'src', font_name)
    if os.path.exists(font_path):pdfmetrics.registerFont(TTFont(call, font_path))
    else: raise FileNotFoundError(f"Font file '{font_name}' not found at path: {font_path}")
        
def render_proposta_p1(DadosProposta: dict, documento=None):
    if not DadosProposta:
        raise ValueError("DadosProposta não pode ser vazio")

    # Tentar registrar variante Bold (TrebuchetMS-Bold.ttf)
    # bold_font_path = os.path.join(base_dir, 'src', 'Trebuchet MS Bold.ttf')
    # bold_font_name = font_name + '-Bold'
    # if os.path.exists(bold_font_path):pdfmetrics.registerFont(TTFont(bold_font_name, bold_font_path))

    documento.drawImage(file_route("capa.png"), 0, 0, width=A4[0], height=A4[1])

    cabeçalho_y, tamanho_fonte = 300, 18

    linhas_cabecalho = [
        ("Proposta Nº: ", f"{DadosProposta['id']}", ""),
        ("Data: ", f"{DadosProposta.get('data', 'N/A')}", ""),
        ("Cliente: ", f"{DadosProposta.get('nome_completo', 'N/A')}", ""),
        ("Potência a ser instalada: ", f"{DadosProposta.get('potencia_kit', 'N/A')}", " kWp"),
        ("Cidade: ", f"{DadosProposta.get('cidade-uf', 'N/A')}", "")
    ]

    register_font(documento, font_name='TrebuchetMS.ttf', call='TrebuchetMS')
    register_font(documento, font_name='Trebuchet MS Bold.ttf', call='TrebuchetMS-Bold')

    for i, (rotulo, valor, sufixo) in enumerate(linhas_cabecalho, start=1):
        y_atual, x_atual = cabeçalho_y - i * p_LINE_HEIGHT, 75

        documento.setFont('TrebuchetMS-Bold', tamanho_fonte)
        documento.drawString(x_atual, y_atual, rotulo)

        x_atual += documento.stringWidth(rotulo, 'TrebuchetMS-Bold', tamanho_fonte)

        documento.setFont('TrebuchetMS', tamanho_fonte)
        documento.drawString(x_atual, y_atual, f"{valor}{sufixo}")

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
    register_font(documento, font_name='TrebuchetMS.ttf', call='TrebuchetMS')
    register_font(documento, font_name='Trebuchet MS Bold.ttf', call='TrebuchetMS-Bold')
    documento.showPage()
    documento.drawImage(file_route("dados do cliente.png"), 15, A4[1]-(1.59*CM)-15, width=8.94*CM, height=1.59*CM)
    dados_cliente = [
        ("Cliente: ", dados.get("nome_completo", "N/A")),
        ("Telefone: ", dados.get("telefone", "N/A")),
        ("Endereço: ", dados.get("endereco", "N/A")),
        ("Email: ", dados.get("email", "N/A")),
    ]
    y = A4[1] - (1.59 * CM) - 15 - 10- p_LINE_HEIGHT
    for rotulo, valor in dados_cliente:
        documento.setFont('TrebuchetMS-Bold', 12)
        documento.drawString(CM, y, rotulo)
        documento.setFont('TrebuchetMS', 12)
        documento.drawString(documento.stringWidth(rotulo, 'TrebuchetMS-Bold', 12)+CM, y, valor)
        y -= p_LINE_HEIGHT

    y -= (1.63*CM)
    documento.drawImage(file_route("capacidade.png"), CM, y, width=16.15*CM, height=1.63*CM)
    y-= p_LINE_HEIGHT*2
    padding = 15
    dados= [
        ("Produção Média: ", f"{dados.get('producao_media', 'N/A')} kWh/mês"),
        ("Área Total: ", f"{dados.get('area_total', 'N/A')} m²"),
        ("Produção Anual: ", f"{dados.get('producao_anual', 'N/A')} kWh/ano"),
        ("Potência do Sistema: ", f"{dados.get('potencia_kit', 'N/A')} kWp")] 
    # space = A4[0]-2*padding - documento.stringWidth("PRODUÇÃO MÉDIAÁREA TOTALPRODUÇÃO ANUALPOTÊNCIA DO SISTEMA", 'TrebuchetMS-Bold', 12)
    space_rotulo = A4[0]-2*padding - documento.stringWidth(dados[0][0]+dados[1][0]+dados[2][0]+dados[3][0], 'TrebuchetMS-Bold', 12)
    gap_rotulos = space_rotulo / 8
    x = padding+gap_rotulos
    for rotulo, valor in dados:
        
        documento.setFont('TrebuchetMS-Bold', 12)
        documento.drawString(x, y, rotulo)
        
        whidth_rotulo = documento.stringWidth(rotulo, 'TrebuchetMS-Bold', 13)
        whidth_valor = documento.stringWidth(valor, 'TrebuchetMS', 10)
        x_ = x + (whidth_rotulo/2) - (whidth_valor/2)
        x+= whidth_rotulo+gap_rotulos*2
        
        documento.setFont('TrebuchetMS', 12)
        documento.drawString(x_, y-p_LINE_HEIGHT, valor)

    return documento
def render_proposta(dados: dict):
    documento = canvas.Canvas(f"proposta_{dados['id']}.pdf", pagesize=A4)
    # documento = render_proposta_p1(dados, documento)
    # documento = render_proposta_p2(dados, documento)
    # documento = render_proposta_p3(dados, documento)
    # documento = render_proposta_p4(dados, documento)
    documento = render_proposta_p5(dados, documento)
    return documento

dados={"id": 1, "nome": "Proposta de Projeto", "descricao": "Descrição detalhada do projeto."}
render_proposta(dados).save()