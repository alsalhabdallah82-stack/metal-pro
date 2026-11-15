from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.core.window import Window
import math


Window.clearcolor = (0.04, 0.08, 0.15, 1)


# =====================================
# METALS DATABASE
# =====================================

METALS = {
    "Aluminum (Pure)": {"Arabic":"الألومنيوم النقي", "aliases":"aluminium الالمنيوم ألمنيوم", "density":2700,
        "detail":"""بيانات وخصائص معدن الألومنيوم النقي (Al)
1) البيانات الكيميائية والذرية
الرمز: Al | العدد الذري: 13 | الكتلة الذرية: 26.982 u
التوزيع الإلكتروني: 1s^2 2s^2 2p^6 3s^2 3p^1
نسبة القشرة الأرضية: نحو 8.1% وزناً (ثالث أكثر العناصر وفرة).

2) الخصائص الفيزيائية والحرارية (قيم تقريبية قرب درجة حرارة الغرفة)
الكثافة: 2700 kg/m^3 | الانصهار: 660.3  deg C | الغليان: 2519  deg C
التوصيل الحراري: 237 W/(m*K) | التوصيل الكهربائي: نحو 37.7 MS/m (نحو 63% IACS)
الحرارة النوعية: 900 J/(kg*K) | التمدد الحراري: 23.1 micro-m/(m* deg C)

3) الخصائص الميكانيكية
معامل يونغ: 69-71 GPa | مقاومة الشد للألومنيوم النقي الملدّن: نحو 45-90 MPa
الصلادة: نحو 2.5-3 على مقياس موس | الاستطالة: تقريباً 20-40% حسب النقاوة والحالة.
للمقارنة: سبيكة 6061-T6 مقاومة شدها النموذجية نحو 310 MPa، وليست ألومنيوم نقياً.

4) أرقام اقتصادية وبيئية
توفير الطاقة بإعادة التدوير: نحو 95% مقارنة بإنتاج الألومنيوم الأولي.
نحو 75% من كل الألومنيوم المنتج تاريخياً ما زال قيد الاستخدام؛ هذه ليست نسبة المحتوى المعاد تدويره في الإنتاج الحالي.

الاستخدامات: الطائرات، النقل، البناء، العبوات، المبادلات الحرارية."""},
    "Copper (Pure)": {"Arabic":"النحاس النقي", "aliases":"copper cu نحاس", "density":8960,
        "detail":"""بيانات وخصائص النحاس النقي (Cu)
1) البيانات الكيميائية والذرية
الرمز: Cu | العدد الذري: 29 | الكتلة الذرية: 63.546 u
التوزيع الإلكتروني: [Ar] 3d^1⁰ 4s^1 | القشرة الأرضية: نحو 0.006% وزناً.

2) الخصائص الفيزيائية والحرارية
الكثافة: 8960 kg/m^3 | الانصهار: 1084.6  deg C | الغليان: 2562  deg C
التوصيل الحراري: 401 W/(m*K) | التوصيل الكهربائي: نحو 58 MS/m (100% IACS)
الحرارة النوعية: 385 J/(kg*K) | التمدد الحراري: 16.5-17 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 117-130 GPa | مقاومة الشد للنحاس الملدّن: نحو 200-230 MPa
الصلادة: نحو 3 على مقياس موس | الاستطالة: غالباً 30-45% للنحاس الملدّن.
تختلف مقاومة الشد والصلادة بشدة مع التشكيل البارد وحالة المادة.

4) الاقتصاد والبيئة
النحاس قابل لإعادة التدوير مرات عديدة مع الاحتفاظ بخصائصه؛ لا توجد نسبة عالمية ثابتة واحدة للمحتوى المعاد تدويره.
الاستخدامات: الأسلاك الكهربائية، المحركات، الأنابيب، المبادلات الحرارية."""},
    "Iron (Pure)": {"Arabic":"الحديد النقي", "aliases":"iron fe حديد", "density":7870,
        "detail":"""بيانات وخصائص الحديد النقي (Fe)
1) البيانات الكيميائية والذرية
الرمز: Fe | العدد الذري: 26 | الكتلة الذرية: 55.845 u
التوزيع الإلكتروني: [Ar] 3d^6 4s^2 | القشرة الأرضية: نحو 5% وزناً.

2) الخصائص الفيزيائية والحرارية
الكثافة: 7870 kg/m^3 | الانصهار: 1538  deg C | الغليان: 2862  deg C
التوصيل الحراري: نحو 80 W/(m*K) | التوصيل الكهربائي: نحو 10 MS/m
الحرارة النوعية: 449 J/(kg*K) | التمدد الحراري: نحو 11.8 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 200-211 GPa | مقاومة الشد للحديد النقي منخفضة نسبياً وتتغير حسب النقاوة والحالة (تقريباً 180-300 MPa)
الصلادة: نحو 4 على مقياس موس | الاستطالة: متغيرة وقد تكون مرتفعة للحديد النقي الملدّن.

4) الاقتصاد والبيئة
يعاد تدوير الحديد والصلب على نطاق واسع؛ النسب تختلف حسب البلد والمنتج.
الاستخدامات: أساس صناعة الفولاذ، الهياكل، الآلات والمعدات."""},
    "Low Carbon Steel 1018": {"Arabic":"فولاذ منخفض الكربون 1018", "aliases":"steel carbon steel فولاذ حديد كربون", "density":7870,
        "detail":"""بيانات وخصائص فولاذ منخفض الكربون AISI 1018 (سبيكة وليست عنصراً نقياً)
1) البيانات الكيميائية والذرية
لا يملك رمزاً أو عدداً ذرياً واحداً لأنه سبيكة أساسها الحديد. يحتوي عادةً نحو 0.15-0.20% كربون مع منغنيز وعناصر أخرى.

2) الخصائص الفيزيائية والحرارية (تقريبية)
الكثافة: 7870 kg/m^3 | مجال الانصهار التقريبي: 1425-1540  deg C
التوصيل الحراري: نحو 50 W/(m*K) | الحرارة النوعية: نحو 486 J/(kg*K)
معامل التمدد: نحو 11.7 micro-m/(m* deg C) | الغليان: لا يستخدم عادةً كقيمة تصميمية للفولاذ.

3) الخصائص الميكانيكية (تختلف حسب المعالجة والتوريد)
معامل يونغ: نحو 205 GPa | مقاومة الشد: نحو 440 MPa للحالة المسحوبة على البارد النموذجية
الصلادة: نحو 126 HB (ليست مقياس موس) | الاستطالة: نحو 15% تقريباً.

4) الاقتصاد والبيئة
الفولاذ من أكثر المواد تدويراً عالمياً، لكن نسبة التدوير تعتمد على السوق ونوع المنتج.
الاستخدامات: الأعمدة، المسامير، المحاور، الأجزاء الميكانيكية."""},
    "Stainless Steel 304": {"Arabic":"فولاذ غير قابل للصدأ 304", "aliases":"stainless steel ستانلس ستيل فولاذ مقاوم للصدأ", "density":8000,
        "detail":"""بيانات وخصائص الفولاذ غير القابل للصدأ AISI 304 (سبيكة)
1) البيانات الكيميائية والذرية
سبيكة أساسها الحديد؛ تركيب نموذجي: 18-20% كروم و8-10.5% نيكل، مع كربون منخفض. لا يوجد عدد ذري واحد للسبيكة.

2) الخصائص الفيزيائية والحرارية
الكثافة: 8000 kg/m^3 | مجال الانصهار: 1400-1450  deg C
التوصيل الحراري: نحو 16 W/(m*K) | الحرارة النوعية: نحو 500 J/(kg*K)
التمدد الحراري: نحو 17.2 micro-m/(m* deg C) | التوصيل الكهربائي: نحو 1.4 MS/m.

3) الخصائص الميكانيكية (ملدن، قيم نموذجية/حدود دنيا تختلف بالمواصفة)
معامل يونغ: نحو 193 GPa | مقاومة الشد: نحو 515-750 MPa بحسب المنتج والمواصفة
الصلادة: نحو 3.5-4 على مقياس موس تقريباً؛ صلادة برينل النموذجية قد تقارب 150-200 HB
الاستطالة: غالباً 40% أو أكثر في الحالة الملدنة.

4) الاقتصاد والبيئة
يحتوي على عناصر ذات قيمة مثل النيكل والكروم ويمكن استرجاعها عند إعادة التدوير.
الاستخدامات: معدات الغذاء، الخزانات، الأنابيب، التجهيزات الكيميائية."""},
    "Cast Iron": {"Arabic":"حديد زهر", "aliases":"cast iron gray iron حديد مصبوب زهر", "density":7200,
        "detail":"""بيانات وخصائص الحديد الزهر الرمادي (قيم تقريبية؛ تختلف باختلاف النوع)
1) البيانات الكيميائية والذرية
سبيكة أساسها الحديد، تحتوي عادةً 2.5-4% كربون و1-3% سيليكون؛ لا رمز ذرياً واحداً لها.

2) الخصائص الفيزيائية والحرارية
الكثافة: نحو 7200 kg/m^3 | مجال الانصهار: نحو 1150-1200  deg C
التوصيل الحراري: نحو 35-55 W/(m*K) | الحرارة النوعية: نحو 460 J/(kg*K)
معامل التمدد: نحو 10-12 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 100-170 GPa | مقاومة الشد للرمادي: نحو 150-300 MPa
الصلادة: نحو 150-250 HB (مقياس برينل) | الاستطالة: منخفضة جداً غالباً أقل من 1%.

4) الاقتصاد والبيئة
يمكن صهر خردة الحديد الزهر وإعادة استخدامها، وتعتمد كفاءة العملية على الفرز والتركيب.
الاستخدامات: هياكل المحركات، قواعد الآلات، أجسام المضخات وأقراص المكابح."""},
    "Titanium Grade 2": {"Arabic":"تيتانيوم درجة 2", "aliases":"titanium ti تيتانيوم", "density":4510,
        "detail":"""بيانات وخصائص التيتانيوم (العنصر Ti؛ مع خواص تجارية تقريبية للدرجة 2)
1) البيانات الكيميائية والذرية
الرمز: Ti | العدد الذري: 22 | الكتلة الذرية: 47.867 u
التوزيع الإلكتروني: [Ar] 3d^2 4s^2 | القشرة الأرضية: نحو 0.6% وزناً.

2) الخصائص الفيزيائية والحرارية
الكثافة: 4510 kg/m^3 | الانصهار: 1668  deg C | الغليان: نحو 3287  deg C
التوصيل الحراري: نحو 22 W/(m*K) | التوصيل الكهربائي: نحو 2.4 MS/m
الحرارة النوعية: نحو 523 J/(kg*K) | التمدد الحراري: نحو 8.6 micro-m/(m* deg C).

3) الخصائص الميكانيكية (درجة 2 التجارية)
معامل يونغ: نحو 103 GPa | مقاومة الشد: نحو 345 MPa كحد أدنى شائع
الصلادة: نحو 6 على مقياس موس للتيتانيوم النقي | الاستطالة: نحو 20-30% حسب المواصفة.

4) الاقتصاد والبيئة
إعادة تدوير خردة التيتانيوم مهمة اقتصادياً بسبب كلفة إنتاجه الأولي المرتفعة؛ لا توجد نسبة عالمية موحدة.
الاستخدامات: الغرسات الطبية، الطيران، الصناعات الكيميائية."""},
    "Magnesium (Pure)": {"Arabic":"المغنيسيوم النقي", "aliases":"magnesium mg مغنيسيوم", "density":1740,
        "detail":"""بيانات وخصائص المغنيسيوم النقي (Mg)
1) البيانات الكيميائية والذرية
الرمز: Mg | العدد الذري: 12 | الكتلة الذرية: 24.305 u
التوزيع الإلكتروني: [Ne] 3s^2 | القشرة الأرضية: نحو 2.1% وزناً.

2) الخصائص الفيزيائية والحرارية
الكثافة: 1740 kg/m^3 | الانصهار: 650  deg C | الغليان: 1091  deg C
التوصيل الحراري: نحو 156 W/(m*K) | التوصيل الكهربائي: نحو 22 MS/m
الحرارة النوعية: 1023 J/(kg*K) | التمدد الحراري: نحو 26 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 45 GPa | مقاومة الشد للمغنيسيوم النقي: نحو 90-150 MPa
الصلادة: نحو 2.5 على مقياس موس | الاستطالة: تتغير بشدة مع البنية والحرارة.

4) الاقتصاد والبيئة
تدوير سبائك المغنيسيوم ممكن، مع ضرورة التحكم بالأكسدة والسلامة أثناء الصهر.
الاستخدامات: سبائك خفيفة، السيارات، الطيران، الإلكترونيات."""},
    "Zinc (Pure)": {"Arabic":"الزنك النقي", "aliases":"zinc zn زنك خارصين", "density":7140,
        "detail":"""بيانات وخصائص الزنك النقي (Zn)
1) البيانات الكيميائية والذرية
الرمز: Zn | العدد الذري: 30 | الكتلة الذرية: 65.38 u
التوزيع الإلكتروني: [Ar] 3d^1⁰ 4s^2 | القشرة الأرضية: نحو 0.007% وزناً.

2) الخصائص الفيزيائية والحرارية
الكثافة: 7140 kg/m^3 | الانصهار: 419.5  deg C | الغليان: 907  deg C
التوصيل الحراري: نحو 116 W/(m*K) | التوصيل الكهربائي: نحو 17 MS/m
الحرارة النوعية: 388 J/(kg*K) | التمدد الحراري: نحو 30 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 108 GPa | مقاومة الشد للزنك النقي: تقريباً 100-150 MPa بحسب الشكل والحالة
الصلادة: نحو 2.5 على مقياس موس | الاستطالة: متغيرة بحسب اتجاه البلورة والمعالجة.

4) الاقتصاد والبيئة
يعاد تدوير الزنك من الفولاذ المجلفن ومن منتجات الزنك؛ تختلف النسب حسب المنطقة.
الاستخدامات: الجلفنة، البطاريات، القوالب المصبوبة، النحاس الأصفر."""},
    "Nickel (Pure)": {"Arabic":"النيكل النقي", "aliases":"nickel ni نيكل", "density":8910,
        "detail":"""بيانات وخصائص النيكل النقي (Ni)
1) البيانات الكيميائية والذرية
الرمز: Ni | العدد الذري: 28 | الكتلة الذرية: 58.693 u
التوزيع الإلكتروني: [Ar] 3d^8 4s^2 | القشرة الأرضية: نحو 0.008% وزناً.

2) الخصائص الفيزيائية والحرارية
الكثافة: 8910 kg/m^3 | الانصهار: 1455  deg C | الغليان: 2913  deg C تقريباً
التوصيل الحراري: نحو 91 W/(m*K) | التوصيل الكهربائي: نحو 14 MS/m
الحرارة النوعية: 444 J/(kg*K) | التمدد الحراري: نحو 13.4 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 200 GPa | مقاومة الشد للنيكل الملدّن التجاري: تقريباً 350-500 MPa
الصلادة: نحو 4 على مقياس موس | الاستطالة: نحو 30-50% حسب الحالة.

4) الاقتصاد والبيئة
إعادة تدوير النيكل مهمة خصوصاً من البطاريات والسبائك الفائقة والفولاذ المقاوم للصدأ.
الاستخدامات: الستانلس ستيل، الطلاء، البطاريات، السبائك المقاومة للحرارة."""},
    "Brass C26000": {"Arabic":"نحاس أصفر C26000", "aliases":"brass نحاس اصفر", "density":8530,
        "detail":"""بيانات وخصائص النحاس الأصفر C26000 (سبيكة نحاس-زنك)
1) البيانات الكيميائية والذرية
تركيب نموذجي: نحو 70% نحاس و30% زنك؛ لا رمز ذرياً أو توزيعاً إلكترونياً واحداً للسبيكة.

2) الخصائص الفيزيائية والحرارية
الكثافة: 8530 kg/m^3 | مجال الانصهار: نحو 915-955  deg C
التوصيل الحراري: نحو 120 W/(m*K) | الحرارة النوعية: نحو 380 J/(kg*K)
معامل التمدد: نحو 20 micro-m/(m* deg C).

3) الخصائص الميكانيكية (تختلف حسب التقسية)
معامل يونغ: نحو 100-110 GPa | مقاومة الشد: نحو 300-500 MPa حسب الحالة
الصلادة: نحو 3 على مقياس موس | الاستطالة: قد تتجاوز 30% بالحالة الملدنة.

4) الاقتصاد والبيئة
قابلة لإعادة التدوير؛ يجب ضبط تركيب النحاس والزنك عند إعادة الصهر.
الاستخدامات: الخراطيش، الوصلات، الصمامات، المبادلات الحرارية."""},
    "Bronze": {"Arabic":"برونز (سبيكة نحاس وقصدير)", "aliases":"bronze برونز", "density":8800,
        "detail":"""بيانات وخصائص البرونز (قيم تقريبية لسبيكة نحاس-قصدير شائعة)
1) البيانات الكيميائية والذرية
سبيكة أساسها النحاس والقصدير؛ التركيب يختلف حسب الدرجة، لذلك لا يوجد عدد ذري أو توزيع إلكتروني واحد.

2) الخصائص الفيزيائية والحرارية
الكثافة: نحو 8800 kg/m^3 | مجال الانصهار: تقريباً 850-1000  deg C
التوصيل الحراري: نحو 50-75 W/(m*K) | الحرارة النوعية: نحو 380 J/(kg*K)
التمدد الحراري: نحو 17-18 micro-m/(m* deg C).

3) الخصائص الميكانيكية
معامل يونغ: نحو 96-120 GPa | مقاومة الشد: نحو 200-500 MPa حسب النوع
الصلادة: نحو 3-4 على مقياس موس تقريباً | الاستطالة تختلف كثيراً حسب السبيكة والصب.

4) الاقتصاد والبيئة
يمكن إعادة تدوير البرونز مع فرز الخردة للمحافظة على التركيب الكيميائي.
الاستخدامات: المحامل، الجلب، التروس، التماثيل والتجهيزات البحرية."""}
}


