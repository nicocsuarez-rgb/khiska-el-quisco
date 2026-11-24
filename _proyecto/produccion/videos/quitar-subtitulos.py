# Quita los subtítulos quemados de V01, V07 y V12 sin volver a renderizar.
# Uso (desde la raíz del repo): python3 _proyecto/produccion/videos/quitar-subtitulos.py <carpeta de trabajo> v01 v01-trailer
# Necesita en <carpeta>/sinsubs/: <vXX>-plate.png (fondo de papel limpio) y plan.json (= cajas-subtitulos.json).
# Tapa cada caja con el papel de fondo solo si alrededor hay papel (no toca ilustraciones que crucen) y corrige sombras.
# Los originales con subtítulos están en el historial de git (commit 2a6ba16).
import json,subprocess,sys,numpy as np
from PIL import Image
S,k,v=sys.argv[1],sys.argv[2],sys.argv[3]
Y0=1440; W,H=1080,1920
plate=np.asarray(Image.open(f'{S}/sinsubs/{k}-plate.png').convert('RGB')).astype(np.int16)
plan=json.load(open(f'{S}/sinsubs/plan.json'))[k]
subs=json.load(open(f'_proyecto/produccion/videos/{k}/subtitulos.json'))
rects=[(s['start']-0.25,s['end']+0.25,c['x']-4,c['y']-4,c['w']+8,c['h']+8) for s,c in zip(subs,plan)]
dec=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',f'assets/video/{v}.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-i',f'assets/video/{v}.mp4',
  '-map','0:v','-map','1:a','-c:v','libx264','-preset','slow','-crf','22','-maxrate','5M','-bufsize','10M','-pix_fmt','yuv420p','-c:a','copy','-shortest','-movflags','+faststart',f'{S}/sinsubs/{v}.mp4'],stdin=subprocess.PIPE)
n=0; tapados=0; saltados=[]
while True:
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    f=np.frombuffer(buf,np.uint8).reshape(H,W,3).copy(); t=n/30
    for a,b,x,y,w,h in rects:
        if not (a<=t<=b): continue
        x0,y0,x1,y1=max(0,x),max(0,y),min(W,x+w),min(plate.shape[0]-1,y+h)
        reg=f[Y0+y0:Y0+y1,x0:x1].astype(np.int16); pl=plate[y0:y1,x0:x1]
        if np.abs(reg-pl).mean()<2: continue  # no hay nada que tapar
        # anillo de 8 px alrededor: debe ser papel limpio
        R0,R1,C0,C1=max(0,y0-8),min(plate.shape[0],y1+8),max(0,x0-8),min(W,x1+8)
        ring=f[Y0+R0:Y0+R1,C0:C1].astype(np.int16)-plate[R0:R1,C0:C1]
        m=np.ones(ring.shape[:2],bool); m[y0-R0:y1-R0,x0-C0:x1-C0]=False
        rd=ring[m].astype(np.float32)
        if np.abs(rd).mean()<30 and rd.std()<9:
            # corrección suave (sombras) desde los 4 bordes: parche de Coons, calza en todo el contorno
            P=plate.shape[0]
            def lado(fs,ps): return (fs.astype(np.float32)-ps).mean(axis=0)
            top=(f[Y0+y0-4:Y0+y0,x0:x1].astype(np.float32)-plate[y0-4:y0,x0:x1]).mean(0)
            yb=min(P,y1+4); bot=(f[Y0+y1:Y0+yb,x0:x1].astype(np.float32)-plate[y1:yb,x0:x1]).mean(0) if yb>y1 else top.copy()
            xl=max(0,x0-4); left=(f[Y0+y0:Y0+y1,xl:x0].astype(np.float32)-plate[y0:y1,xl:x0]).mean(1) if x0>xl else None
            xr=min(W,x1+4); right=(f[Y0+y0:Y0+y1,x1:xr].astype(np.float32)-plate[y0:y1,x1:xr]).mean(1) if xr>x1 else None
            def suav(v,k):
                ker=np.ones(k)/k; return np.stack([np.convolve(np.pad(v[:,c],k//2,mode='edge'),ker,'valid') for c in range(3)],1)
            top=suav(top,15); bot=suav(bot,15)
            hh,ww=y1-y0,x1-x0
            if left is None: left=np.linspace(top[0],bot[0],hh)
            if right is None: right=np.linspace(top[-1],bot[-1],hh)
            left=suav(left,9); right=suav(right,9)
            u=np.linspace(0,1,ww)[None,:,None]; v=np.linspace(0,1,hh)[:,None,None]
            Lv=(1-v)*top[None]+v*bot[None]; Lh=(1-u)*left[:,None]+u*right[:,None]
            Bc=(1-u)*(1-v)*top[0]+u*(1-v)*top[-1]+(1-u)*v*bot[0]+u*v*bot[-1]
            off=np.nan_to_num(Lv+Lh-Bc)
            f[Y0+y0:Y0+y1,x0:x1]=np.clip(plate[y0:y1,x0:x1]+off,0,255).astype(np.uint8); tapados+=1
        else: saltados.append(round(t,2))
    enc.stdin.write(f.tobytes()); n+=1
enc.stdin.close(); enc.wait(); dec.wait()
print(v,"cuadros",n,"tapados",tapados,"sin tocar:",len(saltados),sorted(set(round(x,1) for x in saltados)))
