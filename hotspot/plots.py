import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from .params import HOT_LIM,OIL_LIM

def dayPlot(s,path=None,show=False):
    if not show:
        matplotlib.use("Agg")
    fig,(a1,a2,a3)=plt.subplots(3,1,figsize=(11,10),sharex=True)
    fig.suptitle(f"{s.tfName} {s.kind} {s.season} K={s.peak:.2f}\nload: {s.srcLoad} | amb: {s.srcAmb}",fontsize=11,fontweight="bold")
    a1.plot(s.hrs,s.K,color="tab:blue",lw=2)
    a1.axhline(1,color="tab:blue",ls=":",lw=1)
    a1.set_ylabel("K",color="tab:blue")
    b=a1.twinx()
    b.plot(s.hrs,s.ta,color="tab:green",lw=1.5)
    b.set_ylabel("amb C",color="tab:green")
    a1.grid(alpha=.3)
    a2.plot(s.hrs,s.thot,color="tab:red",lw=2,label="hot")
    a2.plot(s.hrs,s.toil,color="tab:orange",lw=2,label="oil")
    a2.plot(s.hrs,s.ta,color="tab:green",lw=1,alpha=.6,label="amb")
    a2.axhline(HOT_LIM,color="tab:red",ls="--",lw=1)
    a2.axhline(OIL_LIM,color="tab:orange",ls="--",lw=1)
    i=int(np.argmax(s.thot))
    a2.annotate(f"{s.thot[i]:.1f}",(s.hrs[i],s.thot[i]),xytext=(10,8),textcoords="offset points",color="tab:red")
    a2.set_ylim(top=max(s.thot.max(),HOT_LIM)+12)
    a2.set_ylabel("C")
    a2.legend(loc="upper left",fontsize=8)
    a2.grid(alpha=.3)
    a3.fill_between(s.hrs,s.v,color="tab:purple",alpha=.3)
    a3.plot(s.hrs,s.v,color="tab:purple",lw=1.5)
    a3.axhline(1,color="gray",ls=":",lw=1)
    a3.set_ylabel("V")
    a3.set_xlabel("hr")
    c=a3.twinx()
    dt=s.hrs[1]-s.hrs[0]
    c.plot(s.hrs,np.cumsum(s.v)*dt,color="black",lw=1,ls="--")
    c.set_ylabel("cum hrs")
    a3.grid(alpha=.3)
    a3.set_xlim(0,24)
    a3.set_xticks(range(0,25,3))
    fig.tight_layout()
    if path:
        fig.savefig(path,dpi=120)
    if show:
        plt.show()
    plt.close(fig)

def sweepPlot(rows,path=None,show=False):
    if not show:
        matplotlib.use("Agg")
    ks=[r.peak for r in rows]
    ys=[min(r.yrs,200) for r in rows]
    hs=[r.maxHot for r in rows]
    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(ks,ys,"o-",color="tab:purple",lw=2)
    ax.set_yscale("log")
    ax.set_xlabel("K")
    ax.set_ylabel("yrs",color="tab:purple")
    ax.grid(alpha=.3,which="both")
    bx=ax.twinx()
    bx.plot(ks,hs,"s--",color="tab:red")
    bx.axhline(HOT_LIM,color="tab:red",ls=":",lw=1)
    bx.set_ylabel("hot C",color="tab:red")
    r0=rows[0]
    ax.set_title(f"{r0.tfName} {r0.kind} {r0.season}\nload: {r0.srcLoad} | amb: {r0.srcAmb}")
    fig.tight_layout()
    if path:
        fig.savefig(path,dpi=120)
    if show:
        plt.show()
    plt.close(fig)