# Keep legacy keys used by the weight calculator and older screens.
for _metal_name, _metal_data in METALS.items():
    _metal_data["DensityValue"] = _metal_data["density"]
    _metal_data["Density"] = f"{_metal_data['density']} kg/m3"
    _metal_data.setdefault("Melting", "See detailed properties")
    _metal_data.setdefault("Tensile", "See detailed properties")
    _metal_data.setdefault("Hardness", "See detailed properties")
    _metal_data.setdefault("Uses", "See detailed properties")

METALS["Aluminum 6061-T6"] = {
    "Arabic": "سبيكة ألومنيوم 6061-T6", "aliases": "6061 ت6 الومنيوم طيران",
    "density": 2700, "DensityValue": 2700, "Density": "2700 kg/m3",
    "Melting": "582-652  deg C", "Tensile": "نحو 310 MPa", "Hardness": "نحو 95 HB",
    "Uses": "هياكل، أجزاء آلات، تطبيقات نقل",
    "detail": """بيانات سبيكة الألومنيوم 6061-T6 (ليست ألومنيوم نقياً)\n1) التركيب الكيميائي والذري\nسبيكة أساسها Al مع مغنيسيوم وسيليكون، وقد تحتوي نحاساً. لا يوجد عدد ذري واحد للسبيكة؛ العنصر الأساسي Al عدده الذري 13 وكتلته الذرية 26.982 u.\n\n2) الخصائص الفيزيائية والحرارية\nالكثافة: 2700 kg/m^3 | مجال الانصهار: 582-652  deg C\nالتوصيل الحراري: نحو 167 W/(m*K) | الحرارة النوعية: نحو 896 J/(kg*K)\nمعامل التمدد: نحو 23.6 micro-m/(m* deg C) | معامل يونغ: نحو 69 GPa.\n\n3) الخصائص الميكانيكية لحالة T6 (قيم نموذجية)\nمقاومة الشد: نحو 310 MPa | الصلادة: نحو 95 HB | الصلادة على مقياس موس ليست المقياس المعتاد للسبائك الهندسية.\nالاستطالة: نحو 8-12% حسب شكل المنتج والمواصفة.\n\n4) الاقتصاد والبيئة\nإعادة تدوير الألومنيوم توفر نحو 95% من الطاقة مقارنة بالإنتاج الأولي؛ نسبة المحتوى المعاد تدويره تختلف حسب المنتج والسوق.\nالاستخدامات: هياكل ومكونات آلات، مركبات، تجهيزات بحرية."""
}



