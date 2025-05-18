import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi awal
st.set_page_config(page_title="Optimasi Biaya Produksi Baterai EV", layout="wide")
st.title("🔋 Studi Kasus Turunan Parsial - Optimasi Biaya Produksi Baterai Kendaraan Listrik")

st.markdown("""
### 👤 Informasi Mahasiswa
- **Nama**: Galang Sopyan  
- **NIM**: 312410046  
- **Kelas**: TI.24.C1  
- **Mata Kuliah**: Matematika Terapan  
""")

st.markdown("---")

# Input fungsi biaya produksi
st.header("📌 1. Masukkan Fungsi Biaya Produksi")
st.write("Masukkan fungsi biaya total C(x, y), di mana:")
st.markdown("- `x` = jumlah modul baterai **standar**")
st.markdown("- `y` = jumlah modul baterai **performa tinggi**")
fungsi_str = st.text_input("Contoh: x**2 + 3*y**2 + 2*x*y", "x**2 + 3*y**2 + 2*x*y")

x, y = sp.symbols('x y')

try:
    # Proses fungsi dan turunannya
    f = sp.sympify(fungsi_str)
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    st.header("🧮 2. Hasil Turunan Parsial")
    st.latex(f"C(x, y) = {sp.latex(f)}")
    col1, col2 = st.columns(2)
    with col1:
        st.latex(f"\\frac{{\\partial C}}{{\\partial x}} = {sp.latex(fx)}")
    with col2:
        st.latex(f"\\frac{{\\partial C}}{{\\partial y}} = {sp.latex(fy)}")

    # Input titik produksi
    st.header("🏭 3. Evaluasi Biaya di Titik Produksi")
    st.write("Tentukan jumlah modul yang diproduksi:")
    col3, col4 = st.columns(2)
    with col3:
        x0 = st.number_input("Jumlah modul standar (x₀):", value=50.0)
    with col4:
        y0 = st.number_input("Jumlah modul performa tinggi (y₀):", value=30.0)

    # Evaluasi nilai turunan di titik
    f_val = f.subs({x: x0, y: y0})
    fx_val = fx.subs({x: x0, y: y0})
    fy_val = fy.subs({x: x0, y: y0})

    st.success(f"💰 **Biaya produksi total pada titik ({x0}, {y0}) adalah:** {f_val}")
    st.info(f"📈 **Gradien biaya produksi:** ∇C = ({fx_val}, {fy_val})")

    # Visualisasi grafik permukaan dan bidang singgung
    st.header("📊 4. Visualisasi Permukaan Biaya dan Bidang Singgung")

    x_vals = np.linspace(x0 - 20, x0 + 20, 50)
    y_vals = np.linspace(y0 - 20, y0 + 20, 50)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = sp.lambdify((x, y), f, 'numpy')(X, Y)
    Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.75, edgecolor='none')
    ax.plot_surface(X, Y, Z_tangent, color='orange', alpha=0.5)
    ax.set_title("Permukaan Fungsi Biaya dan Bidang Singgung di Titik Produksi")
    ax.set_xlabel("Modul Standar (x)")
    ax.set_ylabel("Modul Performa Tinggi (y)")
    ax.set_zlabel("Biaya Produksi (C)")
    st.pyplot(fig)

    st.markdown("🎯 Grafik di atas menunjukkan bagaimana biaya berubah terhadap jumlah produksi, serta bidang singgung sebagai pendekatan linear di titik yang dipilih.")

    # Penutup
    st.header("📌 5. Kesimpulan")
    st.markdown("""
Turunan parsial digunakan untuk mengetahui pengaruh perubahan masing-masing jenis modul terhadap biaya produksi secara keseluruhan.
Dengan analisis ini, perusahaan bisa mengoptimalkan kombinasi produksi untuk menurunkan biaya atau meningkatkan efisiensi.

Pendekatan ini relevan dalam strategi manufaktur skala besar, khususnya industri kendaraan listrik (EV).
""")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memproses fungsi: {e}")
