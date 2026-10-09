#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Processing Web Application - برنامج معالجة الصور عبر الويب
يعمل داخل المتصفح باستخدام Streamlit
"""

import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import cv2
import numpy as np
from io import BytesIO

# إعداد الصفحة
st.set_page_config(
    page_title="معالج الصور",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# العنوان
st.title("🖼️ برنامج معالجة الصور المتكامل")
st.markdown("---")

# الشريط الجانبي
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # رفع الصورة
    uploaded_file = st.file_uploader(
        "📤 اختر صورة",
        type=["jpg", "jpeg", "png", "bmp", "gif", "webp"]
    )

if uploaded_file is not None:
    # تحميل الصورة
    image = Image.open(uploaded_file)
    if image.mode not in {'RGB', 'L', 'RGBA'}:
        image = image.convert('RGB')
    else:
        image = image.convert('RGB')
    
    original_image = image.copy()
    
    # عمود يساري وعمود يميني
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("الصورة الأصلية")
        st.image(original_image, use_column_width=True)
    
    with col2:
        st.subheader("الصورة المعالجة")
        
        # القائمة الرئيسية للعمليات
        with st.sidebar:
            st.header("🎨 العمليات المتاحة")
            operation = st.radio(
                "اختر العملية:",
                [
                    "بدون تعديل",
                    "تحويل إلى رمادي",
                    "تغيير الحجم",
                    "تدوير الصورة",
                    "ضبط السطوع",
                    "ضبط التباين",
                    "تطبيق ضبابية",
                    "تحديد الحواف",
                    "كشف الحواف",
                    "أبيض وأسود (عتبة)",
                    "قلب أفقي",
                    "قلب عمودي",
                    "معادلة الهستوجرام",
                    "تطبيق مرشح دافئ",
                    "تطبيق مرشح بارد"
                ]
            )
        
        # معالجة الصورة حسب الخيار
        processed_image = image.copy()
        
        if operation == "تحويل إلى رمادي":
            processed_image = ImageOps.grayscale(image).convert('RGB')
            st.success("✅ تم التحويل إلى رمادي")
        
        elif operation == "تغيير الحجم":
            with st.sidebar:
                st.subheader("🔧 إعدادات تغيير الحجم")
                width = st.slider("العرض", 100, 2000, 800, step=50)
                height_mode = st.radio("الارتفاع:", ["تلقائي", "يدوي"])
                
                if height_mode == "يدوي":
                    height = st.slider("الارتفاع", 100, 2000, 600, step=50)
                else:
                    ratio = width / image.size[0]
                    height = int(image.size[1] * ratio)
            
            processed_image = image.resize((width, height), Image.Resampling.LANCZOS)
            st.success(f"✅ تم تغيير الحجم إلى {width}x{height}")
        
        elif operation == "تدوير الصورة":
            with st.sidebar:
                st.subheader("🔧 إعدادات التدوير")
                angle = st.slider("زاوية الدوران (درجة)", -180, 180, 0, step=15)
            
            processed_image = image.rotate(angle, expand=True, fillcolor=(255, 255, 255))
            st.success(f"✅ تم تدوير الصورة بزاوية {angle}°")
        
        elif operation == "ضبط السطوع":
            with st.sidebar:
                st.subheader("🔧 إعدادات السطوع")
                brightness_factor = st.slider("معامل السطوع", 0.1, 3.0, 1.0, step=0.1)
            
            enhancer = ImageEnhance.Brightness(image)
            processed_image = enhancer.enhance(brightness_factor)
            st.success(f"✅ تم ضبط السطوع بمعامل {brightness_factor}")
        
        elif operation == "ضبط التباين":
            with st.sidebar:
                st.subheader("🔧 إعدادات التباين")
                contrast_factor = st.slider("معامل التباين", 0.1, 3.0, 1.0, step=0.1)
            
            enhancer = ImageEnhance.Contrast(image)
            processed_image = enhancer.enhance(contrast_factor)
            st.success(f"✅ تم ضبط التباين بمعامل {contrast_factor}")
        
        elif operation == "تطبيق ضبابية":
            with st.sidebar:
                st.subheader("🔧 إعدادات الضبابية")
                blur_radius = st.slider("نصف قطر الضبابية", 0.5, 20.0, 5.0, step=0.5)
            
            processed_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            st.success(f"✅ تم تطبيق ضبابية بنصف قطر {blur_radius}")
        
        elif operation == "تحديد الحواف":
            processed_image = image.filter(ImageFilter.SHARPEN)
            st.success("✅ تم تحديد الحواف")
        
        elif operation == "كشف الحواف":
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            processed_image = Image.fromarray(edges).convert('RGB')
            st.success("✅ تم كشف الحواف")
        
        elif operation == "أبيض وأسود (عتبة)":
            with st.sidebar:
                st.subheader("🔧 إعدادات العتبة")
                threshold = st.slider("قيمة العتبة", 0, 255, 127, step=1)
            
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            _, thresholded = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            processed_image = Image.fromarray(thresholded)
            st.success(f"✅ تم تطبيق عتبة {threshold}")
        
        elif operation == "قلب أفقي":
            processed_image = ImageOps.mirror(image)
            st.success("✅ تم قلب الصورة أفقياً")
        
        elif operation == "قلب عمودي":
            processed_image = ImageOps.flip(image)
            st.success("✅ تم قلب الصورة عمودياً")
        
        elif operation == "معادلة الهستوجرام":
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            img_yuv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2YCrCb)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YCrCb2BGR)
            processed_image = Image.fromarray(cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB))
            st.success("✅ تم تطبيق معادلة الهستوجرام")
        
        elif operation == "تطبيق مرشح دافئ":
            processed_image = image.copy()
            r, g, b = processed_image.split()
            r = ImageEnhance.Brightness(r).enhance(1.2)
            processed_image = Image.merge('RGB', (r, g, b))
            st.success("✅ تم تطبيق المرشح الدافئ")
        
        elif operation == "تطبيق مرشح بارد":
            processed_image = image.copy()
            r, g, b = processed_image.split()
            b = ImageEnhance.Brightness(b).enhance(1.2)
            processed_image = Image.merge('RGB', (r, g, b))
            st.success("✅ تم تطبيق المرشح البارد")
        
        else:
            st.info("لم يتم تطبيق أي معالجة")
        
        # عرض الصورة المعالجة
        st.image(processed_image, use_column_width=True)
    
    # تحميل الصورة
    st.markdown("---")
    st.subheader("💾 تحميل الصورة المعالجة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # تحميل بصيغة JPG
        buffer_jpg = BytesIO()
        processed_image.save(buffer_jpg, format="JPEG")
        st.download_button(
            label="📥 تحميل JPG",
            data=buffer_jpg.getvalue(),
            file_name="processed_image.jpg",
            mime="image/jpeg"
        )
    
    with col2:
        # تحميل بصيغة PNG
        buffer_png = BytesIO()
        processed_image.save(buffer_png, format="PNG")
        st.download_button(
            label="📥 تحميل PNG",
            data=buffer_png.getvalue(),
            file_name="processed_image.png",
            mime="image/png"
        )
    
    with col3:
        # تحميل بصيغة WebP
        buffer_webp = BytesIO()
        processed_image.save(buffer_webp, format="WEBP")
        st.download_button(
            label="📥 تحميل WebP",
            data=buffer_webp.getvalue(),
            file_name="processed_image.webp",
            mime="image/webp"
        )

else:
    st.warning("⚠️ يرجى رفع صورة للبدء!")
    
    # معلومات توضيحية
    st.markdown("""
    ### 🎯 كيفية الاستخدام:
    1. **رفع صورة** من الشريط الجانبي
    2. **اختيار العملية** المطلوبة
    3. **ضبط الإعدادات** إن لزم الأمر
    4. **تحميل الصورة** بالصيغة المطلوبة
    
    ### ✨ العمليات المتاحة:
    - تحويل إلى رمادي
    - تغيير الحجم
    - التدوير
    - ضبط السطوع والتباين
    - تطبيق الفلاتر (ضبابية، تحديد)
    - كشف الحواف
    - التحويل إلى أبيض وأسود
    - والمزيد...
    """)

# التذييل
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>تم بناء هذا البرنامج باستخدام Python و Streamlit 🚀</p>
</div>
""", unsafe_allow_html=True)
