import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 #(595.2755905511812, 841.8897637795277)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Image, Paragraph
from reportlab.lib import colors
from reportlab.lib.colors import HexColor   
from reportlab.graphics.shapes import Drawing, String, Rect, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF

from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


CM = 28.3464567
p_LINE_HEIGHT = 20
Amarelo_Happy = HexColor('#fbdc06')
sheet_padding_top = 20
sheet_padding_left = 1*CM
font_size = 12

def get_pay_back(finace_data):
    meses = 15
    anos , meses_restantes = meses//12 , meses%12
    return f"{anos} ano{'s' if anos!= 1 else ''} e {meses_restantes} mese{'s' if meses_restantes!= 1 else ''}"

def tousand_separator(value):
    return f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def file_route(filename: str, src_path: str='render/src/imagens'):
    if not filename:
        raise ValueError("filename é obrigatório")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', src_path, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo '{filename}' não encontrado no caminho: {file_path}")
    return os.path.normpath(file_path)

def register_font(doc, font_name='TrebuchetMS.ttf', call='TrebuchetMS'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, 'src', font_name)
    if os.path.exists(font_path):pdfmetrics.registerFont(TTFont(call, font_path))
    else: raise FileNotFoundError(f"Font file '{font_name}' not found at path: {font_path}")
        
