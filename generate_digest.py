import json
import os

with open('/root/.hermes/_build/articles_data.json', 'r') as f:
    data = json.load(f)

articles = data['articles']
target_pmids = [
    "42595326", # Vascular: Recurrent nontraumatic acute subdural hematoma secondary to ruptured accessory meningeal artery aneurysm
    "42595109", # Neuro-oncology: TIMELESS promotes glioma stemness and malignancy through JAK-STAT3 pathway
    "42595494", # Functional: Subthalamic Nucleus Deep Brain Stimulation Enhanced Long-Latency Reflex II in Parkinson's Disease
    "42594313", # Spine: Influence of Preoperative Mental Health on Surgical and Clinical Outcomes in Degenerative Cervical Myelopathy
    "42592584", # Skull Base: Preliminary Clinical Experience With a Novel Foamy Collagen-Based Dural Substitute (Foamagen)
    "42594036", # Neurotrauma: Delayed External Brain Tamponade Following Repeat Craniectomy
    "42595102", # Peripheral/Cranial Nerve: A standardized, surgically relevant map for emergence of organ-specific branches from the human vagus nerve
    "42593631", # Pain: Sinomenine Liposomes Alleviate Neuropathic Pain in a Spared Nerve Injury Model by Regulating Astrocyte Reactivity
    "42595299", # Hydrocephalus/Ventricular: Electromagnetic navigation and ventricular catheter placement
    "42595329"  # Neurovascular/Stroke: Willisian collateral and carotid stenosis during large vessel occlusion stroke
]

selected = [a for a in articles if a['pmid'] in target_pmids]

html_content = '''<div class="digest-intro">
<p>در این شماره از دیسپچ جراحی مغز و اعصاب، ۱۰ مقاله برتر از معتبرترین ژورنال‌های جراحی مغز و اعصاب و نوروساینس جهان در حوزه‌های عروقی، انکولوژی اعصاب، فانکشنال، ستون فقرات، قاعده جمجمه، تروما، عصب محیطی، درد و هیدروسفالی مورد نقد و بررسی دقیق قرار گرفته‌اند. هدف، ارائه شواهد بالینی به‌روز و کاربردی با ادبیات تخصصی جراحی برای همکاران گرامی است.</p>
</div>
'''

