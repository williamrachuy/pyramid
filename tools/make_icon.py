# Draws web/icon.svg: a golden 3D square pyramid, projected from real coordinates.
# Run: python3 tools/make_icon.py
import math
# Square pyramid, base half-width 1, height ~ Giza proportion.
H = 1.30
base = [(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1)]   # NW, NE, SE, SW (z toward viewer = south)
apex = (0,H,0)
yaw = math.radians(28); pitch = math.radians(16)
def proj(p):
    x,y,z = p
    x,z = x*math.cos(yaw) - z*math.sin(yaw), x*math.sin(yaw) + z*math.cos(yaw)
    y,z = y*math.cos(pitch) - z*math.sin(pitch), y*math.sin(pitch) + z*math.cos(pitch)
    return (x, -y, z)   # screen y down
P = [proj(b) for b in base]; A = proj(apex)
# which faces face the viewer (camera looks along -z in camera space -> visible if normal z > 0)
def faces():
    out=[]
    for i in range(4):
        a,b = base[i], base[(i+1)%4]
        e1=[b[k]-a[k] for k in range(3)]; e2=[apex[k]-a[k] for k in range(3)]
        n=[e1[1]*e2[2]-e1[2]*e2[1], e1[2]*e2[0]-e1[0]*e2[2], e1[0]*e2[1]-e1[1]*e2[0]]
        mid=[(a[k]+b[k]+apex[k])/3 for k in range(3)]
        if sum(n[k]*mid[k] for k in range(3))<0: n=[-v for v in n]
        nn=proj(n); 
        # rotate normal only (no translation needed)
        out.append((i,(i+1)%4,n))
    return out
cam = proj((0,0,0))
def cam_normal(n):
    x,y,z=n
    x,z = x*math.cos(yaw) - z*math.sin(yaw), x*math.sin(yaw) + z*math.cos(yaw)
    y,z = y*math.cos(pitch) - z*math.sin(pitch), y*math.sin(pitch) + z*math.cos(pitch)
    return (x,y,z)
light = (-0.55, 0.65, 0.52); L=math.sqrt(sum(v*v for v in light)); light=tuple(v/L for v in light)
vis=[]
for i,j,n in faces():
    cn = cam_normal(n)
    if cn[2] > 0:
        l = sum(n[k]*light[k] for k in range(3))/math.sqrt(sum(v*v for v in n))
        vis.append((i,j,l))
pts = P+[A]
xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
pad=0.12
minx,maxx,miny,maxy=min(xs)-pad,max(xs)+pad,min(ys)-pad,max(ys)+pad
W=400; S=W/(maxx-minx); Hh=round((maxy-miny)*S)
def sc(p): return ((p[0]-minx)*S, (p[1]-miny)*S)
def f(v): return f"{v:.1f}"
a=sc(A)
parts=[]
grads=[]
vis.sort(key=lambda t:-t[2])
for idx,(i,j,l) in enumerate(vis):
    p1,p2=sc(P[i]),sc(P[j])
    lit = l
    stops = ([(0,'#fff6d2'),(0.32,'#f8d567'),(0.72,'#dda22c'),(1,'#a86a12')] if idx==0
             else [(0,'#e0a63c'),(0.38,'#a36912'),(1,'#4a2a03')])
    gid=f"g{idx}"
    mx,my=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2
    grads.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(mx)}" y2="{f(my)}">' + ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops) + '</linearGradient>')
    parts.append(f'<polygon points="{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])} {f(a[0])},{f(a[1])}" fill="url(#{gid})"/>')
    # stone courses: lines parallel to the base edge
    for t in (0.2,0.4,0.6,0.8):
        q1=(p1[0]+(a[0]-p1[0])*t, p1[1]+(a[1]-p1[1])*t); q2=(p2[0]+(a[0]-p2[0])*t, p2[1]+(a[1]-p2[1])*t)
        col = 'rgba(140,84,8,0.22)' if idx==0 else 'rgba(30,14,0,0.26)'
        parts.append(f'<line x1="{f(q1[0])}" y1="{f(q1[1])}" x2="{f(q2[0])}" y2="{f(q2[1])}" stroke="{col}" stroke-width="2"/>')
# shared front ridge between the two visible faces: a bright edge
shared = set(vis[0][:2]) & set(vis[1][:2])
k = shared.pop()
r=sc(P[k])
ridge=f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(r[0])}" y2="{f(r[1])}" stroke="#fff6d6" stroke-width="3" stroke-linecap="round" opacity="0.85"/>'
# capstone (pyramidion): top 16% brighter
cap=[]
for idx,(i,j,l) in enumerate(vis):
    p1,p2=sc(P[i]),sc(P[j]); t=0.84
    q1=(p1[0]+(a[0]-p1[0])*t, p1[1]+(a[1]-p1[1])*t); q2=(p2[0]+(a[0]-p2[0])*t, p2[1]+(a[1]-p2[1])*t)
    cap.append(f'<polygon points="{f(q1[0])},{f(q1[1])} {f(q2[0])},{f(q2[1])} {f(a[0])},{f(a[1])}" fill="{"#fffbe6" if idx==0 else "#f2c96e"}"/>')
outline=' '.join(f"{f(sc(P[i])[0])},{f(sc(P[i])[1])}" for i in sorted({vis[0][0],vis[0][1],vis[1][0],vis[1][1]}, key=lambda i: sc(P[i])[0]))
glint=f'<circle cx="{f(a[0])}" cy="{f(a[1]+6)}" r="5" fill="#ffffff" opacity="0.9"/>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}">
<title>Golden pyramid</title>
<defs>{''.join(grads)}</defs>
{''.join(parts)}
{''.join(cap)}
{ridge}
{glint}
</svg>
'''
open(__import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'web', 'icon.svg'),'w').write(svg)
print(W,Hh, 'visible faces', [(i,j,round(l,2)) for i,j,l in vis])