def render_proposta_p1(dados: dict, documento=None):

    documento.drawImage(file_route("capa.png"), 0, 0, width=A4[0], height=A4[1])

    cabeçalho_y, tamanho_fonte = 300, 18

    linhas_cabecalho = [
        ("Proposta Nº: ", f"{dados['id']}", ""),
        ("Data: ", f"{dados.get('data', 'N/A')}", ""),
        ("Cliente: ", f"{dados.get('nome', 'N/A')}", ""),
        ("Potência a ser instalada: ", f"{dados.get('potencia_kit', 'N/A')}", " kWp"),
        ("Cidade: ", f"{dados.get('cidade-uf', 'N/A')}", "")
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
    documento.drawImage(file_route("dados do cliente.png"), sheet_padding_left, A4[1]-(1.59*CM)-sheet_padding_top, width=8.94*CM, height=1.59*CM)
    
    dados_cliente = [
        ("Cliente: ", dados.get("nome", "N/A")),
        ("Telefone: ", dados.get("telefone", "N/A")),
        ("Endereço: ", dados.get("endereco", "N/A")),
        ("Email: ", dados.get("email", "N/A")),
    ]
    
    y = A4[1] - (1.59 * CM) - sheet_padding_top - 10 - p_LINE_HEIGHT
    for rotulo, valor in dados_cliente:
        documento.setFont('TrebuchetMS-Bold', 12)
        documento.drawString(sheet_padding_left, y, rotulo)
        documento.setFont('TrebuchetMS', 12)
        documento.drawString(documento.stringWidth(rotulo, 'TrebuchetMS-Bold', 12)+sheet_padding_left, y, valor)
        y -= p_LINE_HEIGHT

    # Tabela de especificações do sistema
    dados_tabela, largura_colunas = [
        ['PRODUÇÃO MÉDIA', 'ÁREA TOTAL', 'PRODUÇÃO ANUAL', 'POTÊNCIA DO SISTEMA'],
        [
            f"{(dados.get('potencia_kit', 7.32) * dados.get('CONST_IRRAD', 139)):.2f} kWh", 
            f"{(dados.get('modulos', {'area': 2.39*1.14}).get('area', 0)*dados.get('modulos', {'quantidade': 12}).get('quantidade', 0)*1.1):.2f} m²", 
            f"{dados.get('potencia_kit', 7.32) * 12 * dados.get('CONST_IRRAD', 139)} kWh", 
            f"{dados.get('potencia_kit', 7.32)} kWp"
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
    
    y -= (p_LINE_HEIGHT + tabela_height)
    documento.drawImage(file_route("comparativo.png"), sheet_padding_left, y, width=15.5*CM, height=1.69*CM)

    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    consumo = [0.8*dados.get('potencia_kit',7.32)*dados.get('CONSTS',{'CONST_IRRAD':139}).get('CONST_IRRAD',139)]*12
    geracao = [v*dados.get('potencia_kit', 7.32)*dados.get('CONSTS',{'CONST_IRRAD':139}).get('CONST_IRRAD',139)/6.38 for v in [6.38,6.16,6.03,5.24,4.83,4.58,4.82,5.55,6.32,6.4,6.5,6.38]]
    
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
    
    bc.bars[0].fillColor = Amarelo_Happy
    bc.bars[1].fillColor = HexColor('#000000')

    bc.bars[0].strokeColor = None
    bc.bars[1].strokeColor = None
    
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(max(geracao), max(consumo)) * 1.2
    bc.valueAxis.valueStep = round(round(max(geracao) / 5)/150)*150
    
    bc.categoryAxis.labels.fontName = 'TrebuchetMS'
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.labels.dy = -10
    
    bc.valueAxis.labels.fontName = 'TrebuchetMS'
    bc.valueAxis.labels.fontSize = 8
    
    y_legenda = altura_desenho - 15
    
    # Consumo
    d.add(Rect(130, y_legenda, 10, 10, fillColor=Amarelo_Happy, strokeColor=None))
    d.add(String(145, y_legenda + 1, "Consumo (kWh)", fontSize=9, fontName="TrebuchetMS"))
    
    # Geração
    d.add(Rect(270, y_legenda, 10, 10, fillColor=HexColor('#000000'), strokeColor=None))
    d.add(String(285, y_legenda + 1, "Geração (kWh)", fontSize=9, fontName="TrebuchetMS"))
    
    d.add(bc)
    
    y -= (altura_desenho + 20) 
    
    x_centralizado = (A4[0] - largura_desenho) / 2
    d.drawOn(documento, x_centralizado, y)

    return documento

def render_proposta_p6(dados: dict, documento):
    documento.showPage()
    y= A4[1] - 1.75*CM - sheet_padding_top
    documento.drawImage(file_route("detalhes.png"), sheet_padding_left, y, width=12.12*CM, height=1.75*CM)

    register_font(documento, font_name='TrebuchetMS.ttf', call='TrebuchetMS')
    register_font(documento, font_name='Trebuchet MS Bold.ttf', call='TrebuchetMS-Bold')

    # -------------------------------------------------------------------------
    # ESTRUTURAÇÃO DOS DADOS DA TABELA
    # -------------------------------------------------------------------------
    img_inversor = Image(file_route("inversor weg.png"), width=2.5*CM, height=2.5*CM)

    # Texto longo da descrição formatado com quebras de linha para a tabela respeitar
    descricao_texto = (
        "DESCRIÇÃO:\n"
        f"{dados.get('qtd_modulos', '12')} MÓDULO {dados.get('modulos',{'modelo': '--.--'}).get('modelo')}\n"
        f"{dados.get('qtd_inversores', '01')} INVERSOR {dados.get('inversores', {'marca': 'WEG'}).get('marca', 'WEG')} {dados.get('inversores', {'modelo': '615 Wp - WEG BIFACIAL'}).get('modelo','615 Wp - WEG BIFACIAL')}\n"
        f"ESTRUTURA DE FIXAÇÃO {dados.get('estrutura', {'tipo': 'Fibrocimento'}).get('tipo','Fibrocimento')}\n"
        "KIT COMPLETO DE INSTALAÇÃO"
    )

    # Matriz da tabela (3 linhas x 3 colunas)
    dados_tabela = [
        # Linha 0: Cabeçalho
        ['ITEM', 'QUANTIDADE', 'IMAGEM'],
        # Linha 1: Dados principais do Kit
        [f"KIT {dados.get('potencia_kit', '--.--')} kwp {dados.get('inversor',{'marca',''}.get('marca',''))} LAJE", "1", img_inversor],
        # Linhas 2: Reservada para a descrição longa expandida (via SPAN)
        [dados.get('descricao', ''), '', '']
    ]

    # Larguras das colunas somando exatamente 17.09 CM (para alinhar com o seu gráfico)
    largura_colunas = [9.5*CM, 3.5*CM, 4.09*CM]

    tabela = Table(dados_tabela, colWidths=largura_colunas)
    tabela.setStyle(TableStyle([
        # --- Configurações do Cabeçalho (Linha 0) ---
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#BBBBBB")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1A1A1A')),
        ('FONTNAME', (0, 0), (-1, 0), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),

        # --- Linha Cinza Clara do Kit (Linha 1) ---
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#EAEAEA')),
        ('TEXTCOLOR', (0, 1), (1, 1), colors.HexColor('#222222')),
        ('FONTNAME', (0, 1), (1, 1), 'TrebuchetMS'),
        ('FONTSIZE', (0, 1), (1, 1), 11),
        ('ALIGN', (0, 1), (0, 1), 'LEFT'),      # Texto do kit à esquerda
        ('ALIGN', (1, 1), (1, 1), 'CENTER'),    # Quantidade no centro
        ('ALIGN', (2, 1), (2, 1), 'CENTER'),    # Imagem no centro
        ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
        ('LEFTPADDING', (0, 1), (0, 1), 15),    # Margem interna pro texto não colar na borda
        ('TOPPADDING', (0, 1), (-1, 1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),

        # --- Bloco de Descrição com Mesclagem (Linha 2) ---
        # SPAN mescla da coluna 0 até a coluna 2 na linha 2
        ('SPAN', (0, 2), (2, 2)), 
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#1A1A1A')),
        ('FONTNAME', (0, 2), (-1, 2), 'TrebuchetMS'),
        ('FONTSIZE', (0, 2), (-1, 2), 10.5),
        ('ALIGN', (0, 2), (-1, 2), 'LEFT'),
        ('VALIGN', (0, 2), (-1, 2), 'TOP'),
        ('LEFTPADDING', (0, 2), (-1, 2), 20),
        ('TOPPADDING', (0, 2), (-1, 2), 20),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 20),

        # --- Linhas Divisórias Brancas ---
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.white), # Linha grossa branca abaixo do cabeçalho
        ('LINEBELOW', (0, 1), (-1, 1), 2, colors.white), # Linha grossa branca abaixo do item
    ]))

    tabela_width, tabela_height = tabela.wrap(0, 0)
    
    y -= tabela_height + 20 
    
    tabela.drawOn(documento, (A4[0] - tabela_width) / 2, y)

    tabela_=Table([[f"Valor total: R$ {tousand_separator(dados.get('valor', '0.00'))}"]], colWidths=[A4[0]-3*CM])
    tabela_.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#000000")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#fbfbfb')),
        
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'TrebuchetMS-Bold'),]))
    tabela_width, tabela_height = tabela_.wrap(0, 0)
    tabela_.drawOn(documento, (A4[0] - tabela_width) / 2, y - tabela_height - 10)

    y -= (tabela_height + CM + 1.77*CM)
    documento.drawImage(file_route("garantias.png"), sheet_padding_left, y, width=10.9*CM, height=1.77*CM)

    garantias =[
        ['Painel',dados.get('garantias', {'painel': 'N/A'}).get('painel', 'N/A'),'serviço', dados.get('garantias', {'instalacao': 'N/A'}).get('instalacao', 'N/A')],
        # [None,None,None,None],
        ['Inversor',dados.get('garantias', {'inversor': 'N/A'}).get('inversor', 'N/A'),'Estrutura', dados.get('garantias', {'estrutura': 'N/A'}).get('estrutura', 'N/A')]
    ]

    tabela_garantias = Table(garantias, colWidths=[4.5*CM, 3.5*CM, 4.5*CM, 3.5*CM])

    tabela_garantias.setStyle(TableStyle([
    ('LINEBELOW', (0, 0), (-1, 0), 12, colors.white), 

    # --- Estilização dos Blocos Pretos (Coluna 0 e Coluna 2) ---
    ('BACKGROUND', (0, 0), (0, -1), HexColor("#1A1A1A")), 
    ('BACKGROUND', (2, 0), (2, -1), HexColor("#1A1A1A")), 
    ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
    ('TEXTCOLOR', (2, 0), (2, -1), colors.white),
    ('FONTNAME', (0, 0), (0, -1), 'TrebuchetMS-Bold'),
    ('FONTNAME', (2, 0), (2, -1), 'TrebuchetMS-Bold'),
    ('FONTSIZE', (0, 0), (0, -1), 10),
    ('FONTSIZE', (2, 0), (2, -1), 10),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (2, 0), (2, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (0, -1), 10),
    ('LEFTPADDING', (2, 0), (2, -1), 10),

    # --- Estilização dos Prazos (Coluna 1 e Coluna 3) ---
    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#000000')),
    ('TEXTCOLOR', (3, 0), (3, -1), colors.HexColor('#000000')),
    ('FONTNAME', (1, 0), (1, -1), 'TrebuchetMS'),
    ('FONTNAME', (3, 0), (3, -1), 'TrebuchetMS'),
    ('FONTSIZE', (1, 0), (1, -1), 11),
    ('FONTSIZE', (3, 0), (3, -1), 11),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('ALIGN', (3, 0), (3, -1), 'CENTER'),

    # --- Ajustes Gerais de Altura Interna ---
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),    
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
    tabela_width, tabela_height = tabela_garantias.wrap(0, 0)
    # print(f"Tabela de garantias: {tabela_width} x {tabela_height}")
    tabela_garantias.drawOn(documento, (A4[0] - tabela_width) / 2, y - tabela_height - 10)

    return documento

def render_grafico_investimento(dados: dict, documento, y=A4[1]):
    # Usando a variável global de controle de altura 'y' que você já possui no seu fluxo
    
    # -------------------------------------------------------------------------
    # ESTRUTURAÇÃO DOS DADOS (X, Y)
    # -------------------------------------------------------------------------
    dados_investimento = []
    valor_acumulado = 0
    for ano in range(1, 26):
        # Cria uma curva exponencial suave simulando a imagem
        valor_acumulado += 5000 + (ano * 1300) 
        dados_investimento.append((ano, valor_acumulado))

    # -------------------------------------------------------------------------
    # CONFIGURAÇÃO DO GRÁFICO DE ÁREA
    # -------------------------------------------------------------------------
    largura_desenho = 14 * CM
    altura_desenho = 7.5 * CM
    
    d = Drawing(largura_desenho, altura_desenho)
    
    lp = LinePlot()
    lp.x = 55                   # Margem esquerda maior para os valores não cortarem
    lp.y = 40                   # Espaço inferior para os números inclinados do eixo X
    lp.width = largura_desenho - 75
    lp.height = altura_desenho - 75
    
    # Injeta os dados dentro de uma lista de séries
    lp.data = [dados_investimento]
    
    # --- Estilização da Linha e Preenchimento da Área ---
    lp.lines[0].strokeColor = Amarelo_Happy     # Linha Amarela/Ouro
    lp.lines[0].strokeWidth = 2.5

    # ATENÇÃO: Para o fillColor funcionar como área no LinePlot do ReportLab,
    # é necessário fechar o polígono da série. Aqui ativamos o fechamento
    # e definimos um preenchimento semi-transparente para aparecer como área.
    lp.lines[0].fillColor = colors.Color(26/255, 26/255, 26/255, alpha=0.15)
    
    # --- Configuração dos Marcadores (Pontos pretos com borda amarela nos nós) ---
    lp.lines[0].symbol = makeMarker('FilledCircle')
    lp.lines[0].symbol.size = 4                             # Ajustado para 4 para ficar mais sutil
    lp.lines[0].symbol.fillColor = HexColor('#1A1A1A')   # Miolo preto
    lp.lines[0].symbol.strokeColor = Amarelo_Happy          # Borda amarela
    lp.lines[0].symbol.strokeWidth = 1
    
    # --- Configuração do Eixo X (Anos de 1 a 25) ---
    lp.xValueAxis.valueMin = 1
    lp.xValueAxis.valueMax = 25
    lp.xValueAxis.valueStep = 1
    lp.xValueAxis.labels.fontName = 'TrebuchetMS'
    lp.xValueAxis.labels.fontSize = 8
    lp.xValueAxis.labels.dy = -15
    lp.xValueAxis.labels.angle = 45                  # Inclina os números em 45 graus
    
    # --- Configuração do Eixo Y (Valores de -100k a 600k) ---
    lp.yValueAxis.valueMin = -100000
    lp.yValueAxis.valueMax = 600000
    lp.yValueAxis.valueStep = 100000
    lp.yValueAxis.labels.fontName = 'TrebuchetMS'
    lp.yValueAxis.labels.fontSize = 8
    lp.yValueAxis.labels.rightPadding = 5
    # Formata o Eixo Y para exibir de forma limpa (Ex: 500k ou formato padrão)
    lp.yValueAxis.labelTextFormat = '%d' 
    
    # --- Customização das Linhas de Grade (Grid) ---
    lp.xValueAxis.visibleGrid = 1
    lp.xValueAxis.gridStrokeColor = HexColor('#A1A1A1A')
    lp.xValueAxis.gridStrokeWidth = 0.5
    
    lp.yValueAxis.visibleGrid = 1
    lp.yValueAxis.gridStrokeColor = HexColor('#A1A1A1A')
    lp.yValueAxis.gridStrokeWidth = 0.5

    # -------------------------------------------------------------------------
    # ADICIONANDO ELEMENTOS AO DRAWING
    # - Primeiro adicionamos a área preenchida (por baixo)
    # - Depois adicionamos o LinePlot (linha fica por cima)
    # - Por fim adicionamos a legenda
    # -------------------------------------------------------------------------

    # Construir polígono da área abaixo da curva (transforma dados em coordenadas do plot)
    x_min = lp.xValueAxis.valueMin
    x_max = lp.xValueAxis.valueMax
    y_min = lp.yValueAxis.valueMin
    y_max = lp.yValueAxis.valueMax

    def to_plot_coords(xv, yv):
        x_coord = lp.x + ((xv - x_min) / float(x_max - x_min)) * lp.width
        y_coord = lp.y + ((yv - y_min) / float(y_max - y_min)) * lp.height
        return x_coord, y_coord

    pontos = [to_plot_coords(xv, yv) for xv, yv in dados_investimento]
    if pontos:
        # Baseline correspondente ao eixo X (valor 0) — se 0 estiver fora do
        # intervalo do eixo Y, usamos o limite mais próximo do desenho.
        zero_value = 0
        if zero_value <= y_min:
            baseline_y = lp.y
        elif zero_value >= y_max:
            baseline_y = lp.y + lp.height
        else:
            baseline_y = lp.y + ((zero_value - y_min) / float(y_max - y_min)) * lp.height

        x_first = pontos[0][0]
        x_last = pontos[-1][0]
        poly_points = [(x_first, baseline_y)] + pontos + [(x_last, baseline_y)]
        flat = [coord for p in poly_points for coord in p]
        area = Polygon(flat, strokeColor=None, fillColor=HexColor('#1A1A1A'))
        d.add(area)

    # Adiciona o gráfico (linha) por cima da área
    d.add(lp)

    # Legenda por cima de tudo
    y_legenda = altura_desenho - 15
    x_legenda_centro = largura_desenho / 2

    d.add(Rect(x_legenda_centro - 60, y_legenda, 25, 10, fillColor=HexColor('#1A1A1A'), strokeColor=Amarelo_Happy, strokeWidth=1.5))
    d.add(String(x_legenda_centro - 25, y_legenda + 1, "Investimento", fontSize=9, fontName="TrebuchetMS", textAnchor='start'))
    
    # Desenha o gráfico no canvas
    y -= altura_desenho
    d.drawOn(documento, (A4[0] - largura_desenho) / 2, y)

    # -------------------------------------------------------------------------
    # TABELA INFERIOR DE RESUMO (Tempo de Retorno vs Economia)
    # -------------------------------------------------------------------------
    dados_resumo = [
        ["Tempo de retorno do investimento: 1\nANO E 3 MESES", f"Economia em 25 anos:\nR$ {gen_finace_data(dados).get('economia_total', 0.00)}"]
    ]
    
    tabela_resumo = Table(dados_resumo, colWidths=[largura_desenho/2]*2)
    
    tabela_resumo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#EAEAEA')),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#000000')),
        ('FONTNAME', (0, 0), (-1, -1), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBEFORE', (1, 0), (1, -1), 1.5, colors.white), # Linha divisória branca no centro
    ]))
    
    t_width, t_height = tabela_resumo.wrap(0, 0)
    y -= (t_height + 5)
    tabela_resumo.drawOn(documento, (A4[0] - t_width) / 2, y)
    
    # Retorna o y atualizado para o seu fluxo não sobrepor os próximos elementos do PDF
    return documento

