# Grilla v3: planilla limpia (sin Día/Mes), calendario legible por mes, tráiler, Chapu y 4 videos prioritarios.
import openpyxl, datetime as dt
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter as L

v2 = openpyxl.load_workbook('GRILLA_EL_QUISCO_KHISKA_v2.xlsx')
g = v2['Grilla']; hdr = {c.value: c.column for c in g[4]}
def val(r, k): return g.cell(r, hdr[k]).value
quita = lambda s: (s or '').replace('“', '').replace('”', '').strip()

filas = []
for r in range(5, 44):
    filas.append(dict(fecha=val(r, 'Fecha'), canal=val(r, 'Canal'), formato=val(r, 'Formato'), pieza=quita(val(r, 'Nombre de la pieza')),
                      persona=val(r, 'Audiencia').replace(' (escapada)', '').replace(' (vecino mayor)', '').replace(' (joven local)', '').replace(' (oficios)', '').replace(' · ', ', ').replace('Todas las personas', 'Todos'),
                      objetivo=val(r, 'Objetivo'), copy=val(r, 'Copy'), cta=val(r, 'CTA'), hashtags=val(r, 'Hashtags'), destino=val(r, 'Destino'),
                      tipo=val(r, 'Orgánico / Pagado'), inversion=val(r, 'Inversión (CLP)') or 0, kpi=val(r, 'KPI'), estado=val(r, 'Estado'),
                      produccion=g.cell(r, 20).value or '', guion=g.cell(r, 21).value or '', link=val(r, 'Link de archivo') or ''))

D = lambda d, m: dt.datetime(2027, m, d)
def por_fecha(d): return next(f for f in filas if f['fecha'] == d)

# Tráiler reemplaza al manifiesto del 01/07
t = por_fecha(D(1, 7))
t.update(formato='Reel tráiler', pieza='Tráiler de campaña: El Quisco no termina en la playa', guion='V01',
         copy='El Quisco no termina en la playa. Tiene humedal, quebradas, miradores, memoria y sabores de caleta, y desde hoy una forma nueva de recorrerlo: Khiska. Una ruta, una flor. Pincha tu curiosidad.',
         produccion='Video sin grabar con voz IA que lee el texto en pantalla, igual que el reel V00. Es la presentación de la campaña (portal y examen).')

# Diferenciar piezas que se repetían
por_fecha(D(29, 7)).update(copy='Primero fue la curiosidad. Después, el camino. Al final, una flor. Pronto te contamos cómo se abre la primera.', cta='Activa las notificaciones')
por_fecha(D(22, 9)).update(copy='Julio despertó la curiosidad, agosto la llevó al camino y septiembre abrió las primeras flores. El Quisco sigue ahí, fuera del verano. ¿Qué parte quieres descubrir ahora?')
por_fecha(D(19, 9)).update(copy='Tres razones para volver a El Quisco en invierno: menos gente en los senderos, una agenda que sigue después del verano y rutas que todavía no recorres.')

# Chapu (propuesta para Community Manager, sujeta a acuerdo)
CH = 'PROPUESTA sujeta a acuerdo con Francisco "Chapu" Puelles. Él graba con su celular; nosotros entregamos guion y gráficas. Honorario o canje por definir (impacta el presupuesto).'
filas += [
 dict(fecha=D(6, 7), canal='Instagram', formato='Reel colaborativo', pieza='Chapu: lo que no se ve desde la playa', persona='Vale, Camila',
      objetivo='Sumar una voz conocida que vive el territorio', copy='Chapu conoce El Quisco más allá de la playa: el mar para el surf, las rocas para escalar y los lugares que pocos nombran. Hoy nos cuenta cuál es su rincón favorito. ¿Cuál es el tuyo?',
      cta='Cuéntanos tu rincón', hashtags='#ElQuisco #DondeLaNaturalezaTieneNombre #Khiska #PinchaTuCuriosidad', destino='Portal · Lugares', tipo='Orgánico', inversion=0,
      kpi='Alcance y comentarios', estado='Idea', produccion=CH, guion='V17', link=''),
 dict(fecha=D(13, 8), canal='Instagram', formato='Reel colaborativo', pieza='Chapu hace la primera ruta Khiska', persona='Vale, Camila, Visitante habitual',
      objetivo='Mostrar una ruta completa con alguien real', copy='Chapu eligió su ruta, la preparó con la ficha y la recorrió de principio a fin. Al terminar, abrió la primera flor de su Khiska. Tu turno.',
      cta='Elige tu ruta', hashtags='#ElQuisco #DondeLaNaturalezaTieneNombre #HazFlorecerTuKhiska #Khiska', destino='App · P3 Rutas', tipo='Orgánico', inversion=0,
      kpi='Rutas iniciadas desde la pieza', estado='Idea', produccion=CH + ' Solo con la ruta piloto confirmada.', guion='V18', link=''),
]
filas.sort(key=lambda f: f['fecha'])
PRIOR = {'V01', 'V00', 'V07', 'V12'}

