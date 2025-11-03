import os,sys,time,random,math,shutil,re
from colorama import init,Fore,Back,Style
import pyfiglet
init(autoreset=True)
clear=lambda: os.system('cls' if os.name=='nt' else 'clear')
TC=lambda: shutil.get_terminal_size().columns
TL=lambda: shutil.get_terminal_size().lines
palettes=[[Fore.RED,Fore.MAGENTA,Fore.YELLOW,Fore.GREEN,Fore.CYAN,Fore.BLUE],[Fore.CYAN,Fore.BLUE,Fore.MAGENTA],[Fore.YELLOW,Fore.RED,Fore.GREEN]]
fonts=["slant","standard","big","banner3-D","doom","speed","digital","small"]
syms="abcdefghijklmnopqrstuvwxyz0123456789@#$%&*!~"
stripc=lambda s: re.sub(r'\x1b\[[0-9;]*m','',s)

def colorize(s,p,phase=0,shift=False):
    o="";L=len(p)
    for i,ch in enumerate(s):
        if ch.strip():
            idx=(i+phase)%L if not shift else (i*2+phase)%L
            o+=p[idx]+ch
        else: o+=ch
    return o

def fancy_text(t=None):
    t=(t or input("Text (blank→WOW): ").strip() or "WOW")
    try: art=pyfiglet.figlet_format(t,font=random.choice(fonts))
    except: art=pyfiglet.figlet_format(t)
    p=random.choice(palettes);m=random.choice(["grad","glitch","shadow","tilt","morph","braille"])
    if m=="morph":
        other=input("Morph to (blank→reverse): ").strip() or t[::-1]
        for f in range(10):
            mix=int(len(t)*(f/10));cur=t[:len(t)-mix]+other[:mix]
            try: a=pyfiglet.figlet_format(cur,font=random.choice(fonts))
            except: a=pyfiglet.figlet_format(cur)
            print(colorize(a,p,f%len(p)));time.sleep(0.06);print("\033[F"*(a.count("\n")+1),end="")
        print();out=colorize(art,p,random.randint(0,5));print(out);return out
    if m=="glitch":
        out=[]
        for r,line in enumerate(art.splitlines()):
            row=""
            for c,ch in enumerate(line):
                if ch.strip() and random.random()<0.12: row+=random.choice(p)+random.choice(syms)
                else: row+= (p[(c+r)%len(p)]+ch if ch.strip() else ch)
            out.append(row)
        out="\n".join(out);print(out);return out
    if m=="shadow":
        off=random.randint(1,3);L=art.splitlines();o1=[colorize(" "*off+l,p,2,True) for l in L];o2=[colorize(l,p,0) for l in L];out="\n".join(a+"\n"+b for a,b in zip(o1,o2+[""]*(len(o1)-len(o2))));print(out);return out
    if m=="tilt":
        t=random.choice([-2,-1,0,1,2]);out=[" "*max(0,i*t)+colorize(l,p,i) for i,l in enumerate(art.splitlines())];out="\n".join(out);print(out);return out
    if m=="braille":
        out="\n".join("".join(random.choice([Fore.MAGENTA+'⠿',Fore.CYAN+'⠄',Fore.YELLOW+'⠶']) if ch.strip() else " " for ch in line) for line in art.splitlines());print(out);return out
    out="\n".join(colorize(l,p,random.randint(0,5)) for l in art.splitlines());print(out);return out

def heart(size=18):
    s=max(6,min(40,size));out=[]
    for y in [i*0.5 for i in range(int(-s),s)]:
        row=""
        for x in [i*0.5 for i in range(int(-s*2),int(s*2))]:
            eq=(x**2 + y**2 -1)**3 - x**2 * y**3
            row+=Fore.RED+"❤" if eq<=0 else " "
        out.append(row)
    out="\n".join(out);print(out);return out

def spiral(n=19):
    N=n if n%2==1 else n+1;grid=[[" "]*N for _ in range(N)];l=0;r=N-1;t=0;b=N-1;chs=["@","#","%","*","o"];step=0
    while l<=r and t<=b:
        for i in range(l,r+1):grid[t][i]=chs[step%5]
        for i in range(t+1,b+1):grid[i][r]=chs[step%5]
        if t!=b:
            for i in range(r-1,l-1,-1):grid[b][i]=chs[step%5]
        if l!=r:
            for i in range(b-1,t,-1):grid[i][l]=chs[step%5]
        l+=1;r-=1;t+=1;b-=1;step+=1
    out="\n".join("".join(row) for row in grid);print(out);return out

