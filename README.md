# نظام المحاسبة لشركات المقاولات

نظام محاسبة متكامل مصمم خصيصاً لشركات المقاولات، يدعم إدارة المشاريع والحسابات العامة.

## المميزات الرئيسية
- إدارة المشاريع والحسابات
- نظام صلاحيات متكامل
- إدارة الموردين والفواتير
- تقارير مالية شاملة
- واجهة مستخدم بالعربية

## متطلبات التشغيل
- Python 3.8+
- PostgreSQL
- متطلبات أخرى موجودة في ملف requirements.txt

## التثبيت
1. إنشاء بيئة Python افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
venv\Scripts\activate     # على Windows
```

2. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. إعداد قاعدة البيانات:
```bash
python manage.py migrate
```

4. إنشاء مستخدم مدير:
```bash
python manage.py createsuperuser
```

5. تشغيل الخادم:
```bash
python manage.py runserver
```

## الهيكل التنظيمي للمشروع
- `accounts/`: إدارة المستخدمين والصلاحيات
- `projects/`: إدارة المشاريع
- `finance/`: النظام المالي والمحاسبي
- `suppliers/`: إدارة الموردين
- `reports/`: نظام التقارير

## المساهمة
نرحب بمساهماتكم في تطوير النظام. يرجى اتباع معايير كتابة الكود المتبعة في المشروع.
