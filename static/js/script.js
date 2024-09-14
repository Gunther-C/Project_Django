
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const Cookies = document.cookie.split(';');
        for (let i = 0; i < Cookies.length; i++) {
            const Cookie = Cookies[i].trim();
            if (Cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(Cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//___ Recherche d'un utilisateur
async function _searching(submit_search){

    try{

        const Request_user = await fetch('/env/searching/', {
            method: "POST",
            headers: {
                "Content-Type": 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: 'user-searching=' + encodeURIComponent(submit_search)
        })

       if(!Request_user.ok) throw new Error(`Erreur API`);

        const Users_search =  await Request_user.json();

        return Users_search;

    }
    catch(errors){
        console.error(errors)
    }
}

//___ Message alert success ou erreur (Réglage du temps avant fermeture)
function _alertAlert(){

    if($('.alert-success').is(':visible')){
        setTimeout(() => {
            $('.alert-success').animate({'opacity':'0'},1000);
            setTimeout(() => { $('.alert-success').detach(); }, 1010);
        }, 5000);
    }

    if($('.alert-warning').is(':visible')){
        if (!$('.alert-warning').hasClass(`static-alert`)) {
            setTimeout(() => {
                $('.alert-warning').animate({'opacity':'0'},1000);
                setTimeout(() => { $('.alert-warning').detach(); }, 1010);
            }, 5000);
        }
    }

    if($('.alert-danger').is(':visible')){
        setTimeout(() => {
            $('.alert-danger').animate({'opacity':'0'},1000);
            setTimeout(() => { $('.alert-danger').detach(); }, 1010);
        }, 5000);
    }
}

//___ Gestion class active des boutons de la nav user
function _btnUserNav() {

    $(`.btn-nav-user`).removeClass(`active`);
    let type_id = $(`#content-btn-nav-user`).attr(`data-type`);

    if (type_id !== "") {
        $(`#${type_id}`).addClass(`active`)

        if(typeof localStorage !== undefined && `btnNav-user` in localStorage) {
            localStorage[`btnNav-user`] = type_id;
        }
        else { localStorage.setItem(`btnNav-user`, type_id) }
    }
    else if(typeof localStorage !== undefined && `btnNav-user` in localStorage) {
        let btn_id = localStorage[`btnNav-user`];
        $(`#${btn_id}`).addClass(`active`)
    }
    else { $(`#flux`).addClass(`active`) }
}


(function($) {
$(document).ready(function() {

    _btnUserNav();

    _alertAlert();

    $(`body`).on(`click`, function() {
        if ($(`#follow-users-searching`).is(`:visible`)) $(`#follow-users-searching`).detach();

    })

    $(document).on('mousedown','button, input[type="submit"], .arrow-begin', function() {
        $(this).css({'transform': 'scale(0.95)', 'box-shadow': 'inset 2px 4px 8px rgba(170, 170, 170, 0.4)'})

    })

    $(document).on('mouseup mouseleave','button, input[type="submit"], .arrow-begin', function() {

        if (!$(this).hasClass(`follow-create`)) {
            $(this).css({'transform': 'scale(1)', 'box-shadow': '2px 3px 6px rgba(145, 142, 142, 0.854)'})

        }
        else {
            $(this).css({'transform': 'scale(1)', 'box-shadow': 'unset', 'background-color': 'rgba(236, 244, 253, 0.5)'})
        }
    })

    $(document).on(`keyup past cut click`, `#user-searching`, function(e) {

        if ($(`#follow-users-searching`).is(`:visible`)) $(`#follow-users-searching`).detach();
        if ($(`#empty_search`).is(`:visible`)) $(`#empty_search`).detach();

        let text = $(this).val();
        let child_last = $(this).next();

        if (text.length > 2) {

            const Search_result = _searching(text).then((response) => {
                if (Object.keys(response).length < 1) {

                    $(`#follow_searching`).append(`<div id="empty_search" class="alert alert-warning d-flex align-items-center justify-content-center w-75 mx-auto
                    mt-4 px-3 py-1" role="alert"><i class="bi bi-exclamation-triangle-fill flex-shrink-0
                    me-2 text-warning"></i><div>Pas d'utilisateur à ce nom</div></div>`);
                    _alertAlert();
                }
                else {
                    $(`#follow_searching`).append(`<div id="follow-users-searching" class="mx-auto"></div>`);
                    return response;
                }

            }).then((response) => {
                $.each(response, function(keys, values) {
                    $('#follow-users-searching').append(`<button type="button" onclick="location.href='/env/create_follow/${keys}/'" class="follow-create btn btn-sm">${values}</button>`);
                })

            }).catch((error) => console.warn(error))
        }
    })
})
})(jQuery);


