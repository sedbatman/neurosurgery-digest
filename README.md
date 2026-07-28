# 🧠 Neurosurgery Digest

**neurosurgery.digest** - مروری بر مهم‌ترین مقالات نوروسرجری

یک وبلاگ فارسی برای دکتر علیرضا، جراح آینده ستون فقرات

## 🌟 ویژگی‌ها

- طراحی RTL (راست به چپ) برای فارسی
- تم تاریک با رنگ‌های ایندیگو/بنفش
- نمایش مقالات به صورت کارت با افکت‌های زیبا
- جستجو و فیلتر بر اساس نوع مطالعه
- سازگار با موبایل و تبلت
- پشتیبانی از پرینت

## 🚀 شروع سریع

### نصب

```bash
git clone https://github.com/yourusername/neurosurgery-digest.git
cd neurosurgery-digest
```

### راه‌اندازی وبسایت محلی

```bash
# استفاده از Python
cd public
python -m http.server 8000

# یا استفاده از Node.js
cd public
npx serve
```

سپس مرورگر را باز کنید: `http://localhost:8000`

## 📝 اضافه کردن مقاله جدید

### ۱. فایل محتوا ایجاد کنید

یک فایل HTML با محتوای مقاله ایجاد کنید (بدون تگ‌های `<html>`, `<head>`, `<body>`):

```html
<h2>مقدمه</h2>
<p>متن مقاله...</p>

<h2>روش‌ها</h2>
<p>توضیح روش‌ها...</p>

<h2>نتایج</h2>
<p>نتایج مطالعه...</p>
```

### ۲. اسکریپت اضافه کردن را اجرا کنید

```bash
python scripts/add_post.py \
    --slug spinal-fusion-outcomes \
    --title "نتایج فیوژن ستون فقرات در بیماران مبتلا به اسکولیوز" \
    --summary "بررسی نتایج بلندمدت فیوژن ستون فقرات در بیماران مبتلا به اسکولیوز نوجوانان" \
    --content-file article.html \
    --date 2024-01-15 \
    --journal "Journal of Neurosurgery: Spine" \
    --study_type "مطالعه مروری"
```

### انواع مطالعه معتبر

- `راهنمای بالینی` - Clinical Guidelines
- `مطالعه مروری` - Review Studies
- `کارآزمایی بالینی` - Clinical Trials
- `مطالعه کوهورت` - Cohort Studies
- `مطالعه موردی` - Case Studies

## 🔄 بازسازی صفحه اصلی

اگر نیاز به بازسازی دستی صفحه اصلی دارید:

```bash
python scripts/build_index.py
```

## 🚢 استقرار

### Cloudflare Pages

اسکریپت استقرار از قبل پیکربندی شده است:

```bash
bash scripts/deploy.sh
```

### استقرار دستی

```bash
# اضافه کردن تغییرات
git add -A
git commit -m "Add new post"

# ارسال به GitHub
git push origin main

# استقرار با wrangler
wrangler pages deploy public --project-name=neurosurgery-digest
```

## 📁 ساختار پروژه

```
neurosurgery-digest/
├── public/
│   ├── index.html          # صفحه اصلی
│   ├── style.css           # استایل‌ها
│   ├── post.html           # صفحه مقاله
│   ├── posts.json          # لیست مقالات
│   └── posts/
│       ├── .gitkeep
│       └── *.html          # فایل‌های مقالات
├── scripts/
│   ├── add_post.py         # اسکریپت اضافه کردن مقاله
│   ├── build_index.py      # اسکریپت بازسازی صفحه اصلی
│   └── deploy.sh           # اسکریپت استقرار
├── .gitignore
└── README.md
```

## 🎨 طراحی

- **تم تاریک** با پس‌زمینه `#0f172a`
- **رنگ اصلی**: ایندیگو (`#6366f1`)
- **رنگ فرعی**: بنفش (`#8b5cf6`)
- **فونت**: Vazirmatn برای فارسی
- **افکت‌ها**: انیمیشن‌های نرم و hover effects

## 📄 مجوز

© ۱۴۰۵ neurosurgery.digest | ساخته شده با ❤️ برای علاقه‌مندان به نوروسرجری

---

**دکتر علیرضا | آینده جراح ستون فقرات** 🧠🦴