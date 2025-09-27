from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from Proyecto import Libro, Usuario, Prestamo, actualizar_libro, eliminar_libro, crear_tablas, prestar_libro, devolver_libro

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para mensajes flash

# Crear tablas al iniciar la app
crear_tablas()

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/libros")
def listar_libros():
    libros = Libro.obtener_todos()
    return render_template("libros.html", libros=libros)

@app.route("/agregar_libro", methods=["GET", "POST"])
def agregar_libro_web():
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            titulo = request.form.get("titulo")
            autor = request.form.get("autor")
            editorial = request.form.get("editorial")
            año = request.form.get("año")
            genero = request.form.get("genero")

            # Validar que todos los campos estén presentes
            if not all([titulo, autor, editorial, año, genero]):
                flash("Todos los campos son obligatorios.", "error")
                return render_template("libros.html", libros=Libro.obtener_todos())

            # Convertir año a entero y validar
            try:
                año = int(año)
                if año < 0 or año > 2025:  # Validar rango razonable
                    flash("El año debe estar entre 0 y 2025.", "error")
                    return render_template("libros.html", libros=Libro.obtener_todos())
            except (ValueError, TypeError):
                flash("El año debe ser un número válido.", "error")
                return render_template("libros.html", libros=Libro.obtener_todos())

            # Generar nuevo ID
            libros = Libro.obtener_todos()
            nuevo_id = max([l.id_libro for l in libros], default=0) + 1

            # Crear y guardar el libro
            libro = Libro(id_libro=nuevo_id, titulo=titulo, autor=autor, editorial=editorial, año=año, genero=genero)
            libro.guardar()

            flash("Libro agregado correctamente.", "success")
            return redirect(url_for("listar_libros"))

        except Exception as e:
            flash(f"Error al agregar el libro: {str(e)}", "error")
            return render_template("libros.html", libros=Libro.obtener_todos())

    # Para GET, mostrar el formulario (en la misma página libros.html)
    return render_template("libros.html", libros=Libro.obtener_todos())

@app.route("/libros/eliminar", methods=["POST"])
def eliminar_libros_web():
    try:
        id_libro = request.form.get("id_libro")
        if not id_libro:
            flash("El ID del libro es obligatorio.", "error")
            return render_template("libros.html", libros=Libro.obtener_todos())

        id_libro = int(id_libro)
        resultado = eliminar_libro(id_libro)
        
        if resultado and resultado.get("success"):
            flash(resultado["message"], "success")
        else:
            mensaje = resultado["message"] if resultado else "Error desconocido al eliminar el libro."
            flash(mensaje, "error")
            
        return redirect(url_for("listar_libros"))
    except ValueError:
        flash("El ID del libro debe ser un número válido.", "error")
        return render_template("libros.html", libros=Libro.obtener_todos())
    except Exception as e:
        flash(f"Error al eliminar el libro: {str(e)}", "error")
        return render_template("libros.html", libros=Libro.obtener_todos())

@app.route("/libros/actualizar", methods=["POST"])
def actualizar_libros_web():
    try:
        id_libro = request.form.get("id_libro")
        kwargs = {}
        
        if request.form.get("titulo"):
            kwargs['titulo'] = request.form.get("titulo")
        if request.form.get("autor"):
            kwargs['autor'] = request.form.get("autor")
        if request.form.get("editorial"):
            kwargs['editorial'] = request.form.get("editorial")
        if request.form.get("año"):
            try:
                año = int(request.form.get("año"))
                if año < 0 or año > 2025:
                    flash("El año debe estar entre 0 y 2025.", "error")
                    return render_template("libros.html", libros=Libro.obtener_todos())
                kwargs['año'] = año
            except (ValueError, TypeError):
                flash("El año debe ser un número válido.", "error")
                return render_template("libros.html", libros=Libro.obtener_todos())
        if request.form.get("genero"):
            kwargs['genero'] = request.form.get("genero")
        if request.form.get("disponible"):
            kwargs['disponible'] = request.form.get("disponible") == "si"
            
        if not id_libro:
            flash("El ID del libro es obligatorio.", "error")
            return render_template("libros.html", libros=Libro.obtener_todos())

        id_libro = int(id_libro)
        actualizar_libro(id_libro, **kwargs)
        flash("Libro actualizado correctamente.", "success")
        return redirect(url_for("listar_libros"))
        
    except ValueError:
        flash("El ID del libro debe ser un número válido.", "error")
        return render_template("libros.html", libros=Libro.obtener_todos())
    except Exception as e:
        flash(f"Error al actualizar el libro: {str(e)}", "error")
        return render_template("libros.html", libros=Libro.obtener_todos())

@app.route("/usuarios")
def listar_usuarios():
    usuarios = Usuario.obtener_todos()
    return render_template("usuarios.html", usuarios=usuarios)   

