

function eliminarPelicula(id) {
    Swal.fire({
        title: "¿Está usted seguro eliminar la Pelicula",
        showDenyButton: true,
        confirmButtonText: "SI",
        denyButtonText: "NO"
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = "/eliminarPelicula/" + id; 
        }
    });
}

