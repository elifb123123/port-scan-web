# Port Scan Web


Bu repo, cihazlar için port durumu kayıtları tutan ve IP adresine göre dış portların (external ports) durumunu sorgulayan basit bir web uygulamasıdır. Web arayüzü üzerinden hedef IP’ye port taraması yapabilir ve port durumlarını görebilirsiniz.

## Özellikler

-IP adresi girerek dış port taraması yapma

-Açık/kapalı port durumlarını listeme

-Port tarama sonuçlarını saklama (kayıt defteri)

-Basit ve hızlı web arayüzüyle kullanım


## Teknolojiler

- Python 3
- Flask
- MySQL
- HTML / CSS

## Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/elifb123123/port-scan-web.git
cd port-scan-web
```

Sanal ortam oluşturun ve aktif edin:

```bash
python -m venv venv
source venv/bin/activate
```

Windows için:

```bash
venv\Scripts\activate
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
python flaskdemo.py
```


## Proje Yapısı

```text
port-scan-web/
├── flaskdemo.py
├── app.py
├── templates/
├── static/
├── requirements.txt
└── README.md
```