# ---------- estilos ----------
VERDE, ROSA, PAPEL, SALVIA = 'FF3F6B3A', 'FFEE7F8E', 'FFFAF7EE', 'FFE3EBDC'
fill = lambda c: PatternFill('solid', fgColor=c)
fH = Font(name='Arial', size=10, bold=True, color='FFFFFFFF'); fB = Font(name='Arial', size=10, color='FF1E1E1E')
fT = Font(name='Arial', size=16, bold=True, color='FF263B17'); fBold = Font(name='Arial', size=10, bold=True, color='FF1E1E1E')
lin = Side(style='thin', color='FFE3DDD0'); BR = Border(top=lin, bottom=lin, left=lin, right=lin)
W = Alignment(wrap_text=True, vertical='top'); C = Alignment(horizontal='center', vertical='center', wrap_text=True)

wb = openpyxl.Workbook()
# ---------- Grilla ----------
gs = wb.active; gs.title = 'Grilla'
gs['A1'] = 'Grilla de contenidos · El Quisco: donde la naturaleza tiene nombre'; gs['A1'].font = fT
cols = [('Fecha', 'fecha', 12), ('Fase', None, 15), ('Canal', 'canal', 15), ('Formato', 'formato', 17), ('Pieza', 'pieza', 32),
        ('Para quién', 'persona', 22), ('Objetivo', 'objetivo', 24), ('Copy', 'copy', 62), ('CTA', 'cta', 20), ('Hashtags', 'hashtags', 30),
        ('Lleva a', 'destino', 20), ('Orgánico / Pagado', 'tipo', 12), ('Inversión (CLP)', 'inversion', 13), ('KPI', 'kpi', 20),
        ('Estado', 'estado', 12), ('Cómo se produce', 'produccion', 44), ('Guion', 'guion', 8), ('Archivo', 'link', 26)]
HR = 3
for i, (n, k, w) in enumerate(cols, 1):
    c = gs.cell(HR, i, n); c.font = fH; c.fill = fill(VERDE); c.alignment = C; gs.column_dimensions[L(i)].width = w
gs.row_dimensions[HR].height = 30
for r, f in enumerate(filas, HR + 1):
    for i, (n, k, w) in enumerate(cols, 1):
        if n == 'Fase':
            v = f'=IF(A{r}="","",IF(MONTH(A{r})=7,"Despertar",IF(MONTH(A{r})=8,"Recorrer",IF(MONTH(A{r})=9,"Florecer y volver",""))))'
        else:
            v = f[k]
        c = gs.cell(r, i, v); c.font = fBold if n in ('Fecha', 'Pieza') else fB; c.alignment = W; c.border = BR
        if n == 'Fecha': c.number_format = 'dd/mm/yyyy'
        if n == 'Inversión (CLP)': c.number_format = '$#,##0'
    if f['guion'] in PRIOR:
        gs.cell(r, 17).fill = fill(ROSA); gs.cell(r, 17).font = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
LAST = 200
gs.freeze_panes = gs.cell(HR + 1, 6); gs.auto_filter.ref = f'A{HR}:{L(len(cols))}{HR + len(filas)}'
gs.sheet_view.showGridLines = False
for rng, opts in [('C', 'Instagram,Instagram Stories,Facebook,TikTok,YouTube,YouTube Shorts,Sitio web'), ('L', 'Orgánico,Pagado'),
                  ('O', 'Idea,En diseño,Listo,Programado,Publicado')]:
    dv = DataValidation(type='list', formula1=f'"{opts}"', allow_blank=True); dv.add(f'{rng}{HR+1}:{rng}{LAST}'); gs.add_data_validation(dv)