# =====================================
# BASE SCREEN
# =====================================

class BaseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(10)
        )

        self.add_widget(self.layout)

        self.title_label = Label(
            text="METAL PRO",
            font_size="26sp",
            bold=True,
            color=(0.2, 0.75, 1, 1),
            size_hint_y=None,
            height=dp(55)
        )

        self.layout.add_widget(self.title_label)

    def add_input(self, hint):

        field = TextInput(
            hint_text=hint,
            multiline=False,
            font_size="18sp",
            size_hint_y=None,
            height=dp(50),
            padding=dp(12)
        )

        self.layout.add_widget(field)
        return field

    def add_button(self, text, function):

        btn = Button(
            text=text,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=(0.05, 0.42, 0.72, 1)
        )

        btn.bind(on_press=function)
        self.layout.add_widget(btn)
        return btn

    def add_result(self):

        self.result = Label(
            text="",
            font_size="17sp",
            color=(0.3, 1, 0.6, 1),
            size_hint_y=None,
            height=dp(110)
        )

        self.layout.add_widget(self.result)

    def back_button(self):

        self.add_button(
            "Back to Home",
            lambda x: setattr(self.manager, "current", "home")
        )


# =====================================
# HOME SCREEN
# =====================================

class HomeScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Make the home menu scrollable so every calculator button is visible
        # on smaller phone screens.
        self.remove_widget(self.layout)
        self.layout.size_hint_y = None
        self.layout.bind(minimum_height=self.layout.setter("height"))
        home_scroll = ScrollView()
        home_scroll.add_widget(self.layout)
        self.add_widget(home_scroll)

        self.title_label.text = "METAL PRO"

        self.layout.add_widget(Label(
            text="Metallurgical Engineering Assistant",
            font_size="15sp",
            size_hint_y=None,
            height=dp(40)
        ))

        self.add_button("Gear Calculator",
                        lambda x: self.go("gear"))

        self.add_button("TWO-GEAR SYSTEM CALCULATOR",
                        lambda x: self.go("gear_system"))

        self.add_button("Metal Density",
                        lambda x: self.go("density"))

        self.add_button("Temperature Converter",
                        lambda x: self.go("temperature"))

        self.add_button("Tensile Stress Calculator",
                        lambda x: self.go("stress"))

        self.add_button("STEEL CARBON EQUIVALENT (IIW)",
                        lambda x: self.go("carbon_equivalent"))

        self.add_button("METAL WEIGHT CALCULATOR",
                        lambda x: self.go("weight"))

        self.add_button("CUTTING SPEED & FEED CALCULATOR",
                        lambda x: self.go("cutting"))

        self.layout.add_widget(Label(
            text="Developed by Abdullah Al Saleh",
            font_size="13sp",
            color=(0.7, 0.8, 0.9, 1)
        ))

    def go(self, screen):
        self.manager.current = screen


