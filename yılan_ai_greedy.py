import pygame
import random
import time
import math

# --- Sabitler ve Değişkenler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YESIL = (0, 255, 0)
KIRMIZI = (255, 0, 0)

GENISLIK = 600
YUKSEKLIK = 400
BLOK_BOYUTU = 20
FPS = 15 # Yapay zekanın performansını görmek için hızı biraz artırdık

YUKARI = (0, -1)
ASAGI = (0, 1)
SOL = (-1, 0)
SAG = (1, 0)

# --- Pygame Başlatma ---
pygame.init()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yapay Zeka Destekli Yılan Oyunu")
saat = pygame.time.Clock()

class Yilan:
    def __init__(self):
        self.uzunluk = 1
        self.pozisyonlar = [((GENISLIK / 2), (YUKSEKLIK / 2))]
        self.yon = random.choice([YUKARI, ASAGI, SOL, SAG])
        self.renk = YESIL
        self.skor = 0

    def get_kafa_pozisyonu(self):
        return self.pozisyonlar[0]

    def hareket_et(self):
        kafa = self.get_kafa_pozisyonu()
        x, y = self.yon
        yeni_kafa = ((kafa[0] + (x * BLOK_BOYUTU)), (kafa[1] + (y * BLOK_BOYUTU)))
        self.pozisyonlar.insert(0, yeni_kafa)
        if len(self.pozisyonlar) > self.uzunluk:
            self.pozisyonlar.pop()

    def yon_degistir(self, yeni_yon):
        if self.uzunluk > 1 and (yeni_yon[0] * -1, yeni_yon[1] * -1) == self.yon:
            return
        else:
            self.yon = yeni_yon

    def ciz(self, yuzey):
        for p in self.pozisyonlar:
            r = pygame.Rect((p[0], p[1]), (BLOK_BOYUTU, BLOK_BOYUTU))
            pygame.draw.rect(yuzey, self.renk, r)
            pygame.draw.rect(yuzey, SIYAH, r, 1)

class Yem:
    def __init__(self, yilan_pozisyonlari):
        self.pozisyon = (0, 0)
        self.renk = KIRMIZI
        self.yeni_pozisyon(yilan_pozisyonlari)

    def yeni_pozisyon(self, yilan_pozisyonlari=[]):
        while True:
            x = random.randrange(0, GENISLIK // BLOK_BOYUTU) * BLOK_BOYUTU
            y = random.randrange(0, YUKSEKLIK // BLOK_BOYUTU) * BLOK_BOYUTU
            if (x, y) not in yilan_pozisyonlari:
                self.pozisyon = (x, y)
                break

    def ciz(self, yuzey):
        r = pygame.Rect((self.pozisyon[0], self.pozisyon[1]), (BLOK_BOYUTU, BLOK_BOYUTU))
        pygame.draw.rect(yuzey, self.renk, r)

def carpisma_kontrolu(pozisyon, yilan_pozisyonlari):
    # Duvarlara çarpma kontrolü
    if pozisyon[0] >= GENISLIK or pozisyon[0] < 0 or pozisyon[1] >= YUKSEKLIK or pozisyon[1] < 0:
        return True
    # Yılanın kendine çarpma kontrolü
    if pozisyon in yilan_pozisyonlari:
        return True
    return False

def yapay_zeka_hamlesi(yilan, yem):
    kafa_pozisyonu = yilan.get_kafa_pozisyonu()
    olasi_yonler = [YUKARI, ASAGI, SOL, SAG]
    
    # Mevcut yönün tersini listeden çıkar (gereksiz hamle)
    ters_yon = (yilan.yon[0] * -1, yilan.yon[1] * -1)
    if ters_yon in olasi_yonler:
        olasi_yonler.remove(ters_yon)
        
    guvenli_hamleler = []
    for yon in olasi_yonler:
        # Olası bir sonraki adımı hesapla
        olasi_pozisyon = (kafa_pozisyonu[0] + yon[0] * BLOK_BOYUTU, kafa_pozisyonu[1] + yon[1] * BLOK_BOYUTU)
        # Eğer bu adım güvenliyse, listeye ekle
        if not carpisma_kontrolu(olasi_pozisyon, yilan.pozisyonlar):
            guvenli_hamleler.append(yon)

    if not guvenli_hamleler:
        # Eğer güvenli hamle yoksa, mevcut yönde devam et (kaçınılmaz son)
        return yilan.yon

    # Güvenli hamleler arasından yeme en çok yaklaştıranı seç
    en_iyi_hamle = None
    en_kisa_mesafe = float('inf')
    for hamle in guvenli_hamleler:
        olasi_pozisyon = (kafa_pozisyonu[0] + hamle[0] * BLOK_BOYUTU, kafa_pozisyonu[1] + hamle[1] * BLOK_BOYUTU)
        # Basit Öklid mesafesi hesaplaması
        mesafe = math.sqrt((olasi_pozisyon[0] - yem.pozisyon[0])**2 + (olasi_pozisyon[1] - yem.pozisyon[1])**2)
        if mesafe < en_kisa_mesafe:
            en_kisa_mesafe = mesafe
            en_iyi_hamle = hamle
            
    return en_iyi_hamle

# --- Ana Oyun Döngüsü ---
def ana_dongu():
    yilan = Yilan()
    yem = Yem(yilan.pozisyonlar)
    skor = 0

    oyun_bitti = False
    while not oyun_bitti:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                quit()

        # --- YAPAY ZEKA KONTROLÜ ---
        # Klavye kontrollerini tamamen kaldırdık.
        yeni_yon = yapay_zeka_hamlesi(yilan, yem)
        yilan.yon_degistir(yeni_yon)
        # -------------------------

        yilan.hareket_et()

        kafa = yilan.get_kafa_pozisyonu()
        if carpisma_kontrolu(kafa, yilan.pozisyonlar[1:]): # Kendine çarpma kontrolü için kafa hariç listeyi gönder
             oyun_bitti = True

        if kafa == yem.pozisyon:
            yilan.uzunluk += 1
            skor += 10
            yem.yeni_pozisyon(yilan.pozisyonlar)

        ekran.fill(SIYAH)
        yilan.ciz(ekran)
        yem.ciz(ekran)

        # Skoru Ekrana Yazdır
        font = pygame.font.SysFont('arial', 24)
        skor_yazisi = font.render(f'Skor: {skor}', True, BEYAZ)
        ekran.blit(skor_yazisi, (5, 5))

        pygame.display.flip()
        saat.tick(FPS)

    # Oyun Bitti Ekranı
    font = pygame.font.SysFont('arial', 50)
    mesaj = font.render('OYUN BİTTİ', True, BEYAZ)
    mesaj_kordinat = mesaj.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 - 25))
    ekran.blit(mesaj, mesaj_kordinat)
    
    skor_mesaji = font.render(f'Son Skor: {skor}', True, BEYAZ)
    skor_kordinat = skor_mesaji.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 + 25))
    ekran.blit(skor_mesaji, skor_kordinat)
    
    pygame.display.flip()
    time.sleep(3)
    
    pygame.quit()
    quit()

# Oyunu başlat
ana_dongu()