for estado, color in [('Idea', 'FFF3EEE1'), ('En diseño', 'FFFFF3CC'), ('Listo', SALVIA), ('Programado', 'FFD6EEF8'), ('Publicado', 'FFA7BE9F')]:
    gs.conditional_formatting.add(f'O{HR+1}:O{LAST}', FormulaRule(formula=[f'$O{HR+1}="{estado}"'], fill=fill(color)))
gs.conditional_formatting.add(f'L{HR+1}:M{LAST}', FormulaRule(formula=[f'$L{HR+1}="Pagado"'], fill=fill('FFFBE3E6')))
gs['A2'] = 'Los guiones en rosado son los 4 videos que se producen primero.'; gs['A2'].font = Font(name='Arial', size=9, italic=True, color='FF4A4A42')

RG = lambda col: f'Grilla!${col}${HR+1}:${col}${LAST}'

# ---------- Panel ----------
p = wb.create_sheet('Panel', 0)
p['B1'] = 'Panel de la campaña'; p['B1'].font = fT; p.sheet_view.showGridLines = False
p.column_dimensions['A'].width = 3
for i, w in enumerate([22, 13, 13, 15, 13, 16], 2): p.column_dimensions[L(i)].width = w
kp = [('Publicaciones', f'=COUNT({RG("A")})'), ('Publicadas', f'=COUNTIF({RG("O")},"Publicado")'),
      ('Listas', f'=COUNTIF({RG("O")},"Listo")+COUNTIF({RG("O")},"Programado")'), ('Con pauta', f'=COUNTIF({RG("L")},"Pagado")'),
      ('Inversión en pauta', f'=SUM({RG("M")})')]
for i, (n, fml) in enumerate(kp, 2):
    a = p.cell(3, i, n); a.font = fH; a.fill = fill(VERDE); a.alignment = C
    b = p.cell(4, i, fml); b.font = Font(name='Arial', size=18, bold=True, color='FF263B17'); b.alignment = C; b.border = BR
p['F4'].number_format = '$#,##0'
canales = ['Instagram', 'Instagram Stories', 'Facebook', 'TikTok', 'YouTube', 'YouTube Shorts', 'Sitio web']
for i, n in enumerate(['Canal', 'Julio', 'Agosto', 'Septiembre', 'Total', 'Pagadas'], 2):
    c = p.cell(6, i, n); c.font = fH; c.fill = fill(VERDE); c.alignment = C
for j, ch in enumerate(canales + ['Total'], 7):
    p.cell(j, 2, ch).font = fBold
    for k, m in enumerate([7, 8, 9], 3):
        v = (f'=COUNTIFS({RG("C")},$B{j},{RG("A")},">="&DATE(2027,{m},1),{RG("A")},"<"&DATE(2027,{m+1},1))' if ch != 'Total' else f'=SUM({L(k)}7:{L(k)}13)')
        p.cell(j, k, v)
    p.cell(j, 6, f'=SUM(C{j}:E{j})')
    p.cell(j, 7, f'=COUNTIFS({RG("C")},$B{j},{RG("L")},"Pagado")' if ch != 'Total' else '=SUM(G7:G13)')
    for k in range(2, 8): p.cell(j, k).border = BR; p.cell(j, k).font = fBold if (ch == 'Total' or k == 2) else fB

