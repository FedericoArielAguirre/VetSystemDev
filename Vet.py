import json
import os
from datetime import datetime

ARCHIVO_DATOS = 'datos_veterinaria.json'

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_datos():
    estructura_base = {"mascotas": {}, "inventario": {}, "ventas": []}
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
            # Migración de estructura base
            if "mascotas" not in datos:
                estructura_base["mascotas"] = datos
                datos = estructura_base
            
            # Migración: Agregar "caducidad" a productos antiguos
            if "inventario" in datos:
                for prod_id, info in datos["inventario"].items():
                    if "caducidad" not in info:
                        info["caducidad"] = "N/A"
            
            # Migración: Agregar "peso" a mascotas antiguas
            if "mascotas" in datos:
                for masc_id, info in datos["mascotas"].items():
                    if "peso" not in info:
                        info["peso"] = "N/A"
                        
            return datos
    return estructura_base

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# ==========================================
# MÓDULO DE MASCOTAS Y CLÍNICA
# ==========================================

def generar_id_mascota(datos):
    if not datos["mascotas"]: return "VET-001"
    ids = [int(k.split('-')[1]) for k in datos["mascotas"].keys()]
    return f"VET-{max(ids) + 1:03d}"

def registrar_mascota(datos):
    limpiar_pantalla()
    print("=== REGISTRAR NUEVA MASCOTA ===")
    nombre = input("Nombre de la mascota: ").strip().title()
    especie = input("Especie (Ej. Perro, Gato): ").strip().title()
    raza = input("Raza: ").strip().title()
    edad = input("Edad (Ej. 3 años, 2 meses): ").strip()
    peso = input("Peso (Ej. 15 kg, 4.5 kg): ").strip()
    
    print("\n--- Datos del Dueño ---")
    dueño = input("Nombre del dueño: ").strip().title()
    telefono = input("Teléfono de contacto: ").strip()

    id_mascota = generar_id_mascota(datos)
    datos["mascotas"][id_mascota] = {
        "nombre": nombre, "especie": especie, "raza": raza,
        "edad": edad, "peso": peso, "dueño": dueño, "telefono": telefono, "historial": []
    }
    guardar_datos(datos)
    print(f"\n✅ Mascota registrada. ID: {id_mascota}")
    input("\nPresiona Enter...")

def mostrar_mascotas(datos):
    limpiar_pantalla()
    print("=== LISTA DE MASCOTAS ===")
    if not datos["mascotas"]:
        print("No hay mascotas registradas.")
    else:
        print(f"{'ID':<10} | {'NOMBRE':<15} | {'ESPECIE':<10} | {'PESO':<8} | {'DUEÑO':<20}")
        print("-" * 70)
        for id_m, info in datos["mascotas"].items():
            peso = info.get('peso', 'N/A')
            print(f"{id_m:<10} | {info['nombre']:<15} | {info['especie']:<10} | {peso:<8} | {info['dueño']:<20}")
    input("\nPresiona Enter...")

def buscar_mascota(datos):
    limpiar_pantalla()
    print("=== BUSCAR MASCOTA ===")
    busqueda = input("Ingresa el ID o Nombre: ").strip().title()
    encontrado = False
    for id_m, info in datos["mascotas"].items():
        if busqueda.upper() == id_m or busqueda == info['nombre']:
            encontrado = True
            mostrar_perfil_mascota(id_m, info)
            break
    if not encontrado: print("\n❌ Mascota no encontrada.")
    input("\nPresiona Enter...")

def mostrar_perfil_mascota(id_mascota, info):
    print("\n" + "="*55)
    print(f"🐾 PERFIL DE {info['nombre'].upper()} (ID: {id_mascota})")
    print("="*55)
    print(f"Especie: {info['especie']} | Raza: {info['raza']} | Edad: {info['edad']}")
    print(f"Peso actual: {info.get('peso', 'N/A')}")
    print(f"Dueño:   {info['dueño']} | Tel: {info['telefono']}")
    print("-" * 55)
    print("🩺 HISTORIAL MÉDICO Y DE FARMACIA:")
    if not info['historial']:
        print("   Sin registros.")
    else:
        for reg in info['historial']:
            print(f"   [{reg['fecha']}] {reg['motivo']}")
            if reg['diagnostico'] != "N/A": print(f"   Diagnóstico: {reg['diagnostico']}")
            print(f"   Tratamiento/Despacho: {reg['tratamiento']}")
            print("   " + "-"*45)

