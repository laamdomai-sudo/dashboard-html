import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cài đặt cấu hình trang
st.set_page_config(page_title="Window Guidance Simulator", layout="wide")

st.title("Mô phỏng Cơ chế Window Guidance & ICOR")
st.markdown("Dựa trên Lý thuyết Số lượng Tín dụng (QTC) của GS. Richard Werner")

# 1. SIDEBAR - BẢNG ĐIỀU KHIỂN CỦA NHTW
st.sidebar.header("🕹️ Công cụ điều hành (NHTW)")

# Thanh trượt thiết lập hạn mức tín dụng
total_credit_growth = st.sidebar.slider(
    "Tổng hạn mức tăng trưởng tín dụng (%)", 
    min_value=5.0, max_value=30.0, value=15.0, step=1.0
)

# Thanh trượt Window Guidance (Định hướng dòng vốn)
cr_allocation = st.sidebar.slider(
    "Tỷ lệ ép buộc cấp vốn cho Sản xuất - CR (%)", 
    min_value=10.0, max_value=90.0, value=60.0, step=5.0
)

# Khởi tạo các hằng số giả lập vòng quay tiền
vr_velocity = 0.8  # Vòng quay tiền kinh tế thực
vf_velocity = 1.2  # Vòng quay tiền đầu cơ

# 2. LOGIC TÍNH TOÁN (Cơ chế truyền dẫn)
cf_allocation = 100.0 - cr_allocation

# Tính toán giá trị tuyệt đối giả định (Base = 1000 tỷ)
base_credit = 1000
new_credit = base_credit * (total_credit_growth / 100)

cr_volume = new_credit * (cr_allocation / 100)
cf_volume = new_credit * (cf_allocation / 100)

# Tính toán Đầu ra (Outputs)
# GDP tăng trưởng tỷ lệ thuận với CR
gdp_growth = (cr_volume * vr_velocity) / 100 

# Bong bóng tài sản (Asset Inflation) tỷ lệ thuận với CF
asset_bubble_index = (cf_volume * vf_velocity) / 50 

# Tính toán ICOR = Tổng vốn đầu tư / Mức tăng GDP
# Giả định tổng vốn đầu tư có sự tương quan mạnh với tổng tín dụng mới
if gdp_growth > 0:
    icor = new_credit / (gdp_growth * 20) # Hệ số 20 để scale đồ thị cho thực tế (mức 4-8)
else:
    icor = 0

# 3. HIỂN THỊ KẾT QUẢ KINH TẾ VĨ MÔ
st.header("📊 Kết quả điều hành kinh tế")

col1, col2, col3 = st.columns(3)
col1.metric("Tăng trưởng GDP Thực tế", f"{gdp_growth:.2f}%")
col2.metric("Chỉ số Lạm phát Tài sản", f"{asset_bubble_index:.2f} điểm")

# Cảnh báo màu sắc cho ICOR
if icor < 5:
    col3.metric("Hệ số ICOR (Hiệu quả vốn)", f"{icor:.2f}", "Hiệu quả cao", delta_color="normal")
elif icor < 7:
    col3.metric("Hệ số ICOR (Hiệu quả vốn)", f"{icor:.2f}", "Kém hiệu quả", delta_color="off")
else:
    col3.metric("Hệ số ICOR (Hiệu quả vốn)", f"{icor:.2f}", "Cảnh báo lãng phí vốn!", delta_color="inverse")

st.markdown("---")

# 4. BIỂU ĐỒ TRỰC QUAN HÓA
st.subheader("Phân bổ dòng tiền và Hệ quả")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Biểu đồ 1: Dòng chảy tín dụng (Pie Chart)
labels = [f'Kinh tế thực (CR)\n{cr_allocation}%', f'Đầu cơ Tài chính (CF)\n{cf_allocation}%']
sizes = [cr_volume, cf_volume]
colors = ['#2ca02c', '#d62728']
explode = (0.05, 0)

ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
ax1.set_title("Chỉ đạo phân bổ Tín dụng (Window Guidance)")

# Biểu đồ 2: Tương quan giữa Định hướng và ICOR (Bar Chart)
categories = ['Tổng vốn mới (Đầu vào)', 'Tăng trưởng GDP (Đầu ra)', 'Bong bóng Tài sản']
values = [new_credit/10, gdp_growth*10, asset_bubble_index*10] # Scale lại để vẽ chung biểu đồ
bar_colors = ['#1f77b4', '#2ca02c', '#d62728']

bars = ax2.bar(categories, values, color=bar_colors)
ax2.set_title("Tác động đến Cấu trúc Vĩ mô")
ax2.set_ylabel("Chỉ số quy đổi")

plt.tight_layout()
st.pyplot(fig)

# Khung giải thích lý thuyết
st.info("""
**Ghi chú lý thuyết:** Khi bạn giảm thanh trượt tỷ lệ **CR** xuống thấp, dòng tiền sẽ tự động chảy sang **CF**. Bạn sẽ quan sát thấy **Tăng trưởng GDP giảm**, **Bong bóng tài sản phình to**, và đặc biệt là **Hệ số ICOR tăng vọt** (thể hiện sự lãng phí vốn khổng lồ trong nền kinh tế).
""")
