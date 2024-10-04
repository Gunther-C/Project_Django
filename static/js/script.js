
const Colors_ = Array('#0056ab','#01857a','#02bb46','#04cf32','#05e618');

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

function _rating() {
    $(`.rating`).each( function() {
        let child = $(this).children();
        let nbrKeys = Object.keys(Colors_).length;
        let nbr = 0;

        while (nbr < nbrKeys) {
            if (!$(child[nbr]).hasClass(`bi-star`)) {
                child[nbr].style.color =  Colors_[nbr];
            }
            nbr++;
            if (nbr > 5) break;
        }
    })
}



(function($) {
$(document).ready(function() {

    let WidthBody = parseFloat($('body').css('width'));
    if (WidthBody < 426) {
        $(`#content-btn-nav-user`).appendTo(`#nav-user`);
        $(`#sect-viewScrollFollow > header`).removeClass(`my-5`).addClass(`mt-5`) ;
    }

    _rating();

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

        if (text.length > 2) {

            const Search_ = _searching(text).then((response) => {


                if (Object.keys(response).length < 1 || Object.keys(response) == `errors`) {

                    $(`#follow_searching`).append(`
                        <div id="empty_search" class="alert alert-warning d-flex align-items-center justify-content-center w-75 mx-auto mt-4 px-3 py-1" role="alert">
                        <i class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2 text-warning"></i>
                        <div>Aucun utilisateur à ce nom</div>
                        </div>
                    `);
                    _alertAlert();
                }
                else {
                    $(`#follow_searching`).append(`<div id="follow-users-searching" class="mx-auto"></div>`);
                    return response;
                }

            }).then((response) => {

                $.each(response, function(keys, values) {

                    if (values.includes(`???`)) {
                        values = values.substring(values.lastIndexOf('-')+1);
                        $('#follow-users-searching').append(`<button type="button" class="follow-create btn btn-sm">${values} (abonné)</button>`);
                    }
                    else {
                        $('#follow-users-searching').prepend(`<button type="button" onclick="location.href='/env/create_follow/${keys}/'" class="follow-create btn btn-sm">${values}</button>`);
                    }

                })

            }).catch((error) => console.warn(error))
        }
    })


    $(`#user-parameter`).on(`click`, function () {

        if (!$(`#content-parameter`).is(`:visible`)) {
            $(`body`).append(`
            <div id="content-parameter">
                <button type="button" onclick="location.href='/password_change/'" class="btn btn-sm">Modifiez &nbsp; <strong>Password</strong></button>
                <button type="button" onclick="location.href='/email_change/'" class="btn btn-sm">Modifiez &nbsp; <strong>E-mail</strong></button>
            </div>
            `);
            $(this).find(`.parameter-stat`).text(`Fermer`);
        }
        else {
            $(`#content-parameter`).detach();
            $(this).find(`.parameter-stat`).text(`Ouvrir`);
        }
    })

    $(`#user-parameter`).hover(

        function () {
            let text = `Ouvrir`;
            if ($(`#content-parameter`).is(`:visible`)) text = `Fermer`;

            $(this).find(`.user-name`).hide();
            $(this).append(`<span class="parameter-name"><i class="bi bi-gear pe-2"></i> ${text}</span>`)

        },
        function () {
            $(this).find(`.parameter-name`).detach()
            $(this).find(`.user-name`).show();
        }
    )


    $(`.register-username-infos`).hover(

        function () {
            let parent = $(this).parent();
            if ($(`.register-help`).is(`:visible`)) $(`.register-help`).detach();

            parent.after(`<div class="register-help alert alert-primary d-flex align-items-center justify-content-center mx-auto mb-5 py-1" role="alert">
                    <i class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2 text-primary"></i>
                    <ul>
                        <li>Requis. Votre nom utilisateur doit être unique et contenir moins de 50 caractères,</li>
                        <li>Uniquement des lettres, nombres ou « @ », « . », « + », « - » et « _ »...</li>
                    </ul>
                </div>`)
        },
        function () { $(`.register-help`).detach() }
    )

    $(`.register-password-infos`).hover(

        function () {
            let parent = $(this).parent();
            if ($(`.register-help`).is(`:visible`)) $(`.register-help`).detach();

            parent.after(`<div class="register-help alert alert-primary d-flex align-items-center justify-content-center mx-auto mb-5 py-1" role="alert">
                    <i class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2 text-primary"></i>
                    <ul>
                        <li>Votre ancien mot de passe est incorrect. Veuillez réessayer.</li>
                        <li>Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles.</li>
                        <li>Votre mot de passe doit contenir au minimum 8 caractères.</li>
                        <li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>
                        <li>Votre mot de passe ne peut pas être entièrement numérique.</li>
                    </ul>
                </div>`)
        },
        function () { $(`.register-help`).detach() }
    )


    $('#id_image').change(function(e){

        if ($(`#figure_clone`).is(`:visible`)) $(`#figure_clone`).detach();

        let input = $(this);
        let filePath = $(this).val();

        if(filePath.length > 4 ) {

            let countFiles = input[0].files.length;
            let figure = `<figure id="figure_clone"><img src="" id="img_clone" class="img-fluid img-thumbnail" alt="Photo du ticket"></figure>`;

            const image_ = new Promise((resolve, reject) => {

                if(typeof (FileReader) === undefined) {
                    reject(new Error(`Erreur de chargement`));
                }
                else {
                    resolve($(`#user-index`).append(figure));
                }

            }).then(() => {

                 for(let i = 0; i < countFiles; i++){

                    let newFile = new FileReader();

                    newFile.onload = function(e){
                        $(`#img_clone`).attr(`src`,e.target.result);
                    }
                    newFile.readAsDataURL(input[0].files[i]);
                }

            }).catch((error) => console.warn(error))
        }
    })

})
})(jQuery);