# ---------- Calendario (legible por mes, una pieza por día) ----------
cal = wb.create_sheet('Calendario', 2); cal.sheet_view.showGridLines = False
cal['A1'] = 'Calendario de publicaciones · julio a septiembre de 2027'; cal['A1'].font = fT
for i in range(1, 8): cal.column_dimensions[L(i)].width = 24
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
r = 3
for m, nombre, fase in [(7, 'Julio', 'Despertar'), (8, 'Agosto', 'Recorrer'), (9, 'Septiembre', 'Florecer y volver')]:
    cal.cell(r, 1, f'{nombre} 2027 · {fase}').font = Font(name='Arial', size=13, bold=True, color='FF263B17'); r += 1
    for i, d in enumerate(dias, 1):
        c = cal.cell(r, i, d); c.font = fH; c.fill = fill(VERDE); c.alignment = C
    r += 1
    d0 = dt.date(2027, m, 1); start = d0 - dt.timedelta(days=d0.weekday()); day = start
    while day.month <= m or (day.month == 12 and m == 1):
        if day > dt.date(2027, m, 28) and day.month != m and day.weekday() == 0: break
        for i in range(7):
            cur = day + dt.timedelta(days=i); c = cal.cell(r, i + 1)
            if cur.month == m:
                ref = f'DATE({cur.year},{cur.month},{cur.day})'
                c.value = (f'={cur.day}&IFERROR(CHAR(10)&INDEX({RG("C")},MATCH({ref},{RG("A")},0))&" · "&INDEX({RG("D")},MATCH({ref},{RG("A")},0))'
                           f'&CHAR(10)&INDEX({RG("E")},MATCH({ref},{RG("A")},0)),"")')
                c.fill = fill(PAPEL)
                cal.conditional_formatting.add(c.coordinate, FormulaRule(formula=[f'COUNTIF({RG("A")},{ref})>0'], fill=fill(SALVIA)))
            c.alignment = W; c.border = BR; c.font = fB
        cal.row_dimensions[r].height = 70
        day += dt.timedelta(days=7); r += 1
        if day.month != m and day > dt.date(2027, m, 1): break
    r += 1

# ---------- Guiones y estilo: copiar de v2 y sumar V17-V18 ----------
for nombre in ['Guiones de video', 'Estilo de video']:
    src = v2[nombre]; dst = wb.create_sheet(nombre); dst.sheet_view.showGridLines = False
    for row in src.iter_rows():
        for c in row:
            if c.value is None and not c.has_style: continue
            n = dst.cell(c.row, c.column, quita(c.value) if isinstance(c.value, str) else c.value)
            if c.has_style: n.font = c.font.copy(); n.fill = c.fill.copy(); n.alignment = c.alignment.copy(); n.border = c.border.copy()
    for k, d in src.column_dimensions.items(): dst.column_dimensions[k].width = d.width
    dst.freeze_panes = src.freeze_panes
gsv = wb['Guiones de video']
for r in range(5, gsv.max_row + 1):
    if gsv.cell(r, 1).value == 'V01':
        for col, v in [(4, 'Tráiler de campaña: El Quisco no termina en la playa'), (5, '35 s'), (9, 'Voz IA que lee el texto en pantalla + música (igual que V00)'),
                       (7, 'Pregunta → playa ilustrada que se abre por capas: humedal, quebrada, mirador, caleta (un cartel por lugar) → "y desde hoy, una forma nueva de recorrerlo" → cactus Khiska → "Una ruta. Una flor." → 3 destellos del portal y la app (catálogo, ficha, Mi Khiska) → "Pincha tu curiosidad".')]:
            gsv.cell(r, col).value = v
    if gsv.cell(r, 1).value in PRIOR:
        gsv.cell(r, 1).fill = fill(ROSA); gsv.cell(r, 1).font = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
    if gsv.cell(r, 9).value == 'Música': gsv.cell(r, 9).value = 'Voz IA que lee el texto en pantalla + música'
base = gsv.max_row
for i, fila in enumerate([
    ('V17', '06/07/2027', 'Instagram · Reel colaborativo', 'Chapu: lo que no se ve desde la playa', '30 s', 'Lo grabe Chapu: "¿Sabías que El Quisco no termina en la playa?"',
     'Chapu muestra su rincón favorito (mar, rocas para escalar) con su celular. Nosotros agregamos carteles con el estilo de la campaña y el cierre estándar.', 'Cierre estándar', 'Voz real de Chapu', 'Material que él graba', 'Propuesta'),
    ('V18', '13/08/2027', 'Instagram · Reel colaborativo', 'Chapu hace la primera ruta Khiska', '40 s', 'Lo grabe Chapu: "Hoy hago mi primera ruta Khiska"',
     'Elige ruta en la app → ficha → recorrido → final con la flor abriéndose en su Mi Khiska (captura real).', 'Cierre estándar', 'Voz real de Chapu', 'Material que él graba + app P3-P7', 'Propuesta, solo con ruta piloto')], 1):
    for j, v in enumerate(fila, 1):
        c = gsv.cell(base + i, j, v); c.font = fBold if j == 1 else fB; c.alignment = W; c.border = BR

wb.active = wb.sheetnames.index('Grilla')
wb.save('GRILLA_EL_QUISCO_KHISKA.xlsx'); print(wb.sheetnames, len(filas))