# =====================================
# GEAR CALCULATOR
# Standard spur gear, 20-degree pressure angle,
# standard full-depth involute proportions.
# =====================================

class GearScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll = ScrollView()

        self.layout = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(9),
            size_hint_y=None
        )
        self.layout.bind(
            minimum_height=self.layout.setter("height")
        )

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

        self.title_label = Label(
            text="GEAR CALCULATOR",
            font_size="25sp",
            bold=True,
            color=(0.2, 0.75, 1, 1),
            size_hint_y=None,
            height=dp(55)
        )
        self.layout.add_widget(self.title_label)

        self.layout.add_widget(Label(
            text="Standard Spur Gear - 20 deg  Pressure Angle",
            font_size="14sp",
            color=(0.85, 0.9, 1, 1),
            size_hint_y=None,
            height=dp(32)
        ))

        self.teeth = self.add_input("Number of teeth (Z) - integer")
        self.module = self.add_input("Module (m) in mm")

        self.add_button("CALCULATE GEAR", self.calculate)

        self.result = Label(
            text="Enter the number of teeth and module.",
            font_size="16sp",
            color=(0.3, 1, 0.6, 1),
            size_hint_y=None,
            height=dp(300),
            halign="left",
            valign="middle"
        )
        self.result.bind(
            size=lambda instance, value: setattr(
                instance, "text_size", (value[0] - dp(12), None)
            )
        )
        self.layout.add_widget(self.result)

        self.layout.add_widget(Label(
            text=(
                "Formulas used:\n"
                "Pitch diameter: d = m x Z\n"
                "Outside diameter: da = m x (Z + 2)\n"
                "Root diameter: df = m x (Z - 2.5)\n"
                "Addendum: ha = m\n"
                "Dedendum: hf = 1.25 x m\n"
                "Whole depth: h = 2.25 x m\n"
                "Circular pitch: p = pi x m\n"
                "Tooth thickness: s = pi x m / 2"
            ),
            font_size="13sp",
            size_hint_y=None,
            height=dp(190),
            halign="left",
            valign="middle"
        ))
        self.add_button(
            "Back to Home",
            lambda x: setattr(self.manager, "current", "home")
        )

    def add_input(self, hint):
        field = TextInput(
            hint_text=hint,
            multiline=False,
            input_filter="float",
            font_size="18sp",
            size_hint_y=None,
            height=dp(50),
            padding=dp(12)
        )
        self.layout.add_widget(field)
        return field

    def add_button(self, text, function):
        btn = Button(
            text=text,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=(0.05, 0.42, 0.72, 1)
        )
        btn.bind(on_press=function)
        self.layout.add_widget(btn)
        return btn

    def calculate(self, instance):
        try:
            z_value = float(self.teeth.text.strip())
            m = float(self.module.text.strip())

            if z_value <= 0 or not z_value.is_integer() or m <= 0:
                raise ValueError

            z = int(z_value)

            # Standard full-depth involute spur gear proportions
            pitch = m * z
            outside = m * (z + 2)
            root = m * (z - 2.5)
            addendum = m
            dedendum = 1.25 * m
            whole_depth = 2.25 * m
            circular_pitch = math.pi * m
            tooth_thickness = circular_pitch / 2

            if root <= 0:
                raise ValueError

            self.result.text = (
                "GEAR CALCULATION RESULTS\n\n"
                f"Number of teeth (Z) = {z}\n"
                f"Module (m) = {m:.3f} mm\n\n"
                f"Pitch Diameter (d) = {pitch:.3f} mm\n"
                f"Outside Diameter (da) = {outside:.3f} mm\n"
                f"Root Diameter (df) ~ {root:.3f} mm\n\n"
                f"Addendum (ha) = {addendum:.3f} mm\n"
                f"Dedendum (hf) = {dedendum:.3f} mm\n"
                f"Whole Depth (h) = {whole_depth:.3f} mm\n\n"
                f"Circular Pitch (p) = {circular_pitch:.3f} mm\n"
                f"Tooth Thickness (s) = {tooth_thickness:.3f} mm"
            )

        except (ValueError, TypeError):
            self.result.text = (
                "Invalid input!\n"
                "Enter a positive whole number for teeth (Z)\n"
                "and a positive module (m)."
            )


