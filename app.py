import streamlit as st
import PyPDF2
from google import genai
from google.genai import types
import io

# 1. إعدادات الصفحة والتصميم المتوافق مع الجوال
st.set_page_config(page_title="PharmaStudy Academic", page_icon="💊", layout="wide")

# تصميم مخصص للألوان والخطوط لتبدو احترافية ומريحة للعين
st.markdown("""
<style>
    .reportview-container { background: #f5f7fa; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    .en-line { color: #1e3a8a; font-weight: 600; font-size: 16px; margin-bottom: 2px; }
    .ar-line { color: #047857; font-weight: 500; font-size: 16px; margin-bottom: 15px; background-color: #f0fdf4; padding: 5px; border-radius: 5px; }
</style>
""", unsafe_allow_index=True)

st.title("💊 منصة الصيدلة الأكاديمية الذكية")
st.caption("إصدار 2026 - مدعوم بنموذج Gemini 3 وربط البحث المباشر")

# حقل إدخال الـ API Key لتأمين حسابك
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API Key الخاص بك:", type="password")

if not api_key:
    st.warning("⚠️ يرجى إدخال مفتاح الـ API Key في القائمة الجانبية لتفعيل البرنامج.")
else:
    # تهيئة عميل الجيل الجديد من جوجل ذكاء اصطناعي
    client = genai.Client(api_key=api_key)
    
    # إنشاء التبويبات الأساسية للبرنامج
    tab1, tab2 = st.tabs(["📄 ترجمة PDF سطر بسطر", "🔬 الشرح الأكاديمي والبحث"])

    # --- التبويب الأول: المترجم الصيدلاني المزدوج ---
    with tab1:
        st.header("📄 المترجم المزدوج الاحترافي (سطر بسطر)")
        st.info("ارفع ملف PDF الصيدلاني وسيتم قراءته وترجمته بدقة أكاديمية عالية مع الحفاظ على المصطلحات.")
        
        uploaded_file = st.file_uploader("اختر ملف PDF الصيدلاني", type=["pdf"])
        
        if uploaded_file is not None:
            # قراءة ملف الـ PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            total_pages = len(pdf_reader.pages)
            
            # اختيار الصفحة المراد دراستها لعدم استهلاك الـ API دفعة واحدة
            page_num = st.number_input(f"اختر رقم الصفحة للدراسة (من 1 إلى {total_pages}):", min_value=1, max_value=total_pages, value=1)
            
            if st.button("إخراج وترجمة الصفحة الحالية"):
                with st.spinner("جاري قراءة الصفحة وترجمتها سطر بسطر صيدلانياً..."):
                    page_text = pdf_reader.pages[page_num - 1].extract_text()
                    
                    if page_text.strip() == "":
                        st.error("لم نتمكن من استخراج نص من هذه الصفحة، قد تكون عبارة عن صورة.")
                    else:
                        # صياغة الأمر البرمجي للذكاء الاصطناعي بدقة متناهية
                        prompt = f"""
                        You are an expert academic pharmacist and professional medical translator. 
                        Translate the following pharmaceutical text into Arabic.
                        Requirements:
                        1. Output MUST be strictly line-by-line (or paragraph-by-paragraph for structured ideas).
                        2. For each segment, output the original English line first.
                        3. Immediately below it, output the professional Arabic translation.
                        4. DO NOT translate core scientific terms into literal/funny Arabic (e.g., keep 'Pharmacokinetics' as حركية الدواء (Pharmacokinetics) and keep enzyme names, drug names, and receptors accurate).
                        
                        Text to translate:
                        {page_text}
                        """
                        
                        try:
                            # استخدام نموذج الجيل الثالث للمعالجة الذكية والسريعة
                            response = client.models.generate_content(
                                model="gemini-3-flash",
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    temperature=0.3 # درجة منخفضة لضمان الدقة وعدم التأليف
                                )
                            )
                            
                            st.subheader(f"📖 النتيجة الأكاديمية المزدوجة - الصفحة {page_num}")
                            st.write(response.text)
                            
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

    # --- التبويب الثاني: الشارح الأكاديمي المدعم بالبحث والمراجع ---
    with tab2:
        st.header("🔬 الشارح الأكاديمي المتقدم (Pharma Oracle)")
        st.info("اكتب أي موضوع أو سؤال صيدلاني، وسيقوم النظام بالبحث في الويب والدمج مع المراجع الأكاديمية.")
        
        user_query = st.text_area("أدخل سؤالك الصيدلاني أو المفهوم المراد شرحه عميقاً:", height=150, placeholder="مثال: اشرح آلية عمل دواء الـ Digoxin وتداخلاته مع مراجعك...")
        
        reference_choice = st.selectbox("اختر المرجع الأساسي المفضل لتوثيق الإجابة:", [
            "الشامل (جميع المراجع الصيدلانية الكبرى)",
            "DiPiro (Pharmacotherapy: A Pathophysiologic Approach)",
            "Goodman & Gilman's (The Pharmacological Basis of Therapeutics)",
            "Martindale (The Complete Drug Reference)"
        ])
        
        if st.button("البدء في التحليل والبحث الأكاديمي العميق"):
            if not user_query.strip():
                st.warning("الرجاء كتابة سؤال أولاً.")
            else:
                with st.spinner("جاري تفعيل محرك البحث ومطابقة المراجع الصيدلانية الكبرى..."):
                    
                    # صياغة التوجيه الأكاديمي مع تفعيل ميزة البحث من جوجل (Google Search Grounding)
                    prompt = f"""
                    You are an elite clinical pharmacy professor. Provide a highly detailed, comprehensive, and advanced academic explanation for the query below.
                    Use the context of major pharmaceutical textbooks, especially: {reference_choice}.
                    Structure your answer to cover (if applicable):
                    - Core Concept / Mechanism of Action (at the molecular/cellular level).
                    - Pharmacokinetics & Pharmacodynamics.
                    - Clinical Uses and precise dosing notes.
                    - Severe Adverse Effects and critical Drug-Drug Interactions.
                    - References/Sources used.
                    
                    Query: {user_query}
                    """
                    
                    try:
                        # تفعيل أداة البحث المباشر (Google Search) كما في الكود الذي نسخته
                        tools = [types.Tool(googleSearch=types.GoogleSearch())]
                        
                        response = client.models.generate_content(
                            model="gemini-3-flash",
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                temperature=0.5,
                                tools=tools, # هنا قمنا بدمج البحث الفعلي لتوثيق المعلومات
                                thinking_config=types.ThinkingConfig(thinking_level="HIGH") # تشغيل تفكير عميق
                            )
                        )
                        
                        st.subheader("📚 التقرير الأكاديمي الشامل:")
                        st.write(response.text)
                        
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء معالجة الطلب الأكاديمي: {e}")
