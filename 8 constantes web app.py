
"""
Created on Wed Aug 26 07:38:29 2026
@author: zamo_only

--------------------------------------------------------------------
        CODIGO PARA EL CALCULO DE LAS 8 CONSTANTES (VERSION WEB)
--------------------------------------------------------------------
"""

#-------------Definicion de bibliotecas-----------------------------
import numpy as np
import streamlit as st  # <-- Añadimos la librería para la interfaz web

# El título que se verá en la pestaña y arriba en la página
st.set_page_config(page_title="Calculadora de Coeficientes", page_icon="🏗️")
st.title("🏗️ Cálculo de Coeficientes en Fórmulas de Recurrencia")
st.write("Introduce las variables de tu sistema estructural y presiona el botón para calcular.")
st.write("Creado por:Diego Ivan Zamorano Saldivar II Facultad de ingenieria UNAM")

#-------------Variables de entrada editables desde la web---
st.sidebar.header("Variables de Entrada") # Panel lateral organizado

zeta = st.sidebar.number_input("Coeficiente de amortiguamiento (zeta)", value=0.05, min_value=-1.0, step=0.01, format="%.4f")
k = st.sidebar.number_input("Rigidez (k)", value=14000.0, step=100.0)
m = st.sidebar.number_input("Masa (m)", value=15000.0, step=100.0)
dt = st.sidebar.number_input("Intervalo de tiempo (dt)", value=0.01, min_value=-1.0, step=0.001, format="%.4f")

# Botón para ejecutar el código con un clic
if st.button("⚡ Calcular Coeficientes"):

    #-------------Verificaciones importantes (alertas de error en la web)---
    if zeta <= 0:
        st.error("❌ El amortiguamiento no puede ser negativo o nulo.")
    elif zeta >= 1:
        st.warning("⚠️ Estas fórmulas son válidas para sistemas subamortiguados. Intenta con zeta = 0.05.")
    elif m <= 0:
        st.error("❌ La masa no puede ser negativa.")
    elif k <= 0:
        st.error("❌ La rigidez debe ser mayor a cero.")
    elif dt <= 0:
        st.error("❌ El intervalo de tiempo debe ser mayor que cero.")
    else:
        # Siguiente paso: corre lógica exacta:
        wn = np.sqrt(k / m) 
        wD = wn * np.sqrt(1 - zeta**2) 
        Tn = (2 * np.pi) / wn 
        c = 2 * zeta * m * wn 

        #-------------Operaciones repetidas---------------------------------
        raiz = np.sqrt(1 - zeta**2)
        exp_term = np.exp(-zeta * wn * dt)
        sin_term = np.sin(wD * dt)
        cos_term = np.cos(wD * dt)

        #------------Calculo de los coeficientes ---------------------------
        A = exp_term * ((zeta / raiz) * sin_term + cos_term)
        B = exp_term * ((1 / wD) * sin_term)
        C = (1 / k) * ((2 * zeta) / (wn * dt) + exp_term * (((1 - 2 * zeta**2) / (wD * dt) - zeta / raiz) * sin_term - (1 + (2 * zeta) / (wn * dt)) * cos_term))
        D = (1 / k) * (1 - (2 * zeta) / (wn * dt) + exp_term * (((2 * zeta**2 - 1) / (wD * dt)) * sin_term + ((2 * zeta) / (wn * dt)) * cos_term))
        
        Ap = - exp_term * ((wn / raiz) * sin_term)
        Bp = exp_term * (cos_term - (zeta / raiz) * sin_term)
        
        Cp = (1 / k) * (- (1 / dt) + exp_term * ((wn / raiz + zeta / (dt * raiz)) * sin_term + (1 / dt) * cos_term))
        Dp = (1 / (k * dt)) * (1 - exp_term * ((zeta / raiz) * sin_term + cos_term))

        #----------------Impresion de resultados en la interfaz web--------
        st.success("✨ ¡Cálculo completado con éxito!")
        
        # Estructuramos en columnas para que se vea chidooooo
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Propiedades Dinámicas")
            st.metric("Periodo natural (Tn)", f"{Tn:.5f} s")
            st.metric("Frecuencia natural (Wn)", f"{wn:.5f} rad/s")
            st.metric("Frecuencia Amortiguada (Wd)", f"{wD:.5f} rad/s")
            st.metric("Amortiguamiento Viscoso (c)", f"{c:.2f}")

        with col2:
            st.subheader("Constantes Calculadas")
            st.write(f"**A** = `{A:.8f}`")
            st.write(f"**B** = `{B:.8f}`")
            st.write(f"**C** = `{C:.5e}`")
            st.write(f"**D** = `{D:.5e}`")
            st.divider()
            st.write(f"**Ap** = `{Ap:.8f}`")
            st.write(f"**Bp** = `{Bp:.8f}`")
            st.write(f"**Cp** = `{Cp:.5e}`")
            st.write(f"**Dp** = `{Dp:.5e}`")

        # Tu mensaje final
        st.info("😎 Everything is dude, cool")
        st.info("(Si, asi suena mejor)")
