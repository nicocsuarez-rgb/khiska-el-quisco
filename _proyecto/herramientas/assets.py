import os,glob
from PIL import Image
import numpy as np
A='/mnt/user-data/attachments/816fe078-ff18-5368-a461-e153fd58064f/'
O='/home/claude/sitio-web/assets/'
def src(key): return glob.glob(A+'*'+key+'*')[0]
def save(im,path,w=None,q=78,fmt='webp'):
    im=im.convert('RGBA') if fmt=='png' or im.mode=='RGBA' else im.convert('RGB')
    if w and im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    p=O+path
    if fmt=='webp': im.save(p,'WEBP',quality=q,method=6)
    else: im.save(p,'PNG',optimize=True)
    print(p,im.size,os.path.getsize(p)//1024,'KB')
def trim(im,pad=20,thr=25):
    g=np.asarray(im.convert('L')).astype(int);bg=np.median(g[:4,:])
    ys,xs=np.where(g<bg-thr)
    return im.crop((max(xs.min()-pad,0),max(ys.min()-pad,0),min(xs.max()+pad,im.width),min(ys.max()+pad,im.height)))
def transparent(im,lo=18,hi=60):
    a=np.asarray(im.convert('RGB')).astype(float)
    bg=np.median(a[:4,:4].reshape(-1,3),0)
    d=np.sqrt(((a-bg)**2).sum(2))
    al=np.clip((d-lo)/(hi-lo),0,1)*255
    out=np.dstack([a,al]).astype('uint8')
    return Image.fromarray(out,'RGBA')
# Territorios (ilustraciones)
terr={'el-batro':'humedal_costero','las-petras':'quebrada_costera','mirador-neptuno':'mirador_costero','isla-negra':'iteraria_costera','el-totoral':'paisaje_rural','caleta':'experiencia_gastron'}
for k,v in terr.items():
    im=Image.open(src(v));save(im,f'img/territorio-{k}.webp',1200);save(im,f'img/territorio-{k}-card.webp',640,q=74)
# Logo
lg=trim(Image.open(src('logotipo_tur')),pad=10)
t=transparent(lg);save(t,'img/logo-el-quisco.png',900,fmt='png');save(t,'img/logo-el-quisco.webp',900,q=85)
# Cactus
hero=Image.open(src('e39663e2'));save(trim(hero,40),'img/cactus-khiska-tres-flores.webp',900,q=80)
full=Image.open(src('cactus_artesanal_completo'));save(trim(full,40),'img/cactus-khiska-florecido.webp',900,q=80)
tri=Image.open(src('mismo_cactus'));w=tri.width//3
one=tri.crop((0,0,w+20,tri.height));save(trim(one,30),'img/cactus-khiska-una-flor.webp',500,q=80)
save(trim(Image.open(src('cactus_con_una_flor_abierta_y_una_banderola')),30),'img/cactus-banderola.webp',500,q=80)
save(trim(Image.open(src('cactus_nativo_costero')),30),'img/cactus-nativo-costero.webp',600,q=80)
save(trim(Image.open(src('capullo_cerrado_acompa')),30),'img/capullo-hoja.webp',400,q=80)
# Estados de flor
for k,v in {'capullo':'capullo_cerrado_de_flor','parcial':'flor_de_cactus_parcialmente','abierta':'flor_de_cactus_completamente_abierta.','beneficio':'lor_de_cactus_completamente_abierta_con'}.items():
    im=trim(Image.open(src(v)),25);im=transparent(im,10,45);save(im,f'img/flor-{k}.webp',360,q=82)
save(trim(Image.open(src('sello_circular')),20),'img/sello-ruta-completada.webp',420,q=80)
save(Image.open(src('tarjeta_digital_vertical')),'img/pasaporte-khiska.webp',600,q=80)
save(Image.open(src('patr_n_repetible')).crop((0,0,768,768)),'img/patron-espinas.webp',500,q=60)
save(Image.open(src('franja_horizontal')),'img/franja-territorio.webp',1376,q=72)
save(Image.open(src('fondo_abstracto')),'img/fondo-agenda.webp',1408,q=65)
save(Image.open(src('marco_visual_artesanal')),'img/marco-instagram.webp',700,q=75)
save(Image.open(src('ilustraci_n_circular_peque')),'img/avatar-cuenta.webp',200,q=80)
save(Image.open(src('capa_gr_fica')),'img/capa-papel.webp',900,q=60)
save(Image.open(A+'c46e2d91-9.png').convert('RGB').crop((0,250,5400,1300)),'img/sendero-ilustrado.webp',2000,q=70)
# Iconos
ag=Image.open(src('cuatro__conos_lineales'))
for n,(a,b,c,d) in zip(['calendario','reloj','ubicacion','flor'],[(107,254,349,512),(441,257,696,517),(783,246,955,522),(1040,261,1299,509)]):
    im=transparent(ag.crop((a-12,b-12,c+12,d+12)),10,50);save(im,f'icons/icono-{n}.png',128,fmt='png')
di=Image.open(src('_conos_bot_nicos_de_dificultad'))
for n,(a,b,c,d) in zip(['hoja','sendero','rocas'],[(173,247,382,519),(592,249,833,516),(981,284,1267,484)]):
    im=transparent(di.crop((a-12,b-12,c+12,d+12)),10,50);save(im,f'icons/icono-{n}.png',128,fmt='png')
ri=Image.open(src('contenedores_circulares'));im=transparent(ri.crop((65,34,384,394)),10,50);save(im,'icons/aro-red-social.png',160,fmt='png')
# favicon desde flor abierta
f=trim(Image.open(src('flor_de_cactus_completamente_abierta.')),5);f=transparent(f,10,45)
s=max(f.size);c=Image.new('RGBA',(s,s),(0,0,0,0));c.paste(f,((s-f.width)//2,(s-f.height)//2))
c.resize((180,180),Image.LANCZOS).save(O+'icons/apple-touch-icon.png');c.resize((48,48),Image.LANCZOS).save(O+'icons/favicon.png')
# OG image 1200x630
og=Image.new('RGB',(1200,630),(250,247,238))
t2=t.copy();t2.thumbnail((620,300));og.paste(t2,(60,165),t2)
hc=transparent(trim(hero,40),12,50);hc.thumbnail((470,560));og.paste(hc,(1200-hc.width-50,(630-hc.height)//2),hc)
og.save(O+'img/og-el-quisco.jpg',quality=82);print('og ok')
