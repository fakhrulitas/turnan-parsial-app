import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("🧮 Aplikasi Turunan Parsial")

# Definisi variabel
x, y = sp.symbols('x y')

# Default fungsi C(x, y) tapi user bisa ganti
fungsi_str = st.text_input(
    "Masukkan fungsi f(x, y):",
    "5*x**2 + 4*x + 8*y**2 + 300*x + 500*y + 10000"
)

try:
    # Ubah string jadi fungsi sympy
    f = sp.sympify(fungsi_str)

    # Turunan parsial terhadap x dan y
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    # Tampilkan fungsi dan turunannya dalam LaTeX
    st.latex(f"f(x, y) = {sp.latex(f)}")
    st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
    st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")

    # Input nilai x0 dan y0
    x0 = st.number_input("Nilai x₀:", value=50.0)
    y0 = st.number_input("Nilai y₀:", value=30.0)

    # Hitung nilai fungsi dan gradien di titik (x0, y0)
    f_val = f.subs({x: x0, y: y0})
    fx_val = fx.subs({x: x0, y: y0})
    fy_val = fy.subs({x: x0, y: y0})

    st.write("Nilai fungsi di titik (x₀, y₀):", f_val)
    st.write("Gradien di titik (x₀, y₀):", f"({fx_val}, {fy_val})")

    # Grafik permukaan dan bidang singgung
    st.subheader("📈 Grafik Permukaan & Bidang Singgung")

    x_vals = np.linspace(x0 - 20, x0 + 20, 100)
    y_vals = np.linspace(y0 - 20, y0 + 20, 100)
    X, Y = np.meshgrid(x_vals, y_vals)

    Z = sp.lambdify((x, y), f, 'numpy')(X, Y)
    Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot permukaan fungsi
    ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')

    # Plot bidang singgung
    ax.plot_surface(X, Y, Z_tangent, alpha=0.5, color='purple')

    ax.set_title("Permukaan f(x, y) dan Bidang Singgungnya")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    st.pyplot(fig)

except Exception as m:
    st.error(f"Kalo ga bisa ngoding bilang: {m}")