def gen_finace_data(dados: dict):
    # fator_diurno, consumo_mes, TUSDgd = 0.5, 3700, 0.2 
    CONSTS=dados.get("CONSTS", {})
#    "CONSTS": {
#         "CONST_IRRAD": 139,
#         "CONST_FATOR_DIURNO": 0.5,
#         "CONST_TUSDgd": 0.2,
#         "CRECIMENTO_ANUAL_CONSUMO": 0.0081,
#         "DECRESCIMO_GERACAO": 0.15
#     },
    ano = ['1|0.6', '2|1', '3|2', '4|3', '5|4', '6|5', '7|6', '8|7', '9|8', '10|9', '11|10', '12|11', '13|12', '14|13', '15|14', '16|15', '17|16', '18|17', '19|18', '20|19', '21|20', '22|21', '23|22', '24|23', '25|24']
    fluxo_caixa_acumulado = []
    energia_gerada = [12 * dados.get('potencia_kit', 7.32) * CONSTS.get('CONST_IRRAD', 139) * (1-CONSTS.get('DECRESCIMO_GERACAO', 0.0081))**i for i in range(0, 25)]
    tarifas        = [CONSTS.get('TARIFA_INICIAL', 1.22) * ((1+CONSTS.get('TARIFA_INFLACAO_ANUAL', 0.08))**i) for i in range(0, 25)]
    consumo_ano    = [0.8 * dados.get('potencia_kit', 7.32) * CONSTS.get('CONST_IRRAD', 139) * 12*(( 1 + CONSTS.get('CRECIMENTO_ANUAL_CONSUMO', 0.2))**i) for i in range(0, 25)]
    C_geracao =[]
    for tarifa, energia, consumo in zip(tarifas, energia_gerada, consumo_ano):
        val = energia * tarifa * CONSTS.get('CONST_FATOR_DIURNO', 0.5) *  CONSTS.get('CONST_TUSDgd', 0.2)
        if energia <= consumo:
            val += +((consumo-energia)*tarifa)
        C_geracao.append(val)
    
    # print("--------------------\n",C_geracao,"\n--------------------\n")
    S_geracao = [t*c for t, c in zip(tarifas, consumo_ano)]
    
    custos = []
    for i in range(0, 25):
        monitoramewnto = (dados.get('modulos', {'quantidade': 12}).get('quantidade', 12) * dados.get('Potencia_modulos', 610) * CONSTS.get('CONST_IRRAD',139) / 2500)
        limpeza = (25 * dados.get('modulos', {'quantidade': 12}).get('quantidade', 12))
        custos.append((monitoramewnto + limpeza) * (( 1 + CONSTS.get('MANUTENCAO_INFLACAO_ANUAL', 0.03))**i))
    custos[0] = dados.get('valor', 00.00 )

    economia = [s - c for s, c in zip(S_geracao, C_geracao)]
    fluxo_caixa = [e - c for e, c in zip(economia, custos)]
    fluxo_caixa_acumulado = [sum(fluxo_caixa[0:i]) for i in range(1, 26)]

    ano_ = [2034, 2033, 2032, 2031, 2030, 2029, 2028, 2027, 2026,"Ano"]
    C_geracao_mes, S_geracao_mes = [ f"R$ {tousand_separator(e/12)}" for e in C_geracao[9::-1]], [ f"R$ {tousand_separator(e/12)}" for e in S_geracao[9::-1]]
    c_gem, s_gem = [ e/12 for e in C_geracao[9::-1]], [ e/12 for e in S_geracao[9::-1]]
    
    economia_percentual =[f'{(1-(c / s)):.2%}' for s, c in zip(s_gem, c_gem)]
    print("------------")
    print(S_geracao)
    print(s_gem)
    print("------------")
    economia_mes = [ f"R$ {tousand_separator(s-c)}" for s, c in zip(s_gem, c_gem)]
    
    C_geracao_mes.append("Com Geração")
    S_geracao_mes.append("Sem Geração")
    economia_percentual.append("Economia %")
    economia_mes.append("Economia Mensal")
    
    return {
            "dados_tabela": [[an, f"{tousand_separator(en)} kWh", f"R$ {tousand_separator(ec)}", f"R$ {tousand_separator(fl)}", f"R$ {tousand_separator(ta)}"] for an, en, ec, fl, ta in zip(ano, energia_gerada, economia, fluxo_caixa_acumulado, tarifas)],
            "comparativo": [[an, cg, sg, e_p, e_m] for an, cg, sg, e_p, e_m in zip(ano_[::-1], C_geracao_mes[::-1], S_geracao_mes[::-1], economia_percentual[::-1], economia_mes[::-1])],
            "economia_total": tousand_separator(sum(economia))}

