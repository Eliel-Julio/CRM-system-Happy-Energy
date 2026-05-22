import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 #(595.2755905511812, 841.8897637795277)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor   
from reportlab.graphics.shapes import Drawing, String, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

CM = 28.3464567
p_LINE_HEIGHT = 20
Amarelo_Happy = HexColor('#fbdc06')

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
    
    # Imagem de dados do cliente
    documento.drawImage(file_route("dados do cliente.png"), 15, A4[1]-(1.59*CM)-15, width=8.94*CM, height=1.59*CM)
    
    dados_cliente = [
        ("Cliente: ", dados.get("nome_completo", "N/A")),
        ("Telefone: ", dados.get("telefone", "N/A")),
        ("Endereço: ", dados.get("endereco", "N/A")),
        ("Email: ", dados.get("email", "N/A")),
    ]
    
    y = A4[1] - (1.59 * CM) - 15 - 10 - p_LINE_HEIGHT
    for rotulo, valor in dados_cliente:
        documento.setFont('TrebuchetMS-Bold', 12)
        documento.drawString(CM, y, rotulo)
        documento.setFont('TrebuchetMS', 12)
        documento.drawString(documento.stringWidth(rotulo, 'TrebuchetMS-Bold', 12)+CM, y, valor)
        y -= p_LINE_HEIGHT

    # Tabela de especificações do sistema
    dados_tabela, largura_colunas = [
        ['PRODUÇÃO MÉDIA', 'ÁREA TOTAL', 'PRODUÇÃO ANUAL', 'POTÊNCIA DO SISTEMA'],
        [
            f"{dados.get('producao_media', '--')} kWh", 
            f"{dados.get('area_total', '--')} m²", 
            f"{dados.get('producao_anual', '--')} GWh", 
            f"{dados.get('potencia_kit', '--')} kWp"
        ]
    ], [115, 115, 115, 115] 
    
    tabela = Table(dados_tabela, colWidths=largura_colunas)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A1A1A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),
        ('FONTNAME', (0, 1), (-1, 1), 'TrebuchetMS'),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('TOPPADDING', (0, 1), (-1, 1), 8),
        
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    tabela_width, tabela_height = tabela.wrap(0, 0)
    y -= (tabela_height + 0)
    tabela.drawOn(documento, A4[0]/2 - tabela_width/2, y)
    
    # Imagem comparativo
    y -= (p_LINE_HEIGHT + tabela_height)
    documento.drawImage(file_route("comparativo.png"), 15, y, width=15.5*CM, height=1.69*CM)

    # -------------------------------------------------------------------------
    # CONFIGURAÇÃO DOS DADOS DO GRÁFICO
    # -------------------------------------------------------------------------
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    consumo = [3705, 3705, 3705, 3705, 3705, 3705, 3705, 3705, 3705, 3705, 3705, 3705]
    geracao = [4446, 4323, 4261, 3705, 3396, 3273, 3396, 3890, 4446, 4508, 4631, 4570]
    
    # -------------------------------------------------------------------------
    # CRIAÇÃO DO GRÁFICO (Ajustado para caber nos CM estipulados)
    # -------------------------------------------------------------------------
    largura_desenho = 17.09 * CM
    altura_desenho = 8.0 * CM  
    
    d = Drawing(largura_desenho, altura_desenho)
    
    bc = VerticalBarChart()
    bc.x = 40                  # Recuo para o eixo Y não cortar
    bc.y = 30                  # Recuo inferior para os meses
    bc.height = altura_desenho - 65  # Altura dinâmica proporcional à tela do desenho
    bc.width = largura_desenho - 60  # Largura dinâmica proporcional à tela do desenho
    
    bc.data = [consumo, geracao]
    bc.categoryAxis.categoryNames = meses
    
    # Cores personalizadas
    bc.bars[0].fillColor = Amarelo_Happy
    bc.bars[1].fillColor = HexColor('#000000')

    bc.bars[0].strokeColor = None  # Remove a borda da primeira série (Consumo)
    bc.bars[1].strokeColor = None  # Remove a borda da segunda série (Geração)
    
    # Configuração de escala do eixo Y
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 5000
    bc.valueAxis.valueStep = 1000
    
    # Tipografia dos eixos (alterado para usar a sua fonte registrada)
    bc.categoryAxis.labels.fontName = 'TrebuchetMS'
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.labels.dy = -10
    
    bc.valueAxis.labels.fontName = 'TrebuchetMS'
    bc.valueAxis.labels.fontSize = 8
    
    # -------------------------------------------------------------------------
    # LEGENDA DO GRÁFICO (Centralizada dinamicamente na parte superior)
    # -------------------------------------------------------------------------
    y_legenda = altura_desenho - 15
    
    # Consumo
    d.add(Rect(130, y_legenda, 10, 10, fillColor=Amarelo_Happy, strokeColor=None))
    d.add(String(145, y_legenda + 1, "Consumo (kWh)", fontSize=9, fontName="TrebuchetMS"))
    
    # Geração
    d.add(Rect(270, y_legenda, 10, 10, fillColor=HexColor('#000000'), strokeColor=None))
    d.add(String(285, y_legenda + 1, "Geração (kWh)", fontSize=9, fontName="TrebuchetMS"))
    
    d.add(bc)
    
    # -------------------------------------------------------------------------
    # DESENHANDO O GRÁFICO NO CANVAS
    # -------------------------------------------------------------------------
    # Atualiza a posição 'y' para desenhar o gráfico logo abaixo da última imagem
    y -= (altura_desenho + 20) 
    
    # Centraliza o desenho horizontalmente na página A4
    x_centralizado = (A4[0] - largura_desenho) / 2
    d.drawOn(documento, x_centralizado, y)

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