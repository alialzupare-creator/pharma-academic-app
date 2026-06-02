import streamlit as st
import PyPDF2
from google import genai
from google.genai import types

# 1. إعدادات الصفحة والتصميم المتوافق بالكامل مع شاشة الجوال
st.set_page_config(page_title="Advanced AI Clinical Pharmacist", page_icon="💊", layout="wide")

# تنسيق المظهر العام لإبراز النصوص الثنائية والترجمة المزدوجة
st.markdown("""
<style>
    .reportview-container { background: #f8fafc; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: bold; }
    .english-text { color: #1e3a8a; font-family: 'Courier New', monospace; font-weight: bold; font-size: 15px; margin-top: 10px; }
    .arabic-text { color: #047857; font-family: 'Cairo', sans-serif; font-weight: 500; font-size: 16px; margin-bottom: 15px; background-color: #f0fdf4; padding: 8px; border-right: 4px solid #10b981; border-radius: 4px; }
    .insight-box { background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("🩺 المستشار والمترجم الإكلينيكي الذكي")
st.caption("إصدار المترجم الصيدلاني المحترف 2026 - القائم على ميزة التفكير والربط بالمراجع")

# حقل إدخال الـ API Key في القائمة الجانبية وتأمين الحساب
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API Key الخاص بك:", type="password")

if not api_key:
    st.warning("⚠️ يرجى إدخال مفتاح الـ API Key في القائمة الجانبية لتفعيل النظام الصيدلاني.")
else:
    try:
        # تهيئة العميل بناءً على المكتبة الحديثة google-genai
        client = genai.Client(api_key=api_key)
        
        # واجهة رفع الملفات والتحكم
        st.header("📄 معالجة الكتب والمحاضرات الطبية والصيدلانية")
        uploaded_file = st.file_uploader("قم برفع ملف الـ PDF الأكاديمي (Lecture note / Textbook)", type=["pdf"])
        
        if uploaded_file is not None:
            # تحسين الأداء: تمرير الملف مباشرة لتجنب استهلاك الذاكرة العشوائية
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            total_pages = len(pdf_reader.pages)
            
            # اختيار الصفحة المستهدفة للدراسة العميقة
            page_num = st.number_input(f"اختر رقم الصفحة للمعالجة (1 إلى {total_pages}):", min_value=1, max_value=total_pages, value=1)
            
            # اختيار المرجع المفضل لتعزيز الشرح الأكاديمي
            textbook_ref = st.sidebar.selectbox("المرجع الأكاديمي المفضل للشرح:", [
                "DiPiro (Pharmacotherapy)",
                "Goodman & Gilman's (The Pharmacological Basis of Therapeutics)",
                "Martindale (The Complete Drug Reference)",
                "Katzung (Basic & Clinical Pharmacology)"
            ])

            if st.button("🚀 البدء في الترجمة الاحترافية والتحليل الإكلينيكي"):
                with st.spinner("جاري استخراج النص وتفعيل التفكير العميق للنموذج..."):
                    page_text = pdf_reader.pages[page_num - 1].extract_text()
                    
                    if not page_text or page_text.strip() == "":
                        st.error("⚠️ لم نتمكن من قراءة نص في هذه الصفحة (قد تكون الصورة تحتاج لمعالجة Scanner).")
                    else:
                        
                        # صياغة الـ Prompt الهندسي الصارم بناءً على رغبتك ومواصفاتك الدقيقة
                        prompt = f"""
                        You are an expert AI Clinical Pharmacist and Medical Translator. Your task is to process the following medical/pharmaceutical text and perform a high-precision line-by-line bilingual translation and academic medical explanation.

                        Strict Execution Instructions:
                        
                        1. TRANSLATION SECTION:
                           - Process the text seamlessly from start to finish.
                           - For every single sentence/line in the source English text, output the exact original English line, followed immediately by its precise Arabic medical translation.
                           - Format MUST look exactly like this:
                             [Original English sentence/line]
                             [Precise Arabic medical translation]
                           - Maintain strict professional medical and pharmaceutical terminology. Use accurate Arabic medical equivalents for pharmacology, pharmacokinetics (ADME), medicinal chemistry, and clinical indications rather than literal or generic translations.

                        2. ACADEMIC EXPLANATION SECTION:
                           - After finishing the entire line-by-line translation, provide a dedicated, comprehensive section titled: "Medical Insights & Explanation" (باللغة العربية: الشرح والتحليل الأكاديمي المتقدم).
                           - Break down complex drug mechanisms of action (MOA), pharmacokinetics (ADME), clinical indications, severe side effects, or drug-drug interactions mentioned in the text.
                           - Explain these concepts in professional yet highly accessible academic Arabic tailored for pharmacy students, and ground the knowledge in the context of: {textbook_ref}.

                        Source Text to Process:
                        {page_text}
                        """
                        
                        try:
                            # استخدام التوصيف الأحدث والأكثر استقراراً لتفعيل البحث والتفكير
                            tools = [{"google_search": {}}]
                            
                            generate_content_config = types.GenerateContentConfig(
                                temperature=0.2, # لمنع الهلوسة الطبية وضمان التطابق الأكاديمي
                                tools=tools,     # تفعيل البحث المباشر للتحقق من البروتوكولات الطبية الحديثة
                                thinking_config=types.ThinkingConfig(thinking_level="HIGH") # تشغيل التفكير العالي للربط الدقيق للـ MOA
                            )
                            
                            output_placeholder = st.empty()
                            full_response = ""
                            
                            # استخدام الموديل المستقر والحديث لعام 2026 والمخصص للتفكير
                            for chunk in client.models.generate_content_stream(
                                model="gemini-2.5-flash",
                                contents=prompt,
                                config=generate_content_config
                            ):
                                if chunk.text:
                                    full_response += chunk.text
                                    # تحديث النص بشكل حي ومتدفق على الشاشة
                                    output_placeholder.markdown(full_response)
                                    
                            st.success(f"✅ تم الانتهاء من ترجمة وتحليل الصفحة {page_num} بنجاح!")
                            
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء معالجة البيانات الطبية: {e}")
                            
    except Exception as init_error:
        st.sidebar.error(f"خطأ في تهيئة مكتبة Gemini: {init_error}")