def render_proposta_p7(dados: dict, documento):
    register_font(documento, font_name='TrebuchetMS.ttf', call='TrebuchetMS')
    register_font(documento, font_name='Trebuchet MS Bold.ttf', call='TrebuchetMS-Bold')
    documento.showPage()
    y = A4[1] - 1.61*CM - sheet_padding_top
    documento.drawImage(file_route("investimento.png"), sheet_padding_left, y, width=17.49*CM, height=1.61*CM)
    dados_investimento = [
        ('PREÇO DO SISTEMA INSTALADO: ', f"R$ {tousand_separator(dados.get('valor', '0.00'))}"),
        ('PRAZO DE INSTALAÇÃO: ', f"{dados.get('prazo_instalacao', '0')} Dias"),
        ('FORMA DE PAGAMENTO: ', dados.get('forma_pagamento', 'N/A')),
        ('CONDIÇÃO DE PAGAMENTO: ', dados.get('condicao_pagamento', 'N/A')),
        ('RETORNO DO INVESTIMENTO: ', get_pay_back(''))
    ]

    for rotulo, valor in dados_investimento:
        y -= p_LINE_HEIGHT
        documento.setFont('TrebuchetMS-Bold', 12)
        documento.drawString(sheet_padding_left, y, rotulo)
        documento.setFont('TrebuchetMS', 12)
        documento.drawString(documento.stringWidth(rotulo, 'TrebuchetMS-Bold', 12)+CM, y, valor)
    y-= (p_LINE_HEIGHT *2 + 1.67*CM)

    documento.drawImage(file_route("retorno.png"), sheet_padding_left, y, width=12.19*CM, height=1.67*CM)

    documento = render_grafico_investimento(dados, documento,y=y)

    return documento