# =====================================
# TWO-GEAR TRANSMISSION CALCULATOR
# External standard spur gears
# =====================================

class GearSystemScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        scroll = ScrollView()
        self.layout = BoxLayout(
            orientation="vertical", padding=dp(18), spacing=dp(9),
            size_hint_y=None
        )
        self.layout.bind(minimum_height=self.layout.setter("height"))
        scroll.add_widget(self.layout)
        self.add_widget(scroll)

        self.layout.add_widget(Label(
            text="TWO-GEAR SYSTEM CALCULATOR", font_size="23sp", bold=True,
            color=(0.2, 0.75, 1, 1), size_hint_y=None, height=dp(55)
        ))
        self.driver_teeth = self.add_input("Driving gear teeth Z1")
        self.driven_teeth = self.add_input("Driven gear teeth Z2")
        self.module = self.add_input("Gear module m (mm)")
        self.input_rpm = self.add_input("Input speed n1 (RPM)")
        self.input_torque = self.add_input("Input torque T1 (N.m)")
        self.efficiency = self.add_input("Efficiency (%) - e.g. 95")

        self.add_button("CALCULATE GEAR SYSTEM", self.calculate)
        self.result = Label(
            text="Enter gear and input values.", font_size="16sp",
            color=(0.3, 1, 0.6, 1), size_hint_y=None, height=dp(260),
            halign="left", valign="middle"
        )
        self.result.bind(size=lambda obj, val: setattr(
            obj, "text_size", (val[0] - dp(12), None)
        ))
        self.layout.add_widget(self.result)
        self.layout.add_widget(Label(
            text=("For two external spur gears:\n"
                  "Ratio i = Z2 / Z1\n"
                  "Center distance a = m x (Z1 + Z2) / 2\n"
                  "Output RPM = Input RPM / i\n"
                  "Output torque = Input torque x i x efficiency\n\n"
                  "Assumes no slip and ideal tooth geometry."),
            font_size="13sp", size_hint_y=None, height=dp(150),
            halign="left", valign="middle"
        ))
        self.add_button("Back to Home",
                        lambda x: setattr(self.manager, "current", "home"))

    def add_input(self, hint):
        field = TextInput(
            hint_text=hint, multiline=False, input_filter="float",
            font_size="18sp", size_hint_y=None, height=dp(50),
            padding=dp(12)
        )
        self.layout.add_widget(field)
        return field

    def add_button(self, text, function):
        btn = Button(
            text=text, font_size="16sp", bold=True,
            size_hint_y=None, height=dp(50), background_normal="",
            background_color=(0.05, 0.42, 0.72, 1)
        )
        btn.bind(on_press=function)
        self.layout.add_widget(btn)
        return btn

    def calculate(self, instance):
        try:
            z1v = float(self.driver_teeth.text)
            z2v = float(self.driven_teeth.text)
            m = float(self.module.text)
            n1 = float(self.input_rpm.text)
            t1 = float(self.input_torque.text)
            eff = float(self.efficiency.text)

            if (z1v <= 0 or z2v <= 0 or not z1v.is_integer()
                    or not z2v.is_integer() or m <= 0 or n1 < 0
                    or t1 < 0 or eff <= 0 or eff > 100):
                raise ValueError

            z1, z2 = int(z1v), int(z2v)
            ratio = z2 / z1
            center = m * (z1 + z2) / 2
            output_rpm = n1 / ratio
            output_torque = t1 * ratio * (eff / 100)
            direction = "Opposite to input"

            self.result.text = (
                "GEAR SYSTEM RESULTS\n\n"
                f"Driving gear Z1 = {z1} teeth\n"
                f"Driven gear Z2 = {z2} teeth\n"
                f"Transmission ratio = {ratio:.3f}:1\n"
                f"Center distance = {center:.3f} mm\n\n"
                f"Input speed = {n1:.2f} RPM\n"
                f"Output speed = {output_rpm:.2f} RPM\n"
                f"Input torque = {t1:.2f} N.m\n"
                f"Output torque ~ {output_torque:.2f} N.m\n"
                f"Efficiency = {eff:.1f}%\n"
                f"Rotation direction: {direction}"
            )
        except (ValueError, TypeError):
            self.result.text = (
                "Invalid input!\nEnter positive whole numbers for teeth, "
                "positive module, valid RPM/torque, and efficiency "
                "between 0 and 100%."
            )


