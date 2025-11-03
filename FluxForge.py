import os,sys,time,random,math,shutil,re
from colorama import init,Fore,Style
import pyfiglet
def visual_creator():
    init(autoreset=True)
    clear_cmd='cls' if os.name=='nt' else 'clear'
    clear=lambda:os.system(clear_cmd)
    last_output=""
    fonts=["slant","standard","big","banner3-D","doom","speed","digital"]
    palettes=[[Fore.RED,Fore.MAGENTA,Fore.YELLOW,Fore.GREEN,Fore.CYAN,Fore.BLUE],[Fore.CYAN,Fore.BLUE,Fore.MAGENTA],[Fore.YELLOW,Fore.RED,Fore.GREEN]]
    symbols=list("abcdefghijklmnopqrstuvwxyz0123456789@#$%&*!~")
    while 1:
        try:
            print(Style.BRIGHT+Fore.GREEN+"\nMENU — pick a mode:")
            print("1) Fancy Text → ASCII (random fonts + gradient + effects)")
            print("2) Shapes: Heart, Spiral, Tree, Sine Wave")
            print("3) Animations (DVD, Matrix, Particles, Rings)")
            print("4) Cellular Canvas (particle field / CA / blobs)")
            print("5) Save last output to .txt")
            print("6) Exit")
            choice=input(Fore.CYAN+"\nChoice: ").strip()
        except (KeyboardInterrupt,EOFError):
            print("\nBye.");break
        if choice=="1":
            clear()
            text=input("Enter text (or blank for 'WOW'): ").strip() or "WOW"
            font=random.choice(fonts)
            try: art=pyfiglet.figlet_format(text,font=font)
            except: art=pyfiglet.figlet_format(text)
            cols=shutil.get_terminal_size().columns
            palette=random.choice(palettes)
            def color_wave(s,phase=0,shift=False):
                out="";L=len(palette)
                for i,ch in enumerate(s):
                    if ch.strip():
                        idx=(i+phase)%L if not shift else (i*2+phase)%L
                        out+=palette[idx]+ch
                    else: out+=ch
                return out
            mode=random.choice(["gradient","shadow","glitch","tilt","morph","braille"])
            if mode=="morph":
                other=input("Morph to (text): ").strip() or text[::-1]
                frames=8
                for f in range(frames):
                    mix=""
                    t2=int(len(text)*(f/frames))
                    cur=text[:len(text)-t2]+other[:t2]
                    try:
                        a=pyfiglet.figlet_format(cur,font=random.choice(fonts))
                    except: a=pyfiglet.figlet_format(cur)
                    print(color_wave(a,int(f)))
                    time.sleep(0.08)
                    print("\033[F"*(a.count("\n")+1),end="")
                print()
                last_output=art
                print(color_wave(art,random.randint(0,5)))
            elif mode=="glitch":
                out=[]
                for r,line in enumerate(art.splitlines()):
                    row=""
                    for c,ch in enumerate(line):
                        if ch.strip() and random.random()<0.12:
                            row+=random.choice(palette)+random.choice(symbols)
                        else:
                            row+=palette[(c+r)%len(palette)]+ch if ch.strip() else ch
                    out.append(row)
                last_output="\n".join(out);print(last_output)
            elif mode=="shadow":
                shadow_off=random.randint(1,3)
                out=[]
                for r,line in enumerate(art.splitlines()):
                    shadow_line=" "*shadow_off+line
                    out.append(color_wave(shadow_line,phase=2,shift=True))
                out2=[]
                for r,line in enumerate(art.splitlines()):
                    out2.append(color_wave(line,phase=0))
                composed=[]
                for a,b in zip(out,out2+[""]*(len(out)-len(out2))):
                    composed.append(a+"\n"+b)
                last_output="\n".join(composed);print(last_output)
            elif mode=="tilt":
                tilt=random.choice([-2,-1,0,1,2])
                out=[]
                for i,line in enumerate(art.splitlines()):
                    out.append(" "*max(0,i*tilt)+color_wave(line,phase=i))
                last_output="\n".join(out);print(last_output)
            elif mode=="braille":
                bmap={'.':'⠄','o':'⠶','*':'⠂','@':'⠈'}
                out=[]
                for line in art.splitlines():
                    row=""
                    for ch in line:
                        if ch.strip(): row+=random.choice([Fore.MAGENTA+'⠿',Fore.CYAN+'⠄',Fore.YELLOW+'⠶'])
                        else: row+=" "
                    out.append(row)
                last_output="\n".join(out);print(last_output)
            else:
                out=[]
                for r,line in enumerate(art.splitlines()):
                    out.append(color_wave(line,phase=random.randint(0,5)))
                last_output="\n".join(out);print(last_output)
        elif choice=="2":
            clear()
            print("Shapes: 1) Heart 2) Spiral 3) Tree 4) Sine Wave")
            s=input("Pick shape: ").strip()
            size_in=input("Size (5-40, default 18): ").strip()
            try: n=max(5,min(40,int(size_in))) if size_in else 18
            except: n=18
            if s=="1":
                scale=(n/18)
                points=[]
                for t in [i*0.03 for i in range(0,628)]:
                    x=16*math.sin(t)**3
                    y=13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t)
                    points.append((x*scale,y*scale))
                minx=min(p[0] for p in points);maxx=max(p[0] for p in points)
                miny=min(p[1] for p in points);maxy=max(p[1] for p in points)
                W=int((maxx-minx)*2)+6;H=int((maxy-miny))+6
                canvas=[[" "]*W for _ in range(H)]
                for x,y in points:
                    cx=int((x-minx)*2);cy=int((y-miny))
                    if 0<=cy<H and 0<=cx<W: canvas[H-1-cy][cx]="❤"
                out="\n".join("".join(row) for row in canvas)
                last_output=out;print(Fore.RED+out)
            elif s=="2":
                N=n if n%2==1 else n+1;grid=[[" "]*N for _ in range(N)]
                l=0;r=N-1;t=0;b=N-1;chs=["@","#","%","*","o"];step=0
                while l<=r and t<=b:
                    for i in range(l,r+1):grid[t][i]=chs[step%len(chs)]
                    for i in range(t+1,b+1):grid[i][r]=chs[step%len(chs)]
                    if t!=b:
                        for i in range(r-1,l-1,-1):grid[b][i]=chs[step%len(chs)]
                    if l!=r:
                        for i in range(b-1,t,-1):grid[i][l]=chs[step%len(chs)]
                    l+=1;r-=1;t+=1;b-=1;step+=1
                last_output="\n".join("".join(row) for row in grid);print(last_output)
            elif s=="3":
                levels=max(4,n//3);width=levels*4+4;canvas=[[" "]*width for _ in range(levels*2+4)]
                stack=[(levels*2,width//2,levels)]
                while stack:
                    y,x,size=stack.pop()
                    if y<0 or size<=0 or y>=len(canvas):continue
                    canvas[y][x]="|"
                    if size>1:
                        left=x-size;right=x+size;top=y-size
                        if 0<=top<len(canvas) and 0<=left<width and 0<=right<width:
                            for i in range(left,right+1):canvas[top][i]="^"
                        stack.append((y-size//2,x-size//2,size//2));stack.append((y-size//2,x+size//2,size//2))
                last_output="\n".join("".join((Fore.GREEN+ch if ch!=" " else " ") for ch in row) for row in canvas);print(last_output)
            elif s=="4":
                msg=input("Symbol for wave (default '*'): ").strip() or "*"
                width=shutil.get_terminal_size().columns;amp=max(3,min(12,n//2));freq=0.12
                for t in range(120):
                    line=[" "]*width
                    for x in range(width):
                        y=int((math.sin(x*freq+t*0.25)+1)*amp)
                        pos=max(0,min(width-1,y));line[pos]=Fore.CYAN+msg
                    print("".join(line));time.sleep(0.03);print("\033[F",end="")
                print();last_output=""
            else: print(Fore.RED+"Invalid shape choice.")
        elif choice=="3":
            clear();print("Anim: 1) DVD 2) Matrix 3) Particles 4) Rings 5) Random")
            a=input("Pick or Enter for random: ").strip() or str(random.choice([1,2,3,4]))
            if a=="1":
                text=input("Label (DVD): ").strip() or "DVD";cols=shutil.get_terminal_size().columns;rows=shutil.get_terminal_size().lines-2
                x=random.randint(0,max(0,cols-len(text)-1));y=random.randint(0,max(0,rows-1))
                vx,vy=random.choice([1,-1]),random.choice([1,-1]);color=random.choice([Fore.RED,Fore.GREEN,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW])
                for _ in range(240):
                    print("\033[2J\033[H",end="")
                    for r in range(rows):
                        if r==y: print(" "*x+color+text)
                        else: print()
                    x+=vx;y+=vy
                    if x<=0 or x>=cols-len(text)-1: vx*=-1;color=random.choice([Fore.RED,Fore.GREEN,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW])
                    if y<=0 or y>=rows-1: vy*=-1;color=random.choice([Fore.RED,Fore.GREEN,Fore.CYAN,Fore.MAGENTA,Fore.YELLOW])
                    time.sleep(0.02)
            elif a=="2":
                cols=shutil.get_terminal_size().columns;rows=shutil.get_terminal_size().lines;drops=[0]*cols;syms="abcdefghijklmnopqrstuvwxyz0123456789@#$%&"
                for _ in range(200):
                    line=[]
                    for i in range(cols):
                        if drops[i]==0 and random.random()<0.02: drops[i]=1
                        if drops[i]>0:
                            ch=random.choice(syms)
                            if random.random()<0.08: line.append(Fore.WHITE+ch)
                            else: line.append(Fore.GREEN+ch)
                            drops[i]+=1
                            if drops[i]>rows or random.random()<0.02: drops[i]=0
                        else: line.append(" ")
                    print("".join(line));time.sleep(0.05)
            elif a=="3":
                cols=shutil.get_terminal_size().columns;rows=shutil.get_terminal_size().lines-2;cx=cols//2;cy=rows//2
                particles=[]
                for _ in range(160):
                    ang=random.random()*math.pi*2;speed=random.uniform(0.3,2.5)
                    particles.append([cx,cy,math.cos(ang)*speed,math.sin(ang)*speed,random.choice(["*", "+", "o", "•", "✦"])])
                for step in range(40):
                    screen=[[" "]*cols for _ in range(rows)]
                    for p in particles:
                        p[0]+=p[2];p[1]+=p[3];px,py=int(p[0]),int(p[1])
                        if 0<=py<rows and 0<=px<cols: screen[py][px]=random.choice([Fore.MAGENTA+p[4],Fore.YELLOW+p[4],Fore.CYAN+p[4]])
                        p[2]*=0.95;p[3]*=0.95
                    print("\033[2J\033[H",end="")
                    for r in screen: print("".join(r))
                    time.sleep(0.06)
            elif a=="4":
                cols=shutil.get_terminal_size().columns;rows=shutil.get_terminal_size().lines-2;cx=cols//2;cy=rows//2;maxr=min(cols,rows)//2-1
                for t in range(40):
                    print("\033[2J\033[H",end="")
                    ring=int((math.sin(t*0.3)+1)*(maxr/2))+2
                    for y in range(rows):
                        row=""
                        for x in range(cols):
                            d=int(math.hypot(x-cx,y-cy))
                            row+=Fore.CYAN+"*" if abs(d-ring)<1 else " "
                        print(row)
                    time.sleep(0.08)
            else: print(Fore.RED+"Invalid animation choice.")
        elif choice=="4":
            clear();print("Canvas: 1) Particle field 2) Simple CA 3) Noise blobs")
            cm=input("Pick: ").strip()
            cols=max(20,min(120,shutil.get_terminal_size().columns));rows=max(10,min(40,shutil.get_terminal_size().lines-4))
            if cm=="1":
                particles=[]
                for _ in range(cols//2):particles.append([random.randint(0,cols-1),random.randint(0,rows-1),random.choice([-1,0,1]),random.choice([-1,0,1])])
                for _ in range(120):
                    grid=[[" "]*cols for __ in range(rows)]
                    for p in particles:
                        p[0]=(p[0]+p[2])%cols;p[1]=(p[1]+p[3])%rows
                        if random.random()<0.05: p[2]=random.choice([-1,0,1]);p[3]=random.choice([-1,0,1])
                        grid[p[1]][p[0]]=random.choice([Fore.CYAN+".",Fore.MAGENTA+"o",Fore.YELLOW+"*"])
                    print("\033[2J\033[H",end="")
                    for r in grid: print("".join(r))
                    time.sleep(0.04)
            elif cm=="2":
                grid=[[1 if random.random()<0.25 else 0 for _ in range(cols)] for __ in range(rows)]
                for gen in range(60):
                    nxt=[[0]*cols for _ in range(rows)]
                    for y in range(rows):
                        for x in range(cols):
                            alive=grid[y][x];neighbors=0
                            for dy in (-1,0,1):
                                for dx in (-1,0,1):
                                    if dy==0 and dx==0: continue
                                    ny=(y+dy)%rows;nx=(x+dx)%cols;neighbors+=grid[ny][nx]
                            if alive and (neighbors==2 or neighbors==3): nxt[y][x]=1
                            elif not alive and neighbors==3: nxt[y][x]=1
                            else: nxt[y][x]=0
                    grid=nxt;print("\033[2J\033[H",end="")
                    for r in grid: print("".join([Fore.GREEN+"@" if c else " " for c in r]));time.sleep(0.08)
            elif cm=="3":
                blobs=[]
                for _ in range(6): blobs.append([random.uniform(0,cols),random.uniform(0,rows),random.uniform(-0.6,0.6),random.uniform(-0.6,0.6),random.randint(2,6)])
                for _frame in range(120):
                    canvas=[[" "]*cols for __ in range(rows)]
                    for b in blobs:
                        bx,by=b[0],b[1]
                        for y in range(rows):
                            for x in range(cols):
                                d=math.hypot(x-bx,y-by)
                                if d<b[4]: canvas[y][x]=random.choice([Fore.YELLOW+".",Fore.MAGENTA+"o",Fore.CYAN+"+"])
                        b[0]+=b[2];b[1]+=b[3]
                        if b[0]<0 or b[0]>=cols: b[2]*=-1
                        if b[1]<0 or b[1]>=rows: b[3]*=-1
                    print("\033[2J\033[H",end="")
                    for r in canvas: print("".join(r));time.sleep(0.06)
            else: print(Fore.RED+"Invalid canvas choice.")
        elif choice=="5":
            if not last_output:
                print(Fore.RED+"No recent output to save. Generate something first.")
            else:
                fname=input("Filename (e.g. art.txt): ").strip() or f"ascii_{int(time.time())}.txt"
                if not fname.lower().endswith(".txt"): fname+=(".txt")
                try:
                    plain=re.sub(r'\x1b\[[0-9;]*m','',last_output)
                    with open(fname,"w",encoding="utf-8") as f: f.write(plain)
                    print(Fore.GREEN+f"Saved to {fname}")
                except Exception as e:
                    print(Fore.RED+"Save failed:",e)
        elif choice=="6":
            print(Fore.YELLOW+"Peace out. Visual Creator shutting down.");break
        else:
            print(Fore.RED+"Invalid option — try again.")
if __name__=="__main__": visual_creator()