def render_proposta_p8(dados: dict, documento):
    finace_data = gen_finace_data(dados)
    
    documento.showPage()
    y = A4[1] - 1.67*CM - sheet_padding_top
    documento.drawImage(file_route("analise.png"), sheet_padding_left, y, width=16.1*CM, height=1.67*CM)

    
    colWidths=[(1.5*CM), (A4[0]-3.5*CM)/4, (A4[0]-3.5*CM)/4, (A4[0]-3.5*CM)/4, (A4[0]-3.5*CM)/4]
    tabela = Table(finace_data.get('dados_tabela', []), colWidths=colWidths)
    cabecalho = Table([['Ano', 'Energia Gerada (kWh)', 'Economia (R$)', 'Fluxo de Caixa (R$)', 'Tarifa (R$/kWh)']],colWidths=colWidths)

    cabecalho.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#fbfbfb')),
        ('FONTNAME', (0, 0), (-1, -1), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fbfbfb')),
        ]))

    cabecalho_width, cabecalho_height = cabecalho.wrap(0, 0)
    y -= (cabecalho_height + 10)
    cabecalho.drawOn(documento, (A4[0] - cabecalho_width) / 2, y)

    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#f1f1f1")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('FONTNAME', (0, 0), (-1, 0), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black), # Linha divisória abaixo do cabeçalho
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#A1A1A1A')),
        ]))
    
    tabela_width, tabela_height = tabela.wrap(0, 0)
    y -= (tabela_height)
    tabela.drawOn(documento, (A4[0] - tabela_width) / 2, y)

    footer = Table([
        ["Tempo de retorno do investimento:","1 ANO E 3 MESES"],
        ["Economia em 25 anos: ",f"R$ {finace_data.get('economia_total', 0.00)}"]],
        colWidths=[(A4[0]-2*CM)/2, (A4[0]-2*CM)/2])
    
    footer.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.white),
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f1f1f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),]))
    
    footer_width, footer_height = footer.wrap(0, 0)
    y -= footer_height
    footer.drawOn(documento, (A4[0] - footer_width) / 2, y)
    
    comparatvo = Table(finace_data.get('comparativo', []), colWidths=[(A4[0]-2*CM)/5]*5)
    comparatvo.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1A1A1A')),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f1f1f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#fbfbfb')),
        ('FONTNAME', (0, 0), (-1, 0), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),]))
    comparativo_width, comparativo_height = comparatvo.wrap(0, 0)
    y -= (comparativo_height + p_LINE_HEIGHT)
    comparatvo.drawOn(documento, (A4[0] - comparativo_width) / 2, y)
    return documento