@app.route("/usuarios/agregar", methods=["GET", "POST"])
def agregar_usuario_web():
    if request.method == "POST":
        try:
            documento = request.form.get("documento")
            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")
            telefono = request.form.get("telefono")
            email = request.form.get("email")
            rol = request.form.get("rol", "normal")

            if not all([documento, nombre, apellido, telefono, email]):
                flash("Todos los campos son obligatorios.", "error")
                return redirect(url_for("listar_usuarios"))

            # Verificar que el documento no exista ya
            usuario_existente = Usuario.obtener_por_documento(documento)
            if usuario_existente:
                flash("Ya existe un usuario con ese documento.", "error")
                return redirect(url_for("listar_usuarios"))

            usuario = Usuario(nombre=nombre, apellido=apellido, telefono=telefono, email=email, rol=rol, documento=documento)
            usuario.guardar()

            flash("Usuario agregado correctamente.", "success")
            return redirect(url_for("listar_usuarios"))
        except Exception as e:
            flash(f"Error al agregar el usuario: {str(e)}", "error")
            return redirect(url_for("listar_usuarios"))

    return render_template("agregar_usuarios.html")

@app.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuarios_web():
    try:
        documento = request.form.get("documento")
        if not documento:
            flash("El documento del usuario es obligatorio.", "error")
            return redirect(url_for("listar_usuarios"))

        from Proyecto import eliminar_usuario_por_documento
        exito, mensaje = eliminar_usuario_por_documento(documento)
        if exito:
            flash("Usuario eliminado correctamente.", "success")
        else:
            flash(mensaje, "error")
        return redirect(url_for("listar_usuarios"))
    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "error")
        return render_template("usuarios.html", usuarios=Usuario.obtener_todos())

@app.route("/usuarios/actualizar", methods=["POST"])
def actualizar_usuarios_web():
    try:
        documento = request.form.get("documento")
        kwargs = {}
        
        if request.form.get("nombre"):
            kwargs['nombre'] = request.form.get("nombre")
        if request.form.get("apellido"):
            kwargs['apellido'] = request.form.get("apellido")
        if request.form.get("telefono"):
            kwargs['telefono'] = request.form.get("telefono")
        if request.form.get("email"):
            kwargs['email'] = request.form.get("email")
        if request.form.get("rol"):
            kwargs['rol'] = request.form.get("rol")
            
        if not documento:
            flash("El documento del usuario es obligatorio.", "error")
            return redirect(url_for("listar_usuarios"))

        from Proyecto import actualizar_usuario_por_documento
        exito, mensaje = actualizar_usuario_por_documento(documento, **kwargs)
        if exito:
            flash("Usuario actualizado correctamente.", "success")
        else:
            flash(mensaje, "error")
        return redirect(url_for("listar_usuarios"))
        
    except Exception as e:
        flash(f"Error al actualizar el usuario: {str(e)}", "error")
        return redirect(url_for("listar_usuarios"))

@app.route("/prestamos/menu")
def menu_prestamos():
    return render_template("prestamos.html")

@app.route("/prestamos")
def listar_prestamos():
    prestamos = Prestamo.obtener_todos()
    usuarios = Usuario.obtener_todos()
    libros = Libro.obtener_todos()
    return render_template("prestamos_lista.html", prestamos=prestamos, usuarios=usuarios, libros=libros)

@app.route("/prestamos/prestar", methods=["GET", "POST"])
def prestar_libro_web():
    if request.method == "POST":
        try:
            documento_usuario = request.form.get("documento_usuario")
            id_libro = request.form.get("id_libro")
            dias = request.form.get("dias")

            if not all([documento_usuario, id_libro, dias]):
                flash("Todos los campos son obligatorios.", "error")
                return render_template("prestamos.html", usuarios=Usuario.obtener_todos(), libros=Libro.obtener_todos())

            id_libro = int(id_libro)
            dias = int(dias)

            resultado = prestar_libro(id_libro, documento_usuario, dias)
            if resultado.get("success", True):
                flash("Préstamo registrado correctamente.", "success")
                return redirect(url_for("listar_prestamos"))
            else:
                flash(resultado.get("message", "Error al registrar el préstamo."), "error")
                return render_template("prestamos.html", usuarios=Usuario.obtener_todos(), libros=Libro.obtener_todos())
        except ValueError:
            flash("Los campos ID de libro y días deben ser números válidos.", "error")
            return render_template("prestamos.html", usuarios=Usuario.obtener_todos(), libros=Libro.obtener_todos())
        except Exception as e:
            flash(f"Error al registrar el préstamo: {str(e)}", "error")
            return render_template("prestamos.html", usuarios=Usuario.obtener_todos(), libros=Libro.obtener_todos())

    usuarios = Usuario.obtener_todos()
    libros = Libro.obtener_todos()
    return render_template("prestamos.html", usuarios=usuarios, libros=libros)

