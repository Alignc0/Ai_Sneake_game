import pygame
import random
import time
import math
import heapq
from collections import deque

# --- Sabitler ve Değişkenler ---
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YESIL = (0, 255, 0)
KIRMIZI = (255, 0, 0)

GENISLIK = 600
YUKSEKLIK = 400
BLOK_BOYUTU = 20
FPS = 15

YUKARI = (0, -1)
ASAGI = (0, 1)
SOL = (-1, 0)
SAG = (1, 0)

pygame.init()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("A* + Kuyruk Takipli Yılan Oyunu")
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

    def get_kuyruk_sonu(self):
        return self.pozisyonlar[-1]

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
    if pozisyon[0] >= GENISLIK or pozisyon[0] < 0 or pozisyon[1] >= YUKSEKLIK or pozisyon[1] < 0:
        return True
    if pozisyon in yilan_pozisyonlari:
        return True
    return False

def flood_fill(baslangic, yilan_pozisyonlari):
    ziyaret_edilen = set()
    kuyruk = deque([baslangic])
    sayac = 0

    while kuyruk:
        poz = kuyruk.popleft()
        if poz in ziyaret_edilen or carpisma_kontrolu(poz, yilan_pozisyonlari):
            continue
        ziyaret_edilen.add(poz)
        sayac += 1
        for yon in [YUKARI, ASAGI, SOL, SAG]:
            komsu = (poz[0] + yon[0]*BLOK_BOYUTU, poz[1] + yon[1]*BLOK_BOYUTU)
            if komsu not in ziyaret_edilen:
                kuyruk.append(komsu)

    return sayac

def hayatta_kalabilir_mi(baslangic, engeller, hamle_sayisi):
    kafa = baslangic
    for _ in range(hamle_sayisi):
        max_doluluk = -1
        en_iyi_hamle = None
        for yon in [YUKARI, ASAGI, SOL, SAG]:
            komsu = (kafa[0] + yon[0]*BLOK_BOYUTU, kafa[1] + yon[1]*BLOK_BOYUTU)
            if carpisma_kontrolu(komsu, engeller):
                continue
            bosluk = flood_fill(komsu, engeller)
            if bosluk > max_doluluk:
                max_doluluk = bosluk
                en_iyi_hamle = yon
        if en_iyi_hamle:
            kafa = (kafa[0] + en_iyi_hamle[0]*BLOK_BOYUTU, kafa[1] + en_iyi_hamle[1]*BLOK_BOYUTU)
            engeller.insert(0, kafa)
            engeller.pop()
        else:
            return False
    return True

def karar_ver(yilan, yem):
    kafa = yilan.get_kafa_pozisyonu()
    kuyruk = yilan.get_kuyruk_sonu()
    engeller = yilan.pozisyonlar.copy()
    engellersiz_kuyruk = engeller[:-1]

    yol_yeme = astar(kafa, yem.pozisyon, engellersiz_kuyruk)
    if yol_yeme:
        dx, dy = yol_yeme[0]
        simule_kafa = (kafa[0] + dx * BLOK_BOYUTU, kafa[1] + dy * BLOK_BOYUTU)
        hayali_yilan = [simule_kafa] + engellersiz_kuyruk[:-1]
        if hayatta_kalabilir_mi(simule_kafa, hayali_yilan.copy(), 10):
            return yol_yeme

    yol_kuyruga = astar(kafa, kuyruk, engellersiz_kuyruk)
    if yol_kuyruga:
        return yol_kuyruga

    return [yilan.yon]

# NOT: astar fonksiyonu yukarıda eksik kalmış, geri ekleniyor

def astar(baslangic, hedef, engeller):
    kapanan = set()
    acik = []
    heapq.heappush(acik, (0, baslangic, []))

    while acik:
        _, mevcut, yol = heapq.heappop(acik)

        if mevcut == hedef:
            return yol if yol else [YUKARI]

        if mevcut in kapanan:
            continue
        kapanan.add(mevcut)

        for yon in [YUKARI, ASAGI, SOL, SAG]:
            komsu = (mevcut[0] + yon[0]*BLOK_BOYUTU, mevcut[1] + yon[1]*BLOK_BOYUTU)
            if carpisma_kontrolu(komsu, engeller):
                continue
            yeni_yol = yol + [yon]
            g = len(yeni_yol)
            h = math.hypot(komsu[0] - hedef[0], komsu[1] - hedef[1])
            heapq.heappush(acik, (g + h, komsu, yeni_yol))

    return None

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

        yol = karar_ver(yilan, yem)
        if yol:
            yilan.yon_degistir(yol[0])

        yilan.hareket_et()

        kafa = yilan.get_kafa_pozisyonu()
        if carpisma_kontrolu(kafa, yilan.pozisyonlar[1:]):
            oyun_bitti = True

        if kafa == yem.pozisyon:
            yilan.uzunluk += 1
            skor += 10
            yem.yeni_pozisyon(yilan.pozisyonlar)

        ekran.fill(SIYAH)
        yilan.ciz(ekran)
        yem.ciz(ekran)

        font = pygame.font.SysFont('arial', 24)
        skor_yazisi = font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_yazisi, (5, 5))

        pygame.display.flip()
        saat.tick(FPS)

    font = pygame.font.SysFont('arial', 50)
    mesaj = font.render("OYUN BITTI", True, BEYAZ)
    ekran.blit(mesaj, mesaj.get_rect(center=(GENISLIK / 2, YUKSEKLIK / 2 - 25)))
    skor_mesaji = font.render(f"Son Skor: {skor}", True, BEYAZ)
    ekran.blit(skor_mesaji, skor_mesaji.get_rect(center=(GENISLIK / 2, YUKSEKLIK / 2 + 25)))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    quit()

ana_dongu()
