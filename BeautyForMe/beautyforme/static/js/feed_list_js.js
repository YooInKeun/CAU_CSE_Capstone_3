// Django에서 AJAX로 form post를 할 때 csrf token을 발급해주는 script
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function () {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(window).on('click', function (event) {
        // 0. 공통 변수 초기화
        let target = $(event.target)

        // 1. Dropdown 관련 로직
        let allDropdowns = document.getElementsByClassName("dropdown-content")
        let targetDropdown = target.next('.dropdown-content')[0]
        // map 함수를 이용하기 위해 Array로 치환한다
        let dropdownArr = [...allDropdowns]

        // 클릭한게 icon이 아닌 경우 window를 클릭한 것이다.
        if (!event.target.matches('i')) {
            // show가 있는 div를 닫아준다
            dropdownArr.map(d => {
                if (d.classList.contains('show')) d.classList.remove('show')
            })
        } else if (target.hasClass('fa-ellipsis-v')) {
            //클릭한게 더보기 icon인 경우
            if (targetDropdown.classList.contains('show')) {
                // 만일 클릭한 icon으로부터 가장 가까운 dropdown-content가 열려있으면 단순히 닫아준다.
                targetDropdown.classList.remove('show')
            } else {
                // 만일 클릭한 icon으로부터 가장 가까운 dropdown-content가 닫혀있으면 일단 모든 dropdown을 닫아준다.
                dropdownArr.map(d => d.classList.remove('show'))
                // 그 후 클릭한 icon으로부터 가장 가까운 dropdown-content를 열어준다.
                targetDropdown.classList.toggle('show')
            }
        } else if (target.hasClass('fa-comment')) {
            // 1. 말풍선 기준으로 가장 가까운 .button-container div를 찾는다.
            // 2. 그것과 동일한 위치의 .comment-creator-div div를 찾는다.
            // 3. 하위 요소를 순회하며 textarea 를 찾으면 그것이 포커싱하고자하는 댓글창이다
            target.closest('.button-container')
                .siblings('.comment-creator-div')
                .find('textarea')[0]
                .focus()
        }
    })

    // 댓글창 사이즈 자동조절
    $('textarea').on('keydown keyup', function () {
        $(this).height(1).height($(this).prop('scrollHeight') + 12);
    });
    // 댓글 엔터키 입력
    $('textarea').on('keypress', function (event) {
        if (event.which === 13) {
            event.preventDefault()
            let content = $(this).val()
            if (content === '') return

            let url = $(this).closest('form').attr('action')

            // input을 비워준다
            $(this).val('')

            $.ajax({
                url: url,
                method: 'POST',
                data: {
                    'content': content
                },
                success: (data) => {
                    // 현재 textarea로부터 가장 가까운 omment-container-div 를 찾고 리턴된 데이터로 교체한다
                    $(this).parents('.comment-creator-div')
                        .siblings('.comment-container-div')
                        .html(data)
                },
                fail: (data) => {
                    alert('댓글 등록에 실패하였습니다. 다시 시도해 주세요.')
                    console.log(data)
                }
            })
        }
    })
})