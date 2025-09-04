import pygame, random, time, os

# ======= PNG-NAMEN (final nach deiner Vorgabe) =======
FILENAMES = {
    "front": "file_0000000028a861fb98410ba7c0562c93.png",      # Punkte (links/rechts)
    "side":  "file_00000000187c61f4bc3aed9c27ed2cab (1).png",  # Pfeile links/rechts
    "up":    "file_00000000dae861faae0a8eef36103146 (1).png",  # Pfeil nach oben
}
# =====================================================

def try_set_display(fullscreen=True):
    pygame.display.quit(); pygame.display.init()
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    flags = pygame.FULLSCREEN if fullscreen else 0
    try:
        screen = pygame.display.set_mode((W, H), flags)
        return screen, W, H, True
    except Exception:
        if fullscreen:
            screen = pygame.display.set_mode((int(W*0.9), int(H*0.9)))
            W, H = screen.get_size()
            return screen, W, H, False
        raise

def possible_paths(fname):
    here = os.getcwd()
    return [
        fname,
        os.path.join(here, fname),
        "/storage/emulated/0/Pydroid3/" + fname,
        "/storage/emulated/0/Download/" + fname,
    ]

def safe_load_image(fname, scale_wh):
    last_err = None
    for p in possible_paths(fname):
        if os.path.exists(p):
            try:
                img = pygame.image.load(p).convert_alpha()
                if scale_wh:
                    img = pygame.transform.smoothscale(img, scale_wh)
                return img, p, None
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
    return None, None, (f"PNG NICHT GEFUNDEN: {fname}", last_err)

# --------- Start ---------
pygame.init()
screen, W, H, is_fullscreen = try_set_display(fullscreen=True)
pygame.display.set_caption("Box-Training – PNG Gloves")
clock = pygame.time.Clock()

# UI
delay = 1.6
DELAY_MIN, DELAY_MAX, DELAY_STEP = 0.3, 6.0, 0.1
UI_HEIGHT = int(H * 0.18)
font_small = pygame.font.SysFont(None, int(H*0.04))
font_dbg   = pygame.font.SysFont(None, int(H*0.03))

COL_BG   = (10,10,12)
COL_UI   = (22,22,26)
COL_BTN  = (60,62,70)
COL_BR   = (140,140,150)
COL_TXT  = (235,235,240)
COL_ERR  = (250,80,80)

btn_pad = 20
btn_h = UI_HEIGHT - 2*btn_pad
button_minus = pygame.Rect(32,           H-UI_HEIGHT+btn_pad, 200, btn_h)
button_exit  = pygame.Rect(W//2-100,     H-UI_HEIGHT+btn_pad, 200, btn_h)
button_plus  = pygame.Rect(W-32-200,     H-UI_HEIGHT+btn_pad, 200, btn_h)

def draw_button(rect, label, fill=COL_BTN):
    pygame.draw.rect(screen, fill, rect, border_radius=18)
    pygame.draw.rect(screen, COL_BR, rect, 3, border_radius=18)
    txt = font_small.render(label, True, COL_TXT)
    screen.blit(txt, txt.get_rect(center=rect.center))

# ----- Bilder laden -----
AREA_H = H - UI_HEIGHT
BASE_SIZE = min(W, AREA_H) // 2
scale = (BASE_SIZE, BASE_SIZE)

front_img, front_path, front_err = safe_load_image(FILENAMES["front"], scale)
side_img,  side_path,  side_err  = safe_load_image(FILENAMES["side"],  scale)
up_img,    up_path,    up_err    = safe_load_image(FILENAMES["up"],    scale)

def draw_placeholder(text):
    s = pygame.Surface((BASE_SIZE, BASE_SIZE), pygame.SRCALPHA)
    s.fill((180, 40, 40, 220))
    pygame.draw.rect(s, (255,255,255), s.get_rect(), 6)
    t1 = font_small.render("PNG fehlt", True, (255,255,255))
    t2 = font_small.render(text, True, (255,255,255))
    s.blit(t1, t1.get_rect(center=(BASE_SIZE//2, BASE_SIZE//2 - 20)))
    s.blit(t2, t2.get_rect(center=(BASE_SIZE//2, BASE_SIZE//2 + 20)))
    return s

if front_img is None: front_img = draw_placeholder(FILENAMES["front"])
if side_img  is None: side_img  = draw_placeholder(FILENAMES["side"])
if up_img    is None: up_img    = draw_placeholder(FILENAMES["up"])

CENTER = (W//2, (H-UI_HEIGHT)//2)

# Zeichner
def draw_front_left():
    img = pygame.transform.flip(front_img, True, False)
    rect = img.get_rect(center=(CENTER[0]-BASE_SIZE//2, CENTER[1]))
    screen.blit(img, rect)

def draw_front_right():
    img = front_img
    rect = img.get_rect(center=(CENTER[0]+BASE_SIZE//2, CENTER[1]))
    screen.blit(img, rect)

def draw_side_left():
    img = pygame.transform.flip(side_img, True, False)
    rect = img.get_rect(center=CENTER); screen.blit(img, rect)

def draw_side_right():
    img = side_img
    rect = img.get_rect(center=CENTER); screen.blit(img, rect)

def draw_up():
    img = up_img
    rect = img.get_rect(center=CENTER); screen.blit(img, rect)

STIMULI = [
    ("dot_left",   draw_front_left),
    ("dot_right",  draw_front_right),
    ("arr_left",   draw_side_left),
    ("arr_right",  draw_side_right),
    ("arr_up",     draw_up),
]

def draw_ui():
    pygame.draw.rect(screen, COL_UI, (0, H-UI_HEIGHT, W, UI_HEIGHT))
    t = font_small.render(f"Intervall: {delay:.1f}s", True, COL_TXT)
    screen.blit(t, (W//2 - t.get_width()//2, H-UI_HEIGHT + 6))
    draw_button(button_minus, "Langsamer")
    draw_button(button_exit,  "Beenden", fill=(120,45,45))
    draw_button(button_plus,  "Schneller")

def draw_debug():
    y = 8
    def line(msg, col=(200,200,200)):
        nonlocal y
        txt = font_dbg.render(msg, True, col)
        screen.blit(txt, (10, y)); y += txt.get_height() + 4
    line(f"Fullscreen: {is_fullscreen}")
    line(f"Front: {front_path if front_path else 'FEHLT'}", (120,220,120) if front_path else COL_ERR)
    if front_err: line(front_err[0], COL_ERR)
    line(f"Side : {side_path  if side_path  else 'FEHLT'}", (120,220,120) if side_path  else COL_ERR)
    if side_err:  line(side_err[0], COL_ERR)
    line(f"Up   : {up_path    if up_path    else 'FEHLT'}", (120,220,120) if up_path    else COL_ERR)
    if up_err:    line(up_err[0], COL_ERR)

# Loop
running = True
last_switch = 0.0
current = random.choice(STIMULI)

while running:
    now = time.time()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if button_plus.collidepoint(ev.pos):
                delay = max(DELAY_MIN, round(delay - DELAY_STEP, 2))
            elif button_minus.collidepoint(ev.pos):
                delay = min(DELAY_MAX, round(delay + DELAY_STEP, 2))
            elif button_exit.collidepoint(ev.pos):
                running = False

    if now - last_switch >= delay:
        current = random.choice(STIMULI)
        last_switch = now

    screen.fill(COL_BG)
    current[1]()
    draw_ui()
    draw_debug()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()