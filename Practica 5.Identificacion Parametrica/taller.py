import numpy as np, pandas as pd, json, warnings
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq


REAL="#444444"; P1="#2a6fdb"; P2="#d9731a"; P3="#2a9d5c"
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.alpha":.25,"figure.dpi":130})
R={}
def load(s):
    d=pd.read_csv(f"/mnt/user-data/uploads/Set{s}.csv"); return [d[c].values for c in "t u y uv yv".split()]
def sinus(t,a,f): return a*np.sin(2*np.pi*f*t)

def fft_plot(s,t,y,fn,ok,label):
    Ts=np.mean(np.diff(t)); N=len(y); yf=fft(y); xf=fftfreq(N,Ts)[:N//2]; a=2/N*np.abs(yf[:N//2])
    fig,ax=plt.subplots(figsize=(8,3.2)); ax.plot(xf,a,color=P1,lw=1.2)
    ax.axvspan(*ok,color="#2a9d5c",alpha=.08,label=f"Banda de la señal (0–{ok[1]} Hz)")
    i=np.argmax(np.where(xf>ok[1],a,0)); ax.annotate(f"Ruido: {xf[i]:.0f} Hz\nA≈{a[i]:.3f}",(xf[i],a[i]),(xf[i]-0.25*xf.max(),max(a)*0.45),arrowprops=dict(arrowstyle="->",color=P2),color=P2)
    ax.set_xlabel("Frecuencia (Hz)"); ax.set_ylabel("Amplitud"); ax.set_title(f"FFT de y – {label}"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(f"out/{fn}.png",bbox_inches="tight"); plt.close(fig)
    return xf[i],a[i]

def pred_plot(fn,title,t,y,preds,fits):
    fig,ax=plt.subplots(figsize=(8,3.2)); ax.plot(t,y,color=REAL,lw=1.6,label="Salida real y")
    for (lab,yp,c,ls),fv in zip(preds,fits): ax.plot(t,yp,color=c,lw=1.1,ls=ls,label=f"{lab} (FIT {fv:.2f} %)")
    ax.set_xlabel("t (s)"); ax.set_ylabel("Salida"); ax.set_title(title); ax.legend(frameon=False,fontsize=8,loc="upper center",bbox_to_anchor=(0.5,-0.22),ncol=3); fig.tight_layout(); fig.savefig(f"out/{fn}.png",bbox_inches="tight"); plt.close(fig)

# ---------------- SET A ----------------
t,u,y,uv,yv=load("A"); Ts=0.01
fa,aa=fft_plot("A",t,y,"fft_A",(0,6),"Set A"); R["A_noise"]=(fa,aa)
e=sinus(t,0.2,20); ev=sinus(t,0.2,20)
B,F=oe(y,u,2,3,1); R["A_OE231"]=dict(B=B.tolist(),F=F.tolist())
yp=sim_dlsim(B,F,u,Ts)+e; fit5=fit_percent(y,yp); R["A_OE_fit_eval"]=fit5
pred_plot("p5_A_oe","Punto 5 – OE(2,3,1) en el Set A (evaluación)",t,y,[("OE(2,3,1)+e(t)",yp,P1,"--")],[fit5])
Bm,Am,Cm=armax(y,u,2,2,2,1); R["A_ARMAX2221"]=dict(B=Bm.tolist(),A=Am.tolist(),C=Cm.tolist())
ypm=sim_dlsim(Bm,Am,u,Ts)+sim_dlsim(Cm,Am,e,Ts); fit6=fit_percent(y,ypm); R["A_ARMAX_fit_eval"]=fit6
R["A_ARMAX_fit_eval_sin_e"]=fit_percent(y,sim_dlsim(Bm,Am,u,Ts))
ypm_end=sim_dlsim(Bm,Am,u,Ts)+e; R["A_ARMAX_fit_eval_e_al_final"]=fit_percent(y,ypm_end)
pred_plot("p6_A_armax","Punto 6 – OE(2,3,1) vs ARMAX(2,2,2,1) en el Set A",t,y,[("OE(2,3,1)",yp,P1,"--"),("ARMAX(2,2,2,1)",ypm,P2,":")],[fit5,fit6])
ypv=sim_dlsim(B,F,uv,Ts)+ev; fit7=fit_percent(yv,ypv); R["A_OE_fit_val"]=fit7
pred_plot("p7_A_val","Punto 7 – OE(2,3,1) en validación (uv, yv)",t,yv,[("OE(2,3,1)+e(t)",ypv,P1,"--")],[fit7])

# ---------------- SET B ----------------
t,u,y,uv,yv=load("B")
fb,ab=fft_plot("B",t,y,"fft_B",(0,12),"Set B"); R["B_noise"]=(fb,ab)
e=sinus(t,0.15,35)
B1,A1=arx(y,u,2,1,1); B2,F2=oe(y,u,1,2,1); B3,C3,D3,F3=bj(y,u,1,0,0,2,1)
R["B_ARX211"]=dict(B=B1.tolist(),A=A1.tolist()); R["B_OE121"]=dict(B=B2.tolist(),F=F2.tolist()); R["B_BJ10021"]=dict(B=B3.tolist(),F=F3.tolist(),C=C3.tolist(),D=D3.tolist())
def predB(x):
    return {"ARX":sim_dlsim(B1,A1,x,Ts),"OE":sim_dlsim(B2,F2,x,Ts),"BJ":sim_dlsim(B3,F3,x,Ts)}
pe=predB(u); pv=predB(uv)
errs={"ARX":lambda e:sim_dlsim([1],A1,e,Ts),"OE":lambda e:e,"BJ":lambda e:sim_dlsim(C3,D3,e,Ts)}
fitsB={}
for k in pe:
    fitsB[k]=(fit_percent(y,pe[k]+errs[k](e)),fit_percent(yv,pv[k]+errs[k](e)))
R["B_fits"]=fitsB
for k,c,ls,name in [("ARX",P2,":","ARX(2,1,1)"),("OE",P1,"--","OE(1,2,1)"),("BJ",P3,"-.","BJ(1,0,0,2,1)")]:
    pass
fig,axs=plt.subplots(3,1,figsize=(8,7.2),sharex=True)
for ax,(k,c,ls,name) in zip(axs,[("ARX",P2,"-","ARX(2,1,1)"),("OE",P1,"-","OE(1,2,1)"),("BJ",P3,"-","BJ(1,0,0,2,1)")]):
    ax.plot(t,y,color=REAL,lw=1.6,label="Salida real y"); ax.plot(t,pe[k]+errs[k](e),color=c,lw=1.1,ls="--",label=f"{name} (FIT eval {fitsB[k][0]:.2f} %)")
    ax.legend(frameon=False,fontsize=8,loc="lower right"); ax.set_ylabel("Salida")
axs[-1].set_xlabel("t (s)"); axs[0].set_title("Punto 10 – Set B: ARX vs OE vs BJ (evaluación)"); fig.tight_layout(); fig.savefig("out/p10_B.png"); plt.close(fig)

# ---------------- SET C ----------------
t,u,y,uv,yv=load("C")
fc,ac=fft_plot("C",t,y,"fft_C",(0,5),"Set C"); R["C_noise"]=(fc,ac)
e=sinus(t,0.1,10)
def oe_eval(o,y,u,uv,yv,e):
    r=oe_robust(y,u,*o)
    if r is None: return None
    B,F=r
    return dict(B=B.tolist(),F=F.tolist(),ncoef=int(o[0]+1+o[1]),fit_eval=fit_percent(y,sim_dlsim(B,F,u,Ts)+e),fit_val=fit_percent(yv,sim_dlsim(B,F,uv,Ts)+e),yp=sim_dlsim(B,F,u,Ts)+e,ypv=sim_dlsim(B,F,uv,Ts)+e)
C={}
for o in [(1,1,1),(1,2,1),(3,3,1),(1,2,2),(1,2,3)]:
    C[o]=oe_eval(o,y,u,uv,yv,e)
    R[f"C_OE{o}"]={k:v for k,v in C[o].items() if k not in("yp","ypv")} if C[o] else "sin solución estable"
fig,ax=plt.subplots(figsize=(8,3.2)); ax.plot(t,y,color=REAL,lw=1.6,label="Salida real y")
for o,c,ls in [((1,1,1),P2,":"),((1,2,1),P1,"--")]: ax.plot(t,C[o]["yp"],color=c,ls=ls,lw=1.1,label=f"OE{o} (FIT {C[o]['fit_eval']:.2f} %)")
ax.set_title("Punto 11 – Set C: OE(1,1,1) vs OE(1,2,1)"); ax.set_xlabel("t (s)"); ax.legend(frameon=False,fontsize=8,loc="upper center",bbox_to_anchor=(0.5,-0.22),ncol=3); fig.tight_layout(); fig.savefig("out/p11_C.png",bbox_inches="tight"); plt.close(fig)
fig,ax=plt.subplots(figsize=(8,3.2)); ax.plot(t,y,color=REAL,lw=1.6,label="Salida real y")
for o,c,ls in [((1,2,1),P1,"--"),((3,3,1),P2,":")]: ax.plot(t,C[o]["yp"],color=c,ls=ls,lw=1.1,label=f"OE{o} (FIT {C[o]['fit_eval']:.2f} %)")
ax.set_title("Punto 12 – Set C: OE(1,2,1) vs OE(3,3,1)"); ax.set_xlabel("t (s)"); ax.legend(frameon=False,fontsize=8,loc="upper center",bbox_to_anchor=(0.5,-0.22),ncol=3); fig.tight_layout(); fig.savefig("out/p12_C.png",bbox_inches="tight"); plt.close(fig)
fig,ax=plt.subplots(figsize=(8,3.2)); ax.plot(t,y,color=REAL,lw=1.6,label="Salida real y")
for o,c,ls in [((1,2,1),P1,"--"),((1,2,2),P2,":"),((1,2,3),P3,"-.")]: ax.plot(t,C[o]["yp"],color=c,ls=ls,lw=1.1,label=f"nk={o[2]} (FIT {C[o]['fit_eval']:.2f} %)")
ax.set_title("Punto 13 – Set C: OE(1,2,nk)"); ax.set_xlabel("t (s)"); ax.legend(frameon=False,fontsize=8,loc="upper center",bbox_to_anchor=(0.5,-0.22),ncol=3); fig.tight_layout(); fig.savefig("out/p13_C.png",bbox_inches="tight"); plt.close(fig)

# ---------------- SET D ----------------
t,u,y,uv,yv=load("D")
fd,ad=fft_plot("D",t,y,"fft_D",(0,15),"Set D"); R["D_noise"]=(fd,ad)
e=sinus(t,0.1,40); D={}
for o in [(1,1,1),(1,2,1),(3,3,1)]:
    D[o]=oe_eval(o,y,u,uv,yv,e); R[f"D_OE{o}"]={k:v for k,v in D[o].items() if k not in("yp","ypv")}
fig,ax=plt.subplots(figsize=(8,3.2)); ax.plot(t,y,color=REAL,lw=1.6,label="Salida real y")
for o,c,ls in [((1,1,1),P2,":"),((1,2,1),P1,"--"),((3,3,1),P3,"-.")]: ax.plot(t,D[o]["yp"],color=c,ls=ls,lw=1.1,label=f"OE{o} (FIT {D[o]['fit_eval']:.2f} %)")
ax.set_title("Punto 15 – Set D: OE(1,1,1), OE(1,2,1), OE(3,3,1)"); ax.set_xlabel("t (s)"); ax.legend(frameon=False,fontsize=8,loc="upper center",bbox_to_anchor=(0.5,-0.22),ncol=3); fig.tight_layout(); fig.savefig("out/p15_D.png",bbox_inches="tight"); plt.close(fig)

json.dump(R,open("out/results.json","w"),indent=1,default=float)
print(json.dumps(R,indent=1,default=float))
