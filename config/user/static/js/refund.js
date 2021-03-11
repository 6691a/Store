$(document).ready(function() {
    // $('#cart-container > *').on('click', function (e) {
    $('#content > a').on('click', function (e) {
        e.preventDefault();
        reason = prompt('환불 사유를 입력해 주세요', '단순 변심');
        order_id = $(this).data('id');
        // alert(order_id)
        if(reason){
            $.ajax({
                type: "POST",
                url: ORDER_CANCEL_URL,
                async: false,
                data: {
                    reason,
                    order_id,
                    // amount,
                    csrfmiddlewaretoken: CSRF_TOKEN,
                },
                success: function (json) {
                    alert(json.msg)
                    location.reload();
                },
                error: function (xhr, errmsg, err, json) {
                    if (xhr.status == 404) {
                        alert("페이지가 존재하지 않습니다.");
                    } 
                    else if (xhr.status == 403) {
                        alert("로그인 해주세요.");
                    } 
                    else {
                        alert(xhr.responseJSON['msg']);

                    }
                }
            })
        }
    })
});