def render_grafico_comparativo(dados: dict, documento, y):
    labels = ['Energia Solar (16.42%)', 'CDI (1.13%)', 'Poupança (0.63%)']
    valores = [16.42, 1.13, 0.63]
    
    cor_preto = HexColor('#1A1A1A')
    cores_barras = [Amarelo_Happy, cor_preto, cor_preto] 

    largura_container, altura_container = 18.36 * CM, 7.0 * CM
    
    grafico_container = Drawing(largura_container, altura_container)
    
    # 2. Inicializa o gráfico de barras horizontais
    bc = HorizontalBarChart()
    bc.x = 4.5 * CM       # Recuo à esquerda para acomodar os textos longos dos labels
    bc.y = 0.5 * CM       # Recuo inferior para não cortar os números do eixo X
    bc.height = 5.5 * CM  # Altura útil da área do gráfico
    bc.width = 12.5 * CM  # Largura útil da área do gráfico
    
    # Injeta os dados (precisa ser uma lista de listas para o ReportLab)
    bc.data = [valores]
    
    # --- Customização das Barras e Cores ---
    bc.barSpacing = 10     # Espaçamento entre as barras
    for idx, cor in enumerate(cores_barras):
        bc.bars[0, idx].fillColor = cor
        bc.bars[0, idx].strokeColor = None # Remove bordas para ficar flat como na imagem

    # --- Configuração do Eixo Y (Categorias/Labels à esquerda) ---
    bc.categoryAxis.categoryNames = labels
    bc.categoryAxis.labels.fontName = 'TrebuchetMS'
    bc.categoryAxis.labels.fontSize = 9
    bc.categoryAxis.labels.boxAnchor = 'e'  # Alinha o texto à direita (encostado no eixo)
    bc.categoryAxis.labels.dx = -10         # Afasta um pouco o texto da linha do eixo

    # --- Configuração do Eixo X (Valores/Escala abaixo) ---
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 18
    bc.valueAxis.valueStep = 2
    bc.valueAxis.labels.fontName = 'TrebuchetMS'
    bc.valueAxis.labels.fontSize = 9
    bc.valueAxis.labels.dy = -10            # Empurra os números um pouco para baixo da linha

    # 3. Adiciona o componente gráfico ao Drawing
    grafico_container.add(bc)
    
    # 4. Calcula a posição Y na página e renderiza o gráfico no canvas (documento)
    # Posiciona logo abaixo da imagem do título, dando uma margem de segurança
    y_posicao_grafico = y - altura_container - (0.5 * CM)
    
    # IMPORTANTE: sheet_padding_left deve estar acessível no seu escopo global ou passado por parâmetro
    # Aqui assumirei que está definido ou você pode passar diretamente.
    renderPDF.draw(grafico_container, documento, 1.5 * CM, y_posicao_grafico)
    
    return documento, altura_container