def agregar_consulta(datos):
    limpiar_pantalla()
    print("=== NUEVA CONSULTA MÉDICA ===")
    id_mascota = input("Ingresa el ID de la mascota (Ej. VET-001): ").strip().upper()
    
    if id_mascota in datos["mascotas"]:
        paciente = datos["mascotas"][id_mascota]
        print(f"\nPaciente: {paciente['nombre']} | Peso registrado: {paciente.get('peso', 'N/A')}")
        
        # Opción para actualizar el peso durante la consulta
        nuevo_peso = input("Actualizar peso (Presiona Enter para omitir o mantener el actual): ").strip()
        if nuevo_peso:
            paciente['peso'] = nuevo_peso
            print("✅ Peso actualizado.")

        print("\n--- Datos Clínicos ---")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        motivo = input("Motivo: ").strip()
        diagnostico = input("Diagnóstico: ").strip()
        tratamiento = input("Tratamiento: ").strip()
        
        paciente['historial'].append({
            "fecha": fecha, "motivo": f"Consulta: {motivo}",
            "diagnostico": diagnostico, "tratamiento": tratamiento
        })
        guardar_datos(datos)
        print("\n✅ Consulta agregada exitosamente.")
    else:
        print("\n❌ ID no encontrado.")
    input("\nPresiona Enter...")

# ==========================================
# MÓDULO DE TIENDA Y FARMACIA
# ==========================================

def generar_id_producto(datos):
    if not datos["inventario"]: return "PROD-001"
    ids = [int(k.split('-')[1]) for k in datos["inventario"].keys()]
    return f"PROD-{max(ids) + 1:03d}"

def agregar_producto(datos):
    limpiar_pantalla()
    print("=== AGREGAR PRODUCTO/FÁRMACO ===")
    nombre = input("Nombre del producto: ").strip().title()
    
    print("\nCategorías: 1. Alimento | 2. Accesorio | 3. Fármaco")
    opc_cat = input("Selecciona categoría (1-3): ").strip()
    
    categoria = "Fármaco" if opc_cat == '3' else "Accesorio" if opc_cat == '2' else "Alimento"
    
    requiere_receta = False
    caducidad = "N/A"
    
    if categoria == "Fármaco":
        receta = input("¿Requiere receta médica obligatoria? (S/N): ").strip().upper()
        requiere_receta = (receta == 'S')
        
    if categoria in ["Fármaco", "Alimento"]:
        cad = input("Fecha de caducidad (Ej. DD/MM/AAAA o MM/AA): ").strip()
        caducidad = cad if cad else "N/A"

    try:
        precio = float(input("\nPrecio unitario ($): "))
        stock = int(input("Cantidad en stock: "))
    except ValueError:
        print("\n❌ Error: Valores numéricos inválidos.")
        input("\nPresiona Enter...")
        return

    id_prod = generar_id_producto(datos)
    datos["inventario"][id_prod] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "requiere_receta": requiere_receta,
        "caducidad": caducidad
    }
    
    guardar_datos(datos)
    print(f"\n✅ Guardado con éxito. ID: {id_prod}")
    input("\nPresiona Enter...")

def mostrar_inventario(datos):
    limpiar_pantalla()
    print("=== INVENTARIO Y FARMACIA ===")
    if not datos["inventario"]:
        print("El inventario está vacío.")
    else:
        print(f"{'ID':<9} | {'NOMBRE':<16} | {'CATEGORÍA':<10} | {'CADUCIDAD':<10} | {'PRECIO':<7} | {'STOCK':<5} | {'RECETA'}")
        print("-" * 88)
        for id_p, info in datos["inventario"].items():
            req_receta = "Sí ⚠️" if info.get('requiere_receta', False) else "No"
            cad = info.get('caducidad', 'N/A')
            print(f"{id_p:<9} | {info['nombre'][:16]:<16} | {info['categoria'][:10]:<10} | {cad[:10]:<10} | ${info['precio']:<6.2f} | {info['stock']:<5} | {req_receta}")
    input("\nPresiona Enter...")

