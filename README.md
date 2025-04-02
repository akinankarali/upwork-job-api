# Upwork Job Scraper API

A simple Flask API that uses Playwright to scrape filtered job listings from Upwork.

---

## 🚀 Features

- 🔍 Search jobs on Upwork with filters (query, experience, rate, etc.)
- ⚙️ Scrapes data using headless Chromium via Playwright
- 📦 Returns structured JSON

---

## 📦 Install & Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Run the API
python scraper_api.py
```

The API will be available at:
```
http://127.0.0.1:5000/search
```

---

## 📘 API Documentation

### 🔗 Endpoint
```
GET /search
```

---

### ✅ Supported Query Parameters

| Parametre         | Gerekli | Açıklama                                           | Örnek Değer     |
|-------------------|---------|----------------------------------------------------|-----------------|
| `query`           | ✅      | Arama kelimesi                                     | `python`        |
| `experience`      | ❌      | Deneyim seviyesi                                   | `entry_level`, `intermediate`, `expert` |
| `job_type`        | ❌      | İş türü                                            | `hourly`, `fixed-price` |
| `rate_min`        | ❌      | Saatlik minimum ücret                              | `20`            |
| `rate_max`        | ❌      | Saatlik maksimum ücret                             | `100`           |
| `duration`        | ❌      | Proje süresi                                       | `week`, `month`, `ongoing` |
| `workload`        | ❌      | Haftalık iş yükü                                   | `as_needed`, `full_time` |
| `client_hires`    | ❌      | İşverenin geçmiş işe alım sayısı                   | `0`, `1-9`, `10plus` |
| `contract_to_hire`| ❌      | Uzun vadeli iş teklifi içerip içermediği           | `true`, `false` |

> 🔹 `rate_min` / `rate_max` parametreleri yalnızca `job_type=hourly` iken anlamlıdır.

---

### 📦 Örnek İstekler

#### 1. Sadece arama terimiyle:
```
GET /search?query=python
```

#### 2. Tüm filtrelerle:
```
GET /search?query=python&job_type=hourly&experience=expert&rate_min=30&rate_max=100&duration=month&workload=as_needed&client_hires=10plus&contract_to_hire=true
```

---

## ⚡️ Frontend'den Axios ile Kullanım

```js
import axios from "axios";

const params = {
  query: "python",
  experience: "expert",
  job_type: "hourly",
  rate_min: 30,
  rate_max: 100,
  duration: "month",
  workload: "as_needed",
  client_hires: "10plus",
  contract_to_hire: true
};

axios.get("http://127.0.0.1:5000/search", { params })
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
```

---

## 📬 Postman ile Kullanım

1. Yeni bir `GET` isteği oluştur.
2. URL kısmına:
```
http://127.0.0.1:5000/search
```
3. Sağdaki **Params** sekmesinde şu değerleri gir:

| Key               | Value         |
|------------------|---------------|
| query            | python        |
| job_type         | hourly        |
| experience       | expert        |
| rate_min         | 30            |
| rate_max         | 100           |
| duration         | month         |
| workload         | as_needed     |
| client_hires     | 10plus        |
| contract_to_hire | true          |

---

## 📤 Response Format (JSON)

```json
[
  {
    "title": "Python Developer Needed",
    "url": "https://www.upwork.com/jobs/...",
    "description": "We need a Python expert for web scraping.",
    "rate": "Hourly: $30.00 - $50.00",
    "experience": "Expert",
    "duration": "Est. time: 1 to 3 months, 30+ hrs/week",
    "tags": ["Python", "Web Scraping"]
  },
  ...
]
```

---

## 📌 Notlar

- İstek sonrası veri çekimi 10–20 saniye sürebilir.
- İlk çalıştırmadan önce `playwright install` komutunu çalıştırmayı unutmayın.
- Bu sadece geliştirme ortamı içindir. Production için `gunicorn`, `Docker`, `Render`, `Railway` gibi araçlar önerilir.

---

💻 Built by [@saimakinankarali](https://github.com/saimakinankarali)