def render_proposta_p9(dados: dict, documento):
    documento.showPage()
    register_font(documento, font_name='TrebuchetMS.ttf', call='TrebuchetMS')
    register_font(documento, font_name='Trebuchet MS Bold.ttf', call='TrebuchetMS-Bold')
    y = A4[1] - 1.79*CM - sheet_padding_top
    documento.drawImage(file_route("comparativo_m.png"), sheet_padding_left, y, width=18.36*CM, height=1.79*CM)

    documento, altura_grafico = render_grafico_comparativo(dados, documento, y)

    y-= (1.82*CM + p_LINE_HEIGHT + altura_grafico)
    documento.drawImage(file_route("contribuindo.png"), sheet_padding_left, y, width=16.77*CM, height=1.82*CM)

    imgs = [Image(file_route("COdois.png"), width=2.17*CM, height=2.17*CM),
            Image(file_route("arvore.png"), width=2.17*CM, height=2.17*CM),
            Image(file_route("carro.png"), width=2.17*CM, height=2.17*CM)]

    styles = getSampleStyleSheet()
    estilo_texto = ParagraphStyle(
        'TextoQuebraAutomatica',
        parent=styles['Normal'],
        fontName='TrebuchetMS',
        fontSize=10,
        leading=14,         # ESSENCIAL: Espaço entre as linhas quando o texto quebrar
        alignment=TA_CENTER # Centraliza o texto dentro do parágrafo
    )

    dados_tabela = [
        # Linha 1: Ícones (com tamanho fixo)
        imgs,  
        
        # Linha 2: Textos longos que vão quebrar automaticamente se não couberem
        [
            Paragraph("REDUÇÃO DE CO² NO AMBIENTE", estilo_texto), 
            Paragraph("TOTAL DE ÁRVORES SALVAS NO PERÍODO", estilo_texto), 
            Paragraph("REDUÇÃO DE EMISSÃO DE GASES POLUENTES POR VEÍCULOS", estilo_texto)
        ],  
        
        # Linha 3: Valores
        [
            Paragraph("78 t", estilo_texto), 
            Paragraph("2.112 Árvores", estilo_texto), 
            Paragraph("520.000 km", estilo_texto)
        ]
    ]
    tabela = Table(dados_tabela, colWidths=[(A4[0]-3*CM)/3]*3)

    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'TrebuchetMS-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),]))
    
    tabela_width, tabela_height = tabela.wrap(0, 0)
    y -= (tabela_height + p_LINE_HEIGHT*3)
    tabela.drawOn(documento, (A4[0] - tabela_width) / 2, y)
    
    return documento

