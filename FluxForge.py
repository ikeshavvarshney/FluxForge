import os,sys,time,random,math,shutil,re
from colorama import init,Fore,Style
import pyfiglet

def visual_creator():
    init(autoreset=True)
    clr_cmd='cls' if os.name=='nt' else 'clear'
    clr=lambda: os.system(clr_cmd)
    last=""
    fonts=["slant","standard","big","banner3-D","doom","speed","digital"]
    palettes=[[Fore.RED,Fore.MAGENTA,Fore.YELLOW,Fore.GREEN,Fore.CYAN,Fore.BLUE],[Fore.CYAN,Fore.BLUE,Fore.MAGENTA],[Fore.YELLOW,Fore.RED,Fore.GREEN]]
    syms="abcdefghijklmnopqrstuvwxyz0123456789@#$%&*!~"
    term_cols=lambda: shutil.get_terminal_size().columns
    term_lines=lambda: shutil.get_terminal_size().lines

    def colorize(s,p,phase=0,shift=False):
        out="";L=len(p)
        for i,ch in enumerate(s):
            if ch.strip(): idx=(i+phase)%L if not shift else (i*2+phase)%L; out+=p[idx]+ch
            else: out+=ch
        return out

    def ascii_text_flow(text=None):
        t=text or input("Text (blank→WOW): ").strip() or "WOW"
        f=random.choice(fonts)
        try: art=pyfiglet.figlet_format(t,font=f)
        except: art=pyfiglet.figlet_format(t)
        p=random.choice(palettes);mode=random.choice(["grad","glitch","shadow","tilt","morph","braille"])
        if mode=="morph":
            other=input("Morph to (blank→reverse): ").strip() or t[::-1]
            for fr in range(10):
                mix_index=int(len(t)*(fr/10))
                cur=t[:len(t)-mix_index]+other[:mix_index]
                try: a=pyfiglet.figlet_format(cur,font=random.choice(fonts))
                except: a=pyfiglet.figlet_format(cur)
                print(colorize(a,p,fr%len(p))); time.sleep(0.06); print("\033[F"*(a.count("\n")+1),end="")
            print(); out=colorize(art,p,random.randint(0,5))
        elif mode=="glitch":
            out=[] 
            for r,line in enumerate(art.splitlines()):
                row=""
                for c,ch in enumerate(line):
                    if ch.strip() and random.random()<0.12: row+=random.choice(p)+random.choice(syms)
                    else: row+= (random.choice(p)+ch if ch.strip() else ch)
                out.append(row)
            out="\n".join(out)
        elif mode=="shadow":
            off=random.randint(1,3);out=[];lines=art.splitlines()
            for r,line in enumerate(lines): out.append(colorize(" "*off+line,p,phase=2,shift=True))
            t2=[colorize(line,p,0) for line in lines];out="\n".join([a+"\n"+b for a,b in zip(out,t2+[""]*(len(out)-len(t2)))])
        elif mode=="tilt":
            tilt=random.choice([-2,-1,0,1,2]);out=[] 
            for i,line in enumerate(art.splitlines()): out.append(" "*max(0,i*tilt)+colorize(line,p,phase=i))
            out="\n".join(out)
        elif mode=="braille":
            out="\n".join("".join(random.choice([Fore.MAGENTA+'⠿',Fore.CYAN+'⠄',Fore.YELLOW+'⠶']) if ch.strip() else " " for ch in line) for line in art.splitlines())
        else:
            out="\n".join(colorize(line,p,phase=random.randint(0,5)) for line in art.splitlines())
        print(out); return out

    def heart(size=18):
        s=size;out=[]
        for y in [i*0.5 for i in range(int(-s),s)]:
            row=""
            for x in [i*0.5 for i in range(int(-s*2),int(s*2))]:
                eq=(x**2 + y**2 -1)**3 - x**2 * y**3
                row += Fore.RED+"❤" if eq<=0 else " "
            out.append(row)
        print("\n".join(out)); return "\n".join(out)

    def spiral(n=19):
        N=n if n%2==1 else n+1;grid=[[" "]*N for _ in range(N)]
        l=0;r=N-1;t=0;b=N-1;chs=["@","#","%","*","o"];step=0
        while l<=r and t<=b:
            for i in range(l,r+1): grid[t][i]=chs[step%5]
            for i in range(t+1,b+1): grid[i][r]=chs[step%5]
            if t!=b:
                for i in range(r-1,l-1,-1): grid[b][i]=chs[step%5]
            if l!=r:
                for i in range(b-1,t,-1): grid[i][l]=chs[step%5]
            l+=1;r-=1;t+=1;b-=1;step+=1
        out="\n".join("".join(row) for row in grid); print(out); return out

    def fractal_tree(levels=6,width=None):
        w=width or (levels*6+10);h=levels*4+6;canvas=[[" "]*w for _ in range(h)]
        def draw_line(x1,y1,x2,y2,ch):
            dx=abs(x2-x1);dy=-abs(y2-y1);sx=1 if x1<x2 else -1;sy=1 if y1<y2 else -1;err=dx+dy
            while True:
                if 0<=y1<h and 0<=x1<w: canvas[y1][x1]=ch
                if x1==x2 and y1==y2: break
                e2=2*err
                if e2>=dy: err+=dy; x1+=sx
                if e2<=dx: err+=dx; y1+=sy
        def branch(x,y,angle,depth,lenb):
            if depth==0: return
            nx=int(x+math.cos(angle)*lenb); ny=int(y-math.sin(angle)*lenb)
            ch='|' if abs(nx-x)<2 else ('/' if nx<x else '\\')
            draw_line(x,y,nx,ny,ch)
            branch(nx,ny,angle-math.pi/6,depth-1,int(lenb*0.7))
            branch(nx,ny,angle+math.pi/6,depth-1,int(lenb*0.7))
        branch(w//2,h-1,math.pi/2,levels,levels*3)
        out="\n".join("".join((Fore.GREEN+c if c!=" " else " ") for c in row) for row in canvas)
        print(out); return out

    def sine_wave(symbol="*",amp=6,freq=0.12,cols=None,rows=12,frames=120):
        w=cols or term_cols();H=rows
        for t in range(frames):
            buf=[]
            for y in range(H):
                buf.append([" "]*w)
            for x in range(w):
                y=int((math.sin(x*freq + t*0.25)+1)*(amp))
                y=max(0,min(H-1,y)); buf[y][x]=Fore.CYAN+symbol
            print("\n".join("".join(row) for row in buf)); time.sleep(0.03); print("\033[F"*H,end="")
        print(); return ""

    def dvd_logo(label="DVD",frames=240):
        cols=term_cols();rows=term_lines()-2;x=random.randint(0,max(0,cols-len(label)-1));y=random.randint(0,max(0,rows-1))
        vx,vy=random.choice([1,-1]),random.choice([1,-1]);color=random.choice([Fore.RED,Fore.GREEN,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW])
        for _ in range(frames):
            print("\033[2J\033[H",end="")
            for r in range(rows):
                if r==y: print(" "*x+color+label)
                else: print()
            x+=vx;y+=vy
            if x<=0 or x>=cols-len(label)-1: vx*=-1;color=random.choice([Fore.RED,Fore.GREEN,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW])
            if y<=0 or y>=rows-1: vy*=-1;color.random.choice([Fore.RED,Fore.GREEN,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW])
            time.sleep(0.02)
        return ""

    def matrix_rain(duration=200):
        cols=term_cols();rows=term_lines();drops=[0]*cols;syms="abcdefghijklmnopqrstuvwxyz0123456789@#$%&"
        for _ in range(duration):
            line=[]
            for i in range(cols):
                if drops[i]==0 and random.random()<0.02: drops[i]=1
                if drops[i]>0:
                    ch=random.choice(syms); line.append(Fore.GREEN+ch if random.random()>=0.08 else Fore.WHITE+ch); drops[i]+=1
                    if drops[i]>rows or random.random()<0.02: drops[i]=0
                else: line.append(" ")
            print("".join(line)); time.sleep(0.04)
        return ""

    def particles(frames=40):
        cols=term_cols();rows=term_lines()-2;cx=cols//2;cy=rows//2;parts=[]
        for _ in range(160):
            ang=random.random()*math.pi*2;spd=random.uniform(0.3,2.5);parts.append([cx,cy,math.cos(ang)*spd,math.sin(ang)*spd,random.choice(["*", "+", "o", "•", "✦"])])
        for _ in range(frames):
            scr=[[" "]*cols for _ in range(rows)]
            for p in parts:
                p[0]+=p[2];p[1]+=p[3];px,py=int(p[0]),int(p[1])
                if 0<=py<rows and 0<=px<cols: scr[py][px]=random.choice([Fore.MAGENTA+p[4],Fore.YELLOW+p[4],Fore.CYAN+p[4]])
                p[2]*=0.95;p[3]*=0.95
            print("\033[2J\033[H",end=""); [print("".join(r)) for r in scr]; time.sleep(0.06)
        return ""

    def puls_rings(frames=40):
        cols=term_cols();rows=term_lines()-2;cx=cols//2;cy=rows//2;maxr=min(cols,rows)//2-1
        for t in range(frames):
            print("\033[2J\033[H",end="")
            ring=int((math.sin(t*0.3)+1)*(maxr/2))+2
            for y in range(rows):
                row=""
                for x in range(cols):
                    d=int(math.hypot(x-cx,y-cy)); row+=Fore.CYAN+"*" if abs(d-ring)<1 else " "
                print(row)
            time.sleep(0.07)
        return ""

    def lightning(frames=20,width=None,height=None):
        w=width or term_cols();h=height or term_lines()-2
        for _ in range(frames):
            canvas=[[" "]*w for _ in range(h)]
            x=random.randint(0,w-1);y=0
            while y<h-1:
                canvas[y][x]="|"
                if random.random()<0.15:
                    x+=random.choice([-1,0,1])
                if random.random()<0.08:
                    # branch
                    bx=x+random.choice([-2,-1,1,2]); by=y+random.randint(1,3)
                    for i in range(y, min(h,by+1)):
                        if 0<=i<h and 0<=x<w: canvas[i][x]="/" if random.random()<0.5 else "\\"
                y+=1
            print("\033[2J\033[H",end=""); [print("".join(row)) for row in canvas]; time.sleep(0.06)
        return ""

    def fire(frames=80,w=None,h=16):
        W=w or min(80,term_cols());H=h
        chars=[" ",".",":","*","o","%","@","█"]
        for _ in range(frames):
            canvas=[[ " " for _ in range(W)] for __ in range(H)]
            for x in range(W):
                intensity=int((math.sin(x*0.3+time.time()*6)+1)/2 * (len(chars)-1))
                for y in range(H-1, -1, -1):
                    flick=intensity - (H-1 - y) + random.randint(-1,1)
                    canvas[y][x]=chars[max(0,min(len(chars)-1,flick))]
            print("\033[2J\033[H",end="")
            for row in canvas: print("".join(Fore.YELLOW+ch if ch in ".:*o%@" else ch for ch in row))
            time.sleep(0.05)
        return ""

    def rainfall(duration=200):
        cols=term_cols();rows=term_lines();drops=[random.randint(0,rows) for _ in range(cols)]
        for _ in range(duration):
            scr=[" "]*cols
            for i in range(cols):
                if random.random()<0.4: drops[i]+=1
                if drops[i]>rows: drops[i]=0
                scr[i]=Fore.CYAN+"|" if drops[i]>0 and random.random()<0.9 else " "
            print("".join(scr)); time.sleep(0.03)
        return ""

    def mandala(size=20):
        w=term_cols();h=term_lines()-2;cx=w//2;cy=(h)//2;r=size
        out=[]
        for y in range(h):
            row=""
            for x in range(w):
                d=math.hypot(x-cx,y-cy)
                if abs(d%r - r/2)<r/8: row+=Fore.MAGENTA+"●"
                else: row+=" "
            out.append(row)
        print("\n".join(out)); return "\n".join(out)

    def particle_field(frames=120):
        cols=max(20,min(120,term_cols()));rows=max(10,min(40,term_lines()-4));parts=[]
        for _ in range(cols//2): parts.append([random.randint(0,cols-1),random.randint(0,rows-1),random.choice([-1,0,1]),random.choice([-1,0,1])])
        for _ in range(frames):
            grid=[[" "]*cols for __ in range(rows)]
            for p in parts:
                p[0]=(p[0]+p[2])%cols; p[1]=(p[1]+p[3])%rows
                if random.random()<0.05: p[2]=random.choice([-1,0,1]); p[3]=random.choice([-1,0,1])
                grid[p[1]][p[0]] = random.choice([Fore.CYAN+".",Fore.MAGENTA+"o",Fore.YELLOW+"*"])
            print("\033[2J\033[H",end=""); [print("".join(r)) for r in grid]; time.sleep(0.04)
        return ""

    def conway(cols=None,rows=None,gens=60):
        C=max(20,min(120,cols or term_cols()));R=max(10,min(40,rows or (term_lines()-4)))
        g=[[1 if random.random()<0.25 else 0 for _ in range(C)] for __ in range(R)]
        for _ in range(gens):
            nxt=[[0]*C for _ in range(R)]
            for y in range(R):
                for x in range(C):
                    s=0
                    for dy in (-1,0,1):
                        for dx in (-1,0,1):
                            if dy==0 and dx==0: continue
                            s+=g[(y+dy)%R][(x+dx)%C]
                    nxt[y][x]=1 if (g[y][x] and s in (2,3)) or (not g[y][x] and s==3) else 0
            g=nxt; print("\033[2J\033[H",end=""); [print("".join([Fore.GREEN+"@" if c else " " for c in row])) for row in g]; time.sleep(0.07)
        return ""

    while True:
        try:
            print(Style.BRIGHT+Fore.GREEN+"\nMENU — choose:")
            print("1) Fancy Text  2) Shapes  3) Animations  4) Cellular Canvas  5) Save last .txt  6) Exit")
            ch=input(Fore.CYAN+"Choice: ").strip()
        except (KeyboardInterrupt,EOFError):
            print("\nPeace."); break
        if ch=="1":
            clr(); last=ascii_text_flow(None)
        elif ch=="2":
            clr(); print("Shapes: 1) Heart 2) Spiral 3) Fractal Tree 4) Sine Wave 5) Mandala")
            s=input("Pick: ").strip()
            if s=="1": last=heart(int(input("Size 5-40 (18): ").strip() or 18))
            elif s=="2": last=spiral(int(input("Size 5-39 (19): ").strip() or 19))
            elif s=="3": last=fractal_tree(int(input("Levels 4-10 (6): ").strip() or 6))
            elif s=="4": last=sine_wave(input("Symbol (*): ").strip() or "*",int(input("Amp 3-12 (6): ").strip() or 6),float(input("Freq (0.12): ").strip() or 0.12),None,int(input("Rows (12): ").strip() or 12),int(input("Frames (120): ").strip() or 120))
            elif s=="5": last=mandala(int(input("Radius (10-30): ").strip() or 20))
            else: print(Fore.RED+"Invalid.")
        elif ch=="3":
            clr(); print("Anims: 1) DVD 2) Matrix 3) Particles 4) Rings 5) Lightning 6) Fire 7) Rain 8) Mandala")
            a=input("Pick: ").strip() or str(random.choice(range(1,9)))
            if a=="1": last=dvd_logo(input("Label (DVD): ").strip() or "DVD")
            elif a=="2": last=matrix_rain()
            elif a=="3": last=particles()
            elif a=="4": last=puls_rings()
            elif a=="5": last=lightning()
            elif a=="6": last=fire()
            elif a=="7": last=rainfall()
            elif a=="8": last=mandala(int(input("Radius (10-30): ").strip() or 18))
            else: print(Fore.RED+"Invalid.")
        elif ch=="4":
            clr(); print("Canvas: 1) Particle Field 2) Conway CA")
            cc=input("Pick: ").strip()
            if cc=="1": last=particle_field()
            elif cc=="2": last=conway()
            else: print(Fore.RED+"Invalid.")
        elif ch=="5":
            if not last: print(Fore.RED+"Nothing to save.")
            else:
                fn=input("Filename (art.txt): ").strip() or f"art_{int(time.time())}.txt"
                if not fn.lower().endswith(".txt"): fn+=".txt"
                try:
                    plain=re.sub(r'\x1b\[[0-9;]*m','',last)
                    with open(fn,"w",encoding="utf-8") as f: f.write(plain)
                    print(Fore.GREEN+f"Saved: {fn}")
                except Exception as e: print(Fore.RED+"Save failed:",e)
        elif ch=="6":
            print(Fore.YELLOW+"Shutting down."); break
        else:
            print(Fore.RED+"Invalid.")

if __name__=="__main__": visual_creator()
