Toast = {
    success: function (message) {

        Swal.fire({
            // position: 'center',
            icon: 'success',
            title: message,
            showConfirmButton: true,
            confirmButtonText: "OK",
            // timer: 3000
        }).then((isConfirm) =>{
            if (isConfirm.value) {
                location.reload();
            }})


    },fail: function (message) {

        Swal.fire({
            // position: 'center',
            icon: 'error',
            title: message,
            confirmButtonText: "OK",
            cancelButtonText: "OK",
            // timer: 3000
        }).then((isConfirm)=>{
            if(isConfirm.value){
                $(".bs-example-modal-center").modal("hide")
            }
        })


    },
    detail: function (message) {
        Swal.fire({
            position: 'top',

            // animation: false,
            text: message, showConfirmButton: false,
        })
    },

    error: function (message) {
        Swal.fire({
            position: 'top-end',
            icon: 'error',
            title: message,
            showConfirmButton: false,
            timer: 3000
        })
    },

    warning: function (message) {
        Swal.fire({
            position: 'top-end',
            icon: 'warning',
            title: message,
            showConfirmButton: false,
            timer: 3000
        })
    }
};