from django.shortcuts import render, redirect
from django.db import Error
from appPeliculas.models import Genero, Pelicula
from django.http import JsonResponse,  HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from pathlib import Path
import os
from django.conf import settings
from bson import objectid

# Create your views here. las peticiones del cliente siempre deben tener request

def inicio(request):
    return render(request, "inicio.thml")



def vistaAgregarGenero(request):
    return render(request, "agregarGenero.html")



def agregarGenero(request):

    try:
        #recibe nombre del genero
        nombre = request.POST['txtNombre']
        genero = Genero (getNombre=nombre)
        genero.save()
        mensaje = "genero agregado correctamente"

    except Error as error:
        mensaje =str(error)

    retorno = {"mensaje": mensaje}    
    # return JsonResponse(retorno)
    return render(request, "agregarGenero.html", retorno)



def listarPeliculas(request):
    Peliculas = Pelicula.objects.all()
    print(Peliculas) # para revisar en consola
    retorno = {"peliculas": Peliculas}
    # return JsonResponse(retorno)
    return render(request, "listarPeliculas.html", retorno)



def vistaAgregarPelicula(request):
    generos = Genero.objects.all()
    retorno = {'generos': generos} 
    return render(request, "agregarPelicula.html", retorno)
    


def agregarPelicula(request):
    try:
        codigo = request.POST["txtCodigo"]
        titulo = request.POST['txtTitulo']
        protagonista = request.POST["txtProtagonista"]
        duracion = int(request.POST['txtDuracion'])
        resumen = request.POST['txtResumen']
        foto = request.FILES['fileFoto']
        idGenero = objectid(request.POST['cbGenero'])
        genero = Genero.objects.get(pk=idGenero)

        #crear objeto pelicula

        pelicula = Pelicula (
            pelCodigo = codigo,
            pelTitulo = titulo,
            pelProtagonista = protagonista,
            pelDuracion = duracion,
            pelResumen = resumen,
            pelFoto = foto,
            pelGenero = genero
        )

        pelicula.save()
        mensaje = "pelicula agregada correctamente"

    except Error as error:
        mensaje =str(error)

    retorno = {"mensaje": mensaje, "idPelicula":pelicula.id}
    # return JsonResponse(retorno) 
    return render(request, "agregarPelicula.html", retorno)



def consultarPeliculaPorId(request, id):
    pelicula = Pelicula.objects.get(pk=id)
    generos = Genero.objects.all()
    #retornamos los generos en la interfaz
    retorno = {"pelicula":pelicula, "generos": generos}
    return render(request, "actualizarPelicula.html", retorno)



def actualizarPelicula(request):
    try:
        idPelicula = request.POST['idPelicula']
        #obtener pelicula por su id
        peliculaActualizar = Pelicula.objects.get(pk=idPelicula)
        #actualizar campos
        peliculaActualizar.pelCodigo=request.POST['txtCodigo']
        peliculaActualizar.pelTitulo=request.POST['txtTitulo']
        peliculaActualizar.pelProtagonista=request.POST['txtProtagonista']
        peliculaActualizar.pelDuracion=int(request.POST['txtDuracion'])
        peliculaActualizar.pelResumen=request.POST['txtResumen']
        idGenero = int(request.POST['cbGenero'])
        #obtener genero a partir de su id
        genero = Genero.objects.get(pk=idGenero)
        peliculaActualizar.pelGenero=genero
        foto=request.FILES.get('fileFoto')

        #si han enviado foto se actualiza el campo

        if (foto):
            #primero eliminamos la foto existente
            os.remove(os.path.join(settings.MEDIA_ROOT + "/" + str (peliculaActualizar.pelFoto)))
            # actualizamos la nueva foto
            peliculaActualizar.pelFoto = foto

            #actualizar la pelicula en la base de datos
        peliculaActualizar.save()
        mensaje="Pelicula actualizada correctamente"

    except Error as error:
        mensaje = str(error)

    retorno = {"mensaje": mensaje}
    # Si hay algún error, podrías redirigir a una página de error o mostrar un mensaje de error en la misma página
    return render(request, "actualizarPelicula.html", retorno)



def eliminarPelicula(request,id):
    try:
        peliculaEliminar = Pelicula.objects.get(pk=id)
        peliculaEliminar.delete()
        mensaje = "Película eliminada correctamente"
    except Error as error:
        mensaje =str(error)
    retorno = {"mensaje": mensaje}
    # return JsonResponse(retorno)
    return redirect('/listarPeliculas')
    # return render(request, "listarPeliculas.html", retorno)