def draw_line(canvas,w,h,x1,y1,x2,y2,ch):
    dx=abs(x2-x1);dy=-abs(y2-y1);sx=1 if x1<x2 else -1;sy=1 if y1<y2 else -1;err=dx+dy
    while True:
        if 0<=y1<h and 0<=x1<w: canvas[y1][x1]=ch
        if x1==x2 and y1==y2: break
        e2=2*err
        if e2>=dy: err+=dy; x1+=sx
        if e2<=dx: err+=dx; y1+=sy

def fractal_tree(levels=6):
    levels=max(3,min(10,levels));w=levels*8+20;h=levels*4+10;canvas=[[" "]*w for _ in range(h)]
    def branch(x,y,angle,depth,lenb):
        if depth<=0: return
        nx=int(x+math.cos(angle)*lenb);ny=int(y-math.sin(angle)*lenb)
        ch='|' if abs(nx-x)<2 else ('/' if nx<x else '\\')
        draw_line(canvas,w,h,x,y,nx,ny,ch)
        branch(nx,ny,angle-math.pi/6,depth-1,int(lenb*0.7));branch(nx,ny,angle+math.pi/6,depth-1,int(lenb*0.7))
    branch(w//2,h-1,math.pi/2,levels,levels*3)
    out="\n".join("".join((Fore.GREEN+c if c!=" " else " ") for c in row) for row in canvas);print(out);return out

def sine_wave(sym="*",amp=6,freq=0.12,rows=12,frames=120):
    w=TC();H=max(4,min(24,rows))
    for t in range(frames):
        buf=[[" "]*w for _ in range(H)]
        for x in range(w):
            y=int((math.sin(x*freq + t*0.28)+1)*(amp))
            y=max(0,min(H-1,y)); buf[y][x]=Fore.CYAN+sym
        print("\n".join("".join(r) for r in buf));time.sleep(0.03);print("\033[F"*H,end="")
    print();return ""

def dvd(label="DVD",frames=240):
    cols=TC();rows=TL()-2;x=random.randint(0,max(0,cols-len(label)-1));y=random.randint(0,max(0,rows-1))
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

def matrix_rain(duration=160):
    cols=TC();rows=TL();drops=[0]*cols;syms="abcdefghijklmnopqrstuvwxyz0123456789@#$%&"
    for _ in range(duration):
        line=[]
        for i in range(cols):
            if drops[i]==0 and random.random()<0.02: drops[i]=1
            if drops[i]>0:
                ch=random.choice(syms); line.append(Fore.GREEN+ch if random.random()>=0.08 else Fore.WHITE+ch); drops[i]+=1
                if drops[i]>rows or random.random()<0.02: drops[i]=0
            else: line.append(" ")
        print("".join(line));time.sleep(0.04)
    return ""

def particles(frames=40):
    cols=TC();rows=max(8,TL()-2);cx=cols//2;cy=rows//2;parts=[]
    for _ in range(160):
        ang=random.random()*math.pi*2;spd=random.uniform(0.3,2.5);parts.append([cx,cy,math.cos(ang)*spd,math.sin(ang)*spd,random.choice(["*", "+", "o", "•", "✦"])])
    for _ in range(frames):
        scr=[[" "]*cols for _ in range(rows)]
        for p in parts:
            p[0]+=p[2];p[1]+=p[3];px,py=int(p[0]),int(p[1])
            if 0<=py<rows and 0<=px<cols: scr[py][px]=random.choice([Fore.MAGENTA+p[4],Fore.YELLOW+p[4],Fore.CYAN+p[4]])
            p[2]*=0.95;p[3]*=0.95
        print("\033[2J\033[H",end="");[print("".join(r)) for r in scr];time.sleep(0.06)
    return ""

def puls_rings(frames=40):
    cols=TC();rows=max(8,TL()-2);cx=cols//2;cy=rows//2;maxr=min(cols,rows)//2-1
    for t in range(frames):
        print("\033[2J\033[H",end="")
        ring=int((math.sin(t*0.28)+1)*(maxr/2))+2
        for y in range(rows):
            row=""
            for x in range(cols):
                d=int(math.hypot(x-cx,y-cy)); row+=Fore.CYAN+"*" if abs(d-ring)<1 else " "
            print(row)
        time.sleep(0.07)
    return ""

def lightning(frames=22,cols_wide=4,bolts=3):
    W=TC();H=max(8,TL()-2)
    for _ in range(frames):
        canvas=[[" "]*W for _ in range(H)]
        for b in range(bolts):
            x=random.randint(0,W-1);y=0;width=random.randint(2,cols_wide)
            while y<H-1:
                for xx in range(max(0,x-width),min(W,x+width+1)): canvas[y][xx]=Fore.WHITE+"|"
                if random.random()<0.2:
                    bx=x+random.choice([-1,0,1]);by=y+random.randint(1,3)
                    for i in range(y,min(H,by+1)):
                        if 0<=i<H and 0<=bx<W: canvas[i][bx]=Fore.WHITE+"/" if random.random()<0.5 else Fore.WHITE+"\\"
                x+=random.choice([-2,-1,0,1,2]);x=max(0,min(W-1,x));y+=1
        print("\033[2J\033[H",end="");[print("".join(r)) for r in canvas];time.sleep(0.06)
    return ""

def rain(duration=140,density=0.06):
    cols=TC();rows=TL();drops=[random.randint(0,rows) for _ in range(cols)]
    for _ in range(duration):
        scr=[" "]*cols
        for i in range(cols):
            if random.random()<density: drops[i]+=random.randint(1,3)
            if drops[i]>rows: drops[i]=0
            scr[i]=Fore.CYAN+"|" if drops[i]>0 and random.random()<0.8 else " "
        print("".join(scr));time.sleep(0.02)
    return ""

def mandala(frames=60,rad=14):
    W=TC();H=max(10,TL()-2);cx=W//2;cy=H//2;R=rad
    for t in range(frames):
        out=[]
        for y in range(H):
            row=""
            for x in range(W):
                d=math.hypot(x-cx,y-cy)
                val=math.sin( (d/R)+t*0.15 )
                row+=Fore.MAGENTA+"●" if val>0.6 else (" " if val<-0.6 else Fore.YELLOW+"○" if val>0.1 else " ")
            out.append(row)
        print("\033[2J\033[H",end="");print("\n".join(out));time.sleep(0.06)
    return ""

def hypnosis(frames=120,spirals=3):
    W=TC();H=max(12,TL()-2);cx=W//2;cy=H//2
    for t in range(frames):
        canvas=[[" "]*W for _ in range(H)]
        for s in range(spirals):
            for a in [i*0.1 for i in range(0,360)]:
                r=1+ (s+1)*math.sin(a*0.1 + t*0.12)*(1+0.5*math.sin(t*0.2))
                x=int(cx + math.cos(a+t*0.05)*r*(s+3))
                y=int(cy + math.sin(a+t*0.05)*r*(s+2))
                if 0<=y<H and 0<=x<W: canvas[y][x]=Fore.CYAN+"@"
        print("\033[2J\033[H",end="");[print("".join(r)) for r in canvas];time.sleep(0.04)
    return ""

def fire(frames=80,W=None,H=12):
    W=W or min(80,TC());H=H
    chars=[" ",".",":","*","o","%","@","█"]
    for _ in range(frames):
        canvas=[[ " " for _ in range(W)] for __ in range(H)]
        for x in range(W):
            base=int((math.sin(x*0.3+time.time()*6)+1)/2*(len(chars)-1))
            for y in range(H-1,-1,-1):
                flick=base-(H-1-y)+random.randint(-1,1);canvas[y][x]=chars[max(0,min(len(chars)-1,flick))]
        print("\033[2J\033[H",end="")
        for row in canvas: print("".join(Fore.YELLOW+c if c in ".*o%@" else c for c in row))
        time.sleep(0.05)
    return ""

def snow(duration=140,density=0.02):
    W=TC();H=TL()-2;flakes=[random.randint(0,H) for _ in range(W)]
    for _ in range(duration):
        line=[" "]*W
        for i in range(W):
            if random.random()<density: flakes[i]+=1
            if flakes[i]>H: flakes[i]=0
            line[i]=Fore.WHITE+"*" if flakes[i]>0 and random.random()<0.85 else " "
        print("".join(line));time.sleep(0.05)
    return ""

def starfield(frames=120,stars=120):
    W=TC();H=TL()-2;pts=[[random.uniform(-W,W),random.uniform(-H,H),random.uniform(0.1,1.0)] for _ in range(stars)]
    for _ in range(frames):
        buf=[[" "]*W for _ in range(H)]
        for p in pts:
            p[0]+=p[2]*0.5; p[1]+=p[2]*0.5; p[2]+=0.001
            if abs(p[0])>W or abs(p[1])>H: p[0]=random.uniform(-W,W);p[1]=random.uniform(-H,H);p[2]=random.uniform(0.1,0.6)
            x=int(p[0]+W/2);y=int(p[1]+H/2)
            if 0<=y<H and 0<=x<W: buf[y][x]=Fore.WHITE+"*"
        print("\033[2J\033[H",end="");[print("".join(r)) for r in buf];time.sleep(0.04)
    return ""

def crt_glitch(frames=80):
    W=TC();H=max(8,TL()-2)
    for _ in range(frames):
        for y in range(H):
            line=""
            for x in range(W):
                r=random.random()
                if r<0.005: line+=Back.WHITE+Fore.BLACK+random.choice(list("█▓▒"))
                elif r<0.02: line+=Fore.GREEN+random.choice(list("@#%&$"))
                elif r<0.2: line+=" "
                else: line+=Fore.GREEN+" "
            print(line)
        time.sleep(0.03);print("\033[2J",end="")
    return ""

def ascii_clock():
    try: secs=int(input("Show clock for how many seconds? ").strip() or "30")
    except: secs=30
    end=time.time()+max(1,secs)
    while time.time()<end:
        print("\033[2J\033[H",end="")
        tm=time.localtime();s=time.strftime("%H:%M:%S",tm);date=time.strftime("%d %b %Y",tm)
        art=pyfiglet.figlet_format(s,font=random.choice(fonts));p=random.choice(palettes)
        print(colorize(art,p));print(" "*max(0,(TC()-len(date))//2)+date)
        time.sleep(1)
    return ""

def random_art(iterations=10):
    funcs=[heart,spiral,fractal_tree,particles,puls_rings,starfield,mandala,fire,snow,particle_field]
    for _ in range(max(1,min(20,iterations))):
        clear()
        f=random.choice(funcs)
        try:
            if f in (heart,spiral): f(random.randint(6,20))
            else: f()
        except: 
            try: f()
            except: pass
        time.sleep(0.6)
    return ""

def mandelbrot(W=None,H=None,itermax=40):
    W=W or min(120,TC());H=H or min(40,TL()-4)
    out=[]
    for j in range(H):
        row=""
        for i in range(W):
            x0=(i-W/2)/ (W/4); y0=(j-H/2)/(H/4)
            x=0.0;y=0.0;it=0
            while x*x+y*y<=4 and it<itermax:
                xt=x*x-y*y + x0; y=2*x*y + y0; x=xt; it+=1
            chars=" .:-=+*#%@"
            row+=chars[int(it/itermax*(len(chars)-1))]
        out.append(row)
    print("\n".join(out));return "\n".join(out)

def lissajous(frames=120,A=10,B=20,a=3,b=2,delta=0.5):
    W=TC();H=max(12,TL()-2);cx=W//2;cy=H//2
    for t in range(frames):
        buf=[[" "]*W for _ in range(H)]
        for theta in [i*0.1 for i in range(0,628)]:
            x=int(cx + A*math.sin(a*theta + delta*t*0.02)); y=int(cy + B*math.sin(b*theta))
            if 0<=y<H and 0<=x<W: buf[y][x]=Fore.CYAN+"*"
        print("\033[2J\033[H",end="");[print("".join(r)) for r in buf];time.sleep(0.04)
    return ""

def spectrum(frames=120,bands=80):
    W=TC();H=max(8,TL()-2);bands=min(bands,W)
    for _ in range(frames):
        row=""
        for i in range(bands):
            h=random.randint(1,H); row+=Fore.MAGENTA+"█"*h+Fore.RESET+" "
        print("\033[2J\033[H",end="");print(row);time.sleep(0.06)
    return ""

def typewriter_banner():
    s=input("Banner text: ").strip() or "VISUAL";art=pyfiglet.figlet_format(s,font=random.choice(fonts))
    lines=art.splitlines()
    for i in range(1,len(lines)+1):
        print("\033[2J\033[H",end="");print("\n".join(lines[:i]));time.sleep(0.18)
    return art

def maze(w=41,h=21):
    W=max(21,min(79,w));H=max(11,min(39,h))
    maze=[['#']*W for _ in range(H)]
    def carve(x,y):
        dirs=[(2,0),(-2,0),(0,2),(0,-2)]; random.shuffle(dirs)
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 1<=nx<W-1 and 1<=ny<H-1 and maze[ny][nx]=='#':
                maze[ny][nx]=' '; maze[y+dy//2][x+dx//2]=' '
                carve(nx,ny)
    maze[1][1]=' '; carve(1,1)
    print("\n".join("".join(row) for row in maze)); return "\n".join("".join(row) for row in maze)

def particle_field(frames=120):
    cols=max(20,min(120,TC()));rows=max(10,min(40,TL()-4));parts=[]
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
    C=max(20,min(120,cols or TC()));R=max(10,min(40,rows or (TL()-4)))
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

def save_out(txt):
    if not txt: print(Fore.RED+"Nothing to save."); return
    fn=input("Filename (art.txt): ").strip() or f"art_{int(time.time())}.txt"
    if not fn.lower().endswith(".txt"): fn+=".txt"
    try:
        with open(fn,"w",encoding="utf-8") as f: f.write(stripc(txt))
        print(Fore.GREEN+f"Saved: {fn}")
    except Exception as e: print(Fore.RED+"Save failed:",e)

def menu():
    last=""
    while True:
        try:
            print(Style.BRIGHT+Fore.GREEN+"\nMENU — choose:")
            print("1) Fancy Text   2) Shapes   3) Animations   4) Patterns   5) Tools   6) Save last .txt   7) Exit")
            ch=input(Fore.CYAN+"Choice: ").strip()
        except (KeyboardInterrupt,EOFError):
            print("\nbye");break
        if ch=="1":
            clear(); last=fancy_text(None)
        elif ch=="2":
            clear(); print("Shapes: 1) Heart 2) Spiral 3) Fractal Tree 4) Sine Wave 5) Mandala 6) Maze")
            s=input("Pick: ").strip()
            if s=="1": last=heart(int(input("Size 6-40 (18): ").strip() or 18))
            elif s=="2": last=spiral(int(input("Size 5-39 (19): ").strip() or 19))
            elif s=="3": last=fractal_tree(int(input("Levels 3-10 (6): ").strip() or 6))
            elif s=="4": last=sine_wave(input("Symbol (*): ").strip() or "*",int(input("Amp 3-12 (6): ").strip() or 6),float(input("Freq (0.12): ").strip() or 0.12),int(input("Rows (12): ").strip() or 12),int(input("Frames (120): ").strip() or 120))
            elif s=="5": last=mandala(int(input("Radius (8-24): ").strip() or 14))
            elif s=="6": last=maze(int(input("Width (odd 21-79): ").strip() or 41),int(input("Height (odd 11-39): ").strip() or 21))
            else: print(Fore.RED+"Invalid.")
        elif ch=="3":
            clear(); print("Anims: 1) DVD 2) Matrix 3) Particles 4) Rings 5) Lightning 6) Fire 7) Rain 8) Hypnosis 9) Starfield 10) CRT Glitch 11) Spectrum 12) Lissajous")
            a=input("Pick: ").strip() or str(random.choice(range(1,13)))
            if a=="1": last=dvd(input("Label (DVD): ").strip() or "DVD")
            elif a=="2": last=matrix_rain()
            elif a=="3": last=particles()
            elif a=="4": last=puls_rings()
            elif a=="5": last=lightning()
            elif a=="6": last=fire()
            elif a=="7": last=rain()
            elif a=="8": last=hypnosis()
            elif a=="9": last=starfield()
            elif a=="10": last=crt_glitch()
            elif a=="11": last=spectrum()
            elif a=="12": last=lissajous()
            else: print(Fore.RED+"Invalid.")
        elif ch=="4":
            clear(); print("Patterns: 1) Mandala 2) Mandelbrot 3) Particle Field 4) Conway 5) Snow")
            p=input("Pick: ").strip()
            if p=="1": last=mandala(int(input("Radius (8-24): ").strip() or 14))
            elif p=="2": last=mandelbrot()
            elif p=="3": last=particle_field()
            elif p=="4": last=conway()
            elif p=="5": last=snow()
            else: print(Fore.RED+"Invalid.")
        elif ch=="5":
            clear(); print("Tools: 1) ASCII Clock 2) Braille Pixelizer 3) Random Art 4) Typewriter Banner 5) One-line Minify Save")
            u=input("Pick: ").strip()
            if u=="1": last=ascii_clock()
            elif u=="2":
                txt=input("Enter small text: ").strip() or "A";art=pyfiglet.figlet_format(txt,font=random.choice(fonts))
                out="\n".join("".join("⠿" if c.strip() else " " for c in line) for line in art.splitlines());print(out);last=out
            elif u=="3": last=random_art(10)
            elif u=="4": last=typewriter_banner()
            elif u=="5":
                s=input("Paste text to minify: ")
                m=re.sub(r'\s+',' ',s).strip()
                fn=input("Filename (min.txt): ").strip() or "minified.txt"
                with open(fn,"w",encoding="utf-8") as f: f.write(m)
                print(Fore.GREEN+f"Saved: {fn}");last=m
            else: print(Fore.RED+"Invalid.")
        elif ch=="6":
            save_out(last)
        elif ch=="7":
            print(Fore.YELLOW+"Shutting down.");break
        else: print(Fore.RED+"Invalid.")

if __name__=="__main__": menu()
