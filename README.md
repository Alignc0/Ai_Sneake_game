# 🐍 A\* + Kuyruk Takipli Yılan Oyunu

Bu proje, klasik yılan oyununu yapay zeka destekli bir versiyon haline getirerek A\* algoritması, kuyruk takibi, flood fill (boşluk analizi) ve geleceği simüle ederek karar verme gibi stratejileri entegre eder. 🎮🧠

---

## 🚀 Projenin Özeti

* 🧱 **Pygame tabanlı oyun arayüzü**
* 📍 **A* (A-Star) algoritması ile yem hedefleme*\*
* 🌀 **Kuyruk takibi ile kendini kilitlemeden kurtulma stratejisi**
* 🌊 **Flood fill ile boş alan tespiti (BFS)**
* 🔮 **Geleceği simüle ederek yeme gitme kararının risk analizini yapma**
* 🧑‍💻 **Python teknik bilgisi ve ChatGPT desteği ile geliştirilmiştir**

---

## 👨‍🔬 Teknik Altyapı

Bu oyun, Python programlama dilindeki teknik bilgilerimi kullanarak ve ChatGPT ile ileri düzey prompt stratejileri kurarak oluşturulmuştur. Kodlar algoritmik temele oturtulmuş, modüler yapılandırılmış ve aşağıdaki gibi optimize edilmiştir:

* 🔁 Döngü kontrolleri
* 🎯 A\* algoritmasında `heapq` kullanımı (öncelik kuyruğu)
* 🔍 Flood Fill için `deque` ile BFS
* 🧠 Durumsal karar ağacı mantığı
* 🔂 Kuyruk hedeflemesi ile alternatif kaçış senaryoları

---

## 🧱 Gelişim Aşamaları

### 1. 🟡 Klasik Yapay Zeka (Greedy)

* Yılan, yeme doğru çizgisel olarak hareket eder.
* Çevredeki en kısa mesafeye giden yönü seçer.
* Tehlike tespiti yoktur.

### 2. 🟢 A\* Algoritmasının Entegrasyonu

* Yeme giden en kısa ve en güvenli yol bulunur.
* Engel (yılanın vücudu veya duvar) kontrolü dahil edilmiştir.

### 3. 🔁 Kuyruk Takibi Stratejisi

* A\* ile yeme gidilemediği durumlarda, yılan kendi kuyruğunu hedef alır.
* Kuyruğuyla temasa geçip tekrar hareket alanı oluşturarak hayatta kalmaya çalışır.

### 4. 🌊 Flood Fill Boşluk Analizi

* Flood fill (BFS tabanlı) algoritmayla yılanın yüzeydeki hareket edebileceği boş alan hesaplanır.
* Gelecekteki hamlenin yılanı öldürüp öldürmeyeceği bu analizle belirlenir.

### 5. 🔮 Gelecek Simülasyonu

* A\* ile yeme gitme kararının sonrasındaki olası durumlar simüle edilir.
* Simüle edilen konumda yılanın hayatta kalabileceği garantilenmeden yem hedeflenmez.

---

## ⚙️ Kullanılan Teknolojiler

* 🐍 **Python 3.x**
* 🎮 **Pygame**
* ⛓️ **heapq** (A\* için öncelik kuyruğu)
* 🧵 **collections.deque** (BFS için kuyruk yapısı)
* 📐 **math.hypot** (Heuristik mesafe ölçümü)

---

## 🧠 Strateji Özeti

1. 🎯 Yem hedeflenir.
2. 🧠 Yem hedeflenebiliyorsa, yeme giden yolda hayatta kalıp kalamayacağı simüle edilir.
3. 🚪 Riskli ise kuyruk hedeflenir.
4. 🤖 Kuyruğa da ulaşılamıyorsa mevcut yönde devam edilir.

---
## 📸Görüntüler
![Ekran Alıntısı1](https://github.com/user-attachments/assets/886c0996-5be6-4d1b-8bb8-8333b7a75089)
![Ekran Alıntısı](https://github.com/user-attachments/assets/46fa98a8-6f45-4753-ab14-591b4212c6e1)


## 🔧 Gelecekteki Gelişim Önerileri

* 🪜 Yeme gitmeden önce kalan alan üzerinde en uzun yol alternatifleri incelenebilir.
* 🤖 Q-learning veya DQN gibi reinforcement learning yaklaşımlarıyla daha öğrenen sistemler geliştirilebilir.
* 🌍 Farklı harita modları ve seviyeler eklenebilir.

---

📌 **Not:** Bu proje, yapay zeka algoritmalarını oyun ortamında uygulamak için ideal bir çalışma alanı sunar. Kod yapısı sade, geliştirilebilir ve eğitici niteliktedir. Kodlarım Python teknik bilgisi ve ChatGPT'nin özel prompt destekleri ile geliştirilmiştir. 🧠✨
