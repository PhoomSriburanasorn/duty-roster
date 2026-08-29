#!/usr/bin/env python3
"""สร้างไฟล์สำหรับ publish เป็น Artifact จาก index.html

Artifact จะห่อ <!doctype>/<html>/<head>/<body> ให้เอง → ไฟล์ที่ส่งไปต้องไม่มีแท็กพวกนี้
รันใหม่ทุกครั้งที่แก้ index.html เพื่อให้สองไฟล์ตรงกันเสมอ:
    python3 build_artifact.py
"""
import re, pathlib

src = pathlib.Path(__file__).parent / 'index.html'
out = pathlib.Path(__file__).parent / 'artifact.html'
s = src.read_text(encoding='utf-8')

title = re.search(r'<title>.*?</title>', s, re.S).group(0)
style = re.search(r'<style[^>]*>.*?</style>', s, re.S).group(0)
body  = re.search(r'<body>(.*)</body>', s, re.S).group(1).strip()

out.write_text(f'{title}\n{style}\n{body}\n', encoding='utf-8')
print(f'{out.name}: {out.stat().st_size:,} bytes')

# กันพลาด: ต้องไม่มีแท็กโครงหลงเหลือ
txt = out.read_text(encoding='utf-8')
# ตัดเนื้อในสคริปต์ออกก่อน — buildPortable() มี "<html>/<head>/<body>" เป็นสตริง
# สำหรับประกอบไฟล์ส่งต่อ ซึ่งเป็นข้อมูล ไม่ใช่แท็กจริงของหน้านี้
txt = re.sub(r'<script[^>]*>.*?</script>', '', txt, flags=re.S)
# ต้องเทียบแบบมีขอบเขตคำ ไม่งั้น <header> จะถูกจับว่าเป็น <head>
bad = [t for t in ('!doctype', 'html', 'head', 'body')
       if re.search(r'</?' + t + r'(?=[\s>/])', txt, re.I)]
assert not bad, f'ยังมีแท็กโครงหลงเหลือ: {bad}'
print('ok — ไม่มีแท็กโครงหลงเหลือ')
