function add_request_for_a_call(id_insurance_companies){
            let name = prompt('Представтесь');
            let phone_number = prompt('Номер телефона');
            let comment = prompt('Коментарий');
             $.ajax({
                   url: "/add_request_for_a_call/",
                   type: 'POST',
                   data: { "id":id_insurance_companies,
                       "name":name,
                       "phone_number":phone_number,
                       "comment":comment,
                   },
                   success: function(data) {
                        alert(data);

                   }
            });

        }