@app.route("/prestamos/devolver/", methods=["POST"])
def devolver_libro_web():
    try:
        id_prestamo = request.form.get("id_prestamo")
        devolver_libro(id_prestamo)
        flash("Libro devuelto correctamente.", "success")
        return redirect(url_for("menu_prestamos"))
    except Exception as e:
        flash(f"Error al devolver el libro: {str(e)}", "error")
        return redirect(url_for("menu_prestamos"))

@app.route("/prestamos/devolver_multiples/", methods=["POST"])
def devolver_libros_multiples():
    try:
        # Obtener la lista de IDs de préstamos como string separado por comas
        ids_prestamos_str = request.form.get("ids_prestamos")
        
        if not ids_prestamos_str:
            flash("No se seleccionaron libros para devolver.", "error")
            return redirect(url_for("menu_prestamos"))
        
        # Convertir string a lista de enteros
        try:
            ids_prestamos = [int(id_str.strip()) for id_str in ids_prestamos_str.split(',') if id_str.strip()]
        except (ValueError, TypeError):
            flash("Error en los datos de los préstamos seleccionados.", "error")
            return redirect(url_for("menu_prestamos"))
        
        if not ids_prestamos:
            flash("No se seleccionaron libros válidos para devolver.", "error")
            return redirect(url_for("menu_prestamos"))
        
        # Importar la nueva función de devolución múltiple
        from Proyecto import devolver_libros_multiples as devolver_multiples_func
        
        # Procesar devoluciones múltiples
        resultados = devolver_multiples_func(ids_prestamos)
        
        # Analizar resultados
        exitosos = len([r for r in resultados if r['exito']])
        fallidos = len(resultados) - exitosos
        
        if exitosos > 0:
            flash(f"✅ Se devolvieron {exitosos} libro{'s' if exitosos != 1 else ''} correctamente.", "success")
        
        if fallidos > 0:
            errores = [r['error'] for r in resultados if not r['exito']]
            flash(f"❌ {fallidos} devolución{'es' if fallidos != 1 else ''} fallida{'s' if fallidos != 1 else ''}: {'; '.join(errores)}", "error")
        
        return redirect(url_for("menu_prestamos"))
        
    except Exception as e:
        flash(f"Error al procesar las devoluciones múltiples: {str(e)}", "error")
        return redirect(url_for("menu_prestamos"))

@app.route("/reportes")
def reportes():
    return render_template("reportes.html")

@app.route("/reportes/total_prestamos")
def total_prestamos():
    from Proyecto import reporte_total_prestados
    return "<pre>" + str(reporte_total_prestados()) + "</pre>"

@app.route("/reportes/usuarios_multas")
def usuarios_multas():
    from Proyecto import reporte_usuarios_con_multas
    return "<pre>" + str(reporte_usuarios_con_multas()) + "</pre>"

@app.route("/reportes/genero")
def estadisticas_genero():
    from Proyecto import reporte_estadisticas_por_genero
    return "<pre>" + str(reporte_estadisticas_por_genero()) + "</pre>"

@app.route("/reportes/exportar_csv")
def exportar_csv_web():
    from Proyecto import exportar_csv
    exportar_csv()
    return "Archivo CSV generado correctamente"

@app.route("/libros/editar/<int:id_libro>", methods=["GET", "POST"])
def editar_libro(id_libro):
    libro = next((l for l in Libro.obtener_todos() if l.id_libro == id_libro), None)
    if not libro:
        flash("Libro no encontrado.", "error")
        return redirect(url_for("listar_libros"))

    if request.method == "POST":
        try:
            libro.titulo = request.form.get("titulo")
            libro.autor = request.form.get("autor")
            libro.editorial = request.form.get("editorial")
            libro.año = int(request.form.get("año"))
            libro.genero = request.form.get("genero")
            libro.disponible = request.form.get("disponible") == "si"

            if not all([libro.titulo, libro.autor, libro.editorial, libro.año, libro.genero]):
                flash("Todos los campos son obligatorios.", "error")
                return render_template("editar_libro.html", libro=libro)

            libro.guardar()
            flash("Libro editado correctamente.", "success")
            return redirect(url_for("listar_libros"))
        except ValueError:
            flash("El año debe ser un número válido.", "error")
            return render_template("editar_libro.html", libro=libro)
        except Exception as e:
            flash(f"Error al editar el libro: {str(e)}", "error")
            return render_template("editar_libro.html", libro=libro)

    return render_template("editar_libro.html", libro=libro)