def render_proposta_p10(dados: dict, documento):
    documento.showPage()
    register_font(documento, font_name='TrebuchetMS.ttf', call='TrebuchetMS')
    register_font(documento, font_name='Trebuchet MS Bold.ttf', call='TrebuchetMS-Bold')
    y = A4[1] - 1.49*CM - sheet_padding_top
    documento.drawImage(file_route("local-long.png"), sheet_padding_left, y, width=10*CM, height=1.49*CM)
    y-= (p_LINE_HEIGHT*2 + 3.12*CM)
    img = Image(file_route("pin.png"),  width=2.19*CM, height=3.12*CM )
    img.drawOn(documento, (A4[0] - 2.19*CM)/2, y)
    documento.setFont('TrebuchetMS', 12)
    
    styles = getSampleStyleSheet()
    estilo_texto = ParagraphStyle(
        'TextoQuebraAutomatica',
        parent=styles['Normal'],
        fontName='TrebuchetMS',
        fontSize=12,
        leading=16,         # ESSENCIAL: Espaço entre as linhas quando o texto quebrar
        alignment=TA_CENTER # Centraliza o texto dentro do parágrafo
    )
    endereco = Paragraph(dados.get("endereco", ""), estilo_texto)
    endereco_width, endereco_height = endereco.wrap(A4[0]-2*sheet_padding_left, 0)
    y-= (p_LINE_HEIGHT + endereco_height)
    endereco.drawOn(documento, (A4[0]-endereco_width)/2, y)
    y-= (2*p_LINE_HEIGHT + 1.84*CM)

    documento.drawImage(file_route("validade.png"), sheet_padding_left, y, width=10.7*CM, height=1.84*CM)

    Paragraphs = [
        [Paragraph('Desde já, agradecemos pela confiança. Espero que possamos trabalhar juntos para garantir a vocês todos os benefícios que a energia solar pode proporcionar.', estilo_texto)],
        [Paragraph('Para esclarecer qualquer dúvida, conte com nosso atendimento, estaremos de prontidão para você.', estilo_texto)],
        [Paragraph(f'Essa proposta tem validade de {dados.get("CONSTS", {"validade_proposta": "30 dias"}).get("validade_proposta", "30 dias")}.', estilo_texto)],
    ]
    tabela = Table(Paragraphs, colWidths=[A4[0]-2*sheet_padding_left])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'TrebuchetMS'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    tabela_width, tabela_height = tabela.wrap(0, 0)
    y-= (tabela_height + p_LINE_HEIGHT)
    tabela.drawOn(documento, (A4[0] - tabela_width) / 2, y)
    y-= (2*p_LINE_HEIGHT + 3.14*CM)
    documento.drawImage(file_route("social-midias-tag.png"), (A4[0] - 13.65*CM)/2, y, width=13.65*CM, height=3.14*CM)

    return documento

def render_proposta(dados: dict):
    if not dados:raise ValueError("Dados não pode ser vazio")

    documento = canvas.Canvas(f"proposta_{dados['id']}.pdf", pagesize=A4)
    documento = render_proposta_p1(dados, documento)
    documento = render_proposta_p2(dados, documento)
    documento = render_proposta_p3(dados, documento)
    documento = render_proposta_p4(dados, documento)
    documento = render_proposta_p5(dados, documento)
    documento = render_proposta_p6(dados, documento)
    documento = render_proposta_p7(dados, documento)
    documento = render_proposta_p8(dados, documento)
    documento = render_proposta_p9(dados, documento)
    documento = render_proposta_p10(dados, documento)
    return documento
if __name__ == "__main__":
    dados={
    "id": 1,
    "nome": "Eliel Júlio Soares da Silva",
    "endereco": "Rua das Flores, 123 - Petrolina, PE",
    "descricao": "12 MÓDULO FOTOVOLTAICO 610W - WEG BIFACIAL \n01 INVERSOR FOTOVOLTAICO SIW400G M050 W00, Monofasico 220V \nESTRUTURA DE FIXAÇÃO FIBROCIMENTO \nKIT COMPLETO DE INSTALAÇÃO",
    "data": "2024-06-01",
    "telefone": "(11) 99999-9999",
    "email": "eliel.silva@email.com",
    "potencia_kit": 7.32,
    "cidade-uf":"Petrolona-PE",
    "CONSTS": {
        "CONST_IRRAD": 139,
        "CONST_FATOR_DIURNO": 0.5,
        "CONST_TUSDgd": 0.2,
        "CRECIMENTO_ANUAL_CONSUMO": 0.2,
        "DECRESCIMO_GERACAO": 0.0081,
        "TARIFA_INICIAL": 1.22,
        "TARIFA_INFLACAO_ANUAL": 0.08,
        "MANUTENCAO_INFLACAO_ANUAL": 0.03
    },
    "valor": 16342.95,
    "garantias": {"painel": "10 anos", "inversor": "10 anos", "estrutura": "10 anos", "instalacao": "1 ano"},
    "economia_total":"errado aqui oh",
    "prazo_instalacao": 60,
    "forma_pagamento": "Financiamento Solfacil",
    "condicao_pagamento": "Entrada de 30% e o restante em 12x sem juros",
    "modulos": {"potencia": 610, "marca": "WEG", "modelo": "615 Wp - WEG BIFACIAL", "quantidade": 12, "area": 2.39*1.14},
    "inversor":{"potencia": 5.0, "marca": "WEG", "modelo": "SIW 200G M050 W00"    , "quantidade": 1, "tipo": "Monofásico"},
    "estrutura": {"tipo": "Fibrocimento", "marca": "WEG", "quantidade": 12},
    "CONSUMO_MES_INICIAL": 800,
    "validade_proposta": "30 dias"
    }

    render_proposta(dados).save()