articles_data = [
    {
        "slug": "accessory-meningeal-artery-aneurysm-asdh",
        "title": "هماتوم ساب‌دورال حاد عودکننده ناشی از پارگی آنوریسم سرخرگ مننژیال فرعی: گزارش مورد و مرور متون",
        "en_title": "Recurrent nontraumatic acute subdural hematoma secondary to ruptured accessory meningeal artery aneurysm: A case report and literature review.",
        "study_type": "گزارش مورد",
        "journal": "J Cerebrovasc Endovasc Neurosurg",
        "doi": "10.7461/jcen.2026.E2026.07.003",
        "findings": [
            "شناسایی یک مورد نادر از هماتوم ساب‌دورال حاد خودبه‌خودی (aSDH) ناشی از پارگی ساکولار آنوریسم سرخرگ مننژیال فرعی (AMA) در بیمار ۳۶ ساله.",
            "بروز عود هماتوم ساب‌دورال یک هفته پس از کرانیوتومی رفع فشار اولیه، که با انجام آنژیوگرافی دیجیتال (DSA) مشخص گردید.",
            "درمان قطعی و موفقیت‌آمیز ضایعه با آمبولیزاسیون اندوواسکولار انتخابی بدون عارضه نورولوژیک بعدی."
        ],
        "conclusion": "آنوریسم‌های عروق مننژیال فرعی باید به عنوان یک علت نادر اما مهم در بروز هماتوم‌های ساب‌دورال خودبه‌خودی یا عودکننده با منشأ نامشخص در نظر گرفته شوند و DSA ابزار تشخیصی استاندارد است.",
        "clinical": "در مواجهه با aSDH خودبه‌خودی بدون پاتولوژی مشخص در CT آنژیوگرافی اولیه، انجام DSA برای رد کردن مالفورماسیون‌های عروقی دورال و مننژیال حیاتی است."
    },
    {
        "slug": "timeless-glioma-stemness-jak-stat3",
        "title": "پروتئین TIMELESS با واسطه‌گری مسیر JAK-STAT3 باعث تحریک سلول‌های بنیادی و بدخیمی در گلیوما می‌شود",
        "en_title": "TIMELESS promotes glioma stemness and malignancy through JAK-STAT3 pathway.",
        "study_type": "مطالعه پایه و مولکولی",
        "journal": "J Biol Chem",
        "doi": "10.1016/j.jbc.2026.113447",
        "findings": [
            "اثبات نقش افزایشی پروتئین TIMELESS در تکثیر، مهاجرت و حفظ فنوتیپ سلول‌های بنیادی در سلول‌های گلیوما.",
            "نشان داده شد که اثرات انکوژنیک TIMELESS از طریق فعال‌سازی مسیر سیگنالینگ JAK-STAT3 اعمال می‌گردد.",
            "سطح بالای بیان TIMELESS در بافت‌های گلیومای درجه بالا (HGG) با پروگنوز ضعیف‌تر و بقای کوتاه‌تر بیماران همبستگی مستقیم دارد."
        ],
        "conclusion": "پروتئین TIMELESS یک تنظیم‌کننده کلیدی در بدخیمی گلیوما است و به‌عنوان یک مارکر پروگنوستیک و تارگت درمانی بالقوه مطرح می‌گردد.",
        "clinical": "درک مسیرهای مولکولی مانند JAK-STAT3 راه را برای طراحی درمان‌های هدفمند نوین در کنار رزکسيون جراحی و رادیوتراپی گلیوبلاستوما هموار می‌کند."
    },
    {
        "slug": "stn-dbs-long-latency-reflex-parkinson",
        "title": "تحقیقی بر تحریک عمقی مغز هسته ساب‌تالامیک و تقویت رفلکس تأخیری بلند II در بیماری پارکینسون از طریق مدولاسیون سریع ساب‌تالامیک-قشر مغز",
        "en_title": "Subthalamic Nucleus Deep Brain Stimulation Enhanced Long-Latency Reflex II in Parkinson's Disease Through Rapid Subthalamic-Cortical Modulation.",
        "study_type": "مطالعه بالینی",
        "journal": "Mov Disord",
        "doi": "10.1002/mds.70508",
        "findings": [
            "بررسی پاسخ‌های رفلکس تأخیری بلند (LLR II) به عنوان رفلکس ترانس‌کورتیکال در ۱۳ بیمار پارکینسون تحت عمل STN-DBS.",
            "نشان داده شد که پارامترهای تحریک STN-DBS (فرکانس ۶۰ هرتز در برابر ۱۳۰ هرتز و ولتاژ) به‌طور معنی‌داری دامنه LLR II را مدولاسیون می‌کنند.",
            "پاسخ سریع قشری-زیرقشری نشان‌دهنده تاثیر پالس‌های DBS بر بازسازی تحریک‌پذیری حرکتی در این بیماران است."
        ],
        "conclusion": "رفلکس Lllr II می‌تواند به‌عنوان یک بیومارکر الکتروفیزیولوژیک معتبر برای بهینه‌سازی پارامترهای تحریک عمقی مغز در بیماری پارکینسون استفاده شود.",
        "clinical": "جراحان مغز و اعصاب و تیم‌های نورومودولاسیون می‌توانند از ارزیابی‌های الکتروفیزیولوژیک حین و پس از عمل برای تنظیم دقیق‌تر فرکانس و شدت پالس‌های DBS بهره بگیرند."
    },
    {
        "slug": "preoperative-mental-health-cervical-myelopathy",
        "title": "پاسخ به نامه درباره «تأثیر سلامت روان پیش‌ازعمل بر پیامدهای جراحی و بالینی در میلوپاتی گردنی دژنراتیو»: یک مطالعه هم‌گروهی آینده‌نگر چندمرکزی",
        "en_title": "Response to the Letter Regarding \"Influence of Preoperative Mental Health on Surgical and Clinical Outcomes in Degenerative Cervical Myelopathy\": A Multicenter Prospective Cohort Study.",
        "study_type": "مطالعه هم‌گروهی آینده‌نگر",
        "journal": "Spine (Phila Pa 1976)",
        "doi": "10.1097/BRS.0000000000005828",
        "findings": [
            "تحلیل جامع داده‌های آینده‌نگر در خصوص وضعیت روانی بیماران مبتلا به میلوپاتی گردنی دژنراتیو (DCM) پیش از جراحی دکمپرسیو.",
            "ثبت همبستگی مستقیم بین اختلالات خلقی و اضطرابی پیش‌ازعمل با میزان رضایتمندی و بهبود نمرات عملکردی پس از جراحی.",
            "تاکید بر اینکه فاکتورهای روان‌شناختی نقشی تعدیل‌کننده در درک بیمار از بهبود علائم نورولوژیک پس از رفع فشار طناب نخاعی دارند."
        ],
        "conclusion": "وضعیت سلامت روان پیش‌ازعمل عامل مهمی در پیش‌بینی پیامدهای گزارش‌شده توسط بیمار (PROMs) پس از جراحی میلوپاتی گردنی است.",
        "clinical": "غربالگری و مدیریت افسردگی و اضطراب پیش از جراحی‌های بزرگ ستون فقرات مانند رفع فشار DCM می‌تواند انتظار بالینی بیمار را تعدیل کرده و شاخص‌های رضایت را بهبود بخشد."
    },
    {
        "slug": "foamagen-dural-substitute-translabyrinthine",
        "title": "تجربه بالینی مقدماتی با جایگزین درور مبتنی بر کلاژن فوم‌مانند جدید (Foamagen) برای ترمیم دورا متعاقب کرانیوتومی ترانس‌لابرینتین: مقایسه اکتشافی با DuraSeal",
        "en_title": "Preliminary Clinical Experience With A Novel Foamy Collagen-Based Dural Substitute (Foamagen) For Dural Closure Following Translabyrinthine Craniotomy: An Exploratory Comparison With DuraSeal.",
        "study_type": "مطالعه بالینی آینده‌نگر",
        "journal": "Neurosurg Pract",
        "doi": "10.1227/neuprac.0000000000000280",
        "findings": [
            "ارزیابی کارایی و ایمنی جایگزین دورال جدید Foamagen در مقایسه با DuraSeal در جراحی‌های بیس کرانیوم و ترانس‌لابرینتین.",
            "میزان نشت مایع مغزی-نخاعی (CSF leak) و عوارض عفونی در گروه Foamagen مشابه یا مطلوب‌تر از استانداردهای قبلی بود.",
            "خاصیت ارتجاعی و انطباق‌پذیری بالای ماتریس کلاژنی فوم‌مانند، دوختن و فیکس کردن آن را در فضاهای تنگ استخوانی تسهیل کرد."
        ],
        "conclusion": "ماتریس کلاژنی Foamagen یک جایگزین دورال ایمن و مؤثر با قابلیت هندسینگ عالی برای ترمیم دنده‌های قاعده جمجمه فراهم می‌کند.",
        "clinical": "استفاده از جایگزین‌های دورال با جذب استاندارد و ساختار کلاژنی می‌تواند خطر نشت CSF و فیستول را در دسترسی‌های پیچیده قاعده جمجمه کاهش دهد."
    },
    {
        "slug": "delayed-external-brain-tamponade-craniectomy",
        "title": "تامپوناد مغزی خارجی تاخیری متعاقب کرانیوتومی مجدد: درس‌های بالینی و رادیولوژیک",
        "en_title": "Delayed External Brain Tamponade Following Repeat Craniectomy: Clinical and Radiological Lessons.",
        "study_type": "گزارش مورد و تحلیل بالینی",
        "journal": "Ann Afr Med",
        "doi": "10.4103/aam.aam_206_26",
        "findings": [
            "بررسی پدیده نادر تامپوناد خارجی مغز و ایجاد فشار منفی یا گیر افتادن پارانشیم مغز به دنبال جراحی‌های رفع فشار مکرر (repeat craniectomy).",
            "تجزیه و تحلیل تصاویر رادیولوژیک که نشان‌دهنده تغییرات شدید هیدرودینامیک CSF و فشار داخل جمجمه (ICP) بودند.",
            "اهمیت تشخیص زودهنگام افت ناگهانی سطح هوشیاری یا بروز نقص جدید نورولوژیک ناشی از عدم تعادل فشارهای محفظه‌ای."
        ],
        "conclusion": "تامپوناد خارجی تاخیری یک اورژانس نوروسرجیکال است که نیاز به دقت در مدیریت پانسمان‌های فشاری و بازسازی به‌موقع استخوان یا پلاستیک جمجمه دارد.",
        "clinical": "در بیماران با کرانیکتومی قبلی که تحت جراحی‌های مکرر قرار می‌گیرند، پایش دقیق شیفت‌های ادم مغزی و گرادیان فشار برای پیشگیری از کمپرسورهای پارانشیمی الزامی است."
    },
    {
        "slug": "vagus-nerve-organ-specific-branches-map",
        "title": "نقشه استاندارد و از نظر جراحی مرتبط برای خروج شاخه‌های اختصاصی ارگان‌ها از عصب واگ انسانی",
        "en_title": "A standardized, surgically relevant map for emergence of organ-specific branches from the human vagus nerve.",
        "study_type": "مطالعه آناتومیک و کاداوریک",
        "journal": "Brain Stimul",
        "doi": "10.1016/j.brs.2026.103182",
        "findings": [
            "دالبور و کالبدشکافی دقیق ۵۸ عصب واگ (۲۹ جفت) از ۲۹ لاشه انسانی از فورامن ژوگولار تا حفره توراسیک.",
            "دسته‌بندی و نقشه‌برداری شاخه‌های عصب واگ به ۷ گروه اصلی (عروقی، قلبی، ریوی، مری، عضلانی، سمپاتیک و چندگانه).",
            "نرمال‌سازی فاصله‌های محل خروج شاخه‌ها نسبت به لندمارک‌های جراحی استاندارد شامل شاخه کاروتید، برجستگی حنجره و ترقوه."
        ],
        "conclusion": "این نقشه آناتومیک کمی، مبنای بسیار دقیقی برای جایگذاری بهینه الکترودهای تحریک عصب واگ (VNS) جهت حداکثر اثربخشی و کاهش عوارض ناخواسته فراهم می‌کند.",
        "clinical": "جراحان ایمپلنت‌کننده VNS می‌توانند با بهره‌گیری از این لندمارک‌ها، محل تحریک را برای اهداف درمانی خاص (مانند صرع یا نارسایی قلبی) دقیق‌تر انتخاب کنند."
    },
    {
        "slug": "sinomenine-liposomes-neuropathic-pain-jak2",
        "title": "لیپوزوم‌های سینومنین درد نوروپاتیک را در مدل آسیب عصبی حفاظت‌شده با تنظیم واکنش‌پذیری آستروسیت‌ها مرتبط با مهار مسیر JAK2/STAT3 تسکین می‌دهند",
        "en_title": "Sinomenine Liposomes Alleviate Neuropathic Pain in a Spared Nerve Injury Model by Regulating Astrocyte Reactivity Associated with Inhibition of the JAK2/STAT3 Pathway.",
        "study_type": "مطالعه پایه و تجربی",
        "journal": "Neurochem Res",
        "doi": "10.1007/s11064-026-04839-y",
        "findings": [
            "بررسی اثرات ضددرد لیپوزوم‌های سینومنین در مدل حیوانی آسیب عصبی (SNI) برای درد نوروپاتیک مزمن.",
            "ثبت مهار چشمگیر فعال‌سازی آستروسیت‌ها در شاخ پشتی نخاع و کاهش سایتوکین‌های پیش‌التهابی.",
            "مشخص شد که اثرات محافظتی دارو از طریق سرکوب آبشار سیگنالینگ JAK2/STAT3 در سلول‌های گلیال اعمال می‌شود."
        ],
        "conclusion": "نانولیپوزوم‌های دارویی حاوی سینومنین پتانسیل بالایی در کنترل درد نوروپاتیک مزمن مقاوم به درمان از طریق مهار التهاب عصبی دارند.",
        "clinical": "شناخت مسیرهای التهابی گلیال نظیر JAK2/STAT3 دریچه‌های تازه‌ای برای رویکردهای فارماکولوژیک در درمان درد نوروپاتیک مداوم پس از جراحی‌های ستون فقرات یا اعصاب محیطی باز می‌کند."
    },
    {
        "slug": "electromagnetic-navigation-ventricular-catheter",
        "title": "ناوبری الکترومغناطیسی و تعگذاری کاتتر بطنی: آنالیز همسان‌شده با امتیاز تمایل از تجدیدنظر پروگزیمال زودهنگام و جابجایی پارانشیمی",
        "en_title": "Electromagnetic navigation and ventricular catheter placement: a propensity-score-matched analysis of early proximal revision and parenchymal misplacement.",
        "study_type": "مطالعه هم‌گروهی همسان‌شده",
        "journal": "World Neurosurg",
        "doi": "10.1016/j.wneu.2026.125247",
        "findings": [
            "مقایسه نتایج تعگذاری شنت بطنی با استفاده از سیستم ناوبری الکترومغناطیسی (EMN) در مقایسه با روش استاندارد در بیماران هیدروسفالی.",
            "کاهش معنی‌دار میزان مال‌پوزیشن کاتتر در پارانشیم مغز و نیاز کمتر به جراحی‌های اصلاحی پروگزیمال زودهنگام در گروه ناوبری.",
            "اثبات مقرون‌به‌صرفه بودن و دقت بالای هدایت ناوبری به‌ویژه در بطن‌های با اندازه کوچک یا دفرمه."
        ],
        "conclusion": "استفاده از ناوبری الکترومغناطیسی در تعگذاری شنت‌های بطنی نرخ عوارض ناشی از خطای مسیر و نیاز به تعویض مجدد کاتتر را به طور قابل‌توجهی کاهش می‌دهد.",
        "clinical": "به‌کارگیری ناوبری در تعگذاری شنت یا درن بطنی خارجی (EVD) در موارد آناتومی دشوار یا بطن‌های کوچک قویاً توصیه می‌شود."
    },
    {
        "slug": "willisian-collateral-carotid-stenosis-lvo",
        "title": "کلترال‌های ویلیس و تنگی کاروتید حین سکته مغزی انسداد عروق بزرگ: مشاهدات از آنژیوگرافی توموگرافی کامپیوتری",
        "en_title": "Willisian collateral and carotid stenosis during large vessel occlusion stroke: Observations from computed tomography angiography.",
        "study_type": "مطالعه رادیولوژیک و عروقی",
        "journal": "J Cerebrovasc Endovasc Neurosurg",
        "doi": "10.7461/jcen.2026.E2026.02.004",
        "findings": [
            "بررسی نقش و وضعیت جانبی‌سازی حلقه ویلیس در بیماران دچار انسداد عروق بزرگ مغزی (LVO) همراه با تنگی کاروتید.",
            "نشان داده شد که کفایت کلترال‌های حلقه ویلیس تعیین‌کننده اصلی وسعت ناحیه ایسکمی (Penumbra) پیش از ترومبکتومی مکانیکی است.",
            "حضور تنگی‌های مزمن کاروتید داخلی سبب بازسازی و تقویت مسیرهای کلترال ورودی می‌گردد اما در شرایط انسداد حاد می‌تواند ظرفیت جبرانی را محدود کند."
        ],
        "conclusion": "ارزیابی دقیق وضعیت گردش خون جانبی ویلیس در CT آنژیوگرافی پیش‌ازعمل ترومبکتومی، پیش‌بینی‌کننده کلیدی نتیجه عملکردی بیمار است.",
        "clinical": "در جراحی‌های نوروواسکولار و اینترونشنال سکته‌های حاد، توجه به وضعیت آناتومیک حلقه ویلیس در تعیین پنجره زمانی و موفقیت ترومبکتومی حائز اهمیت است."
    }
]

