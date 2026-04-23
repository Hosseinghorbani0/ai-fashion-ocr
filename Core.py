from flask import Flask, request , render_template,jsonify,redirect, url_for
from flask_cors import CORS
from openai import OpenAI
import sqlite3
import os
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
import base64



client = OpenAI(
    base_url="",
    api_key="",    
)
app = Flask(__name__)
CORS(app)
# مسیر ذخیره‌سازی عکس‌ها
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# نوع فایل‌های قابل آپلود
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# بررسی پسوند فایل
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ایجاد جدول در دیتابیس
def database():
    db = sqlite3.connect("chat.db", check_same_thread=False)
    sql = db.cursor()

    sql.execute('''
                
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT DEFAULT NULL,
            user_id TEXT DEFAULT NULL,
            tokens INTEGER DEFAULT NULL,
            req TEXT,
            res TEXT,
            timestamp1 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT DEFAULT NULL,
            imagein TEXT DEFAULT NULL,
            disable INTEGER DEFAULT 0
        );
    ''')
    db.commit()
    db.close()

database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']

    # ذخیره فایل در مسیر مشخص شده
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    a=cv2.imread(file_path)
    if a is None:
         return jsonify({'error': 'Failed to read image'}), 400
    a2=cv2.resize(a,(32,32))
    a3=cv2.cvtColor(a2,cv2.COLOR_BGR2GRAY)
    a4=a3.flatten()
    a5=a4/255
    a5=a5.reshape((-1, 32, 32, 1))
    encoder = LabelEncoder()

    #size
    y_size=np.array([42,42,46,46,46,48,48,48,50,50,46,46,46,44,44,50,50,50,50,44,44,44,44,44,44,50,50,42,42,48,48,48,44,44,44])
    y_size= encoder.fit_transform(y_size)
    model = load_model('modelsize.h5')
    out1= model.predict(a5)
    out1_classes = np.argmax(out1, axis=1) 
    out1=encoder.inverse_transform(out1_classes)

    #ghad
    y_ghad=np.array([70,70,70,70,70,80,80,80,80,80,75,75,75,75,75,80,80,80,80,70,70,70,70,70,70,100,100,80,80,75,75,75,75,75,75])
    y_ghad= encoder.fit_transform(y_ghad)
    model2 = load_model('modelghad.h5')
    out2= model2.predict(a5)
    out2_classes = np.argmax(out2, axis=1) 
    out2=encoder.inverse_transform(out2_classes)

    #gheymat
    y_gheymat=np.array([4500000,4500000,3100000,3100000,3100000,3800000,3800000,3800000,2500000,2500000,4200000,4200000,4200000,2100000,2100000,3200000,3200000,3200000,3200000,3600000,3600000,3600000,3600000,3600000,3600000,4100000,4100000,1500000,1500000,2200000,2200000,2200000,3400000,3400000,3400000])
    y_gheymat = encoder.fit_transform(y_gheymat)
    model3 = load_model('modelgheymat.h5')
    out3= model3.predict(a5)
    out3_classes = np.argmax(out3, axis=1) 
    out3=encoder.inverse_transform(out3_classes)

    #jense
    y_jense = np.array([
    "کتان استر دار", "کتان استر دار", "فوتر", "فوتر", "فوتر",
    "ژاکاد", "ژاکارد", "ژاکارد", "فوتر", "فوتر", "فوتر", "فوتر",
    "فوتر", "فوتر", "فوتر", "فوتر", "فوتر", "فوتر", "فوتر",
    "فوتر آستردار", "فوتر آستردار", "فوتر آستردار", "فوتر آستردار",
    "فوتر آستردار", "فوتر آستردار", "فوتر آستردار", "فوتر آستردار",
    "فوتر و چرم و جین", "فوتر و چرم و جین", "فوتر", "فوتر",
    "فوتر", "فوتر", "فوتر", "فوتر"
    ])
    y_jense= encoder.fit_transform(y_jense)
    model4 = load_model('modeljense.h5')
    out4= model4.predict(a5)
    out4_classes = np.argmax(out4, axis=1) 
    out4=encoder.inverse_transform(out4_classes)

    return jsonify({
    'message': [
        {'سایز': int(out1[0])},
        {'قیمت': int(out3[0])},
        {'قد': int(out2[0])},
        {'جنس': str(out4[0])}
    ]
})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # خواندن داده‌ها از بدنه درخواست JSON
    chat1 = data.get("content")  # دریافت پیام کاربر
    mobile = data.get("phone")  # دریافت شماره تلفن کاربر

    db = sqlite3.connect("chat.db", check_same_thread=False)
    sql = db.cursor()


    out = ''
    content_prompt =  """تو منشی یک مزون لباسی و تو منشی هوشمند یونیکا هستی،اسم مزون ما حس هست که به حس کالکشن معروف،در مزون هم مانتو داریم و هم عبا و هم لباس های مجلسی مخصوص مهمونی و دورهمی و شلوار،همه ی اجناس به طور خاص طراحی شده 
      این اجناس فقط توی مزون ما موجود 
      تمامی اجناس در دو سایز 1 و 2 طراحی شده که سایز 1 تا سایز 42 و سایز 2 تا سایز 48 را پوشش میده
      قیمت اجناس بسته به مدل متفاوت است و در تمامی رنج قیمت جنس داریم و اونا میتونن عکس محصول بفرستند تا بهشون قیمت بدیم
      برای ثبت سفارش میتونند توی دایرکت اینستا پیام بدن
      آدرس مزون در کامرانیه کوچه حاتم خوانی پلاک 6 است قبل از آمدن به مزون باید تماس بگیرند و هماهنگ کنند،
      شماره تماس مزون: 0989999999 است
      پیج اینستاگرام:abcdef
      هم مدل های آماده موجود و هم امکان سفارش دوزی برای اشخاص هست،،امکان تغییرات در مدل ها به صورت جزعی وجود دارد
      چون عکس ها دقیقا با لباس های موجود در مزون گرفته میشه عکس ها دقیقا شبیه لباس ها هستن
      ساعت کاری مزون 9صبح الی 19 است
      با لحن بسیار جذاب و دوستانه و با صحبت عامیانه صحبت کن بر اساس اطلاعات جواب بده
        فقط به اطلاعات مربوط به مزون و اطلاعات بالا پاسخ بده
        این متن را با استفاده از تگ‌های HTML قالب‌بندی کن تا زیباتر نمایش داده شود.
        اگر جنس فوتر دارند لباسها  مناسب پاییز و زمستان است 
        ، همه ی اجناس موجود هستن
        ، درخواست عکس نکن 
        لطفاً متن را به صورتی بنویس که دوستانه‌تر و حرفه‌ای‌تر به نظر برسد.
        فقط اگه ادرس و شماره تلفن خواستند بهشون بگوو ایموجی استفاده کن."""

    messages = [
        {
            "role": "system",
            "content": content_prompt
        },
    ]

    try:
        # بازیابی آخرین چت‌های کاربر
        sql.execute("""
            SELECT * FROM (
                SELECT * FROM chat 
                WHERE user_id = ? AND disable = 0 
                ORDER BY id DESC 
                LIMIT 40
            ) tmp ORDER BY tmp.id ASC
        """, (mobile,))
        results = sql.fetchall()
        for row in results:
            messages.append({"role": "user", "content": row[4]})
            messages.append({"role": "assistant", "content": row[5]})
    except Exception as e:
        print(f"Database retrieval error: {str(e)}")

    # افزودن پیام جدید کاربر
    messages.append({"role": "user", "content": chat1})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages     
    )

    out = response.choices[0].message.content

    images = []  # لیستی برای ذخیره تصاویر ارسال‌شده
    find={"role": "user", "content": chat1}

    try:
     if str(find).find("مانتو") > -1 and str(find).find("زمستانه")> -1 and str(find).find("عکس") > -1 :
         for s in range (1,6):
             path = f"ax/winter/{s}.jpg"
             im = cv2.imread(path)
             _, buffer = cv2.imencode('.jpg', im)
             image_base64 = base64.b64encode(buffer).decode('utf-8')
             images.append(image_base64)

     if str(chat1).find("مانتو") > -1 and str(chat1).find("بهار")> -1 and str(chat1).find("عکس") > -1 :
         for m in range (1,6):
             path = f"ax/spring/{m}.jpg"
             im = cv2.imread(path)
             _, buffer = cv2.imencode('.jpg', im)
             image_base64 = base64.b64encode(buffer).decode('utf-8')
             images.append(image_base64)   

    except Exception as e:
        print(f'Error while processing images: {e}')


    query = """
        INSERT INTO chat (model, user_id, tokens, req, res, ip, imagein)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        sql.execute(query, ('gpt-4o-mini', mobile, '0', chat1, out, '0', '-'))
        db.commit()
    except Exception as e:
        print(f"Insert error: {str(e)}")
        return jsonify({'error': 'Failed to save chat'}), 500
    finally:
        db.close()  

    out = out.replace("\n", "<br>")
    out = out.replace("\r", "")  # حذف \r که ممکن است تداخل ایجاد کند
    out = out.replace("**", "")  # حذف ستاره‌های اولیه و ثانویه برای جلوگیری از بولد کردن
    out = out.replace("***", "")  # حذف ستاره‌های بیشتر
    out = out.replace("<b>", "")  # حذف تگ‌های <b> باز
    out = out.replace("</b>", "")  # حذف تگ‌های <b> بسته
    out = out.replace("####", "✅")  # تغییرات مربوط به علامت‌ها
    out = out.replace("###", "✅")
    out = out.replace("##", "✅")
    out = out.replace("* ", "◾️")
    out = out.replace("????", "")  # حذف متن اضافی
# جایگزین دقیق‌تر تگ‌ها
    out = out.replace("<b>", "</b>")


    return jsonify({'message': out, 'images': images})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
