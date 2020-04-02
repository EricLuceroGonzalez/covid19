# -----------------------------------------
# ------------ ---------------
#           prob3_regresion.m
#        Version 2 (Mayo, 2016)
#       Autor: Eric A. Lucero G., 2016
# ------------ ---------------
# -----------------------------------------
# # ----------------- DATOS DE ENTRADA - ----------------

# Datos de los Slides de clases
# # -----------------
Data = load('data.txt')
x = Data(: , 1)
# Primera columna de Data es la variable x
y = Data(: , 2)
# Segunda columna de Data es la variable y
# # -----------------
m = length(x)
# Se introduce el orden de la aproximación
orden = input('Orden de aproximacion = ')
tic # RELOJ
# # Regresion Multivariada
d = orden # Se define orden de la aproximación
for p = 1:
    d
fprintf('\n Orden (p = #d)\n', p)
X(: , p) = [x.^p ]
# Eleva la variable x de acuerdo al orden
A = [X]
fprintf('- - - - - - - - - - - - - - - \n')
Axy = [X y]
# Tamaño de las matrices
[m1, n1] = size(Axy)
[mA, nA] = size(A)
# REDEFINICION DE LA MATRIZ EN CADA ITERACION
AA = [ones(m, 1) A]
# # Calculo de pesos optimos
XT1 = transpose(AA)
XTA = XT1*AA
w = inv(XTA)*(XT1*y)
#(x_cont) Dominio 'continuo' para trazar la regresion
x_cont = linspace(min(x), max(x), length(x))
# Tamaño del dominio 'continuo'
[fil_xcont, col_xcont] = size(x_cont)
# Eleva el dominio 'continuo' para multiplicarlo con la hipotesis
x_cont_orden(: , p) = [x_cont.^p]
# REDEFINICION DEL DOMINIO EN CADA ITERACION(+ COLUMNA DE CEROS)
B = [ones(col_xcont, 1) x_cont_orden]
h = w'*B'
# calcula la hipotesis
hipotesis(p, : ) = h
# La guarda en cada iteracion para graficar
# # Graficos
subplot(d/2, d/2, p)
plot(x, y, 'o')
hold on
plot(x_cont, h, 'r-')
grid on
xlabel('Input(x)', 'FontSize', 12)
ylabel('Output(y)', 'FontSize', 12)
title(['Regresion de orden $d =$', num2mstr(p)],
      'FontSize', 14, 'Interpreter', 'latex')
set(gca, 'FontSize', 12)
# print -depsc2 regresionmultivariada.eps
end
# # FUNCION K foldeo - VALIDACION CRUZADA(K=1)
# Funcion que realiza la VALIDACION CRUZADA
Kfoldeo(x, y, orden)
fprintf('Tiempo transcurrido: #f segundos\n', toc) # Termina cronometro