html_parts = [html_content]
for item in articles_data:
    card = f'''<div class="article-card">
<h2 id="{item['slug']}">{item['title']}</h2>
<div class="article-en-title">{item['en_title']}</div>
<div class="article-meta"><span class="badge">{item['study_type']}</span>Journal: {item['journal']} | <a href="https://doi.org/{item['doi']}" target="_blank">Link</a></div>
<h3>YAFTEHAYE KELIDI</h3>
<ul>
'''
    for f in item['findings']:
        card += f'<li>{f}</li>\n'
    card += '''</ul>
<h3>NATIJEH GIRI</h3>
<p>''' + item['conclusion'] + '''</p>
<h3>KARBORD BALINI</h3>
<p>''' + item['clinical'] + '''</p>
</div>
'''
    html_parts.append(card)

# Add tip-box
tip_box = '''<div class="tip-box">
<h3>نکته بالینی طلایی (Clinical Pearl)</h3>
<p>در جراحی‌های قاعده جمجمه و عروق مغزی، ترکیب هدایت ناوبری الکترومغناطیسی با آنژیوگرافی پیشرفته و شناخت دقیق نقشه‌های آناتومیک اعصاب و عروق (مانند عصب واگ و کلترال‌های حلقه ویلیس)، کلید اصلی کاهش موربیدیتی و افزایش موفقیت درمان در جراحی‌های پیچیده مغز و اعصاب است.</p>
</div>
'''
html_parts.append(tip_box)

final_html = "".join(html_parts)

os.makedirs('/root/neurosurgery-digest/_build', exist_ok=True)
with open('/root/neurosurgery-digest/_build/today_content.html', 'w') as f:
    f.write(final_html)

print("Successfully generated _build/today_content.html with 10 articles covering diverse subspecialties.")
