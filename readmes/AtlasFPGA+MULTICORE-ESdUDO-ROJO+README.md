# MULTICORE-ESdUDO-ROJO
Diseñar la placa - ¡Créalo tu mismo! de coste más reducido para la Fpga CYC1000 con una bluepill STM32F103C8T6

# https://t.me/INICIATIVAATLAS -> El grupo ATLAS esta en Telegram pueden encontrarnos allí, Group ATLAS in Telegram

[![Escudo ROJO](https://img.youtube.com/vi/kMc1XR39d8Y/maxresdefault.jpg)](https://youtu.be/kMc1XR39d8Y)


   Se muestra el multicore en desarrollo para cyc1000 de arrow/trenz el cual aloja una fpga Cyclone 10 LP de intel con 25kles y 66 bloques de Bram de 9Kbytes, tiene integrada una memoria de celular de bajo consumo y reducida latencia, siendo una sdram a 166Mhz con 8MBytes en un bus de 16bits, La familia Cyclone 10 LP permite implementar modelos que superan los 400Mhz en sus diseños, manteniendo un bajo consumo. 
También hay que disponer de una bluepill con un STM32F103C8Tx, posee 64Kbytes de Flash y 20Kbytes de sram, con una unidad de proceso ARM cortex M3 de 32bit funcionando a 72Mhz. 

---
# Esquema analógico totalmente configurable por el usuario en el vídeo compuesto de 512 colores.

![Ajuste ANALÓGICO VIDEO COMPUESTO](https://github.com/AtlasFPGA/MULTICORE-ESDUDO-ROJO/blob/main/Fotos/Esquema_Anal%C3%B3gico_Ajustable_y_Usb-directo.png)

Nota:

Creamos una tabla para proceder con el ajuste analógico de la salida de vídeo compuesto.

| R3  |     RV1   | VALOR RESISTIVO RAMA COMPOSITE 0  | R4  | RV2  |  VALOR RESISTIVO RAMA COMPOSITE 1|
|:-------------:|------:|------:|------:|------:|------:|
|750 Ohm|0 Ohm|750 Ohm| 80 Ohm| 0 Ohm|80 Ohm|
|1500 Ohm|1000 Ohm|2500 Ohm|80 Ohm|150 Ohm|230 Ohm|

Para Composite 0 la corriente máxima se obtiene con 750 Ohm -> +3,3V/(750_Ohm)= 0,0044 Amperios

Para Composite 0 la corriente mínima se obtiene con 2500 Ohm -> +3,3V/(2500_Ohm)= 0,00132 Amperios

Para Composite 1 la corriente máxima se obtiene con 80 Ohm -> +3,3V/(80_Ohm)= 0,04125 Amperios -> La CYCLONE 10 LP esta limitada a 12Miliamperios ¿Lo fundimos?

Para Composite 1 la corriente mínima en el diseño propuesto se obtiene con 230 Ohm -> +3,3V/(230_Ohm)= 0,014347926 Amperios -> Por encima de la limitación de corriente 12Miliamperios

Luego hay que calcular que valores de resistencia usar, en Composite 1 en las dos posiciones extremas se drena más corriente por pin.
También vemos que aporta más corriente Composite1 un valor más fuerte que Composite0, por lo que tenemos bien ordenadas las lineas por donde van las señales, pero al ser hardware programable, imaginamos que nos equivocamos, esta es una de las grandes cualidades de una FPGA, con una simple reordenadión de pineado y reetiquetado todo funciona perfectamente,es por esto que muchos diseños actualmente son programables ya sean microcontroladores, cplds o fpgas.

Luego la pregunta es, que resistencia en serie a +3,3V coloco para no fundir un pin de... ¿la preciada FPGA?
doce miliamperios = 0,012_Amperios = +3,3_Voltios/Resistencia_protección_pin

Resistencia_protección_pin = 275 Ohm

Es lo más importante dado que la FPGA tiene limitada la cantidad de corriente que es capaz de entregar, y hacerle una conexión muy baja en resistencia puede fundir o dicho pin o parte de los pines de salida de la fpga, raramente toda la FPGA.

Sus resistencias se suman, la posición de las resistencias fijas es para proteger los circuitos y limitar la corriente, en realidad hemos puesto el valor represantado con el mayor valor resistivo y el menor de todos.

# Pero como siempre pasa os he mentido, porque... ¿Realmente llega a 0V cuando el televisor recoge la señal?

El caso de los condensadores/capacitores de filtrado es algo más complejo dado que las ramas que estan en serie siguen esta ley (Condensador=Capacitor):
1/Condensador_equivalente = 1/Condensador_serie1 + 1/Condensador_serie2 + 1/Condensador_serie3 + ... + 1/Condensador_serieN
Pero como vamos a usar valores del mismo condensador tenemos una rama preparada en serie.
El condensador usado para el montaje son 6 condensadores de 22 pico faradios, ya ser verán si se colocan todos o no, una capacidad bastante pequeña.
1 Mili = 0'001 Faradios
1 Nano = 0'000001 Faradios
1 Pico = 0'000000001 Faradios

Entondes en realidad usamos condensadores/capacitores de:
22 Pico Faradios = 0'000000022 Faradios

cuando hacemos y despejamos esta ecuación 1/Faradios_rama_serie = 1/0'000000022_F + 1/0'000000022_F
Sale un resultado de Faradios_rama_serie = 1/0'000000011 Faradios y en lenguaje de pico -> 11 pico Faradios

Cuando hay condensadore/capacitores en paralelo se suman sus capacidades:
Podemos no filtrar la señal -> 0Faradios pero esto nunca se cumple y menos con señales generadas a tanta frecuencia las pistas siempre tienen un contenido continuo de capacitancia, por eso siempre aparecen modelizaciones de spice.

Usando los 2 condensadores en una sola rama en serie:
Una capacidad de 11 Pico faracios.

Poniendo un Condensador de 22 picofaracios entre la señal de salida de la fpga y GND.
Una capacidad de 22 Pico faradios.

Poniendo los 2 condensadores en paralelo se suman sus capacidades, (Tampoco es verdad si los condensaores estan limitados en voltaje):
Pero bueno digamos que todo es ideal y son 44 Pico Faradios.

La maxima capacidad es usar 2 condensadores en paralelo más una rama de condensadores en serie:
22 Pico Faradios + 22 Pico Faradios + 11 Pico Faradios = 55 Pico Faradios.

Luego con 4 condensadores en la disposición del circuito podemos tener estas capacidades.

Practicamente 0 Faradios , 0'000000022 Faradios,0'000000033 Faradios ,0'000000044 Faradios y 0'000000055 Faradios
Hay un modo que he puesto su filtrado pero no esta explicado.
Pero se vé lo útil de tener la dispoción de filtrado en capacidad, por supuesto si alguien quiere filtrar más la señal puede cambiando los modelos de condensador.

Las resistencias tienen un valor fijo en R3 y R4 y al menos tendrían que limitar la corriente al máximo que permite la familia Cyclone 10 Lp.
---
# Esquema ESdUDO V0101
![Esquemario ESdUDO ROJO V0101](https://github.com/AtlasFPGA/MULTICORE-ESDUDO-ROJO/blob/main/Fotos/Esquema_ESdUDO_ROJO_V0101-Correcci%C3%B3n_Licencia.png)
---
# Capas de la placa ESdUDO V0101
![Placa ESdUDO ROJO V0101](https://github.com/AtlasFPGA/MULTICORE-ESDUDO-ROJO/blob/main/Fotos/Placa%20ESdUDO%20ROJO.png)
---

   Este modelo implementa soluciones de muy baja latencia, al usar envoltorios con máquinas de estado finito para el video compuesto y el teclado.
   
###   https://github.com/TheSonders/COLOR_PAL
   
###   https://github.com/TheSonders/USBKeyboard

   El diseño es de reducido tamaño, permitiendo alojarlo en equipos estropeados y no recuperables.

   En precio asociado a la placa son aproximadamente 6€.
---

#   Una lista de los pocos componentes necesarios

| Unidades  |     descripción      |  Precio medio en tienda física en España |
|----------|:-------------:|------:|
| 8 |  • condensadores de filtrado, ramas serie y paralelo. | ?€|
| 4 |  • resistencias. Dos de ellas prescindibles mediante programacion de pull down en las patillas K1 y L1 de la cyc1000. |  ?€ |
| 2 | • potenciometros de señal para ajustar la intensidad. |    ?€ |
  | numerosos | • Asi como bastantes tiras de pines, machos y hembras también pines apilables usados en arduino. |    ?€ |
  | 1 | • Un condensador electrolítico. |    ?€ |
  | 1 | • Un pulsador. |    ?€ |
  | 1 | • Un puerto usb A. |    ?€ |
  | 1 | • Un puerto de vídeo compuesto. |    ?€ |
  | 1 | • Disponer de una muestra de cyc1000 del programa Europero de fpgas de intel/arrow. |    ?€ |
  | 1 | • Disponer de una bluepill. |    ?€ |
  | 1 | • Así como un módulo i2s de texas instruments MCP5102A. |    ?€ |

--- 
   Es con diferencia el sistema multicore más económico.

Las placas necesarias:

# ¡ATENCIÓN A LA BLUPILL COLOCADA! 
# HAY DOS MODELOS DE BLUEPILL, LA BLUEPILL PLUS, Y LA PRIMERA BLUEPILL.

BLUEPILL STM32F103C8T6 (Usada en el DISEÑO V0101):

https://es.aliexpress.com/item/1005003429884084.html

BLUEPILL STM32F103C8T6 Plus (Necesita adaptación una linea de 5V existe en lugar de GND, se producirá un buen corto si se opta por este modelo),
por lo demás es compatible en un rango de funcionamiento del 99% y tiene un punto que para el programador es interesante  duplica la flash disponible 128Kbytes.

https://m.es.aliexpress.com/item/1005004918334754.html

SD+TFT AZ-Delivery de 1,8Pulgadas:

https://es.aliexpress.com/item/1005005060814683.html

CYC1000 versión mejorada del 2023 TEI0003-03-QFCR4A-CYC1000:

https://shop.trenz-electronic.de/en/TEI0003-03-QFCR4A-CYC1000-with-Cyclone-10-FPGA-8-MB-SDRAM-8-MB-Flash-6.15-x-2.5-cm?c=480

O una muestra en el programa europeo de microfpgas:

https://www.arrow.com/en/family/intel-solutions-europe

Grupo de la iniciativa ATLAS en TELEGRAM:

# https://t.me/INICIATIVAATLAS

Licencia CERN OHL V2 STRICT:

https://ohwr.orgcern_ohl_s_v2.txt