@app.route("/libros/eliminar/<int:id_libro>")
def eliminar_libro_web(id_libro):
    try:
        eliminar_libro(id_libro)
        flash("Libro eliminado correctamente.", "success")
        return redirect(url_for("listar_libros"))
    except Exception as e:
        flash(f"Error al eliminar el libro: {str(e)}", "error")
        return redirect(url_for("listar_libros"))

@app.route("/usuarios/editar/<documento>", methods=["GET", "POST"])
def editar_usuario(documento):
    usuario = Usuario.obtener_por_documento(documento)
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("listar_usuarios"))

    if request.method == "POST":
        try:
            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")
            telefono = request.form.get("telefono")
            email = request.form.get("email")
            rol = request.form.get("rol", "normal")

            if not all([nombre, apellido, telefono, email]):
                flash("Todos los campos son obligatorios.", "error")
                return render_template("editar_usuario.html", usuario=usuario)

            # Usar la función de actualización por documento
            from Proyecto import actualizar_usuario_por_documento
            exito, mensaje = actualizar_usuario_por_documento(documento, 
                                                            nombre=nombre, 
                                                            apellido=apellido, 
                                                            telefono=telefono, 
                                                            email=email, 
                                                            rol=rol)
            if exito:
                flash("Usuario editado correctamente.", "success")
            else:
                flash(mensaje, "error")
            return redirect(url_for("listar_usuarios"))
        except Exception as e:
            flash(f"Error al editar el usuario: {str(e)}", "error")
            return render_template("editar_usuario.html", usuario=usuario)

    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/usuarios/eliminar/<documento>")
def eliminar_usuario_web(documento):
    try:
        from Proyecto import eliminar_usuario_por_documento
        exito, mensaje = eliminar_usuario_por_documento(documento)
        if exito:
            flash("Usuario eliminado correctamente.", "success")
        else:
            flash(mensaje, "error")
        return redirect(url_for("listar_usuarios"))
    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "error")
        return redirect(url_for("listar_usuarios"))

@app.route("/verificar_consistencia")
def verificar_consistencia_web():
    """Verifica y corrige inconsistencias en la base de datos"""
    try:
        from Proyecto import verificar_consistencia_libros
        inconsistencias = verificar_consistencia_libros()
        
        if inconsistencias:
            for inconsistencia in inconsistencias:
                flash(inconsistencia, "warning")
            flash(f"Se corrigieron {len(inconsistencias)} inconsistencias.", "success")
        else:
            flash("No se encontraron inconsistencias en la base de datos.", "info")
            
        return redirect(url_for("menu_principal"))
    except Exception as e:
        flash(f"Error al verificar consistencia: {str(e)}", "error")
        return redirect(url_for("menu_principal"))

# =================================================================
# RUTAS DE API PARA BÚSQUEDA EN TIEMPO REAL
# =================================================================

@app.route("/api/buscar_usuarios")
def buscar_usuarios_api():
    """API para buscar usuarios por documento o nombre"""
    termino = request.args.get('q', '')
    if len(termino) < 2:
        return jsonify([])
    
    try:
        from Proyecto import Usuario
        usuarios = Usuario.buscar_por_documento_o_nombre(termino)
        resultado = []
        for usuario in usuarios[:10]:  # Limitar a 10 resultados
            resultado.append({
                'documento': usuario.documento,
                'nombre_completo': f"{usuario.nombre} {usuario.apellido}",
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'rol': usuario.rol
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/buscar_libros")
def buscar_libros_api():
    """API para buscar libros por ID, título o género"""
    termino = request.args.get('q', '')
    if len(termino) < 1:
        return jsonify([])
    
    try:
        from Proyecto import Libro
        libros = Libro.buscar_por_termino(termino)
        resultado = []
        for libro in libros[:10]:  # Limitar a 10 resultados
            if libro.disponible:  # Solo mostrar libros disponibles
                resultado.append({
                    'id_libro': libro.id_libro,
                    'titulo': libro.titulo,
                    'autor': libro.autor,
                    'genero': libro.genero,
                    'año': libro.año,
                    'disponible': libro.disponible
                })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/prestamos_usuario/<documento>")
def prestamos_usuario_api(documento):
    """API para obtener los préstamos activos de un usuario"""
    try:
        from Proyecto import Prestamo
        prestamos = Prestamo.obtener_prestamos_activos_por_usuario(documento)
        resultado = []
        for prestamo in prestamos:
            resultado.append({
                'id_prestamo': prestamo.id,
                'id_libro': prestamo.id_libro,
                'titulo': prestamo.titulo_libro,
                'autor': prestamo.autor_libro,
                'fecha_prestamo': prestamo.fecha_prestamo,
                'fecha_devolucion_esperada': prestamo.fecha_devolucion_esperada,
                'nombre_usuario': prestamo.nombre_usuario,
                'apellido_usuario': prestamo.apellido_usuario
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)