def realizar_venta(datos):
    limpiar_pantalla()
    print("=== PUNTO DE VENTA Y FARMACIA ===")
    id_prod = input("ID del producto (Ej. PROD-001): ").strip().upper()
    
    if id_prod not in datos["inventario"]:
        print("\n❌ Producto no encontrado.")
        input("\nPresiona Enter...")
        return

    prod = datos["inventario"][id_prod]
    texto_cad = f" | Caducidad: {prod.get('caducidad', 'N/A')}" if prod.get('caducidad') != 'N/A' else ""
    print(f"\nProducto: {prod['nombre']} | Stock: {prod['stock']} | Precio: ${prod['precio']:.2f}{texto_cad}")
    
    if prod.get("requiere_receta", False):
        print("\n⚠️  ATENCIÓN: Este fármaco requiere receta médica.")
        id_mascota = input("Ingresa el ID del paciente (Ej. VET-001): ").strip().upper()
        if id_mascota not in datos["mascotas"]:
            print("❌ Paciente no registrado. No se puede realizar la venta.")
            input("\nPresiona Enter...")
            return
        paciente_nombre = datos["mascotas"][id_mascota]["nombre"]
        print(f"✅ Paciente verificado: {paciente_nombre}")
        cliente_ref = f"{paciente_nombre} ({id_mascota})"
    else:
        id_mascota = None
        cliente_ref = "Público General"

    try:
        cantidad = int(input("\nCantidad a vender: "))
    except ValueError:
        print("❌ Cantidad no válida.")
        input("\nPresiona Enter...")
        return

    if cantidad <= 0 or cantidad > prod['stock']:
        print("❌ Cantidad inválida o stock insuficiente.")
    else:
        total = cantidad * prod['precio']
        datos["inventario"][id_prod]['stock'] -= cantidad
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        datos["ventas"].append({
            "fecha": fecha_actual,
            "producto": prod['nombre'],
            "cantidad": cantidad,
            "total": total,
            "cliente": cliente_ref
        })

        if id_mascota:
            datos["mascotas"][id_mascota]['historial'].append({
                "fecha": fecha_actual,
                "motivo": "Compra en Farmacia (Fármaco Controlado)",
                "diagnostico": "N/A",
                "tratamiento": f"Se despacharon {cantidad} unidad(es) de {prod['nombre']}"
            })
            print(f"📋 Fármaco registrado en el historial de {paciente_nombre}.")
        
        guardar_datos(datos)
        print(f"\n✅ Venta realizada. Total a cobrar: ${total:.2f}")
    
    input("\nPresiona Enter...")

def mostrar_ventas(datos):
    limpiar_pantalla()
    print("=== REGISTRO DE VENTAS ===")
    if not datos["ventas"]:
        print("Aún no hay ventas.")
    else:
        total_ingresos = 0
        print(f"{'FECHA':<18} | {'PRODUCTO':<20} | {'CLIENTE/PACIENTE':<20} | {'TOTAL'}")
        print("-" * 80)
        for v in datos["ventas"]:
            cliente = v.get('cliente', 'Público General')
            print(f"{v['fecha']:<18} | {v['producto']:<20} | {cliente:<20} | ${v['total']:.2f}")
            total_ingresos += v['total']
        print("-" * 80)
        print(f"INGRESOS TOTALES: ${total_ingresos:.2f}")
    input("\nPresiona Enter...")

def menu_tienda(datos):
    while True:
        limpiar_pantalla()
        print("=========================================")
        print("🛒 TIENDA Y FARMACIA VETERINARIA")
        print("=========================================")
        print("1. 📦 Ver inventario (Alimentos, Accesorios, Fármacos)")
        print("2. ➕ Agregar nuevo producto / Fármaco")
        print("3. 💲 Realizar venta / Despachar receta")
        print("4. 📊 Ver registro de ingresos")
        print("5. 🔙 Volver al Menú Principal")
        print("=========================================")
        
        opcion = input("Selecciona una opción (1-5): ").strip()
        
        if opcion == '1': mostrar_inventario(datos)
        elif opcion == '2': agregar_producto(datos)
        elif opcion == '3': realizar_venta(datos)
        elif opcion == '4': mostrar_ventas(datos)
        elif opcion == '5': break

# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def menu_principal():
    datos = cargar_datos()
    while True:
        limpiar_pantalla()
        print("=========================================")
        print("🏥 SISTEMA DE GESTIÓN VETERINARIA 🏥")
        print("=========================================")
        print("1. 🐶 Registrar nueva mascota")
        print("2. 📋 Ver lista de mascotas")
        print("3. 🔍 Buscar paciente y ver perfil clínico")
        print("4. 🩺 Agregar consulta médica")
        print("5. 💊 Tienda y Farmacia")
        print("6. 🚪 Salir")
        print("=========================================")
        
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == '1': registrar_mascota(datos)
        elif opcion == '2': mostrar_mascotas(datos)
        elif opcion == '3': buscar_mascota(datos)
        elif opcion == '4': agregar_consulta(datos)
        elif opcion == '5': menu_tienda(datos)
        elif opcion == '6':
            limpiar_pantalla()
            print("¡Gracias por usar el sistema! 👋")
            break

if __name__ == "__main__":
    menu_principal()