# =====================================
# DENSITY CALCULATOR
# =====================================

class DensityScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_label.text = "METAL DENSITY"

        self.mass = self.add_input("Mass (kg)")
        self.volume = self.add_input("Volume (m3)")

        self.add_button("Calculate Density", self.calculate)

        self.add_result()
        self.back_button()

    def calculate(self, instance):

        try:
            mass = float(self.mass.text)
            volume = float(self.volume.text)

            if mass <= 0 or volume <= 0:
                raise ValueError

            density = mass / volume

            self.result.text = (
                f"Density = {density:.2f} kg/m3"
            )

        except:
            self.result.text = "Please enter valid positive values."


# =====================================
# TEMPERATURE CONVERTER
# =====================================

class TemperatureScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_label.text = "TEMPERATURE CONVERTER"

        self.value = self.add_input("Enter temperature")

        self.add_button("Celsius to F and K", self.from_celsius)
        self.add_button("Fahrenheit to C and K", self.from_fahrenheit)
        self.add_button("Kelvin to C and F", self.from_kelvin)

        self.add_result()
        self.back_button()

    def from_celsius(self, instance):

        try:
            c = float(self.value.text)

            if c < -273.15:
                raise ValueError

            k = c + 273.15
            f = (c * 9 / 5) + 32

            self.result.text = (
                f"Celsius = {c:.2f}  deg C\n"
                f"Fahrenheit = {f:.2f}  deg F\n"
                f"Kelvin = {k:.2f} K"
            )

        except:
            self.result.text = "Enter a valid temperature."

    def from_fahrenheit(self, instance):

        try:
            f = float(self.value.text)

            if f < -459.67:
                raise ValueError

            c = (f - 32) * 5 / 9
            k = c + 273.15

            self.result.text = (
                f"Fahrenheit = {f:.2f}  deg F\n"
                f"Celsius = {c:.2f}  deg C\n"
                f"Kelvin = {k:.2f} K"
            )

        except:
            self.result.text = "Enter a valid temperature."

    def from_kelvin(self, instance):

        try:
            k = float(self.value.text)

            if k < 0:
                raise ValueError

            c = k - 273.15
            f = (c * 9 / 5) + 32

            self.result.text = (
                f"Kelvin = {k:.2f} K\n"
                f"Celsius = {c:.2f}  deg C\n"
                f"Fahrenheit = {f:.2f}  deg F"
            )

        except:
            self.result.text = "Kelvin cannot be below zero."


# =====================================
# TENSILE STRESS CALCULATOR
# =====================================

class StressScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_label.text = "TENSILE STRESS"

        self.force = self.add_input("Force (N)")
        self.area = self.add_input("Area (mm2)")

        self.add_button("Calculate Stress", self.calculate)

        self.add_result()
        self.back_button()

    def calculate(self, instance):

        try:
            force = float(self.force.text)
            area = float(self.area.text)

            if force < 0 or area <= 0:
                raise ValueError

            stress = force / area

            self.result.text = (
                f"Tensile Stress = {stress:.2f} MPa"
            )

        except:
            self.result.text = "Enter valid force and area."


# =====================================
# STEEL CARBON EQUIVALENT CALCULATOR
# IIW formula: CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15
# All inputs are chemical composition in weight percent.
# =====================================

class CarbonEquivalentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView(do_scroll_x=False)
        page = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(8), size_hint_y=None)
        page.bind(minimum_height=page.setter("height"))
        scroll.add_widget(page)
        self.add_widget(scroll)

        page.add_widget(Label(text="STEEL CARBON EQUIVALENT | مكافئ الكربون للفولاذ",
                              font_size="19sp", bold=True, color=(0.2, 0.75, 1, 1),
                              size_hint_y=None, height=dp(58)))
        page.add_widget(Label(text="أدخل نسب العناصر الكيميائية وزناً (%) لحساب قابلية الفولاذ للحام.",
                              font_size="14sp", size_hint_y=None, height=dp(48)))

        self.fields = {}
        specs = [
            ("C", "الكربون C (%) مثال 0.20"),
            ("Mn", "المنغنيز Mn (%) مثال 1.20"),
            ("Cr", "الكروم Cr (%) مثال 0.10"),
            ("Mo", "الموليبدينوم Mo (%) مثال 0.05"),
            ("V", "الفاناديوم V (%) مثال 0.01"),
            ("Ni", "النيكل Ni (%) مثال 0.10"),
            ("Cu", "النحاس Cu (%) مثال 0.10"),
        ]
        for key, hint in specs:
            field = TextInput(hint_text=hint, multiline=False, input_filter="float",
                              font_size="16sp", size_hint_y=None, height=dp(47), padding=dp(10))
            self.fields[key] = field
            page.add_widget(field)

        calc = Button(text="احسب مكافئ الكربون", font_size="17sp", bold=True,
                      size_hint_y=None, height=dp(50), background_normal="",
                      background_color=(0.05, 0.42, 0.72, 1))
        calc.bind(on_press=self.calculate)
        page.add_widget(calc)

        self.result = Label(text="أدخل التركيب الكيميائي ثم اضغط احسب.", font_size="15sp",
                            color=(0.3, 1, 0.6, 1), halign="left", valign="top",
                            size_hint_y=None, height=dp(150))
        self.result.bind(width=lambda inst, w: setattr(inst, "text_size", (w-dp(12), None)))
        self.result.bind(texture_size=lambda inst, size: setattr(inst, "height", max(dp(150), size[1]+dp(20))))
        page.add_widget(self.result)

        formula = Label(text="معادلة IIW:\nCE = C + Mn/6 + (Cr + Mo + V)/5 + (Ni + Cu)/15\n\n"
                             "جميع القيم نسب مئوية وزنية. هذا تقدير إرشادي للفولاذ، وليس بديلاً عن إجراء اللحام المعتمد.",
                        font_size="13sp", color=(0.85, 0.85, 0.85, 1), halign="left", valign="top",
                        size_hint_y=None, height=dp(110))
        formula.bind(width=lambda inst, w: setattr(inst, "text_size", (w-dp(12), None)))
        page.add_widget(formula)

        back = Button(text="Back to Home", size_hint_y=None, height=dp(48), font_size="16sp")
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "home"))
        page.add_widget(back)

    def calculate(self, *_):
        try:
            values = {k: (float(v.text.strip()) if v.text.strip() else 0.0)
                      for k, v in self.fields.items()}
            if any(v < 0 for v in values.values()):
                raise ValueError
            ce = (values["C"] + values["Mn"]/6.0 +
                  (values["Cr"]+values["Mo"]+values["V"])/5.0 +
                  (values["Ni"]+values["Cu"])/15.0)
            if ce < 0.40:
                category = "قابلية اللحام غالباً جيدة من ناحية مكافئ الكربون"
            elif ce <= 0.60:
                category = "قابلية اللحام متوسطة؛ قد يلزم ضبط شروط اللحام والتسخين المسبق"
            else:
                category = "قابلية اللحام أصعب؛ يلزم تقييم هندسي وقد يلزم تسخين مسبق"
            self.result.text = (f"مكافئ الكربون CE = {ce:.3f} %\\n\\n{category}\\n\\n"
                                "تنبيه: القرار النهائي يعتمد أيضاً على السماكة والهيدروجين ومدخل الحرارة ومواصفة الإجراء.")
        except ValueError:
            self.result.text = "الرجاء إدخال أرقام صحيحة غير سالبة. اترك العنصر غير الموجود فارغاً أو اكتب 0."


# =====================================
# METAL WEIGHT CALCULATOR
# =====================================

class WeightScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scroll = ScrollView()

        self.layout = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(10),
            size_hint_y=None
        )

        self.layout.bind(
            minimum_height=self.layout.setter("height")
        )

        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

        self.title_label = Label(
            text="METAL WEIGHT CALCULATOR",
            font_size="24sp",
            bold=True,
            color=(0.2, 0.75, 1, 1),
            size_hint_y=None,
            height=dp(55)
        )

        self.layout.add_widget(self.title_label)

        self.add_section("Select metal:")

        self.metal_spinner = Spinner(
            text="Aluminum 6061-T6",
            values=tuple(METALS.keys()),
            size_hint_y=None,
            height=dp(48)
        )

        self.layout.add_widget(self.metal_spinner)

        self.add_section("Select shape:")

        self.shape_spinner = Spinner(
            text="Plate",
            values=("Plate", "Solid Cylinder", "Hollow Pipe"),
            size_hint_y=None,
            height=dp(48)
        )

        self.layout.add_widget(self.shape_spinner)

        self.a = self.add_input("Dimension A (mm)")
        self.b = self.add_input("Dimension B (mm)")
        self.c = self.add_input("Dimension C (mm)")

        self.add_section("HOLES INFORMATION")

        self.hole_count = self.add_input("Number of holes (0 if none)")
        self.hole_diameter = self.add_input("Hole diameter (mm)")
        self.hole_depth = self.add_input("Hole depth (mm)")

        self.add_section("MATERIAL LOSS")

        self.loss = self.add_input("Loss percentage (%)")

        self.add_button("CALCULATE WEIGHT", self.calculate)

        self.result = Label(
            text="",
            font_size="16sp",
            color=(0.3, 1, 0.6, 1),
            size_hint_y=None,
            height=dp(145)
        )

        self.layout.add_widget(self.result)

        self.layout.add_widget(Label(
            text=(
                "Plate: A=Length, B=Width, C=Thickness\n"
                "Cylinder: A=Diameter, B=Length\n"
                "Pipe: A=Outer diameter, B=Inner diameter, C=Length\n\n"
                "Holes are cylindrical."
            ),
            font_size="13sp",
            size_hint_y=None,
            height=dp(95)
        ))

        self.add_button(
            "Back to Home",
            lambda x: setattr(self.manager, "current", "home")
        )

    def add_section(self, text):

        self.layout.add_widget(Label(
            text=text,
            font_size="16sp",
            bold=True,
            color=(0.2, 0.75, 1, 1),
            size_hint_y=None,
            height=dp(35)
        ))

    def add_input(self, hint):

        field = TextInput(
            hint_text=hint,
            multiline=False,
            font_size="18sp",
            size_hint_y=None,
            height=dp(50),
            padding=dp(12)
        )

        self.layout.add_widget(field)
        return field

    def add_button(self, text, function):

        btn = Button(
            text=text,
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=(0.05, 0.42, 0.72, 1)
        )

        btn.bind(on_press=function)
        self.layout.add_widget(btn)
        return btn

    def calculate(self, instance):

        try:
            a = float(self.a.text)
            b = float(self.b.text)

            if a <= 0 or b <= 0:
                raise ValueError

            shape = self.shape_spinner.text
            metal = self.metal_spinner.text

            density = METALS[metal]["DensityValue"]

            # Original volume

            if shape == "Plate":

                c = float(self.c.text)

                if c <= 0:
                    raise ValueError

                volume = a * b * c
                max_depth = c

            elif shape == "Solid Cylinder":

                volume = math.pi * (a / 2) ** 2 * b
                max_depth = b

            elif shape == "Hollow Pipe":

                c = float(self.c.text)

                if c <= 0 or b >= a:
                    raise ValueError

                volume = math.pi / 4 * (a ** 2 - b ** 2) * c
                max_depth = c

            else:
                raise ValueError

            # Holes

            count_text = self.hole_count.text.strip()
            count = float(count_text) if count_text else 0

            if count < 0 or not count.is_integer():
                raise ValueError

            holes_volume = 0

            if count > 0:

                diameter = float(self.hole_diameter.text)
                depth = float(self.hole_depth.text)

                if diameter <= 0 or depth <= 0:
                    raise ValueError

                if depth > max_depth:
                    raise ValueError

                holes_volume = (
                    count * math.pi * (diameter / 2) ** 2 * depth
                )

            net_volume = volume - holes_volume

            if net_volume <= 0:
                raise ValueError

            # Weight

            weight_before_loss = (
                net_volume / 1000000000
            ) * density

            # Loss

            loss_text = self.loss.text.strip()
            loss = float(loss_text) if loss_text else 0

            if loss < 0 or loss >= 100:
                raise ValueError

            final_weight = weight_before_loss * (1 - loss / 100)

            self.result.text = (
                f"Metal: {METALS[metal]['Arabic']}\n"
                f"Net Volume = {net_volume / 1000000000:.6f} m3\n"
                f"Before Loss = {weight_before_loss:.3f} kg\n"
                f"Final Weight = {final_weight:.3f} kg\n"
                f"Loss = {loss:.2f}%"
            )

        except (ValueError, TypeError):
            self.result.text = (
                "Invalid input!\n"
                "Check dimensions, holes and loss percentage."
            )




# =====================================
# CUTTING SPEED & FEED CALCULATOR
# =====================================

class CuttingScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title_label.text = "CUTTING SPEED & FEED"

        self.layout.add_widget(Label(
            text="Enter values to calculate RPM, feed rate and machining time.",
            font_size="14sp", size_hint_y=None, height=dp(42)
        ))

        self.diameter = self.add_input("Tool diameter D (mm)")
        self.speed = self.add_input("Cutting speed Vc (m/min)")
        self.teeth = self.add_input("Number of teeth Z")
        self.feed_tooth = self.add_input("Feed per tooth fz (mm/tooth)")
        self.length = self.add_input("Machining length L (mm)")

        self.add_button("CALCULATE", self.calculate)
        self.add_result()
        self.back_button()

    def calculate(self, instance):
        try:
            d = float(self.diameter.text)
            vc = float(self.speed.text)
            z = int(self.teeth.text)
            fz = float(self.feed_tooth.text)
            length = float(self.length.text)

            if d <= 0 or vc <= 0 or z <= 0 or fz <= 0 or length < 0:
                raise ValueError

            rpm = (1000 * vc) / (math.pi * d)
            feed_rate = fz * z * rpm
            time_min = length / feed_rate if feed_rate else 0
            time_sec = time_min * 60

            self.result.text = (
                f"Spindle Speed = {rpm:.1f} RPM\n"
                f"Feed Rate = {feed_rate:.2f} mm/min\n"
                f"Machining Time = {time_min:.3f} min\n"
                f"Machining Time = {time_sec:.1f} sec"
            )
        except (ValueError, TypeError):
            self.result.text = (
                "Invalid input!\nEnter positive numeric values.\n"
                "Number of teeth must be a whole number."
            )


# =====================================
# MAIN APPLICATION
# =====================================

class MetalProApp(App):

    def build(self):

        manager = ScreenManager()

        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(GearScreen(name="gear"))
        manager.add_widget(GearSystemScreen(name="gear_system"))
        manager.add_widget(DensityScreen(name="density"))
        manager.add_widget(TemperatureScreen(name="temperature"))
        manager.add_widget(StressScreen(name="stress"))
        manager.add_widget(CarbonEquivalentScreen(name="carbon_equivalent"))
        manager.add_widget(WeightScreen(name="weight"))
        manager.add_widget(CuttingScreen(name="cutting"))

        return manager


if __name__ == "__main__":
    MetalProApp().run()
